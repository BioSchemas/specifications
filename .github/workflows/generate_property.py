from generate_types_cardinality import generate_types_cardinality

def generate_property (g, prop, req_label, marginality):
    
    #print(Fore.GREEN + Style.BRIGHT + f'Property : {req_label}' + Style.RESET_ALL)
    new_p = dict()
    #If I want to create a dict, new_p[] = {'description':prop["description"]}
    
    new_p['property'] = req_label
    new_p['marginality'] = marginality
    new_p['cardinality'], new_p['expected_types'] = generate_types_cardinality(g, prop)

    if "description" in prop.keys():
        new_p['description'] = prop["description"]
    else:
        new_p['description']=""
    if "type_url" in prop.keys():
        new_p['type_url'] = prop["type_url"]
    else:
        new_p['type_url']=""
    if "bsc_description" in prop.keys():
        new_p['bsc_description'] = prop["bsc_description"]
    else:
        new_p['bsc_description']=""
    if "controlled_vocab" in prop.keys():
        new_p['controlled_vocab'] = prop["controlled_vocab"]
    else:
        new_p['controlled_vocab']=""
    
    if "example" in prop.keys():
        new_p['example'] = prop["example"]
    else:
        new_p['example']=""

    # Here we'll suppose that all properties are in default schemas.org 
    new_p['type']=""

    return new_p