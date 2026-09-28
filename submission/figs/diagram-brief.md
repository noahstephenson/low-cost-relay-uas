# Diagram brief for MagicDraw

The paper uses architecture_assessment_workflow.mmd as the editable content source for its assessment-workflow figure. four_flow_architecture.mmd is a separate architecture view for a possible later redraw. Both describe the proposed architecture and analysis; neither records a completed aircraft integration or flight test.

## Workflow activity diagram

Keep three labeled regions. The gray method frame sets the outbound relay target, allocates carrier and payload roles, and declares the scenario and limits. The blue analysis region shows the two calculations performed here: an obstruction and link-margin screen, and a hover-power and mass screen. Their results are checked independently before a candidate placement and dwell are selected. A dashed connector leads to installed relay tests and operational validation, which remain outstanding. Use the labels as well as color so the distinction survives grayscale printing.

## Four-flow architecture view

Put the relay payload, carrier avionics, battery and distribution, and airframe and mount inside one relay-aircraft boundary. Ground endpoint, remote aircraft, and operator are outside it. Mission traffic runs ground endpoint to payload to remote aircraft. Carrier command runs between operator and carrier avionics and is separate from mission traffic. Power runs from battery and distribution to avionics and through a regulated branch to the payload. Mechanical support runs from airframe and mount to payload. Both information paths still share one aircraft and battery; do not imply fault isolation.

## Export handoff

In MagicDraw, recreate the workflow as an activity diagram or the four-flow view as a SysML internal block diagram. Preserve the labels, arrow direction, boundary, and dashed future-work connector. Export vector PDF for LaTeX and a PNG at 300 dpi or higher for Word. Place an export in submission/figs/ with the corresponding Mermaid base name; the existing Mermaid source remains the reviewable content specification. Use only one workflow figure in the manuscript.
