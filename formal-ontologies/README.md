# Definitional Architectures: From Conceptualization to Ontology

[![PDF](https://img.shields.io/badge/PDF-Download-blue?logo=adobe-acrobat-reader)](https://github.com/izzortsi/weird-science/releases/download/latest/formal-ontologies.pdf)

## Overview

A philosophical excavation of formal system concepts, tracing the conceptual trajectory from extensional mathematical structures through intensional conceptualizations to formal ontologies. This document follows the architectonic framework established by Guarino, Oberle, and Staab, excavating the epistemological substrata underlying computational ontology and situating these definitions within the broader discourse of General Systems Theory.

## Structure

- `main.tex` - Main LaTeX document
- `sections/` - Document sections:
  - `introduction.tex` - The Phenomenology of Formal Representation
  - `extensional-foundations.tex` - Extensional Foundations
  - `intensional-turn.tex` - The Intensional Turn
  - `ontological-commitment.tex` - Ontological Commitment
  - `intended-models.tex` - Intended Models
  - `ontology-specification.tex` - Ontology Specification
  - `conclusion.tex` - Conclusion
- `references/` - Bibliography files:
  - `bibliography.bib` - Reference database with foundational texts on systems theory and ontology

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

📄 [Download latest PDF](https://github.com/izzortsi/weird-science/releases/download/latest/formal-ontologies.pdf)

## Status

Document in development phase.

## Contributors

[To be filled in during paper development]

## License

[To be determined]
