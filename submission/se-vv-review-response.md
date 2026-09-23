# Systems engineering reviewer response, draft after r3

This branch is a review draft. The published aeroconf-2027-paper-2784-r3 tag remains unchanged. The scientific inputs, solver, and 1,890 saved records remain the r3 baseline.

## Incorporated in the manuscript

- The abstract distinguishes the architecture-screening method from the notional relay case study and reduces the number of reported results.
- Section 2 names two candidate service measures: separation at fixed dwell and dwell at fixed separation. The 10/20 km and 30/45 min threshold/objective points are analyst-selected values from the existing grid. They are not stakeholder-approved requirements.
- A four-flow allocation table maps mission traffic, aircraft command, electrical power, and mechanical support to existing interface IDs and open integration attributes.
- Section 3 names the selected NASA handbook process areas and distinguishes model verification, limited model validation, unperformed system verification, and unperformed operational validation. A planning matrix traces seven existing REQ candidates to present evidence and future acceptance work.
- The existing reserve, peak-power, link-loss, and operating-condition allowances are stated as an analysis margin policy, not an approved project standard.
- A 2 by 2 table preserves joint link/carrier outcomes: 18 both pass, 12 link-only pass, 36 carrier-only pass, and 24 neither pass.

## Reviewer points that require qualification

- The current LaTeX bibliography is already in first-citation order. This was checked by comparing the first appearance of each citation key with the bibliography sequence.
- The manuscript already states that the two smaller commercial hover comparisons are sensitive to the assumed auxiliary load. Only the Matrice 30 stays within 10 percent across the sweep.
- The approved title is retained. The text states that only stationary outbound hover service is calculated.
- Existing REQ values for endurance, mass, payload envelope, and rail specifications remain TBD in the architecture catalog. The study points do not close those owner decisions.
- A normalized tornado chart, fixed-airframe branch, and alternative aircraft trade would require additional declared analyses. They are not presented as completed results.

## Needed from the author before release

1. Confirm or replace the generic operator context and the analyst-selected 10/20 km and 30/45 min study points.
2. Supply the presenter name in the conference portal. Presenter N/A is not present in the manuscript source; the conference website manages presentation details separately.
3. Upload the manually formatted Word copy after applying the companion Word prompt. The generated repository DOCX was left at r3 for this draft.
4. Decide whether a MagicDraw four-flow export should replace the informal architecture panel. The editable source remains figs/four_flow_architecture.mmd.

The draft PDF is 12 letter pages, within the conference's published 6-20-page paper range. The 35 unit tests, baseline check, and independent 1,890-row checker pass. No draft commit or tag has been published.
