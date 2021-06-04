import data.db_access as dba

g = dba.load_db('course_database')

print(f"loaded database of {len(g)} entries")

qres = g.query(
    """SELECT DISTINCT ?prof ?cname
       WHERE {
            ?prof ns:type ns:Person .
            ?prof pns:teaches ?b .
            ?b cns:course_name ?cname .
       }""", initNs={
           'ns' : dba.calpass_namespace,
           'pns' : dba.calpass_professor_properties,
           'cns' : dba.calpass_course_properties
           })


for row in qres:
    print(row)

qres = g.query('SELECT * WHERE { ?p ns:type ns:Person }', initNs={ 'ns' : dba.calpass_namespace })

for row in qres:
    print(row)


print(dba.object_name_associations['time'])