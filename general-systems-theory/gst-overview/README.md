# Foundations of General Systems Theory: A Survey of Formal Definitions

A systematic compilation of foundational definitions of systems and major theoretical insights drawn from the mathematical literature on General Systems Theory.

## Overview

This document presents a comprehensive survey of the mathematical formalization of systems theory, tracing conceptual foundations through the seminal contributions of Mesarovic, Takahara, Yi Lin, and other key figures in the formalization of systems theory within set-theoretic and logical frameworks.

## Structure

- `main.tex` - Main LaTeX document
- `sections/` - Document sections:
  - `foundational-definitions.tex` - Foundational definitions of systems from seminal literature
  - `theoretical-insights.tex` - Major theoretical insights from GST
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

📄 [Download latest PDF](../../../releases/latest/download/gst-overview.pdf)

## Status

Document in development phase.

## Contributors

[To be filled in during paper development]

## License

[To be determined]