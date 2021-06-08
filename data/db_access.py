import json
import re
from rdflib import Graph, Literal, URIRef, BNode
from rdflib.store import NO_STORE, VALID_STORE
from rdflib.namespace import ClosedNamespace, Namespace

calpass_namespace = Namespace("calpass:namespace:")

calpass_course_properties = ClosedNamespace(
    uri='/course/',
    terms=[
        'course_class', 
        'course_days',
        'course_name',
        'course_req',
        'course_section',
        'course_type',
        'dropped',
        'ecap',
        'end_time',
        'enrolled',
        'location',
        'start_time',
        'waitlisted',

        # node reference props
        'professor', # reference to bnode of type Person
        'section_of' # reference to bnode of type Course
    ]
)

calpass_professor_properties = ClosedNamespace(
    uri='/professor/',
    terms=[
        'classes_href',
        'personAlias',
        'personLocation',
        'personName',
        'personOfficeHours',
        'personPhone',
        'personTitle',

        # node reference props
        'teaches'
    ]
)

property_templates = {
    calpass_professor_properties.classes_href: ('prof', 'classes_href'),
    calpass_professor_properties.personAlias: ('prof', 'personAlias'),
    calpass_professor_properties.personLocation: ('prof', 'personLocation'),
    calpass_professor_properties.personName: ('prof', 'personName'),
    calpass_professor_properties.personOfficeHours: ('prof', 'personOfficeHours'),
    calpass_professor_properties.personPhone: ('prof', 'personPhone'),
    calpass_professor_properties.personTitle: ('prof', 'personTitle'),
    calpass_professor_properties.teaches: ('prof', 'course'),

    calpass_course_properties.course_class : ('course', 'course_class'),
    calpass_course_properties.course_days : ('course', 'course_days'),
    calpass_course_properties.course_name : ('course', 'course_name'),
    calpass_course_properties.course_req : ('course', 'course_req'),
    calpass_course_properties.course_section : ('course', 'course_section'),
    calpass_course_properties.course_type : ('course', 'course_type'),
    calpass_course_properties.dropped : ('course', 'dropped'),
    calpass_course_properties.ecap : ('course', 'ecap'),
    calpass_course_properties.end_time : ('course', 'end_time'),
    calpass_course_properties.enrolled : ('course', 'enrolled'),
    calpass_course_properties.location : ('course', 'location'),
    calpass_course_properties.start_time : ('course', 'start_time'),
    calpass_course_properties.waitlisted : ('course', 'waitlisted'),
    calpass_course_properties.professor : ('course', 'prof'),
    calpass_course_properties.section_of : ('course', 'course_node')
}

parse_map = {
    calpass_professor_properties.classes_href : (re.compile(r'(.*)'), lambda f : f),
    calpass_professor_properties.personLocation : (re.compile(r'([\d\w]+)-([\d\w]+)', re.IGNORECASE), lambda b, r : f'{b} {r}'),
    calpass_professor_properties.personName : (re.compile(r'([\w\s]+),\s+([\w\s]+)', re.IGNORECASE), lambda l, f : f'{f} {l}'),
    
    calpass_course_properties.course_class : (re.compile(r'([\d]+)', re.IGNORECASE), lambda n : int(n)),
    calpass_course_properties.course_days : (re.compile(r'([MTWRF]+)', re.IGNORECASE), lambda days : days),
    calpass_course_properties.dropped : (re.compile(r'([\d]+)'), lambda n : int(n)),
    calpass_course_properties.ecap : (re.compile(r'([\d]+)'), lambda n : int(n)),
    calpass_course_properties.enrolled : (re.compile(r'([\d]+)'), lambda n : int(n)),
    calpass_course_properties.waitlisted : (re.compile(r'([\d]+)'), lambda n : int(n))
}

# knowledge base property name alternatives
object_name_map = {
    # course properties
    ('time', 'day') : calpass_course_properties.course_days,
    ('course name', 'title', 'course title', 'course') : calpass_course_properties.course_name,
    ('req', 'requirements', 'require', 'prereq', 'prerequisite') : calpass_course_properties.course_req,
    ('section', 'section number') : calpass_course_properties.course_section,
    ('students', 'people', 'number', 'drop', 'withdrawn') : calpass_course_properties.dropped,
    ('students', 'people', 'number', 'enrollment capacity', 'capacity', 'seats') : calpass_course_properties.ecap,
    ('time', 'end', 'finish') : calpass_course_properties.end_time,
    ('students', 'people', 'number', 'enroll', 'maximum', 'max') : calpass_course_properties.enrolled,
    ('location', 'room') : calpass_course_properties.location,
    ('time', 'start', 'begin') : calpass_course_properties.start_time,
    ('students', 'people', 'number', 'waitlist', 'wait') : calpass_course_properties.waitlisted,
    ('professor', 'teach', 'instruct') : calpass_course_properties.professor,
    ('section') : calpass_course_properties.section_of,


    # professor properties
    ('url', 'website', 'site') : calpass_professor_properties.classes_href,
    ('email', 'alias', 'username', 'contact') : calpass_professor_properties.personAlias,
    ('location', 'office hour', 'office') : calpass_professor_properties.personLocation,
    ('name') : calpass_professor_properties.personName,
    ('time', 'day', 'office hour', 'available', 'free', 'schedule', 'visit') : calpass_professor_properties.personOfficeHours,
    ('phone number', 'number', 'contact') : calpass_professor_properties.personPhone,
    ('title', 'job') : calpass_professor_properties.personTitle,
    ('course', 'teach', 'instruct') : calpass_professor_properties.teaches
}

def load_db(dbpath):
    g = Graph(store="Sleepycat", identifier='mygraph')

    rt = g.open(dbpath, create=False)
    if rt == NO_STORE:
        # There is no underlying Sleepycat infrastructure, so create it
        g.open(dbpath, create=True)
    else:
        assert rt == VALID_STORE, "The underlying store is corrupt"

    return g

def query_prof_names(g):
    result = g.query("""SELECT DISTINCT ?pname
       WHERE {
            ?prof ns:type ns:Person .
            ?prof pns:personName ?pname .
       }""", initNs={
           'ns' : calpass_namespace,
           'pns' : calpass_professor_properties,
           'cns' : calpass_course_properties
           })
    results = []
    for r in result:
        results.append(r[0].toPython())
    return results

def literal_parser(text, prop):
    """parse a value for graph db based on its property type"""
    parser = parse_map.get(prop)
    if parser and text is not None:
        reg, mapper = parser
        match = reg.match(text)
        if match is None:
            # print(f"failed to find pattern in value {text} for property {prop}")
            return None
        value = mapper(*match.groups())
        # print(value)
        return value
    return text

def build_db(courses, profs, dbpath):
    g = load_db(dbpath)

    for alias, properties in profs.items():
        node = BNode(alias)
        g.set((node, calpass_namespace.type, calpass_namespace.Person))
        for p, v in properties.items():
            exval = literal_parser(v.strip().lower(), calpass_professor_properties.term(p)) if v is not None else None
            g.set((node, calpass_professor_properties.term(p), Literal(exval)))

    for course in courses:
        course_name = re.sub(r'\s+', '-', course['course_name'].strip())
        course_node = BNode(course_name)
        section = BNode(course_name + '-' + course['course_section'].strip())
        g.set((course_node, calpass_namespace.type, calpass_namespace.Course))
        g.set((section, calpass_namespace.type, calpass_namespace.Section))
        g.set((section, calpass_course_properties.section_of, course_node))
        for p, v in course.items():
            if p not in ['personName', 'prof_alias', 'course_name', 'course_days']:
                exval = literal_parser(v.strip(), calpass_course_properties.term(p)) if v is not None else None
                g.set((section, calpass_course_properties.term(p), Literal(exval)))
            elif p == 'prof_alias':
                prof = BNode(v) # professor node
                g.set((section, calpass_course_properties.professor, prof))
                g.add((prof, calpass_professor_properties.teaches, section))
            elif p == 'course_name':
                g.set((section, calpass_course_properties.term(p), Literal(course_name)))
            elif p == 'course_days':
                for d in v.lower():
                    if d == 'm':
                        g.add((section, calpass_course_properties.course_days, Literal('monday')))
                    elif d == 't':
                        g.add((section, calpass_course_properties.course_days, Literal('tuesday')))
                    elif d == 'w':
                        g.add((section, calpass_course_properties.course_days, Literal('wednesday')))
                    elif d == 'r':
                        g.add((section, calpass_course_properties.course_days, Literal('thursday')))
                    elif d == 'f':
                        g.add((section, calpass_course_properties.course_days, Literal('friday')))
                    else:
                        g.add((section, calpass_course_properties.course_days, Literal(None)))



    print(g.serialize(format='nt').decode("utf-8"))
    print(len(g))

    return g

