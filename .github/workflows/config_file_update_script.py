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

stream = open(profile_verions_file, "r")
docs = yaml.load_all(stream, yaml.FullLoader)

d = {}

for doc in docs:
    try:
        for k, v in doc.items():
            print(k, "->", v)
            d[k] = v
            print("\n")
    except Exception as e:
        print(e)

args = sys.argv

# For each new uploaded JSON-LD file
for arg in args:
    if "jsonld" in arg.split("/"):
        if "json" in arg.split("."):
            arglist = arg.split("/")
            profile_name = arg.split("/")[-1].split(".")[0].split("_")[0]
            profile_version = arg.split("_")[1].split("v")[1].split(".json")[0]

            print(
                Fore.LIGHTBLUE_EX
                + "profile name and version: "
                + profile_name
                + ", "
                + profile_version
                + Style.RESET_ALL
            )

            if profile_name in d.keys():
                if arg.split("-")[1].split(".")[0] == "DRAFT":
                    print(Fore.GREEN + str(d[profile_name]) + Style.RESET_ALL)
                elif arg.split("-")[1].split(".")[0] == "RELEASE":
                    print(Fore.GREEN + str(d[profile_name]) + Style.RESET_ALL)

print(
    Fore.YELLOW + "Profile versions updated " + profile_verions_file + Style.RESET_ALL
)
