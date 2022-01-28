#!/usr/bin/env python3

from rdflib import Graph
from rdflib.query import Result
import sys
import os

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
g.parse(absolute_from_rel_file_path('../ontology/shapes_graph.json'))

# look for sh:node references that cannot be resolved
query = """
PREFIX sh: <http://www.w3.org/ns/shacl#> 

SELECT ?nodeShape
WHERE {
        
    ?propShape sh:node ?nodeShape .
    
    # find all node shapes lacking a definition 
    # (their IRI only occurs as an object, not as a subject)
    FILTER NOT EXISTS {
        ?nodeShape a sh:NodeShape .
    }
}
"""

q_res: Result = g.query(query)

if (len(q_res)) > 0:
    print('Broken sh:node reference(s) detected:', file=sys.stderr)
    for row in q_res:
        print(row.get('nodeShape'), file=sys.stderr)
    exit(1)



