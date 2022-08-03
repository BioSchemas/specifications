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

from generate_transformed_profile import generate_transformed_profile

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
                
                print(Fore.BLUE + Style.BRIGHT + f'Profile : {g["@id"]}' + Style.RESET_ALL) 
                #print(Style.BRIGHT + f'{g.keys()}' + Style.RESET_ALL)
                
                #For each profile : 
                #Prepare the transfermed profile : spec_info & mapping fields
                transformed_profile = generate_transformed_profile(g)
                
                #print(json.dumps(transformed_profile, indent=True))
                #print(yaml.dump(transformed_profile, indent=4, default_flow_style=False))
                
                ### Metadata
                profile_metadata = dict()

                profile_metadata['name']=g["@id"].split(':')[1]
                profile_metadata['use_cases_url']='/useCases/'+profile_metadata['name']

                with open('bioschemas-dde/draft_profile_list.txt') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 0
                    for row in csv_reader:
                        line_count += 1
                        if line_count > 1:
                            fields = row[0].split('\t')
                            if fields[1]==profile_metadata['name']:
                                #print(f'\n namespace={fields[0]}, name={fields[1]}, subclassof={fields[2]}, type={fields[3]}, version={fields[4]}, url={fields[5]}.')    

                                profile_metadata['redirect_from']=list()
                                profile_metadata['hierarchy']=list()
                                profile_metadata['previous_version']=fields[4]
                                profile_metadata['previous_release']=""
                                profile_metadata['status']=""
                                profile_metadata['spec_type']=fields[3]
                                profile_metadata['group']="tools"
                                profile_metadata['cross_walk_url']=fields[5]
                                profile_metadata['gh_tasks']=""
                                profile_metadata['live_deploy']="/liveDeploys"
                                profile_metadata['parent_type']=""

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
            
            message='''
# spec_info content generated using GOWeb
# DO NOT MANUALLY EDIT THE CONTENT
'''
            with open(out_HTML_file, "w", encoding="utf-8") as o:
                o.write('''---
''')
                yaml.dump(profile_metadata, o)
                o.write(message)
                yaml.dump(transformed_profile, o)
                o.write("---")

            print(Style.BRIGHT + "HTML Profile page created " + out_HTML_file + Style.RESET_ALL)
