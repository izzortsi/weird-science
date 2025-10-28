# Non-well-founded Hierarchies of Nested Systems

[![PDF](https://img.shields.io/badge/PDF-Download-blue?logo=adobe-acrobat-reader)](https://github.com/izzortsi/weird-science/releases/download/latest/nested-systems.pdf)

## Overview

A systematic investigation of the definitional foundations of complex systems, proceeding from first principles to articulate a formalism grounded in the recursive nesting of subsystems. The theoretical apparatus permits a rigorous examination of emergence as a structural phenomenon arising from inter-level functional dependencies within hierarchical architectures. This framework synthesizes set-theoretic precision with mereological intuitions, characterizing systems by their stratified organization across potentially infinite scales of description.

## Structure

- `main.tex` - Main LaTeX document
- `sections/` - Document sections:
  - `introduction.tex` - Introduction to complex systems and computational simulations
  - `preliminaries.tex` - Notational conventions and foundational definitions from model theory
  - `systems.tex` - Fundamental definitions and valued relations
  - `subsystems.tex` - Subsystems, supersystems, and nested structures
  - `hierarchies.tex` - Hierarchical organization and operations
- `references/` - Bibliography files:
  - `bibliography.bib` - Reference database

## Building

To build this document locally, run:
```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Or use the automated GitHub Actions workflow which builds PDFs on every push.

## Download

📄 [Download latest PDF](https://github.com/izzortsi/weird-science/releases/download/latest/nested-systems.pdf)

## Status

Document in development phase.

## Contributors

[To be filled in during paper development]

## License

[To be determined]