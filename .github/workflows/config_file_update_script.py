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

profile_verions_file = "./bioschemas.github.io/_data/profile_versions.yaml"

if path.exists(profile_verions_file):
    print("file esists")

    with open(profile_verions_file) as f:
        data = yaml.load(f, Loader=SafeLoader)
        print(data)

    print(
        Style.BRIGHT
        + "Profile versions updated "
        + profile_verions_file
        + Style.RESET_ALL
    )
