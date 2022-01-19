# SHACL Shapes

This repo contains the SHACL shapes for RESCS (**Res**earch **C**ommon**s**).

## SHACL Shapes Library Source Files

The JSON-LD files contained in the `shapes` directory are the SHACL shape source files.
They are optimised for use with [Nexus Forge](https://github.com/BlueBrain/nexus-forge/).

For instructions on how to build the documentation, see [README](docs/README.md) in the `docs` directory.

## Configuration For Use With Nexus Forge

For a complete overview of Forge configuration options, see the official Forge [docs](https://nexus-forge.readthedocs.io/en/latest/configuration.html) 
and a [sample configuration](https://github.com/BlueBrain/nexus-forge/blob/master/examples/notebooks/getting-started/00%20-%20Initialization.ipynb).

### Authentication

For authentication a token has to be obtained from <https://nexus.switch.ch/>.
The token and other configuration options have to be set in a file called `.env` in the project root:

```bash
TOKEN="mytoken"
ORG="SW"
PROJECT="my_test"
NEXUS="https://nexus.switch.ch/v1"
```
`ORG` defines the organisation setting for Nexus.
`PORJECT` sets the project.
`NEXUS` defines the server address (API).

### Using SHACL Shapes From Local File System

To use these shapes with Nexus Forge,
set up a YAML configuration file:

```yaml
Model:
  name: RdfModel
  origin: directory
  source: "shapes" # --> path to the shapes directory (paths are relative to execution context of config file)
  context:
    iri: "ontology/jsonld-context.json" # --> path to the JSON-LD context object (paths are relative to execution context of config file)

Store:
  name: BlueBrainNexus
  searchendpoints:
    sparql:
      endpoint: "https://bluebrain.github.io/nexus/vocabulary/defaultSparqlIndex"
  versioned_id_template: "{x.id}?rev={x._store_metadata._rev}"
  file_resource_mapping: ./configurations/nexus-store/file-to-resource-mapping.hjson

Formatters:
  identifier: https://kg.example.ch/{}/{}
```

Alternatively use `configuration.yml` in your setup.

### Using Shapes Registered in Nexus

Once the SHACL shapes are registered in Nexus, 
you can use them for validation instead of using those from your local files system.

```yaml
Model:
  name: RdfModel
  origin: store # --> change this from "directory" to "store".
  source: BlueBrainNexus # --> change this from the directory on your local file system, e.g. "store" to "BlueBrainNexus".
  context:
    iri: "./jsonld-context.json" # --> Note that the JSON-LD context object is stilled required on your local file system.
```

### Registering SHACL Shapes in Nexus

To register the SHACL shapes located on your local file system in Nexus, run `scripts/register_schemas.py`.
The script will create the SHACL shapes in Nexus in a **predefined** order. 
If you add new shapes, note that you have to add them here:

```python
# order in which schemas are created (dependency)
order: List[str] = ['thing', 'person', 'organization', 'place', 'creativework', 'intangible', 'structuredvalue', 'contactpoint',
         'monetaryamount', 'article', 'dataset', 'mediaobject', 'scholarlyarticle', 'datadownload', 'grant',
         'monetarygrant', 'project', 'researchproject']
```

Note that the schemas that are referred to from other schemas have to be created first.

If you attempt to register a schema with an existing name, it will be rejected.

## Demo

### Requirements

It is recommended to set up a [virtual environment](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) 
in the project root (by convention, the virtual environment directory `env` is contained in `.gitignore` and is not tracked).
Install the dependencies listed in `requirements.txt`: `pip3 install -r requirements.txt`.

**Please note that you have to install nexus-forge from [master](https://github.com/BlueBrain/nexus-forge/issues/194#issuecomment-963381914): `pip3 install git+https://github.com/BlueBrain/nexus-forge`.**
A new release (> 0.6.3) should make this unnecessary.

### Run Demo

For a demonstration of the SHACL shapes, you can use `test.py`.
Make sure to create a file `.env` first containing configuration settings (see [above](#authentication)).

### Use with Standard Tools

Run `scripts/generate_shapes.py` to build a graph of **all** SHACL shapes contained in the library.
The generated file is called `ontology/shapes_graph.json`.
The resulting collection contains all shapes in **one** JSON-LD graph
and only contains standard SHACL statements (no Nexus Forge specifics).

Then use it for validation, e.g., `pyshacl -sf json-ld -s ontology/shapes_graph.json -df json-ld test/thing/thing.json`
(use the debug mode `-d` for more detailed error messages).

## Tests

Run `scripts/test_all.sh` directly from within the directory `scripts`
to check if the test data files contained in the directory `test` conform to the shapes.

**Note that relative paths won't work when you do not run this script directly from within `scripts`.**

## Architecture

### Source Files

The JSON-LD files contained in the `shapes` directory are the **source files** of the SHACL shapes library.
Running `scripts/generate_shapes.py` will generate a file called `ontology/shapes_graph.json` containing all SHACL shapes.

**Please note that you have to run `generate_shapes.py` each time you changed something in the JSON-LD shape files.** 

#### Structure of a SHACL Shape File

By convention, each source file goes in a separate folder in the `shapes` directory and has the name `schema.json`, 
e.g., `shapes/monetarygrant/schema.json`, `shapes/monetaryamount/schema.json`.  
A SHACL source file is a JSON-LD document with the following structure:

```json
{
  "@context": [
    "https://incf.github.io/neuroshapes/contexts/schema.json", --> reference to an external context object simplifying properties such as targetClass etc.
    {
      "this": "http://rescs.org/dash/monetarygrant/" --> base reference path for each shape defined in this schema file
    }
  ],
  "@type": "nxv:Schema", --> Nexus vocabulary schema type (<https://bluebrain.github.io/nexus/vocabulary/>)
  "@id": "http://rescs.org/dash/monetarygrant", --> id of this schema file (used in import paths of other schema files)
  "imports": [
     "http://rescs.org/dash/grant",
     "http://rescs.org/dash/monetaryamount" --> import of other schema files by their id
  ],
  "shapes": [
    ... --> SHACL shape definitions (one or more shapes can be defined in one schema file)
  ]
}
```

Each file contains one node shape. Each node shape is identified by its unique id.
A shape definition looks like this:

```json
{
    ... --> main file structure, see above
    "shapes": [
    {
      "@id": "this:MonetaryGrantShape", --> unique name of this shape
      "@type": "sh:NodeShape", --> SHACL node shape
      "label": "A monetary grant",
      "targetClass":"schema:MonetaryGrant", --> the shape targets schema:MonetaryGrant
      "and": [
          {
          "node": "http://rescs.org/dash/grant/GrantShape" --> "inherits" from schema:Grant
        },
        {
          "property": [
            {
              "path": "schema:amount",
              "name": "amount",
              "description": "The amount of money.",
              "nodeKind": "sh:BlankNode",
              "class": "schema:MonetaryAmount",
              "node": "http://rescs.org/dash/monetaryamount/MonetaryAmountShape", --> reference to another shape (has to be imported)
              "minCount": 1,
              "maxCount": 1
            },
            {
              "path": "schema:funder",
              "name": "funder",
              "description": "A person or organization that supports a thing through a pledge, promise, or financial contribution. e.g. a sponsor of a Medical Study or a corporate sponsor of an event.",
              "or": [
                {
                  "class": "schema:Person",
                  "nodeKind": "sh:IRI"
                },
                {
                  "class": "schema:Organization",
                  "nodeKind": "sh:IRI"
                }
              ],
              "minCount": 1
            }
          ]
        }
      ]
    }
  ]
}
```

For more details about SHACL shape definitions, see the [official docs](https://www.w3.org/TR/shacl/#shacl-example).

#### JSON-LD Context Object

The JSON-LD context object located in `ontology/jsonld-context.json` serves as a kind of registry file for Forge,
translating shorthands like `MonetaryGrant` to a full IRI.
Each class and property for which shapes and constraints are defined has to be listed here.

Example:

```json
  { 
    ...
    "MonetaryGrant": {
      "@id": "http://schema.org/MonetaryGrant"
    },
    "name": {
      "@id": "http://schema.org/name"
    },
    "amount": {
      "@id": "http://schema.org/amount"
    }
  ...
```

`forge.types()` and `forge.template()` will only list classes defined in the JSON-LD context object.

#### Adding a New Schema File

1. Add a new directory to the `shapes` directory, e.g., `person`.
2. Within the new subdirectory, add a file `schema.json`.
3. Add the schema file structure as described [above](#structure-of-a-shacl-shape-file),
4. Make sure to use unique ids. 
   (Re-use the subfolder's name as the last part of the id, e.g., <http://rescs.org/dash/person> and adapt `this` in the context object accordingly.)
5. Add `NodeShape`s with property constraints as described [above](#structure-of-a-shacl-shape-file).
6. Add class and property names (`sh:targetClass`, `sh:name`) to the JSON-LD context object, e.g., `Person`, `givenName` etc., see [above](#json-ld-context-object). 
7. Add the new to shape in `scripts/register_schemas.py`, see [above](#registering-shacl-shapes-in-nexus).
8. Add the class and its properties to `ontology/ontology.json` (needed to generate the HTML docs).
