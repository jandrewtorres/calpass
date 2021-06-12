import data.db_access as dba
import data


g = dba.load_db('course_database')

print(f"loaded database of {len(g)} entries")

qres = g.query(
    """SELECT DISTINCT ?cname
       WHERE {
            _:djanzen <calpass:namespace:type> ns:Person .
            _:djanzen pns:teaches ?b .
            ?b cns:course_name ?cname .
       }""", initNs={
           'ns' : dba.calpass_namespace,
           'pns' : dba.calpass_professor_properties,
           'cns' : dba.calpass_course_properties
           })


for row in qres:
    print(row)

query = data.QueryBuilder()
query.add_property(('prof', dba.calpass_namespace.type, dba.calpass_namespace.Person), isfinalvar=True)
print(query.get_query_text())
qres = g.query(query.get_query_text())

# qres = g.query('SELECT * WHERE { ?p ns:type ns:Person }', initNs={ 'ns' : dba.calpass_namespace })

for row in qres:
    print(row)

qres = g.query(
    """SELECT DISTINCT ?object ?type
       WHERE {
            ?object ns:type ?type .
       }""", initNs={
           'ns' : dba.calpass_namespace,
           'pns' : dba.calpass_professor_properties,
           'cns' : dba.calpass_course_properties
           })

# for row in qres:
#     print(row)

print(dba.calpass_professor_properties['teaches'])