from .knowledge_model import object_name_associations
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