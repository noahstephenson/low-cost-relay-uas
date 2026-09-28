# Project report and manuscript files

The author-supplied relay_uas_aeroconf.pdf is the current 15-page project report, prepared as paper 2784 for IEEE Aerospace 2027. It supersedes the repository's earlier review PDF. The LaTeX file remains a working source for an earlier revision and does not reproduce this PDF.

## Files and diagrams

- relay_uas_aeroconf.tex: earlier working source; do not use it to overwrite the final PDF.
- relay_uas_aeroconf.pdf: current author-supplied paper.
- figs/architecture_assessment_workflow.mmd: editable draft of the study-specific workflow (Figure 3 in the final PDF).
- figs/four_flow_architecture.mmd: editable four-flow architecture draft.
- figs/diagram-brief.md: block, connector, and MagicDraw export instructions.
- render_workflow.py and render_architecture_word.py: render the workflow and the narrow Word variant of the existing architecture figure.

The workflow applies selected system definition and analysis practices from the cited NASA Systems Engineering Handbook. Its dashed final step marks physical verification and operational validation as outstanding.

## Earlier source build

For the earlier LaTeX revision, render its figures with a Python environment containing Matplotlib:

    python submission/render_workflow.py
    python submission/render_architecture_word.py

To build the earlier LaTeX revision, run two TeX passes from the submission directory using the supplied class:

    cd submission
    pdflatex relay_uas_aeroconf.tex
    pdflatex relay_uas_aeroconf.tex

Tectonic can also resolve the LaTeX dependencies. These commands do not recreate the author-supplied final PDF. build_word.py remains available for the earlier LaTeX source, but its generated DOCX is not a current paper edition.

## Evidence and review

Run the 35 unit tests, generated-baseline check, and independent 1,890-record checker described in the top-level README. The earlier claim ledger is in result-audit-r3.md; the offset and combined hover-stress arithmetic are in paper-2784-review-audit.md. These checks establish reproducibility of a conditional assessment; physical relay performance, full-mission energy, and packet delivery are unverified.

Before submission, the author should review the biography and the applicability of the retained U.S. Government copyright notice, complete any required institutional release, and confirm the conference portal requirements. No upload or approval is claimed.
