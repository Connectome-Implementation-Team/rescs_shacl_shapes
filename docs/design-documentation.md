# Introduction

RESCS (**Res**earch **C**ommon**s**) is an adoption of [schema.org](http://schema.org) 
to represent metadata of research projects. [@wu_guidelines_2021, p. 14ff.] It also includes parts of [PROV-O](https://www.w3.org/TR/prov-o/) 
to represent provenance information of metadata records. 
The goal is to reuse classes and properties of existing ontologies in order to be compatible with existing standards ([FAIR principles](https://www.go-fair.org/fair-principles/)).

RESCS is part of the [Connectome project](https://www.switch.ch/connectome/).

# Formalisation

The formalisation consists of two parts:

1. Definition of [SHACL shapes](https://www.w3.org/TR/shacl/) to define constraints the data can be validated against.
   Validation will be integrated into the process of [resource creation](https://bluebrainnexus.io/docs/delta/api/schemas-api.html) in Nexus.

2. Besides the SHACL shapes, an ontology (RDF(S), OWL) will be provided.
   It expresses the semantics of RESCS, refining the rather generic definitions provided by schema.org and PROV-O.
   The ontology serves documentation purposes, e.g., when defining a mapping for RESCS.
   It is not machine-actionable in Nexus.

# Adopting schema.org

## General Approach

The vocabulary of schema.org is very generic and flexible so it can cover a wide range of very different use cases. 
However, for our use case we needed to make a *selection* of classes (called *types* on schema.org) 
and properties and further restrict the properties' ranges (their expected data or object types). [@simsek_domain-specific_2020, p. 588]
Since schema.org does not define properties as required, optional etc. 
the SHACL shapes define cardinalities for each class used in RESCS.

The RESCS selection of schema.org classes and properties should be as concise as possible,
i.e. the same information should always be expressed using the same properties and data types. [@simsek_domain-specific_2020, p. 585ff.]

## Conventions

In the formalisation process we followed Holger Knublauch's [SHACL version of schema.org](https://datashapes.org/schema) as a reference implementation
and made a selection of classes and properties as mentioned above.

To represent the (primitive) datatypes of schema.org, we use the following conventions:

| schema.org              | RESCS (SHACL PropertyShape)                                                                  |
|-------------------------|----------------------------------------------------------------------------------------------|
| schema:Text             | sh:datatype xsd:string                                                                       |
| schema:URL              | sh:nodeKind sh:IRI                                                                           |
| schema:Number           | sh:datatype xsd:integer / xsd:float (depending on precision needed)                          |
| schema:Date	            | sh:datatype xsd:date (ISO 8601)                                                              |
| schema:Boolean        	 | sh:datatype xsd:boolean                                                                      |
| schema:Language	        | sh:datatype xsd:string, sh:pattern `[a-z]{3}` (ISO 639-3, three char lang code, e.g., `eng`) |

The type `schema:PropertyValue` (property-value pair) is not used, instead properties are used directly.

## Exceptions

### General Approach

There are cases in which schema.org does not offer a class or property that is needed in RESCS 
or where schema.org properties are used on other classes than defined on schema.org.
This means that they would not pass [validation](https://validator.schema.org/).
Such cases will be kept to the minimum. 
Each case will be documented so that a schema.org aware client can adapt quickly. 
If generic enough, we will submit  [proposals](https://github.com/schemaorg/schemaorg#improving-schemas) 
to schema.org so that our case could be covered in the future by schema.org.

### Known Exceptions

Currently, we are using the following properties on classes where schema.org does not allow for their usage:

- `schema:startDate` on `schema:Project`, severity: Warning thrown by schema.org validator. Reason for breakage: Expressing this via `schema:MonetaryAmount`'s property `schema:validFrom` is not very intuitive.
- `schema:endDate` on `schema:Project`: severity: Warning thrown by schema.org validator. Reason for breakage: Expressing this via `schema:MonetaryAmount`'s property `schema:validThrough` is not very intuitive.

### Known Validation Issues

In general, the schema.org validator does not accept XSD datatypes in JSON-LD:

```json
  "value": {
    "@type": "xsd:float",
    "@value": 10000.5
  },
  "validFrom": {
    "@type": "xsd:date",
    "@value": "2021-10-01"
  },
  "validThrough": {
    "@type": "xsd:date",
    "@value": "2026-10-01"
  }
```

Although this is valid JSON-LD (RDF), the schema.org validator throws [errors](https://github.com/schemaorg/schemaorg/issues/3005)
since XSD datatypes are used instead of the schema.org datatypes, e.g., `xsd:float` instead of `schema:Float`. 

# PROV-O

# Prefixes

| Prefix  | URI |
|---------|-----|
| sh:     | http://www.w3.org/ns/shacl# |
| schema: | http://schema.org/ |
| xsd:    | http://www.w3.org/2001/XMLSchema# |


# References
