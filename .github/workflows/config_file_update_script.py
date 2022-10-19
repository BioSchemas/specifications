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

if path.exists(profile_verions_file):
    with open(profile_verions_file, "r", encoding="utf-8") as f:
        print(Fore.YELLOW + "File opened!" + Style.RESET_ALL)

        try:
            print(yaml.safe_load(f))
        except yaml.YAMLError as exc:
            print(exc)

    print(
        Style.BRIGHT
        + "Profile versions updated "
        + profile_verions_file
        + Style.RESET_ALL
    )
