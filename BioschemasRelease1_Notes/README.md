# Types to support discovery of life sciences resources

The [Bioschemas Community](https://bioschemas.org/) have prepared an initial set of types for representing core life sciences resources to be considered for inclusion in Schema.org. The types support searching for resources, but leave the accurate modelling of bioinformatics to the numerous specialised overlapping domain ontologies. For each type, leading domain ontologies have been considered.

The collection of types focuses on genes, proteins, and their chemical interactions. We have proposed one generic type (BioChemEntity) under which we expect the majority of Bioschemas proposed types to sit. We believe that Taxon is a more generic type and have thus not put it under BioChemEntity. Development work on other types continues and can be seen in the drafts section of the [types page](https://bioschemas.org/types/).

The development of the types has been driven by use cases and experiences from working deployed markup (list of [live deployments](https://bioschemas.org/liveDeploys/)). Each type is available from the Bioschemas [website](https://bioschemas.org/types/) with detailed notes on the modelling of the type included in the Bioschemas examples [repository](https://github.com/BioSchemas/specifications/tree/master/BioschemasRelease1_Notes). We also include a link to a live deployment of the type.

## Proposed Types and Hierarchy

- Thing
  - [BioChemEntity](https://bioschemas.org/BioChemEntity) ([notes](BioChemEntityCodingNotes.md)) *abstract type not expected to have deployments*
    - [ChemicalSubstance](https://bioschemas.org/ChemicalSubstance) ([notes](ChemicalSubstanceCodingNotes.md)) deployment on [NanoCommons](https://www.nanocommons.eu/) ([Google SDTT](https://search.google.com/structured-data/testing-tool?url=https://nanocommons.github.io/specifications/jrc/))
    - [Gene](https://bioschemas.org/Gene) ([notes](GeneCodingNotes.md)) deployment on [eDGAR](http://edgar.biocomp.unibo.it/cgi-bin/gene_disease_db/gene.py?gene=A2M) ([Google SDTT](https://search.google.com/structured-data/testing-tool?url=http://edgar.biocomp.unibo.it/cgi-bin/gene_disease_db/gene.py?gene=A2M))
    - [MolecularEntity](https://bioschemas.org/MolecularEntity) ([notes](MolecularEntityCodingNotes.md)) deployment on [ChEMBL](https://www.ebi.ac.uk/chembl/compound_report_card/CHEMBL59/) ([Google SDTT](https://search.google.com/structured-data/testing-tool#url=https%3A%2F%2Fwww.ebi.ac.uk%2Fchembl%2Fbeta%2Fcompound_report_card%2FCHEMBL59%2F))
    - [Protein](https://bioschemas.org/Protein) ([notes](ProteinCodingNotes.md)) deployment on [DisProt](https://www.disprot.org/DP00086) ([Google SDTT](https://search.google.com/structured-data/testing-tool?url=https://www.disprot.org/DP00086))
  - [Taxon](https://bioschemas.org/Taxon) ([notes](TaxonCodingNotes.md)) deployment at [Muséum National D’Histoire Naturelle](https://inpn.mnhn.fr/espece/cd_nom/60878/) ([Google SDTT](https://search.google.com/structured-data/testing-tool?url=https://inpn.mnhn.fr/espece/cd_nom/60878/))

## Ontologies Considered

This is a non-exhaustive list of domain specific and general purpose ontologies that have been considered during the development of the Bioschemas types:

- Biodiversity Information Standards ([TDWGOntology](https://github.com/tdwg/ontology))
- Chemical Entities of Biological Interest ([ChEBI](https://www.ebi.ac.uk/chebi/))
- Chemical Information Ontology ([CHEMINF](http://semanticchemistry.github.io/semanticchemistry/))
- Feature Annotation Location Description Ontology ([FALDO](https://github.com/OBF/FALDO))
- Gene Ontology ([GO](http://geneontology.org/))
- NCBI [Taxonomy](https://www.ncbi.nlm.nih.gov/taxonomy)Protein Ontology ([PRO](https://proconsortium.org/))
- SemanticScience Integrated Ontology ([SIO](http://sio.semanticscience.org/))
- UniProt RDF Schema Ontology ([UniProt](https://www.uniprot.org/core/))
- Wikidata [Ontology](https://www.wikidata.org/wiki/Wikidata:WikiProject_Ontology/Modelling)
