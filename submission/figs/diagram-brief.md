# Diagram brief

The paper uses architecture_assessment_workflow.mmd as the editable Mermaid source for Figure 3. Its gray frame adapts selected system design practices in the cited NASA Systems Engineering Handbook: define a service need, derive candidate criteria, and allocate functions. This is an analyst-defined study frame, not a NASA-prescribed named workflow or an approved requirements baseline. four_flow_architecture.mmd is a separate architecture view for a possible later redraw. Neither diagram records a completed aircraft integration or flight test.

## Workflow activity diagram

The gray NASA-aligned frame sets the need, candidate criteria, and functional allocation. The blue study boxes show the two screens actually performed here (clearance and link margin; hover power and mass) and the candidate placement and dwell comparison. A dashed connector leads to installed tests and field validation, which remain outstanding. Labels make the distinction legible in grayscale.

## Four-flow architecture view

Put the relay payload, carrier avionics, battery and distribution, and airframe and mount inside one relay-aircraft boundary. Ground endpoint, remote aircraft, and operator are outside it. Mission traffic runs ground endpoint to payload to remote aircraft. Carrier command runs between operator and carrier avionics and is separate from mission traffic. Power runs from battery and distribution to avionics and through a regulated branch to the payload. Mechanical support runs from airframe and mount to payload. Both information paths still share one aircraft and battery; do not imply fault isolation.

## Export handoff

Render the Mermaid workflow with `python submission/render_workflow.py`; the script generates its PDF and PNG assets in this directory. If a later MagicDraw version is needed, preserve the labels, arrow direction, color distinction, and dashed future-work connector. Use only one workflow figure in the manuscript.
