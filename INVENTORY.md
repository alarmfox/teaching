# Repository Audit: DTLab

## 1. Courses & Labs Mapping
*   **its-intro-to-linux**: Extensive collection of ODT/PDF course material.
*   **its-vapt**: DOCX/PDF course material.
*   **arpspoof-lab**: PDF/ODT lab material.
*   **firewall-lab**: DOCX lab material.
*   **hashcat-lab**: DOCX lab material.
*   **rec-metasploit-lab**: DOCX lab material.
*   **virtual-machine**: DOCX/MD material.
*   **dtlab-api-solution**: API project (Python, Docker).
*   **software-security**: Source code, binaries.
*   **hacking-tools**: Source code (Python, C).
*   **devnet-workshop**: Workshop material.
*   **learn-shell**: Go project.
*   **simple-http-server**: Go project.

## 2. Redundancy & Cleanup Plan
*   **Duplicate Detection**: Multiple formats (.pdf, .docx, .odt) of the same content in `its-intro-to-linux` and `its-vapt`.
*   **Build Artifacts**: Compiled binaries (a.out, bof, etc.), temporary files, and cache folders (e.g., `__pycache__`) to be gitignored or removed.
*   **Markdown Migration**: All .docx, .odt, .pptx files need conversion to .md using Pandoc.

## 3. Action Items
1.  [ ] Define target directory structure (courses/, labs/, tools/).
2.  [ ] Script mass-conversion of docs to Markdown.
3.  [ ] Remove redundant artifacts.
4.  [ ] Create consistent READMEs for each module.
