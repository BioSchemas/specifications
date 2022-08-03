
from generate_spec_info import generate_spec_info
from generate_property import generate_property
from colorama import Fore
from colorama import Style
from generate_metadata import *

def generate_transformed_profile(g, path_changed_file):
    
    transformed_profile = dict()
    
    ### Spec_info
    transformed_profile["spec_info"] = generate_spec_info(g)    
    
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

    ### Generate the metadata
    transformed_profile['name']=g["@id"].split(':')[1]
    transformed_profile['use_cases_url']='/useCases/'+transformed_profile['name']

    with open('draft_profile_list.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
            if line_count > 1:
                fields = row[0].split('\t')
                if fields[1]==transformed_profile['name']:
                    #print(f'\n namespace={fields[0]}, name={fields[1]}, subclassof={fields[2]}, type={fields[3]}, version={fields[4]}, url={fields[5]}.')    
                    transformed_profile['spec_type']={fields[3]}
    
    transformed_profile['previous_version']=get_previous_version(path_changed_file)
    transformed_profile['previous_release']= get_previous_release(path_changed_file)
    transformed_profile['status']=get_status(transformed_profile["spec_info"]["version"])
    transformed_profile['group']=get_group()
    transformed_profile['cross_walk_url']=get_cross_walk_url()
    transformed_profile['gh_tasks']= "https://github.com/Bioschemas/specifications/labels/type%3A%20"+transformed_profile['name']
    transformed_profile['live_deploy']="/liveDeploys"
    transformed_profile['parent_type']=transformed_profile["spec_info"]["official_type"]
    transformed_profile['redirect_from']=get_redirect_from()
    transformed_profile['hierarchy']=get_hierarchy()
    
    
    for i in transformed_profile:
        if i !="spec_info" and i!="mapping":
            print(Fore.YELLOW + Style.BRIGHT + f'{i} = {transformed_profile[i]}' + Style.RESET_ALL)    

    return transformed_profile