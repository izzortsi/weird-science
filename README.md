# weird-science

Repository dedicated to organizing and versioning study topics in systems theory, formal ontologies, and related areas. These materials serve as stepping-stones for future paper development.

## 📚 Study Topics

### General Systems Theory

Collection of documents exploring systems theory, complexity, and emergent phenomena.

#### Foundations of General Systems Theory: A Survey of Formal Definitions
[![PDF](https://img.shields.io/badge/PDF-Download-blue?logo=adobe-acrobat-reader)](../../releases/latest/download/gst-overview.pdf)

A systematic compilation of foundational definitions of systems and major theoretical insights drawn from the mathematical literature on General Systems Theory.

[View Document →](./general-systems-theory/gst-overview/)

### Formal Ontologies

Collection of documents on formal ontologies and knowledge representation.

*Documents coming soon...*

## 📁 Repository Structure

```
weird-science/
├── general-systems-theory/
│   └── gst-overview/
│       ├── README.md
│       ├── main.tex
│       ├── sections/
│       │   └── gst-overview.tex
│       └── references/
│           └── bibliography.bib
└── formal-ontologies/
    └── (future documents)
```

Each document folder contains:
- `main.tex` - Main LaTeX document
- `sections/` - LaTeX source files organized by section
- `references/` - Bibliography files and reference materials
- `README.md` - Document-specific information

## 🔨 Building PDFs

PDFs are automatically built via GitHub Actions on every push to `main` and for pull requests. You can:

- **Download the latest PDFs** from the [Releases](../../releases/latest) page
- **Build locally** by running `pdflatex` in each document directory
- **View PR-specific builds** as artifacts on pull request pages

## 🤝 Contributing

This repository uses comprehensive LaTeX .gitignore rules to keep auxiliary files out of version control while preserving source files and important assets.
