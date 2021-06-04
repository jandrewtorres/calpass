import json
from collections import defaultdict
from rdflib import Graph, Literal, RDF, URIRef, BNode
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

# knowledge base property name alternatives
object_name_map = {
    # course properties
    ('time', 'day') : calpass_course_properties.course_days,
    ('course name', 'title', 'course title', 'course') : calpass_course_properties.course_name,
    ('req', 'requirements', 'require', 'prereq', 'prerequisite') : calpass_course_properties.course_req,
    ('section', 'section number') : calpass_course_properties.course_section,
    ('students', 'people', 'number', 'drop') : calpass_course_properties.dropped,
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
    ('time', 'office hour', 'available', 'free', 'schedule') : calpass_professor_properties.personOfficeHours,
    ('phone number', 'number', 'contact') : calpass_professor_properties.personPhone,
    ('title', 'job') : calpass_professor_properties.personTitle,
    ('course', 'teach', 'instruct') : calpass_professor_properties.teaches
}

def iterfy(iterable):
    if isinstance(iterable, str):
        yield iterable
    else:
        try:
            # need "iter()" here to force TypeError on non-iterable
            # as e.g. "yield from 1" doesn't throw until "next()"
            yield from iter(iterable)
        except TypeError:
            yield iterable

# one to many name map
object_name_associations = defaultdict(list)
for k, v in object_name_map.items():
    for key in iterfy(k):
        object_name_associations[key].append(v)

def load_db(dbpath):
    g = Graph(store="Sleepycat", identifier='mygraph')

    rt = g.open(dbpath, create=False)
    if rt == NO_STORE:
        # There is no underlying Sleepycat infrastructure, so create it
        g.open(dbpath, create=True)
    else:
        assert rt == VALID_STORE, "The underlying store is corrupt"

    return g

def build_db(courses, profs, dbpath):
    g = load_db(dbpath)

    for alias, properties in profs.items():
        node = BNode(alias)
        g.set((node, calpass_namespace.type, calpass_namespace.Person))
        for p, v in properties.items():
            g.set((node, calpass_professor_properties.term(p), Literal(v)))

    for course in courses:
        course_node = BNode(course['course_name'])
        section = BNode(course['course_name'] + '-' + course['course_section'])
        g.set((course_node, calpass_namespace.type, calpass_namespace.Course))
        g.set((section, calpass_namespace.type, calpass_namespace.Section))
        g.set((section, calpass_course_properties.section_of, course_node))
        for p, v in course.items():
            if p not in ['personName', 'prof_alias']:
                g.set((section, calpass_course_properties.term(p), Literal(v)))
            elif p == 'prof_alias':
                prof = BNode(v) # professor node
                g.set((section, calpass_course_properties.professor, prof))
                g.add((prof, calpass_professor_properties.teaches, section))

    print(g.serialize(format='nt').decode("utf-8"))
    print(len(g))

    return g

