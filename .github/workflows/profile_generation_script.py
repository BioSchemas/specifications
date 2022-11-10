import json
from pathlib import Path
from pydoc import doc
from unittest import skip
import uuid
import yaml
from colorama import Fore
from colorama import Style
import sys
import os.path
import csv
from os import path
import datetime


def generate_transformed_profile(
    data, g, path_changed_file, external_properties, dict_definitions
):

    transformed_profile = dict()

    ### Spec_info
    transformed_profile["spec_info"] = generate_spec_info(g, path_changed_file)

    ### Mapping
    transformed_profile["mapping"] = list(dict())

    # Browse properties by marginality and add them to the mappings
    if "$validation" in g.keys():
        transformed_profile["spec_type"] = "Profile"
        for req_label in g["$validation"]["required"]:
            prop = g["$validation"]["properties"][req_label]
            new_p = generate_property(
                data,
                g,
                prop,
                req_label,
                "Minimum",
                external_properties,
                dict_definitions,
            )
            transformed_profile["mapping"].append(new_p)

        for reco_label in g["$validation"]["recommended"]:
            prop = g["$validation"]["properties"][reco_label]
            new_p = generate_property(
                data,
                g,
                prop,
                reco_label,
                "Recommended",
                external_properties,
                dict_definitions,
            )
            transformed_profile["mapping"].append(new_p)

        for opt_label in g["$validation"]["optional"]:
            prop = g["$validation"]["properties"][opt_label]
            new_p = generate_property(
                data,
                g,
                prop,
                opt_label,
                "Optional",
                external_properties,
                dict_definitions,
            )
            transformed_profile["mapping"].append(new_p)
    else:
        transformed_profile["spec_type"] = "Type"

    ### Generate the metadata
    transformed_profile["name"] = g["@id"].split(":")[1]
    transformed_profile["use_cases_url"] = "/useCases/" + transformed_profile["name"]

    # with open("bioschemas-dde/draft_profile_list.txt") as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter=",")
    #     line_count = 0
    #     for row in csv_reader:
    #         line_count += 1
    #         if line_count > 1:
    #             fields = row[0].split("\t")
    #             if fields[1] == transformed_profile["name"]:
    #                 # print(f'\n namespace={fields[0]}, name={fields[1]}, subclassof={fields[2]}, type={fields[3]}, version={fields[4]}, url={fields[5]}.')
    #                 transformed_profile["type"] = {fields[3]}

    transformed_profile["previous_version"] = get_previous_version(path_changed_file)
    transformed_profile["previous_release"] = get_previous_release(path_changed_file)
    transformed_profile["status"] = get_status(
        transformed_profile["spec_info"]["version"]
    )
    transformed_profile["group"] = get_group(transformed_profile["name"])
    transformed_profile["cross_walk_url"] = get_cross_walk_url(
        transformed_profile["name"]
    )
    transformed_profile["gh_tasks"] = (
        "https://github.com/Bioschemas/specifications/labels/type%3A%20"
        + transformed_profile["name"]
    )
    transformed_profile["live_deploy"] = "/liveDeploys"
    transformed_profile["parent_type"] = transformed_profile["spec_info"][
        "official_type"
    ]
    transformed_profile["redirect_from"] = get_redirect_from(
        transformed_profile["name"]
    )
    transformed_profile["hierarchy"] = get_hierarchy()
    transformed_profile["json-ld_url"] = arg
    transformed_profile["dde_ui_url"] = "https://discovery.biothings.io/view/"

    if transformed_profile["spec_type"] == "Profile":
        if arg.split("-")[1].split(".")[0] == "DRAFT":
            transformed_profile["dde_ui_url"] = (
                transformed_profile["dde_ui_url"]
                + "bioschemasdrafts/bioschemasdrafts:"
                + transformed_profile["name"]
            )
        elif arg.split("-")[1].split(".")[0] == "RELEASE":
            transformed_profile["dde_ui_url"] = (
                transformed_profile["dde_ui_url"]
                + "bioschemas/bioschemas:"
                + transformed_profile["name"]
            )
    else:
        if arg.split("-")[1].split(".")[0] == "DRAFT":
            transformed_profile["dde_ui_url"] = (
                transformed_profile["dde_ui_url"]
                + "bioschemastypesdrafts/bioschemastypesdrafts:"
                + transformed_profile["name"]
            )
        elif arg.split("-")[1].split(".")[0] == "RELEASE":
            transformed_profile["dde_ui_url"] = (
                transformed_profile["dde_ui_url"]
                + "bioschemas/bioschemastypes/bioschemastypes:"
                + transformed_profile["name"]
            )

    for i in transformed_profile:
        if i != "spec_info" and i != "mapping":
            print(
                Fore.YELLOW
                + Style.BRIGHT
                + f"{i} = {transformed_profile[i]}"
                + Style.RESET_ALL
            )

    return transformed_profile


# display all files and get the -1 file
from os import listdir
from os.path import isfile, join


def get_previous_version(arg):
    previous_version = ""

    mypath = arg.split("/")[0] + "/" + arg.split("/")[1]
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    if arg.split("-")[1].split(".")[0] == "DRAFT":
        print("Get the DRAFT just before")
        arg_version = arg.split("_")[1].split("v")[1].split("-")[0]
        max = int(arg_version.split(".")[1]) - 1
        curent_previous_version = 0
        for f in onlyfiles:
            if f.split("_")[1].split("-")[1].split(".")[0] == "DRAFT":
                file_version = f.split("_")[1].split("v")[1].split("-")[0]
                if int(file_version.split(".")[0]) == int(
                    arg.split("_")[1].split("v")[1].split("-")[0].split(".")[0]
                ):
                    if (
                        int(file_version.split(".")[1]) <= max
                        and int(file_version.split(".")[1]) > curent_previous_version
                    ):
                        previous_version = f.split(".json")[0].split("_v")[1]
                        curent_previous_version = int(
                            f.split(".json")[0]
                            .split("_v")[1]
                            .split("-")[0]
                            .split(".")[1]
                        )

    elif arg.split("-")[1].split(".")[0] == "RELEASE":
        print("Get simply the last draft")
        arg_version = arg.split("_")[1].split("v")[1].split("-")[0]
        max = int(arg_version.split(".")[1])
        curent_previous_version = 0

        for f in onlyfiles:
            if f.split("_")[1].split("-")[1].split(".")[0] == "DRAFT":
                file_version = f.split("_v")[1].split("-")[0]
                if (
                    int(file_version.split(".")[0])
                    == int(arg.split("_")[1].split("v")[1].split("-")[0].split(".")[0])
                    - 1
                ):

                    if (
                        int(file_version.split(".")[1])
                        <= int(
                            arg.split("_")[1].split("v")[1].split("-")[0].split(".")[1]
                        )
                        - 1
                    ):
                        if (
                            int(file_version.split(".")[1]) <= max
                            and int(file_version.split(".")[1])
                            > curent_previous_version
                        ):
                            previous_version = f.split(".json")[0].split("_v")[1]
                            curent_previous_version = int(
                                f.split(".json")[0]
                                .split("_v")[1]
                                .split("-")[0]
                                .split(".")[1]
                            )
    return previous_version


def get_previous_release(arg):
    previous_release = ""

    mypath = arg.split("/")[0] + "/" + arg.split("/")[1]
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    if arg.split("-")[1].split(".")[0] == "DRAFT":
        # Get the last Release
        for f in onlyfiles:
            if f.split("_")[1].split("-")[1].split(".")[0] == "RELEASE":
                version = f.split("_")[1].split("v")[1].split("-")[0]  # "O.2"
                if int(version.split(".")[0]) == int(
                    arg.split("_")[1].split("v")[1].split("-")[0].split(".")[0]
                ):

                    previous_release = f.split(".json")[0].split("_v")[1]

    elif arg.split("-")[1].split(".")[0] == "RELEASE":
        # Get release just before
        for f in onlyfiles:
            if f.split("_")[1].split("-")[1].split(".")[0] == "RELEASE":
                version = f.split("_")[1].split("v")[1].split("-")[0]  # "O.2"

                if (
                    int(version.split(".")[0])
                    == int(arg.split("_")[1].split("v")[1].split("-")[0].split(".")[0])
                    - 1
                ):
                    previous_release = f.split(".json")[0].split("_v")[1]

    return previous_release


# if its draft it's revision, case release, deprecated
def get_status(version):
    status = ""
    if version.split("-")[-1] == "DRAFT":
        status = "revision"
    elif version.split("-")[-1] == "RELEASE":
        status = "deprecated"
    return status


# Create a mapping file grp == classes, and put it in the _data/ then fetch them from there
def get_group(profile_name):
    group = ""

    with open("bioschemas.github.io/_data/metadata_mapping.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            line_count += 1
            if line_count > 1:
                if row[0] == profile_name:
                    group = row[1]
    return group


# same as grps, we need a mapping file. [The admin should make sure he updates the config files in the right order!]
def get_cross_walk_url(profile_name):
    cross_walk_url = ""

    with open("bioschemas.github.io/_data/metadata_mapping.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            line_count += 1
            if line_count > 1:
                if row[0] == profile_name:
                    cross_walk_url = row[5]

    return cross_walk_url


# follow the pattern for most, and when I see an exception, hardcoded it an dictionary
def get_redirect_from(profile_name):
    redirect_from = list()

    with open("bioschemas.github.io/_data/metadata_mapping.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            line_count += 1
            if line_count > 1:
                if row[0] == profile_name:
                    redirect_from = row[2]

    return redirect_from


# from the profiles json-ld :
def get_hierarchy():
    hierarchy = list()

    return hierarchy


def generate_spec_info(g, path_changed_file):
    spec_info = dict()

    if "rdfs:label" in g.keys():
        spec_info["title"] = g["rdfs:label"]
    else:
        spec_info["title"] = path_changed_file.split("_")[0]

    if "rdfs:comment" in g.keys():
        spec_info["description"] = g["rdfs:comment"]
    else:
        spec_info["description"]

    spec_info["version"] = arg.split("/")[-1].split(".json")[0].split("v")[-1]

    spec_info["version_date"] = (
        str(datetime.datetime.now().date().year)
        + str(datetime.datetime.now().date().month)
        + str(datetime.datetime.now().date().day)
        + "T"
        + str(datetime.datetime.now().time().hour)
        + str(datetime.datetime.now().time().minute)
        + str(datetime.datetime.now().time().second)
    )

    if "rdfs:subClassOf" in g.keys():
        spec_info["official_type"] = g["rdfs:subClassOf"]["@id"].split(":")[1]
    else:
        spec_info["official_type"] = ""

    spec_info["full_example"] = (
        "https://github.com/BioSchemas/specifications/tree/master/"
        + spec_info["title"]
        + "/examples"
    )

    return spec_info


def generate_property(
    data, g, prop, req_label, marginality, external_properties, dict_definitions
):

    new_p = dict()

    # Replace property definitions with their type
    for g in data["@graph"]:
        if req_label == g["rdfs:label"]:
            if not "bioschemas" in g["@id"].split(":")[0]:
                req_label = g["@id"]

    new_p["property"] = req_label
    print(Fore.GREEN + Style.BRIGHT + f"Property : {req_label}" + Style.RESET_ALL)
    new_p["marginality"] = marginality
    new_p["cardinality"], new_p["expected_types"] = generate_types_cardianlity(g, prop)

    if "owl:cardinality" in prop.keys():
        new_p["cardinality"] = prop["owl:cardinality"].upper()

    if "description" in prop.keys():
        new_p["description"] = prop["description"]
    else:
        new_p["description"] = ""
    if "type_url" in prop.keys():
        new_p["type_url"] = prop["type_url"]
    else:
        new_p["type_url"] = ""
    if "bsc_description" in prop.keys():
        new_p["bsc_description"] = prop["bsc_description"]
    else:
        new_p["bsc_description"] = ""
    if "controlled_vocab" in prop.keys():
        new_p["controlled_vocab"] = prop["controlled_vocab"]
    else:
        new_p["controlled_vocab"] = ""

    if "example" in prop.keys():
        new_p["example"] = prop["example"]
    else:
        new_p["example"] = ""

    # Here we'll suppose that all properties are in default schemas.org !!!!!!!
    new_p["type"] = ""
    for p in external_properties:
        if len(p.split(":")) > 1:
            if req_label == p.split(":")[1]:
                if len(p.split(":")[0].split("bioschemas")) > 1:
                    new_p["type"] = "bioschemas"
                else:
                    new_p["type"] = p.split(":")[0]
    t = new_p["type"]
    print(Fore.GREEN + Style.DIM + f"Property type : {t}" + Style.RESET_ALL)

    return new_p


def generate_types_cardianlity(g, prop):

    list_types = list()
    cardianliy = "ONE"

    if "type" in prop.keys():
        if "format" in prop.keys():
            list_types.append(prop["format"])
        else:
            list_types.append(prop["type"])

    if "$ref" in prop.keys():
        list_types.append(prop["$ref"])

    if "anyOf" in prop.keys():
        for e in prop["anyOf"]:
            if "format" in e.keys():
                list_types.append(e["format"])
            elif "items" in e.keys():
                list_types.append(e["items"])
                cardianliy = "MANY"
            else:
                for t in e.keys():
                    list_types.append(e[t])

    if "oneOf" in prop.keys():
        for e in prop["oneOf"]:
            if "format" in e.keys():
                list_types.append(e["format"])
            elif "items" in e.keys():
                list_types.append(e["items"])
                cardianliy = "MANY"
            else:
                for t in e.keys():
                    list_types.append(e[t])

    i = 1
    j = 1
    while i == 1:
        i = 0
        j = j + 1
        for t in list_types:
            if isinstance(t, dict):
                i = 1
                e = t
                list_types.remove(t)
                if "format" in e.keys():
                    list_types.append(e["format"])
                else:
                    for sous_type in e.keys():
                        list_types.append(e[sous_type])

    if len(list_types) == 0:
        cardianliy = ""

    ### Some cleaning up
    expected_types = []
    remove_deplicates_expected_types = []
    upper_case_expected_types = []

    for t in list_types:
        if len(t.split("/")) > 1:
            expected_types.append(t.split("/")[-1])
        else:
            expected_types.append(t)

    # Remove duplicates
    remove_deplicates_expected_types = list(set(expected_types))

    # Some treatments on the type's label
    clean_expected_types = remove_deplicates_expected_types

    # Replace 'String' with 'Text'
    for i in remove_deplicates_expected_types:
        if i == "string":
            clean_expected_types.remove(i)
            clean_expected_types.append("Text")

    # Replace 'Uri' with 'URI'
    for i in remove_deplicates_expected_types:
        if i == "uri":
            clean_expected_types.remove(i)
            clean_expected_types.append("URL")

    # Replace property definitions with their type
    # Replace property definitions with their type
    for i in remove_deplicates_expected_types:
        if i in dict_definitions.keys():
            if not "bioschemas" and not "schema" in dict_definitions[i]:
                clean_expected_types.remove(i)
                clean_expected_types.append(dict_definitions[i])
            elif len(dict_definitions[i].split(":")) > 0:
                clean_expected_types.remove(i)
                clean_expected_types.append(dict_definitions[i].split(":")[-1])

    upper_case_expected_types = clean_expected_types
    for i in upper_case_expected_types:

        t = ""

        for c in range(len(i)):
            if c == 0:
                t += i[c].upper()
            else:
                t += i[c]
        print(t)
        clean_expected_types.remove(i)
        clean_expected_types.append(t)

    print(Fore.MAGENTA + f"Expected Types : {clean_expected_types}" + Style.RESET_ALL)

    print(Fore.RED + f"Cardinality = {cardianliy}" + Style.RESET_ALL)

    return cardianliy, sorted(clean_expected_types)


# ## Main Script

args = sys.argv
website_repo = args[-1]
args.remove(website_repo)

# For each new uploaded JSON-LD file
for arg in args:
    if "jsonld" in arg.split("/"):
        if "json" in arg.split("."):
            arglist = arg.split("/")

            profile_name = arg.split("/")[-1].split(".json")[0].split("_")[0]

            print(Fore.YELLOW + "added/updated profile: " + arg + Style.RESET_ALL)

            in_file = "./" + arg

            with open(in_file, "r", encoding="utf-8") as i:
                data = json.load(i)

            # print(json.dumps(data['@graph'][0], indent=True))

            external_properties = []
            for g in data["@graph"]:
                if g["@type"] == "rdf:Property":
                    external_properties.append(g["@id"])

            for g in data["@graph"]:
                if g["@type"] == "rdfs:Class":
                    print(
                        Fore.BLUE
                        + Style.BRIGHT
                        + f'Profile : {g["@id"]}'
                        + Style.RESET_ALL
                    )
                    # Dictionary of all external definitions
                    dict_definitions = dict()

                    if "$validation" in g.keys():
                        if "definitions" in g["$validation"].keys():
                            for d in g["$validation"]["definitions"]:
                                dict_definitions[d] = g["$validation"]["definitions"][
                                    d
                                ]["@type"]
                        else:
                            print(
                                Fore.RED
                                + Style.BRIGHT
                                + "WARNING: There was no definitions parsed!"
                            )
                        # For each profile :
                        # Prepare the transfermed profile : spec_info & mapping fields
                        transformed_profile = generate_transformed_profile(
                            data, g, arg, external_properties, dict_definitions
                        )

                        # Inject the YAML in a HTML File
                        # Note: The folder should be in the transformed_profile["spec_info"]["title"] folder

                        ### PROBLEM: if the forlder "profile name" doesn't exist it will throw an exception, so we need to create it manually

                        folderpath = (
                            "./" + website_repo + "/pages/_profiles/" + profile_name
                        )
                        # out_YAML_file = folderpath+"/"+"generated_"+profile_name+".yaml"
                        out_HTML_file = (
                            folderpath
                            + "/"
                            + arg.split("/")[-1].split(".json")[0].split("v")[-1]
                            + ".html"
                        )

                        if path.exists(folderpath):
                            print("folder esists")
                        else:
                            # os.makedirs(os.path.dirname(folderpath), exist_ok=True)
                            Path(folderpath).mkdir(parents=True, exist_ok=True)
                            print("Create folder : ", folderpath)

                        # with open(out_YAML_file, "w", encoding="utf-8") as o:
                        #    yaml.dump(transformed_profile, o)

                        # print(Style.BRIGHT + "Transformed profiles Generated and saved in " + out_YAML_file + Style.RESET_ALL)

                        message = """---
# spec_info content generated using GOWeb
# DO NOT MANUALLY EDIT THE CONTENT
"""
                        with open(out_HTML_file, "w", encoding="utf-8") as o:
                            o.write(message)
                            yaml.dump(transformed_profile, o)
                            o.write("---")

                        print(
                            Style.BRIGHT
                            + "HTML Profile page created "
                            + out_HTML_file
                            + Style.RESET_ALL
                        )

                        ############# DDE REPOSITORY #############
                        dde_folderpath = "./bioschemas-dde/latest-updated-profiles"
                        if path.exists(dde_folderpath):
                            print("Folder latest-updated-profiles exists in DDE")
                        else:
                            # os.makedirs(os.path.dirname(folderpath), exist_ok=True)
                            Path(dde_folderpath).mkdir(parents=True, exist_ok=True)
                            print("Create folder in DDE: ", dde_folderpath)

                        latest_updated_profiles = (
                            dde_folderpath + "/" + profile_name + ".csv"
                        )

                        header = [
                            "time",
                            "namespace",
                            "name",
                            "subclassOf",
                            "version",
                            "url",
                        ]

                        SubClass = ""

                        with open(
                            "bioschemas.github.io/_data/metadata_mapping.csv"
                        ) as csv_file:
                            csv_reader = csv.reader(csv_file, delimiter=",")
                            line_count = 0
                            for row in csv_reader:
                                line_count += 1
                                if line_count > 1:
                                    if row[0] == profile_name:
                                        SubClass = row[4]

                        data = [
                            uuid.uuid1(),
                            "bioschams",
                            profile_name,
                            SubClass,
                            arg.split("_")[1].split(".json")[0],
                            "https://github.com/BioSchemas/specifications/tree/master/"
                            + arg,
                        ]

                        with open(latest_updated_profiles, "w", encoding="utf-8") as f:
                            writer = csv.writer(f)

                            # write the header
                            writer.writerow(header)

                            # write the data
                            writer.writerow(data)
                    else:
                        print(
                            Fore.RED
                            + Style.BRIGHT
                            + "WARNING: There was no $validation to parse!"
                        )
