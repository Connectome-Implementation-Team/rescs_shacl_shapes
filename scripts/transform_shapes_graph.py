#!/usr/bin/env python3

from rdflib import Graph
from rdflib.query import Result
from pyld import jsonld
import os
import json

def absolute_from_rel_file_path(relative_path: str) -> str:
    """
    Given a path relative to this file,
    returns the absolute path.

    :param relative_path: the path relative to this file.
    :return: the absolute path.
    """
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, relative_path)

# load and parse the shapes graph
g: Graph = Graph()
g.parse(absolute_from_rel_file_path('../ontology/shapes_ontology_graph.json'))

# transform shapes graph so that it does not use sh:and but inheritance instead
query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sh: <http://www.w3.org/ns/shacl#>
PREFIX rescs: <http://rescs.org/>

CONSTRUCT {

    ?nodeShape a sh:NodeShape ;
        rdfs:comment ?nodeComment ;
        rdfs:label ?nodeLabel ;
        sh:property ?nodeProperty ;
        sh:targetClass ?targetClass .

    ?nodeProperty ?np ?no .

    ?no ?npp ?noo .

    ?noo ?nppp ?nooo .

    ?nooo ?npppp ?noooo .


} WHERE {

    #BIND(<http://rescs.org/dash/thing/ThingShape> AS ?nodeShape)  .

    ?nodeShape a sh:NodeShape ;
        rdfs:comment ?nodeComment ;
        rdfs:label ?nodeLabel ;
        sh:targetClass ?targetClass .

    {
        ?nodeShape sh:property ?nodeProperty .

        ?nodeProperty ?np ?no .

        OPTIONAL {
            ?no ?npp ?noo .

            OPTIONAL {
                ?noo ?nppp ?nooo .

                OPTIONAL {
                    ?nooo ?npppp ?noooo .
                }
            }
        }
    } UNION {
        ?nodeShape sh:and ?and .

        OPTIONAL {
            ?and rdf:rest ?listRest .

            ?listRest ?pp ?oo .

            ?oo ?ppp ?nodeProperty .

            ?nodeProperty ?np ?no .

            OPTIONAL {
                ?no ?npp ?noo .

                OPTIONAL {
                    ?noo ?nppp ?nooo .

                    OPTIONAL {
                        ?nooo ?npppp ?noooo .
                    }
                }
            }
        }
    }
}
"""

q_res: Result = g.query(query)

# write transformed graph
q_res.serialize(destination=absolute_from_rel_file_path('../ontology/shapes_graph_transformed.json'), format='json-ld')

# read the transformed graph
f = open(absolute_from_rel_file_path('../ontology/shapes_graph_transformed.json'), 'r')
data = json.load(f)
f.close()

# compact the transformed graph
compacted = jsonld.compact(data, {
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "prov": "http://www.w3.org/ns/prov#",
    "dcat": "http://www.w3.org/ns/dcat#",
    "sh": "http://www.w3.org/ns/shacl#",
    "shsh": "http://www.w3.org/ns/shacl-shacl#",
    "dcterms": "http://purl.org/dc/terms/",
    "schema": "http://schema.org/",
    "rescs": "http://rescs.org/"
})

# write the compacted transformed graph back
f = open(absolute_from_rel_file_path('../ontology/shapes_graph_transformed.json'), 'w')
f.write(json.dumps(compacted))
f.close()
