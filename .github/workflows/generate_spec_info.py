def generate_spec_info(g):
    spec_info = dict()    
        
    if "rdfs:label" in g.keys():
        spec_info["title"] = g['rdfs:label']
    else:
        raise Exception("Please Provide the title of your profile!")

    if "rdfs:comment" in g.keys():
        spec_info["description"] = g['rdfs:comment']
    else:
        spec_info["description"]
        
    if "schema:schemaVersion" in g.keys():
        spec_info["version"] = g['schema:schemaVersion'][0].split('/')[-1]
    else:
        spec_info["version"]=""
        #raise Exception("Please Provide the version of your profile!")
        
    if "rdfs:subClassOf" in g.keys():
        spec_info["official_type"] = g['rdfs:subClassOf']
    else:
        spec_info["official_type"]=""

    spec_info["full_example"] = "https://github.com/BioSchemas/specifications/tree/master/"+spec_info["title"]+"/examples"

    return spec_info