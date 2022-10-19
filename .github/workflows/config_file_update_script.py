import json
from pathlib import Path
import yaml
from colorama import Fore
from colorama import Style
import sys
import csv
from os import path
from os import listdir
from os.path import isfile, join
from yaml.loader import SafeLoader

## Main Script
print(Fore.YELLOW + "Started updating profile versions config file" + Style.RESET_ALL)

profile_verions_file = "profile_versions.yaml"
# profile_verions_file = "./bioschemas.github.io/_data/profile_versions.yaml"

stream = open(profile_verions_file, "r")
docs = yaml.load_all(stream, yaml.FullLoader)
for doc in docs:
    for k,v in doc.items():
        print (k, "->", v)
    print ("\n"),


print(
    Style.BRIGHT
    + "Profile versions updated "
    + profile_verions_file
    + Style.RESET_ALL
)
