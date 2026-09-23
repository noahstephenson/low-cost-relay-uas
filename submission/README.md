# IEEE Aerospace 2027 manuscript package

Paper 2784 uses the approved IEEE Aerospace class. The PDF is the submission copy; the DOCX is an editable conference-style copy built from the same LaTeX manuscript.

## Files and diagrams

- relay_uas_aeroconf.tex: manuscript source.
- relay_uas_aeroconf.pdf and relay_uas_aeroconf.docx: current editions.
- figs/architecture_assessment_workflow.mmd: editable workflow content used in Figure 2.
- figs/four_flow_architecture.mmd: editable four-flow architecture draft.
- figs/diagram-brief.md: block, connector, and MagicDraw export instructions.
- render_workflow.py and render_architecture_word.py: render the workflow and the narrow Word variant of the existing architecture figure.

The workflow applies selected system definition and analysis practices from the cited NASA Systems Engineering Handbook. Its dashed final step marks physical verification and operational validation as outstanding.

## Build

From the repository root, render the two new figures with a Python environment containing Matplotlib:

    python submission/render_workflow.py
    python submission/render_architecture_word.py

Build the PDF from the submission directory with two TeX passes using the supplied class:

    cd submission
    pdflatex relay_uas_aeroconf.tex
    pdflatex relay_uas_aeroconf.tex

Tectonic can also resolve the LaTeX dependencies and run the passes. Build the DOCX from the repository root with Python, python-docx, and Pandoc 3.x:

    python submission/build_word.py

Pass --pandoc PATH_TO_PANDOC when Pandoc is not on PATH. The builder uses a system temporary directory and has no dependency on tmp/paper-review. In Microsoft Word, update the document's table of contents before final export. The submission PDF remains the conference file.

## Evidence and review

Run the 35 unit tests, generated-baseline check, and independent 1,890-record checker described in the top-level README. The paper's numerical and source-claim review is recorded in result-audit-r3.md. These checks establish reproducibility of a conditional assessment; physical relay performance, full-mission energy, and packet delivery are unverified.

Before submission, the author should review the biography and the applicability of the retained U.S. Government copyright notice, complete any required institutional release, and confirm the conference portal requirements. No upload or approval is claimed.
