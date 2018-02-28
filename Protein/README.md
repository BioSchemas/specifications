# Protein specification v. 0.4 

**Profile** 

Thing > BioChemEntity(Protein profile)

**Bioschemas specification describing a Protein (BioChemEntity profile) in Life Sciences** 

## Description 
This Protein profile specification presents the BioChemEntity usage when describing a Protein. 
## Links 
- [Stable specification at bioschemas.org](http://bioschemas.org/specifications/Protein/specification/)
- [Specification candidate release](proteinProfileSpecification.html)
- [Mapping Spreadsheet](https://docs.google.com/spreadsheets/d/1WZmPPEPa6JE4iq3OSQOatUH5TeSvWj5lcRi_kDTSayU/edit?usp=drivesdk)
- [Coding Examples](https://github.com/BioSchemas/specifications/tree/master/Protein/examples)
- [GitHUb Issues](https://github.com/BioSchemas/bioschemas/labels/type%3A%20Protein)
## Examples
We include examples not just for proteins but also for records describing proteins. As Protein we will model the entity itself (name, organism, gene, and so), while as Record we will model a bit more technical stuff (latest modifed date, dataset where it belongs to, citations, distribution and so).
- [Protein entity in JSON-LD](https://github.com/BioSchemas/specifications/blob/master/Protein/examples/ProteinEntity-with-context.json)
- [Protein entity in Turtle](https://github.com/BioSchemas/specifications/blob/master/Protein/examples/ProteinEntity-with-context.n3)
- [Record of a protein entity](https://github.com/BioSchemas/specifications/blob/master/Protein/examples/ProteinRecord.json)
- [Full example of a protein record about a protein entity](https://github.com/BioSchemas/specifications/blob/master/Protein/examples/ProteinRecordAndEntity_wtihContext.json)
## Links to other relevant types/profiles
Protein records will be included in a Dataset which will belong to a DataCatalog. A Protein can also be related to Protein Annotation or Protein Structure
- [DataCatalog](https://github.com/BioSchemas/specifications/blob/master/DataCatalog/examples/UniProt.json)
- [Dataset](https://github.com/BioSchemas/specifications/blob/master/Dataset/examples/uniprot.json)
## Validation
- [ShEx](http://shex.io/shex-primer/index.html)
  - [Protein profile](https://github.com/BioSchemas/specifications/blob/master/Protein/ProteinEntity-with-context.shex)
  - [Try it on!](Currently broken, working on it!) 
- With [SHACL](https://www.w3.org/TR/shacl/), coming soon

