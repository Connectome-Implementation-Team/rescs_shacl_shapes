#!/usr/bin/env python3

#
#      RESCS SHACL Shapes: Build Tools for the RESCS SHACL Shapes Library
#      Copyright (C) 2022 SWITCH
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU Affero General Public License as published
#      by the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU Affero General Public License for more details.
#
#      You should have received a copy of the GNU Affero General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

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



