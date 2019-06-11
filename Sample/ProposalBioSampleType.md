# Proposal of BioSample Type

The [Bioschemas](https://bioschemas.org) community would like to propose a new type for marking up details of biological samples such as those found in bio banks, museums, and herbaria.

## Background

The BioSample type has been discussed in the Bioschemas community in:

- [Issue 306](https://github.com/BioSchemas/specifications/issues/306)
- Bioschemas community mailing list thread
  - [BioSamples type for review](https://lists.w3.org/Archives/Public/public-bioschemas/2019May/0007.html)

The proposal is an evolution of an earlier prototype of a Sample type developed for exchanging data about samples and deployed on the [EBI BioSamples archive](https://www.ebi.ac.uk/biosamples/).

## Proposal

The proposed type is available at

We summarise here the design decisions taken to reach this proposal.

### Type Hierarchy

We are proposing to add the BioSample type under a BioChemEntity type which inherits from Thing. BioChemEntity is being proposed as an umbrella type that the various types coming from Bioschemas will be placed under to prevent bloat at the top level of schema.org. BioSample will reuse some of the properties from BioChemEntity, e.g. `associatedDisease` and `taxonomicRange`.

An alternative would be for there to be a more generic Sample type in schema.org with BioSample being a child. You could imagine there being a need to markup a sample of a product for sale which would have a different emphasis from a BioSample, similarly there have been discussions about have a GeoSample that would include spatial properties, or StatisticalSample. If this approach is favoured, then the `associatedDisease` and `taxonomicRange` properties would need their definitions extended, unless a multi-inheritance of `Sample` and `BioChemEntity` is used.

### Properties

#### additionalProperty

Range extended to include BioSample.

#### collector

New property

Considered [`creditedTo`](https://schema.org/creditedTo) but felt that the two were distinct from each other in their intended use. 

There are also distinct uses of these terms to refer to different entities, i.e. who collected the sample versus who it is credited to.

#### custodian

New property

Considered `accountablePerson` but range only permitted `Person` and the custodian of a sample is often an `Organization`.

#### dateCreated

Range extended to include BioSample.

Potential issue is that the description of `dateCreated` mentions `CreativeWork` which `BioSample` does not inherit from.

#### gender

Range extended to include BioSample.

#### isControl

New property

#### itemLocation

Range extended to include BioSample.

#### locationCreated

Range extended to include BioSample.

Potential issue is that the description of `locationCreated` mentions `CreativeWork` which `BioSample` does not inherit from.

#### samplingAge

New property 

Considered `age` but felt that was too generic, particularly with the proposed description of the property.

#### 



