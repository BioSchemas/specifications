import json
from pathlib import Path
from pydoc import doc
import yaml
from colorama import Fore
from colorama import Style
import sys
import os.path
import csv
from os import path



def generate_transformed_profile(g, path_changed_file):
    
    transformed_profile = dict()
    
    ### Spec_info
    transformed_profile["spec_info"] = generate_spec_info(g)    
    
    ### Mapping
    transformed_profile["mapping"] = list(dict())
            
    # Browse properties by marginality and add them to the mappings        
    if "$validation" in g.keys():
        transformed_profile["type"]="Profile"
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
    else:
        transformed_profile["type"]="Type"

    ### Generate the metadata
    transformed_profile['name']=g["@id"].split(':')[1]
    transformed_profile['use_cases_url']='/useCases/'+transformed_profile['name']

    with open('bioschemas-dde/draft_profile_list.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
            if line_count > 1:
                fields = row[0].split('\t')
                if fields[1]==transformed_profile['name']:
                    #print(f'\n namespace={fields[0]}, name={fields[1]}, subclassof={fields[2]}, type={fields[3]}, version={fields[4]}, url={fields[5]}.')    
                    transformed_profile['spec_type']={fields[3]}
    
    transformed_profile['previous_version']= get_previous_version(path_changed_file)
    transformed_profile['previous_release']= get_previous_release(path_changed_file)
    transformed_profile['status']=get_status(transformed_profile["spec_info"]["version"])
    transformed_profile['group']=get_group(transformed_profile['name'])
    transformed_profile['cross_walk_url']=get_cross_walk_url(transformed_profile['name'])
    transformed_profile['gh_tasks']= "https://github.com/Bioschemas/specifications/labels/type%3A%20"+transformed_profile['name']
    transformed_profile['live_deploy']="/liveDeploys"
    transformed_profile['parent_type']=transformed_profile["spec_info"]["official_type"]
    transformed_profile['redirect_from']=get_redirect_from(transformed_profile['name'])
    transformed_profile['hierarchy']=get_hierarchy()
    transformed_profile['json-ld_url']=arg
    transformed_profile['dde_ui_url']="https://discovery.biothings.io/view/"
    
    ## Case Profile
    if arg.split("-")[1].split('.')[0]=="DRAFT":
        transformed_profile['dde_ui_url'] = transformed_profile['dde_ui_url'] + "bioschemasdrafts/bioschemasdrafts:" + transformed_profile["name"]
    elif arg.split("-")[1].split('.')[0]=="RELEASE":
        transformed_profile['dde_ui_url'] = transformed_profile['dde_ui_url'] + "bioschemas/bioschemas:" + transformed_profile["name"]

    for i in transformed_profile:
        if i !="spec_info" and i!="mapping":
            print(Fore.YELLOW + Style.BRIGHT + f'{i} = {transformed_profile[i]}' + Style.RESET_ALL)    

    return transformed_profile

# display all files and get the -1 file
from os import listdir
from os.path import isfile, join

def get_previous_version(path_changed_file):
    previous_version=""
    
    mypath=path_changed_file.split('/')[0]+"/"+path_changed_file.split('/')[1]
    #print(Fore.LIGHTRED_EX + 'mypath: ' + mypath + Style.RESET_ALL)
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    
    for f in onlyfiles:
        max=0
        if f.split('_')[1].split('-')[1].split('.')[0]=="DRAFT":
            if int(f.split('_')[1].split('-')[0].split('.')[1]) > max:
                max = int(f.split('_')[1].split('-')[0].split('.')[1])
        print(Fore.LIGHTRED_EX + 'Latest Draft: ' + str(max) + Style.RESET_ALL)
    
    return previous_version

def get_previous_release(path_changed_file):
    previous_release=""
    mypath=path_changed_file.split('/')[0]+"/"+path_changed_file.split('/')[1]
    #print(Fore.LIGHTRED_EX + 'mypath: ' + mypath + Style.RESET_ALL)
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    
    for f in onlyfiles:
        if f.split('_')[1].split('-')[1].split('.')[0]=="RELEASE":
            print(Fore.LIGHTBLUE_EX + 'Releases: ' + f + Style.RESET_ALL)

    return previous_release

# if its draft it's revision, case release, deprecated
def get_status(version):
    status =""
    if version.split("-")[-1]=="DRAFT":
        status = "Revision"
    elif version.split("-")[-1]=="RELEASE":
        status ="Deprecated"
    return status

# Create a mapping file grp == classes, and put it in the _data/ then fetch them from there
def get_group(profile_name):
    group=""
    
    with open('bioschemas.github.io/_data/metadata_mapping.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
            if line_count > 1:
                if row[0]==profile_name:
                    group=row[1]
    return group

# same as grps, we need a mapping file. [The admin should make sure he updates the config files in the right order!]
def get_cross_walk_url(profile_name):
    cross_walk_url=""
    
    with open('bioschemas.github.io/_data/metadata_mapping.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
            if line_count > 1:
                if row[0]==profile_name:
                    cross_walk_url=row[3]

    return cross_walk_url

# follow the pattern for most, and when I see an exception, hardcoded it an dictionary
def get_redirect_from(profile_name):
    redirect_from=list() 

    with open('bioschemas.github.io/_data/metadata_mapping.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
            if line_count > 1:
                if row[0]==profile_name:
                    redirect_from=row[2]

    return redirect_from

# from the profiles json-ld : 
def get_hierarchy():
    hierarchy=list()
    
    return hierarchy

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
        raise Exception("Please Provide the version of your profile!")
        
    if "rdfs:subClassOf" in g.keys():
        spec_info["official_type"] = g['rdfs:subClassOf']['@id'].split(':')[1]
    else:
        spec_info["official_type"]=""

    spec_info["full_example"] = "https://github.com/BioSchemas/specifications/tree/master/"+spec_info["title"]+"/examples"

    return spec_info

def generate_property (g, prop, req_label, marginality):
    
    print(Fore.GREEN + Style.BRIGHT + f'Property : {req_label}' + Style.RESET_ALL)
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
    print(Fore.MAGENTA + f'Expected Types : {clean_expected_types}' + Style.RESET_ALL)

    print(Fore.RED + f'Cardinality = {cardianliy}' + Style.RESET_ALL)

    return cardianliy, clean_expected_types

# ## Main Script

args = sys.argv
website_repo= args[-1]
args.remove(website_repo)

# For each new uploaded JSON-LD file 
for arg in args:
    if 'jsonld' in arg.split('/'):
        if 'json' in arg.split('.'):
            arglist= arg.split('/')
            profile_name=arg.split('/')[-1].split('.')[0].split('_')[0]
            print(Fore.YELLOW + 'added/updated profile: ' + arg + Style.RESET_ALL)

            in_file = "./"+arg

            with open(in_file, "r", encoding="utf-8") as i:
                data = json.load(i)

            #print(json.dumps(data['@graph'][0], indent=True))


            for g in data["@graph"]:

                if g["@type"]=="rdfs:Class":
                
                    print(Fore.BLUE + Style.BRIGHT + f'Profile : {g["@id"]}' + Style.RESET_ALL) 
                    #print(Style.BRIGHT + f'{g.keys()}' + Style.RESET_ALL)
                    
                    #For each profile : 
                    #Prepare the transfermed profile : spec_info & mapping fields
                    transformed_profile = generate_transformed_profile(g, arg)
                    
                    # Inject the YAML in a HTML File
                    # Note: The folder should be in the transformed_profile["spec_info"]["title"] folder

                    ### PROBLEM: if the forlder "profile name" doesn't exist it will throw an exception, so we need to create it manually
                    
                    folderpath = "./"+website_repo+"/pages/_profiles/"+profile_name
                    #out_YAML_file = folderpath+"/"+"generated_"+profile_name+".yaml"
                    out_HTML_file= folderpath+"/"+ transformed_profile["spec_info"]["version"] +".html"
                    
                    if path.exists(folderpath):
                        print ("folder esists")
                    else:
                        #os.makedirs(os.path.dirname(folderpath), exist_ok=True)
                        Path(folderpath).mkdir(parents=True, exist_ok=True) 
                        print("Create folder : ", folderpath)

                    #with open(out_YAML_file, "w", encoding="utf-8") as o:
                    #    yaml.dump(transformed_profile, o)

                    #print(Style.BRIGHT + "Transformed profiles Generated and saved in " + out_YAML_file + Style.RESET_ALL)
                    
                    message='''---
# spec_info content generated using GOWeb
# DO NOT MANUALLY EDIT THE CONTENT
'''
                    with open(out_HTML_file, "w", encoding="utf-8") as o:
                        o.write(message)
                        yaml.dump(transformed_profile, o)
                        o.write("---")

                    print(Style.BRIGHT + "HTML Profile page created " + out_HTML_file + Style.RESET_ALL)