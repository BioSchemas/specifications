# Types to support discovery of life sciences resources

The [Bioschemas Community](https://bioschemas.org/) have prepared seven types to be considered for inclusion in Schema.org. The types support searching for resources, but leave the accurate modelling of bioinformatics to the numerous specialised overlapping domain ontologies. For each type, leading domain ontologies have been considered.

The collection of types focuses on genes, proteins, and their chemical interactions. We have proposed one generic type (BioChemEntity) under which we expect the majority of Bioschemas proposed types to sit. We believe that Taxon is a more generic type and have thus not put it under BioChemEntity.

The development of the types has been driven by use cases and experiences from working deployed markup. Each type is available from the Bioschemas website with detailed notes on the modelling of the type included in the Bioschemas examples repository. We also include a link to a live deployment of the type.

## Proposed Types and Hierarchy

- Thing
  - [BioChemEntity](https://bioschemas.org/BioChemEntity) ([notes](https://github.com/BioSchemas/specifications/tree/master/BioschemasRelease1_Notes/BioChemEntityCodingNotes.md)) *abstract type not expected to have deployments* 
    - [BioSample](https://bioschemas.org/BioSample) ([notes](https://github.com/BioSchemas/specifications/tree/master/BioschemasRelease1_Notes/BioSampleCodingNotes.md)) 10 million+ pages on [BioSamples](https://www.ebi.ac.uk/biosamples/samples/SAMEA491372) ([Google SDTT](https://search.google.com/structured-data/testing-tool#url=https%3A%2F%2Fwww.ebi.ac.uk%2Fbiosamples%2Fsamples%2FSAMEA491372)), further deployments in development
    - [ChemicalSubstance](https://bioschemas.org/ChemicalSubstance) ([notes](https://github.com/BioSchemas/specifications/tree/master/BioschemasRelease1_Notes/ChemicalSubstanceCodingNotes.md)) test server deployment on [AMBIT](http://ambit.sourceforge.net/) for eNanoMapper
    - [Gene](https://bioschemas.org/Gene) ([notes](https://github.com/BioSchemas/specifications/tree/master/BioschemasRelease1_Notes/GeneCodingNotes.md)) deployment on [eDGAR](http://edgar.biocomp.unibo.it/cgi-bin/gene_disease_db/gene.py?gene=A2M) ([Google SDTT](https://search.google.com/structured-data/testing-tool?url=http://edgar.biocomp.unibo.it/cgi-bin/gene_disease_db/gene.py?gene=A2M))
    - [MolecularEntity](https://bioschemas.org/MolecularEntity) ([notes](https://github.com/BioSchemas/specifications/tree/master/BioschemasRelease1_Notes/MolecularEntityCodingNotes.md)) deployment on [ChEMBL](https://www.ebi.ac.uk/chembl/compound_report_card/CHEMBL59/) ([Google SDTT](https://search.google.com/structured-data/testing-tool#url=https%3A%2F%2Fwww.ebi.ac.uk%2Fchembl%2Fbeta%2Fcompound_report_card%2FCHEMBL59%2F))
    - [Protein](https://bioschemas.org/Protein) ([notes](https://github.com/BioSchemas/specifications/tree/master/BioschemasRelease1_Notes/ProteinCodingNotes.md)) deployment on [DisProt](https://www.disprot.org/DP00086) ([Google SDTT](https://search.google.com/structured-data/testing-tool?url=https://www.disprot.org/DP00086))
  - [Taxon](https://bioschemas.org/Taxon) ([notes](https://github.com/BioSchemas/specifications/tree/master/BioschemasRelease1_Notes/TaxonCodingNotes.md)) deployment at [Muséum National D’Histoire Naturelle](https://inpn.mnhn.fr/espece/cd_nom/60878/) ([Google SDTT](https://search.google.com/structured-data/testing-tool?url=https://inpn.mnhn.fr/espece/cd_nom/60878/))

## Domain Ontologies Considered

This is a non-exhaustive list of the domain specific ontologies that have been considered during the development of the Bioschemas types:

- Biodiversity Information Standards ([TDWGOntology](https://github.com/tdwg/ontology))
- Chemical Entities of Biological Interest ([ChEBI](https://www.ebi.ac.uk/chebi/))
- Chemical Information Ontology ([CHEMINF](http://semanticchemistry.github.io/semanticchemistry/))
- Feature Annotation Location Description Ontology ([FALDO](https://github.com/OBF/FALDO))
- Gene Ontology ([GO](http://geneontology.org/))
- NCBI [Taxonomy](https://www.ncbi.nlm.nih.gov/taxonomy)Protein Ontology ([PRO](https://proconsortium.org/))
- SemanticScience Integrated Ontology ([SIO](http://sio.semanticscience.org/))
- UniProt RDF Schema Ontology ([UniProt](https://www.uniprot.org/core/))
- Wikidata