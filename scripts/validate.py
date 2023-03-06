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

from typing import List
import getopt
import sys
from pathlib import Path
from pyshacl import validate
from multiprocessing import Pool, cpu_count
import time

data_dir = ''

shapes_graph = ''

ontology_file = ''

move_dir = ''


def validate_file(file: Path):

    r = validate(
        str(file),
        shacl_graph=shapes_graph,
        ont_graph=ontology_file,
        inference='rdfs'
    )

    conforms, results_graph, results_text = r

    if conforms:
       print(f'{str(file)} is valid')
    else:
        print(f'{str(file)} is invalid, {str(results_text)}', file=sys.stderr)

def usage() -> None:
    print('Usage: ' + sys.argv[0] + ' -d <data dir> -s <shapes_graph.jsonld> -o <ontology.jsonld> -m <move dir>')
    print('Validates a data graph against the given shapes graph and moves invalid files.')
    exit(1)


argv = sys.argv[1:]

try:
    opts, args = getopt.getopt(argv, "d:s:o:m:")
except getopt.GetoptError as err:
    print(err)
    usage()

for opt, arg in opts:
    if opt in ['-d']:
        data_dir = arg
    elif opt in ['-s']:
        shapes_graph = arg
    elif opt in ['-o']:
        ontology_file = arg
    elif opt in ['-m']:
        move_dir = arg

# check for empty values (still initialised to empty strings)
if not data_dir or not shapes_graph or not ontology_file or not move_dir:
    usage()

if __name__ == '__main__':

    files: List[Path] = list(Path(data_dir).rglob("*.ttl"))
    sorted_files: List[Path] = sorted(files)

    print(len(sorted_files))

    start = time.time()
    # TODO: if errors are written to stdout from different processes at the same time, they could get intermingled. Solve this by using a lock.
    with Pool(processes=cpu_count()) as p:
        p.map(validate_file, sorted_files)
    elapsed = (time.time() - start)
    print("\n", "time elapsed is :", elapsed)