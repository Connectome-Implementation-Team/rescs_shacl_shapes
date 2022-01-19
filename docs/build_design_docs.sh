#!/usr/bin/env bash

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
