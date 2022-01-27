#!/usr/bin/env python3

from pyld import jsonld
import os
import json
from typing import List

def absolute_from_rel_file_path(relative_path: str) -> str:
    """
    Given a path relative to this file,
    returns the absolute path.

    :param relative_path: the path relative to this file.
    :return: the absolute path.
    """
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, relative_path)


def remove_and_conjunction_from_shapes(graph: List) -> List:
    """
    Removes sh:and conjunction from shapes.
    If present, transforms second element of sh:and to sh:property.


    :param graph: The graph containing the shapes.
    :return: The transformed graph.
    """

    # Attention: shallow copy
    copy = graph.copy()

    for node_shape in copy:

        if not node_shape['@type'] == 'http://www.w3.org/ns/shacl#NodeShape':
            continue

        target_class = node_shape['http://www.w3.org/ns/shacl#targetClass']['@id']

        if target_class != 'http://schema.org/Thing':
            # sh:and: take second element if present (local props), first element is the superclass's shape.
            and_conjunction = node_shape['http://www.w3.org/ns/shacl#and']['@list']
            if len(and_conjunction) > 1:
                props = and_conjunction[1]['http://www.w3.org/ns/shacl#property']
                node_shape['http://www.w3.org/ns/shacl#property'] = props

            # Remove the sh:and conjunction -> inference has to be used instead when validating
            #
            # not sure if this mutates the originally given graph since we are
            # operating on a shallow copy
            del node_shape['http://www.w3.org/ns/shacl#and']

    return copy

f = open(absolute_from_rel_file_path('../ontology/shapes_graph.json'), 'r')
graph = json.load(f)
compacted = jsonld.compact(graph, {})
f.close()

transformed_graph = remove_and_conjunction_from_shapes(compacted['@graph'])

# compact the transformed graph
transformed = jsonld.compact(transformed_graph, {
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
f.write(json.dumps(transformed))
f.close()
