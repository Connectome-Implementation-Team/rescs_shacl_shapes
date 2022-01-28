#!/usr/bin/env bash

# Validates the given test data against the shapes graph.
# Expects validation to succeed.
# arg1: folder (in directory "test")
# arg2: name of JSON-LD test data file in test/arg1
function validate () {
  echo "validating: test/$1/$2.json"
  pyshacl -o /dev/null -sf json-ld -s ../ontology/shapes_graph.json -df json-ld ../test/$1/$2.json
  status=$?
  if (($status != 0)); then
    printf "%s\n" "Test case test/$1/$2.json failed, running in single mode for details:" >&2  # write error message to stderr
    pyshacl -sf json-ld -s ../ontology/shapes_graph_transformed.json -ef json-ld -e ../ontology/ontology.json -df json-ld ../test/$1/$2.json
    exit 1
  fi
}

# Attempts to validate the given test data against the shapes graph.
# Expects validation to fail.
# arg1: folder (in directory "test")
# arg2: name of JSON-LD test data file in test/arg1
function attempt () {
  echo "attempting: test/$1/$2.json"
  pyshacl -o /dev/null -sf json-ld -s ../ontology/shapes_graph.json -df json-ld ../test/$1/$2.json
  status=$?
  # status is expected to be 1 (validation failed, see https://github.com/RDFLib/pySHACL#command-line-use)
  if (($status != 1)); then
    printf "%s\n" "Test case test/$1/$2.json should have failed with exit code 1." >&2  # write error message to stderr
    exit 1
  fi
}

./generate_shapes_graph.py
status=$?
if (($status != 0)); then
  printf "%s\n" "Could not properly generate SHACL shapes graph" >&2  # write error message to stderr
  exit 1
fi

./check_shapes_consistency.py
status=$?
if (($status != 0)); then
  printf "%s\n" "Detected inconsistencies in SHACL shapes graph" >&2  # write error message to stderr
  exit 1
fi

pyshacl -o /dev/null -sf turtle -s ../shacl-shacl/shacl-shacl.ttl -df json-ld ../ontology/shapes_graph.json
status=$?
if (($status != 0)); then
  printf "%s\n" "SHACL Ssapes graph did not pass shacl-shacl validation" >&2  # write error message to stderr
  exit 1
fi

./transform_shapes_graph.py
status=$?
if (($status != 0)); then
  printf "%s\n" "Could not properly transform SHACL shapes graph" >&2  # write error message to stderr
  exit 1
fi

validate "thing" "thing"
validate "creativework" "creativework"
validate "article" "article"
validate "scholarlyarticle" "scholarlyarticle"
validate "datadownload" "datadownload"
validate "dataset" "dataset"
validate "mediaobject" "mediaobject"
validate "organization" "organization"
validate "project" "project"
validate "researchproject" "researchproject"
validate "person" "person"
validate "intangible" "intangible"
validate "structuredvalue" "structuredvalue"
validate "contactpoint" "contactpoint"
validate "monetaryamount" "monetaryamount"
validate "grant" "grant"
validate "monetarygrant" "monetarygrant"
validate "place" "place"

attempt "thing" "bad_thing"
attempt "person" "bad_person"


