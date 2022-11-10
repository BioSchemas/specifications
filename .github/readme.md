# Steps to Render a Bioschemas Profile on the Bioschema Website

It is assumed that you have already made the edits to the profile (see this [tutorial](/tutorials/dde/) for details on how to edit a profile), stored it in the [Bioschemas Specification repository](https://github.com/BioSchemas/specifications), and that you are now ready to get it published on the Bioschemas website.

## 1. Manual Configuration in the Website Repository
For new profiles:

1. Create a new branch in the [Bioschemas website repository](https://github.com/BioSchemas/bioschemas.github.io) with a suitable name to identify the intended outcome of the work, e.g. for a new "example profile" we might have `draft-example-0.1`.
1. In the `_data/profile_versions.yaml` file, add an entry for the new profile replicating the information in other draft profiles.
1. In the `_data/metadata_mapping.csv` file add a row for your profile stating the profile name and working group name.
1. Create a pull request from your branch to the master.

## 2 Automated Rendering (Github Action)

Once the pull request in the specifiaction repository is merged, a [GitHub Action workflow](.github/workflows/generate_profile_workflow.yml) is launched. It converts the JSON-LD representation of the Bioschemas profile from the specifications repository into the format needed for the Bioschemas website. 

*Workflow steps (shown in figure below):*

![Computational Tool Workflow Steps](https://i.imgur.com/XPC7M3k.png)

1. Clone the [specification repository](https://github.com/BioSchemas/specifications) and retreive the last commit.
1. Clone the [website](https://github.com/BioSchemas/bioschemas.github.io)  repository.
2. Execute a [python script](https://github.com/BioSchemas/specifications/blob/last-modif/.github/workflows/config_file_update_script.py) that will update some config files:
    1. Get the [profile versioning config file](https://github.com/BioSchemas/bioschemas.github.io/blob/profile-auto-generation/_data/profile_versions.yaml) from the website repository and parse it
    2. Check if the profile exists in the file
    3. Update it's version 
4. Execute a [python script](https://github.com/BioSchemas/specifications/blob/cleanup-branch/.github/workflows/profile_generation_script.py) that will generate the profile:
    1. Maps each field of the JSON-LD to properties in the profile
    1. Generates a YAML from this mapping
    1. Transforms the YAML into an HTML file
    1. Write the file in the appropriate profiles folder in the website repository
5. Setup the GitHub TOKEN, so the GitHub action can publish into the website repository. 
6. Commit and push the changes in an intermediate branch. The file has the following name pattern: profile name + today's date concatenated. e.g: `ComputationalTool-2022-08-17`.
7. Creates a Pull Request from the branch to be integrated into the master branch.

### 3.3  To the Web
Now, if you go to the [bioschemas repository pull requests](https://github.com/BioSchemas/bioschemas.github.io/pulls), you should find a PR for the generated branch.
You just need to merge it to master branch and your profile will be taken into consideration in the [bioschemas website](https://bioschemas.org/profiles/).

## 3. Possible Occuring Problems

### 3.1 At the workflow level

* The Github TOKEN that the github action is using to add and commit a change in the Github action is owned by [Sahar Frikha](https://github.com/sahar-frikha/).

### 3.2 At the python script level
* The format of the generated HTML is tightly coupled to the Jekyll Profile template used to render the profile as a web page. Any modifications to the template should be taken into consideration in the python script. For now, we are following this [template](https://github.com/BioSchemas/bioschemas.github.io/blob/render-dde-profile-json/_layouts/profile.html).

## 4. Sequence Diagram
The following [diagram](https://app.diagrams.net/#G1xGR7iElX8lD3Dq7Eqg4mpsfbLuVyE0dx) illustrates how files are routed through the three main entities: DDE, Bioschemas specifications and Bioschemas website repositories.


![Sequence Diagram](https://i.imgur.com/47Mff4k.png)