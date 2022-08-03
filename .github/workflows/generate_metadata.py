# display all files and get the -1 file
from os import listdir
from os.path import isfile, join
from colorama import Fore
from colorama import Style

def get_previous_version(path_changed_file):
    previous_version=""
    
    mypath="../"+path_changed_file.split('/')[0]+path_changed_file.split('/')[1]
    
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    
    print(Fore.Green + Style.BRIGHT + f'{onlyfiles}' + Style.RESET_ALL)
    return previous_version

def get_previous_release(path_changed_file):
    previous_release=""
    
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
def get_group():
    group=""
    
    return group

# same as grps, we need a mapping file. [The admin should make sure he updates the config files in the right order!]
def get_cross_walk_url():
    cross_walk_url=""
    
    return cross_walk_url

# follow the pattern for most, and when I see an exception, hardcoded it an dictionary
def get_redirect_from():
    redirect_from=list() 
    
    return redirect_from

def get_hierarchy():
    hierarchy=list()
    
    return hierarchy