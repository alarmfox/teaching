# Teaching Repository

Welcome to the Teaching repository. This project provides a collection of teaching materials, practical labs, and security tools designed for educational purposes.

## Repository Structure

- `courses/`: Theoretical content and course curricula for Linux fundamentals, security, and more.
- `labs/`: Hands-on exercises and practical lab setups, including networking, exploit challenges, and virtualization.
- `tools/`: Scripts, helper tools, and example code to support learning and experimentation.

## Build System (Markdown to LaTeX/PDF)

The repository uses a centralized build system to convert Markdown source files into professional LaTeX documents and PDFs.

### Requirements
- **Pandoc**: Used for converting Markdown to LaTeX source.
- **TeX Live** (or equivalent LaTeX distribution): Includes `pdflatex` and `latexmk`.
- **latexmk**: Automates the LaTeX compilation process.

### Components
- `build.sh`: The main build script. It handles recursive conversion of `.md` to `.tex` and triggers the PDF compilation.
- `template.tex`: A global Pandoc LaTeX template that defines the visual style and structure of the generated documents.
- `.latexmkrc`: Global configuration for `latexmk`, ensuring all build artifacts are placed in a local `build/` directory.

### Usage
To build all materials in the repository:
```bash
./build.sh
```

To build a specific directory or file:
```bash
./build.sh courses/vapt/
./build.sh labs/arpspoof/README.md
```

All generated `.tex` files will be placed alongside their source `.md` files, and the final PDFs will be located in a `build/` subdirectory.

## Educational Purpose

The materials in this repository are intended for **educational and training purposes only**. Certain examples demonstrate security vulnerabilities or insecure practices (e.g., hardcoded passwords) to help students learn how to identify and remediate them. **Never use these examples in production environments.**

---

*For further information on specific topics, please refer to the README files within each directory.*
