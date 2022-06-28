import json
from pathlib import Path
from pydoc import doc
import yaml
from colorama import Fore
from colorama import Style
import sys
import os.path
from os import path

def generate_types_cardianlity(g,prop):
    
    list_types=list()
    cardianliy="ONE"
    
    if "type" in prop.keys():
        if "format" in prop.keys():
            list_types.append(prop["format"])
        else :
            list_types.append(prop["type"])
    
    if "anyOf" in prop.keys():
        for e in prop["anyOf"]:
            if "format" in e.keys():
                list_types.append(e["format"])
            elif "items" in e.keys():
                list_types.append(e["items"])
                cardianliy = "MANY"
            else :
                for t in e.keys():
                    list_types.append(e[t])
    
    if "oneOf" in prop.keys():
        for e in prop["oneOf"]:
            if "format" in e.keys():
                list_types.append(e["format"])
            elif "items" in e.keys():
                list_types.append(e["items"])
                cardianliy = "MANY"
            else :
                for t in e.keys():
                    list_types.append(e[t])

    i=1
    j=1
    while i==1:
        i=0
        j=j+1
        for t in list_types:
            if isinstance(t,dict):
                i=1
                e=t
                list_types.remove(t)
                if "format" in e.keys():
                    list_types.append(e["format"])
                else:
                    for sous_type in e.keys():
                        list_types.append(e[sous_type])
                   
    if len(list_types)==0:
        cardianliy=""
        
    #Some cleaning up
    expected_types =[]
    
    for t in list_types:
        if len(t.split('/'))>1 :
            expected_types.append(t.split('/')[-1].capitalize())
            ##If we ever needed it
            #external_type= g['$validation']["definitions"][t.split('/')[-1]]
            #print(Fore.YELLOW + f'Def of the External Type : {external_type}' + Style.RESET_ALL)            

        else :
            expected_types.append(t.capitalize())    

    ##Remove duplicates
    clean_expected_types = list(set(expected_types))

    #Replace 'String' with 'Text'
    for i in clean_expected_types:
        if i == "String":
            clean_expected_types.remove(i)
            clean_expected_types.append("Text")
    #print(Fore.MAGENTA + f'Expected Types : {clean_expected_types}' + Style.RESET_ALL)

    #print(Fore.RED + f'Cardinality = {cardianliy}' + Style.RESET_ALL)

    return cardianliy, clean_expected_types


def generate_property (g, prop, req_label, marginality):
    
    #print(Fore.GREEN + Style.BRIGHT + f'Property : {req_label}' + Style.RESET_ALL)
    new_p = dict()
    #If I want to create a dict, new_p[] = {'description':prop["description"]}
    
    new_p['property'] = req_label
    new_p['marginality'] = marginality
    new_p['cardinality'], new_p['expected_types'] = generate_types_cardianlity(g, prop)

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
        spec_info["version"]="0.5-DRAFT"
        #raise Exception("Please Provide the version of your profile!")
        
    if "rdfs:subClassOf" in g.keys():
        spec_info["official_type"] = g['rdfs:subClassOf']
    else:
        spec_info["official_type"]=""

    spec_info["full_example"] = "https://github.com/BioSchemas/specifications/tree/master/"+spec_info["title"]+"/examples"

    return spec_info


def generate_transformed_profile(g):
    
    transformed_profile = dict()
    
    ###Spec_info
    transformed_profile["spec_info"] = generate_spec_info(g)    
    print(Style.BRIGHT + "Spec Info Generated" + Style.RESET_ALL)

    ### Mapping
    transformed_profile["mapping"] = list(dict())

    # Browse properties by marginality and add them to the mappings        
    if "$validation" in g.keys():
        for req_label in g['$validation']["required"]:
            prop = g['$validation']["properties"][req_label]
            new_p = generate_property (g, prop, req_label, "Required")
            transformed_profile["mapping"].append(new_p)

        for reco_label in g['$validation']["recommended"]:
            prop = g['$validation']["properties"][reco_label]
            new_p = generate_property (g, prop, reco_label, "Minimum")
            transformed_profile["mapping"].append(new_p)

        for opt_label in g['$validation']["optional"]:
            prop = g['$validation']["properties"][opt_label]
            new_p = generate_property (g, prop, opt_label, "Optional")
            transformed_profile["mapping"].append(new_p)
    
    print(Style.BRIGHT + "Mappings Generated" + Style.RESET_ALL)

    return transformed_profile

# ## Main Script
# 
# Prepare the YAML data, save then display it
# Generate the HTML profile page

# For each new uploaded JSON-LD file 
for arg in sys.argv:
    if ".github" in arg.split('/'):
        print(Fore.YELLOW + 'No Profiles added.' + Style.RESET_ALL)
    else:
        arglist= arg.split('/')
        profile_name=arg.split('/')[-1].split('.')[0]
        print(Fore.YELLOW + 'added/updated profile: ' + profile_name + Style.RESET_ALL)

        in_file = "./"+arg

        with open(in_file, "r", encoding="utf-8") as i:
            data = json.load(i)

        #print(json.dumps(data['@graph'][0], indent=True))


        for g in data["@graph"]:
            
            print(Fore.BLUE + Style.BRIGHT + f'Profile : {g["@id"]}' + Style.RESET_ALL) 
            #print(Style.BRIGHT + f'{g.keys()}' + Style.RESET_ALL)
            
            #For each profile : 
            #Prepare the transfermed profile : spec_info & mapping fields
            transformed_profile = generate_transformed_profile(g)
            
            #print(json.dumps(transformed_profile, indent=True))
            #print(yaml.dump(transformed_profile, indent=4, default_flow_style=False))
            
            #To display only the bioschemas:ComputationalTool
            break

        # Inject the YAML in a HTML File
        # Note: The folder should be in the transformed_profile["spec_info"]["title"] folder

        ### PROBLEM: if the forlder "profile name" doesn't exist it will throw an exception, so we need to create it manually
        
        folderpath = "./Profiles/"+profile_name
        out_YAML_file = folderpath+"/"+"generated_"+profile_name+".yaml"
        out_HTML_file= folderpath+"/"+ transformed_profile["spec_info"]["version"] +".html"

        if path.exists(folderpath):
            print ("folder esists")
        else:
            #os.makedirs(os.path.dirname(folderpath), exist_ok=True)
            Path(folderpath).mkdir(parents=True, exist_ok=True) 
            print("Create folder : ", folderpath)


        with open(out_YAML_file, "w", encoding="utf-8") as o:
            yaml.dump(transformed_profile, o)

        print(Style.BRIGHT + "Transformed profiles Generated and saved in " + out_YAML_file + Style.RESET_ALL)
        
        top_of_the_page='''
        redirect_from:
        - "devSpecs/Tool/specification"
        - "devSpecs/Tool/specification/"
        - "/devSpecs/Tool/"
        - "/devSpecs/Tool"
        - "/specifications/drafts/Tool"
        - "/specifications/drafts/Tool/"
        - "/profiles/Tool/"
        - "/profiles/Tool"
        - "/profiles/ComputationalTool/"
        - "/profiles/ComputationalTool"
        - "/profiles/Tool/0.6-DRAFT/"

        hierarchy:
        - Thing
        - CreativeWork
        - SoftwareApplication

        name: ComputationalTool

        previous_version: 0.5-DRAFT
        previous_release:

        status: revision
        spec_type: Profile
        group: tools
        use_cases_url: '/useCases/ComputationalTool'
        cross_walk_url: https://docs.google.com/spreadsheets/d/12W7DQkUfsY0lrHEVvowgHXAcO2WJyNI6c8ZJzXgzoRI/edit
        gh_tasks: https://github.com/Bioschemas/bioschemas/labels/type%3A%20Tool
        live_deploy: /liveDeploys

        parent_type: SoftwareApplication
        hierarchy:
        - Thing
        - CreativeWork
        - SoftwareApplication

        # spec_info content generated using GOWeb
        # DO NOT MANUALLY EDIT THE CONTENT
        '''


        with open(out_HTML_file, "w", encoding="utf-8") as o:
            o.write("---")
            o.write(top_of_the_page)
            yaml.dump(transformed_profile, o)
            o.write("---")

        print(Style.BRIGHT + "HTML Profile page created " + out_HTML_file + Style.RESET_ALL)