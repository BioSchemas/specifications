# Proposal of BioChemEntity Type

The [Bioschemas](https://bioschemas.org) community would like to propose a new top-level type from which the majority of life sciences focused types will extend.

## Background

The `BioChemEntity` type has been discussed in the Bioschemas community in:

- Issues
  - [BioChemEntity definition discussions](https://github.com/BioSchemas/specifications/issues/215)
  - [Relationship to schema.org/Intangible](https://github.com/BioSchemas/specifications/issues/226)
  - All issues labelled [BioChemEntity](https://github.com/BioSchemas/specifications/issues?utf8=✓&q=label:"type:+BioChemEntity")
- Bioschemas community mailing list thread
  - [Discussion](https://lists.w3.org/Archives/Public/public-bioschemas/2017Nov/0001.html) on different representation approaches for a Protein
  - All emails containing the term [BioChemEntity](https://www.w3.org/Search/Mail/Public/advanced_search?keywords=&hdr-1-name=subject&hdr-1-query=biochementity&hdr-2-name=from&hdr-2-query=&hdr-3-name=message-id&hdr-3-query=&period_month=&period_year=&index-grp=Public__FULL&index-type=t&type-index=public-bioschemas&resultsperpage=20&sortby=date-asc)

The Bioschemas community were originally looking for a minimal extension to Schema.org that could be specialised with properties from other life sciences ontologies. The original version of `BioChemEntity` was devised for this purpose with specialisms defined in usage profiles to enable the markup of pages about proteins, chemicals, etc. This proved to make the markup overly complicated both for publishers and consumers of the markup.

This revised version of `BioChemEntity` now serves the purpose of being a parent type for the various types required for the life sciences to support search use cases, and some data exchange. We have deliberately chosen to go for a shallow and wide subtree from `BioChemEntity` to avoid focusing on acurate biological modelling, instead focusing on the properties required for search.

The following ontologies were considered when developing this proposal:

- Chemical Entities of Biological Interest ([ChEBI](https://www.ebi.ac.uk/chebi/))
- Chemical Information Ontology ([CHEMINF](http://semanticchemistry.github.io/semanticchemistry/)) 
- Feature Annotation Location Description Ontology ([FALDO](https://github.com/OBF/FALDO))
- Gene Ontology ([GO](http://geneontology.org/))
- Protein Ontology ([PRO](https://proconsortium.org/))
- SemanticScience Integrated Ontology ([SIO](http://sio.semanticscience.org/))
- UniProt RDF Schema Ontology ([UniProt](https://www.uniprot.org/core/))

## Proposal

For convenience the `BioChemEntity` proposal is available from the Bioschemas website (https://bioschemas.org/types/BioChemEntity/).

We summarise here the design decisions taken to reach this proposal.

### Type Hierarchy

We are proposing to add the `BioChemEntity` type directly under `schema:Thing`. `BioChemEntity` is being proposed as an umbrella type that the various types coming from Bioschemas will be placed under. This is to prevent bloat at the top level of Schema.org. 

### Properties

- associatedDisease: *New property*
- bioChemInteraction: *New property*
- bioChemSimilarity: *New property*
- biologicalRole: *New property*
- hasBioChemEntityPart: *New property*
Enables the capture of sub-parts but keeping the property distinct from `hasPart` which is used for creative works.
- hasMolecularFunction: *New property*
- hasRepresentation: *New property*
- isEncodedByBioChemEntity: *New property*
Property is generic to not only be used for gene/protein encodings
- isInvolvedInBiologicalProcess: *New property*
- isLocatedInSubcellularLocation: *New property*
- isPartOfBioChemEntity: *New property*
Inverse of hasBioChemEntity part. Corresponds with `schema:isPartOf`
- taxonomicRange: *New property*

