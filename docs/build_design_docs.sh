#!/usr/bin/env bash

#
#
#     RESCS SHACL Shapes: Build Tools for the RESCS SHACL Shapes Library
#     Copyright (C) 2022  Tobias Schweizer, Kurt Baumann, Laura Rettig
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as published
#     by the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

usage() { echo "Usage: $0 [-f <html|pdf>]" 1>&2; exit 1; }

while getopts ":f:" o; do
    case "${o}" in
        f)
            f=${OPTARG}
            if [[ $f != "html" ]] && [[ $f != "pdf" ]]
            then
              usage
            fi
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

# check for empty string
if [ -z "${f}" ]; then
    usage
fi

pandoc -s --bibliography bibliography.bib --citeproc --csl ieee.csl --from markdown design-documentation.md metadata.yaml -o design-documentation.${f}
