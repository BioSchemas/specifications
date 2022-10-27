# Proposal of MolecularEntity Type

The [Bioschemas](https://bioschemas.org) community would like to propose a new type for marking up details of a molecular entity. 

## Background

The `MolecularEntity` type has been discussed in the Bioschemas community in:

- Issues
  - [Clarifying ChemicalSubstance vs MolecularEntity](https://github.com/BioSchemas/specifications/issues/327)
  - All issues labelled [MolecularEntity](https://github.com/BioSchemas/specifications/issues?utf8=✓&q=label:"type:+MolecularEntity")
- Bioschemas community mailing list thread
  - [Difference between ChemicalSubstance and MolecularEntity](https://lists.w3.org/Archives/Public/public-bioschemas/2019Jun/0008.html)
  - All emails containing the term [MolecularEntity](https://www.w3.org/Search/Mail/Public/advanced_search?keywords=&hdr-1-name=subject&hdr-1-query=MolecularEntity&hdr-2-name=from&hdr-2-query=&hdr-3-name=message-id&hdr-3-query=&period_month=&period_year=&index-grp=Public__FULL&index-type=t&type-index=public-bioschemas&resultsperpage=20&sortby=date-asc)

The proposal is based on the [ChEBI ontology](https://www.ebi.ac.uk/chebi/) and its definition of a molecular entity ([CHEBI:23367](https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI%3A23367)).

The following ontologies were also considered when developing this proposal:

- Chemical Entities of Biological Interest ([ChEBI](https://www.ebi.ac.uk/chebi/))
- Chemical Information Ontology ([CHEMINF](http://semanticchemistry.github.io/semanticchemistry/)) 
- SemanticScience Integrated Ontology ([SIO](http://sio.semanticscience.org/))

## Proposal

For convenience the `MolecularEntity` proposal is available from the Bioschemas website (https://bioschemas.org/types/MolecularEntity/)).

Schema.org already includes a [`schema:Substance`](https://schema.org/Substance) type which is defined as a subclass of [`schema:MedicalEntity`](https://schema.org/MedicalEntity). A `ChemicalSubstance` and `MolecularEntity` in general are not medical tools and many properties of `MedicalEntity` simply do not apply to the two newly proposed concepts.

We summarise here the design decisions taken to reach this proposal.

### Type Hierarchy

We are proposing to add the `MolecularEntity` type under a `BioChemEntity` type which inherits from `schema:Thing`. `BioChemEntity` is being proposed as an umbrella type that the various types coming from Bioschemas will be placed under. This is to prevent bloat at the top level of Schema.org.

### Properties

- chemicalRole: *New property*
- inChI: *New property*
- inChIKey: *New property*
- iupacName: *New property*
- molecularFormula: *New property*
- molecularWeight: *New property*
- monoisotopicMolecularWeight: *New property*
- potentialUse: *New property*
- smiles: *New property*
