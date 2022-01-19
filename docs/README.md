# Documentation

## Build SHACL Shapes HTML Documentation

An HTML documentation can be generated using [Ontospy](https://github.com/lambdamusic/Ontospy):
- Install `Ontospy` and its dependencies: `pip3 install ontospy django pygments`
- Run `scripts/generate_shapes.py` to generate a graph of all SHACL shapes and some extracted ontology information.
- Run `ontospy gendocs ontology/shapes_graph.json` and choose option 2 ("Html: multi page")

The script `scripts/generate_shapes.py` generates the property definitions from the SHACL shapes.
However, class definitions have to be added to `ontology/onytology.json` including their relations to other classes (`rdfs:subClassOf`).
In the SHACL shapes, we do not use inference but conjunctions (`sh:and`, see [docs](https://www.w3.org/TR/shacl/#AndConstraintComponent)).

For more details, see the [official docs](https://lambdamusic.github.io/Ontospy/).

Note that currently `Ontospy` does not fully support SHACL shapes yet and does not include cardinalities.
We have requested this [feature](https://github.com/lambdamusic/Ontospy/issues/104).

## Design Documentation

The [design documentation](design-documentation.md) explains the design principles of RESCS.
From the Markdown source, an HTML and a PDF version can be built.
- Install `pandoc` (<https://pandoc.org/>)
- Run `./build_design_docs.sh -f <pdf/html>` directly from withing the `docs` folder to generate either a PDF or an HTML version.
  Note that creating the PDF version requires LaTeX to be installed on your system, see `pandoc` [docs](https://pandoc.org/MANUAL.html#creating-a-pdf).

Note that we are using `pandoc`'s [YAML extension](https://pandoc.org/MANUAL.html#extension-yaml_metadata_block)
for the design document's metadata (title, authors etc.), see `docs/metadata.yaml`.

The design documentation may have references to publications defined in 
`docs/bibliography.bib`, e.g., `[@wu_guidelines_2021, p. 14ff.]`,
see `pandoc` [docs](https://pandoc.org/MANUAL.html#citations).

