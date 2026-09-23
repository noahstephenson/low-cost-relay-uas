# IEEE Aerospace manuscript package

Prepared for the 2027 IEEE Aerospace Conference on 2026-09-12.

## Files

- `relay_uas_aeroconf.pdf`: compiled conference manuscript; preferred review copy.
- `relay_uas_aeroconf.docx`: editable Word version with native equations and an updated contents list. **Stale against the current `.tex`** (predates the abstract trim, the table-of-contents restoration, and the 28.4 km correction). The conference accepts PDF only for this submission, so the Word path is not required. To regenerate: `python build_word.py`, which needs pandoc 3.x (pandoc 2.x fails on the `CONTENTS_FIELD` marker; the bundled binary in `tmp/` is Windows-only).
- `relay_uas_aeroconf.tex`, `IEEEAerospaceCLS.cls`, and `figs/`: LaTeX source and publication figures.
- `relay_uas_aeroconf_latex.zip`: self-contained LaTeX package.

The Word and LaTeX versions have the same substantive text, tables, and equations. Their pagination differs. The original files in `Claude outputs/` are preserved.

## Before submitting

1. Add the author's headshot. The conference instructions request a 1.25 by 1.5 inch image at 300 dpi. No portrait was supplied or invented.
2. Confirm the biography and the applicability of the retained U.S. Government copyright notice. The supplied name, affiliation, and email have been incorporated. A statement that there is no copyright concern does not establish the applicable conference notice.
3. Complete the author's scientific review, any required institutional release, abstract acceptance, and submission-portal requirements. No paper has been uploaded or approval claimed.

The manuscript is a bounded architecture case study. Publication readiness does not guarantee peer-review acceptance, and the analysis does not validate a physical relay aircraft.

## Revision of 2026-09-16 (adversarial review response)

Text-only revision; no solver input or production code changed. Added numbers were recomputed with the repository solver at the same baseline.

- States that the fitted FM absorbs k_env, so the reference case carries no operating-condition margin; reports that a separate 15% margin gives 35.7 / 44.5 min.
- Reports the least-squares weight concentration (DAx8 79%), the single-point refit band (33.0-49.2 / 41.2-61.3 min), the alternative-estimator range (41.4-44.6 / 51.5-55.6 min), and the unconfirmed DAx8 rotor arrangement (coaxial refit 58.8 / 73.5 min).
- Notes the in-tunnel hover tests of the DAx8 and Endurance (new reference: Russell et al., AHS Forum 2016).
- Describes the structural anchor as a sized design value, not a weighed vehicle.
- Adds the auxiliary-power sensitivity (0/10/40 W) of the held-out comparison.
- States the direction of the link-model simplifications (opaque screen; midpoint placement, 28.3 km at 0.44 of span).
- Word copy regenerated with build_word.py; update fields (or run render_word.ps1) before exporting. relay_uas_aeroconf_word.pdf predates this revision.
- Second-review pass (same day): removed the AI-tool acknowledgment (to be re-added by the author); restored the branch name in Data Availability; added the 25 W condition to the abstract; stated why the coaxial DAx8 case is implausible; added the Matrice 4 pack value (248 Wh/kg, boundaries 54.4 / 67.7 min); added the Fresnel-clearance caveat (threshold about 108 m in the 10 km case); placed the Matrice 30 / Matrice 4 hover times (about 22 min each) beside Table 4.
- feasibility-inputs.yaml: the 0.83 drive efficiency is now marked declared rather than sourced to ANL-SRC-001, which used 0.75. All 25 tests and the generated-artifact, calibration, and boundary checks still pass.

## Scientific and editorial verification

Computational baseline: `4f9e2cde8c429e6b241d4a09dc5f8e7dbb877069`.

- All 25 repository tests passed.
- Generated artifact verification passed.
- The independent manuscript checker reconstructed all 1,890 case records.
- The current calibrated baseline supersedes the older manuscript outline and evidence audit's numerical examples.
- No scientific input or production solver was changed for this revision.
- Corrected the structural anchor description, aggregate hover-coefficient interpretation, scope of commercial hover comparisons, adverse-case interpretation, and unsupported performance language.
- Added the complete component mass balance and branch-consistency conditions.
- Rebuilt five figures from the saved results and stated equations. The continuous mass curve is a visualization of the existing model, not a new experiment.
- Replaced manual citation numbers with LaTeX citation keys.
- Expanded the abstract to the conference's 250--500 word requirement and used the official 2027 class unchanged. The manuscript preamble uses the written 0.75-inch margin specification.

## Build

From this directory, run `latexmk -pdf relay_uas_aeroconf.tex`, or run `pdflatex relay_uas_aeroconf.tex` twice. This task used Tectonic. The computational revision and full inputs remain in the repository.

For Word regeneration, `build_word.py` converts the LaTeX content through Pandoc, then applies conference layout with python-docx. `render_word.ps1` updates fields and exports through Microsoft Word on Windows. The packaged LibreOffice renderer was attempted but unavailable; native Word export was used for visual verification.

## Official instructions

https://www.aeroconf.org/paper-submission

Official 2027 Word template: https://www.aeroconf.org/cms/content_attachments/76/download

Official 2027 LaTeX template: https://www.aeroconf.org/cms/content_attachments/21/download
