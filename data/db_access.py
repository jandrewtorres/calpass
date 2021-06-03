import json
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
        'professor',
        'start_time',
        'waitlisted'
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
        'teaches'
    ]
)

def load_db(path):
    pass

def get_object_names():
    pass

def build_db(courses, profs, dbpath):
    g = Graph(store="Sleepycat", identifier='mygraph')

    rt = g.open(dbpath, create=False)
    if rt == NO_STORE:
        # There is no underlying Sleepycat infrastructure, so create it
        g.open(dbpath, create=True)
    else:
        assert rt == VALID_STORE, "The underlying store is corrupt"

    for alias, properties in profs.items():
        node = BNode(alias)
        for p, v in properties.items():
            g.set((node, calpass_professor_properties.term(p), Literal(v)))

    for course in courses:
        node = BNode(course['course_name'])
        for p, v in course.items():
            if p not in ['personName', 'prof_alias']:
                g.set((node, calpass_course_properties.term(p), Literal(v)))
            elif p == 'prof_alias':
                prof = BNode(v)
                g.set((node, calpass_course_properties.professor, prof))
                g.add((prof, calpass_professor_properties.teaches, node))

    print(g.serialize(format='nt').decode("utf-8"))
    print(len(g))

    return g

    