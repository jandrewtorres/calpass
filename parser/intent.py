from .knowledge_model import object_name_associations
from data import query_builder, db_access
from rdflib import URIRef

def get_associated_properties(entity_extracted_token_list):
    properties = []
    for t in entity_extracted_token_list:
        if not isinstance(t[0], URIRef):
            if not isinstance(t, str):
                properties.append((object_name_associations[t[0]], t[1]))
            else:
                otherprops = object_name_associations[t]
                if len(otherprops) > 0:
                    properties.append(otherprops)
        else:
            properties.append(t)
    return properties

def build_query_for(properties):
    builder = query_builder.QueryBuilder()
    for prop in properties:
        print(prop)
        if isinstance(prop, tuple): # property and value pairs, can be multiple properties
            template = db_access.property_templates[prop[0]]
            builder.add_property((template[0], prop[0], template[1]))
            #  TODO add all alternate properties as optional parts or query
            # for p in prop[0]:
            #     template = db_access.property_templates[p]
            #     builder.add_property((template[0], prop[0], template[1]))
        elif isinstance(prop, list): # list of db props without values
            for p in prop:
                template = db_access.property_templates[p]
                builder.add_property((template[0], p, template[1]))
    return builder.get_query_text()
