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
    with open(profile_verions_file, "r") as stream:
        try:
            print(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)

    print(
        Style.BRIGHT
        + "Profile versions updated "
        + profile_verions_file
        + Style.RESET_ALL
    )
