# weird-science

Repository dedicated to organizing and versioning study topics in systems theory, formal ontologies, and related areas. These materials serve as stepping-stones for future paper development.

## 📚 Study Topics

### General Systems Theory

Collection of documents exploring systems theory, complexity, and emergent phenomena.

#### Document 1: Complex Systems as Unbounded Dynamical Holarchies
[![PDF](https://img.shields.io/badge/PDF-Download-blue?logo=adobe-acrobat-reader)](../../releases/latest/download/document-1.pdf)

A framework for understanding and simulating emergent phenomena in complex systems through the lens of unbounded dynamical holarchies.

[View Document →](./general-systems-theory/document-1/)

#### Document 2: Open-Ended Evolution in Multiagent Formal Systems
[![PDF](https://img.shields.io/badge/PDF-Download-blue?logo=adobe-acrobat-reader)](../../releases/latest/download/document-2.pdf)

Exploring curiosity, novelty, and the adjacent possible in multiagent formal systems.

[View Document →](./general-systems-theory/document-2/)

### Formal Ontologies

Collection of documents on formal ontologies and knowledge representation.

*Documents coming soon...*

## 📁 Repository Structure

```
weird-science/
├── general-systems-theory/
│   ├── document-1/
│   │   ├── README.md
│   │   ├── main.tex
│   │   ├── sections/
│   │   │   ├── introduction.tex
│   │   │   ├── framework.tex
│   │   │   ├── applications.tex
│   │   │   └── conclusion.tex
│   │   └── references/
│   └── document-2/
│       ├── README.md
│       ├── main.tex
│       ├── sections/
│       │   ├── introduction.tex
│       │   ├── methodology.tex
│       │   ├── results.tex
│       │   └── conclusion.tex
│       └── references/
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
