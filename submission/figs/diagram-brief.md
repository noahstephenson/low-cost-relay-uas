# Diagram brief for MagicDraw

The paper uses architecture_assessment_workflow.mmd as the editable content source for its assessment-workflow figure. four_flow_architecture.mmd is a separate architecture view for a possible later redraw. Both describe the proposed architecture and analysis; neither records a completed aircraft integration or flight test.

## Workflow activity diagram

Keep the arrows in this order: operational need; carrier and black-box payload boundary; allocation of mission traffic, aircraft command, electrical power, and mechanical support; declared geometry, radio, payload, and carrier assumptions. Then split to parallel link and carrier checks and merge at independent numerical review. The decision node reports link failure, excessive finite size, mathematical nonclosure, or a conditional pass. Use a dashed connector to outstanding physical verification and operational validation. The dashed connector is essential: those activities have not been performed.

## Four-flow architecture view

Put the relay payload, carrier avionics, battery and distribution, and airframe and mount inside one relay-aircraft boundary. Ground endpoint, remote aircraft, and operator are outside it. Mission traffic runs ground endpoint to payload to remote aircraft. Carrier command runs between operator and carrier avionics and is separate from mission traffic. Power runs from battery and distribution to avionics and through a regulated branch to the payload. Mechanical support runs from airframe and mount to payload. Both information paths still share one aircraft and battery; do not imply fault isolation.

## Export handoff

In MagicDraw, recreate the workflow as an activity diagram or the four-flow view as a SysML internal block diagram. Preserve the labels, arrow direction, boundary, and dashed future-work connector. Export vector PDF for LaTeX and a PNG at 300 dpi or higher for Word. Place an export in submission/figs/ with the corresponding Mermaid base name; the existing Mermaid source remains the reviewable content specification. Use only one workflow figure in the manuscript.
