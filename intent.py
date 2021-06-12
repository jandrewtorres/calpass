import knowledge_model as km
from data import query_builder, db_access
from rdflib import URIRef

def get_associated_properties(entity_extracted_token_list):
    properties = []
    for t in entity_extracted_token_list:
        print(t)
        if not isinstance(t[0], URIRef):
            if not isinstance(t, str):
                for p in t[0]:
                    properties.append((km.object_name_associations[p], t[1]))
            else:
                otherprops = km.object_name_associations[t]
                if len(otherprops) > 0:
                    properties.append(otherprops)
        else:
            properties.append(t)
    return properties

def build_query_for(properties):
    builder = query_builder.QueryBuilder()
    # print(properties)
    for prop in properties:
        if isinstance(prop, tuple): # property and value pairs
            known_prop, value = prop
            template = db_access.property_templates[known_prop]
            builder.add_property((template[0], known_prop, template[1]), filter=value)
            #  TODO add all alternate properties as optional parts or query
            # for p in prop[0]:
            #     template = db_access.property_templates[p]
            #     builder.add_property((template[0], prop[0], template[1]))
        elif isinstance(prop, list): # list of db props without values
            for p in prop:
                template = db_access.property_templates[p]
                builder.add_property((template[0], p, template[1]))
    return builder.get_query_text()
