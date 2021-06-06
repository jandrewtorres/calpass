from .knowledge_model import object_name_associations

def get_associated_properties(entity_extracted_token_list):
    properties = []
    for t in entity_extracted_token_list:
        if isinstance(t, str):
            properties.append((t, object_name_associations[t]))
        else:
            properties.append((t[0], object_name_associations[t[0]]))
    print(properties)
    return properties