<!-- GENERATED VIEW - DO NOT EDIT. -->

> Generated from `system.yaml`, `model/architecture.yaml`, `model/assurance.yaml`, `model/traceability.yaml`, `.seal/sources.yaml`, `.seal/proof.yaml` with `python scripts/validate-baseline.py --write-reports`.
> This report is a model view, not an approval or verification record.

# Baseline Candidate - Not Approved

## Baseline status

- Model version: `0.4.0-baseline-candidate`
- Status: `baseline_candidate_not_approved`
- Approval: `not_approved`
- Model-valid means structurally consistent; it does not mean safe, verified, or ready.

## Configuration summary

| ID | Role | Maturity | Relationship | Approval |
|---|---|---|---|---|
| CFG-REC | Record the recovered or reference article as represented by available teardown records without treating inference as observation. | observed_record_with_gaps | reference configuration | not_approved |
| CFG-REP | Describe a non-deployable, architecture-level functional replica derived from the reference article while preserving black-box payload and safety constraints. | proposed_architecture | proposed functional derivation, not an exact clone | not_approved |
| CFG-DOM | Describe a domestically sourced low-cost relay-UAS architecture at system and interface level. | proposed_architecture | proposed substitution architecture | not_approved |
| CFG-DIG | Describe a future architecture-level digital relay capable of serving more than one external platform type. | concept_candidate | future concept branch | not_approved |
| CFG-SOS | Describe the complete architecture context connecting operator, ground control, relay UAS, remote UAS, UGV, radio users, services, authorities, and support infrastructure. | context_and_scenario_candidate | outer system-of-systems context containing the relay UAS as one constituent | not_approved |

## Evidence and claim summary

- Claims: 14 (gapped: 10, proven: 4)
- Evidence records: 4
- Claim evidence basis: engineering_inference: 3, internal_document: 1, physically_observed: 2, proposed_design: 7, unknown: 1
- Evidence supports claims; it does not approve the candidate architecture.

<details>
<summary>Claim register summary</summary>

| Claim | Subject | Status | Confidence | Gaps |
|---|---|---|---|---|
| CLM-SCP-001 | Baseline scope and safety controls | proven | 0.99 | - |
| CLM-BND-001 | Two-boundary architecture | gapped | 0.9 | GAP-REC-001 |
| CLM-BND-002 | Independent management of external constituents | gapped | 0.85 | GAP-SOS-001 |
| CLM-ARC-001 | Black-box relay payload | gapped | 0.95 | GAP-REC-001 |
| CLM-ARC-002 | Current platform-to-payload coupling | gapped | 0.95 | GAP-REC-001 |
| CLM-ARC-003 | Platform-command and relay separation | gapped | 0.95 | GAP-IFC-001 |
| CLM-REC-001 | Recovered-article flight-controller identification record | proven | 0.9 | GAP-SRC-001 |
| CLM-REC-002 | Recovered-article power-distribution identification record | proven | 0.9 | GAP-SRC-001 |
| CLM-REC-003 | Recovered relay-payload functional interpretation | gapped | 0.7 | GAP-SRC-001, GAP-REC-001 |
| CLM-REC-004 | Recovered-article unknowns | gapped | 0.95 | GAP-SRC-001, GAP-REC-001 |
| CLM-REC-005 | Recovered-to-generic model reconciliation | proven | 0.9 | GAP-REC-001 |
| CLM-CAP-001 | Intended capability contribution | gapped | 0.9 | GAP-VER-001 |
| CLM-HAZ-001 | Platform control following payload loss | gapped | 0.85 | GAP-VER-001 |
| CLM-SOS-001 | Proposed system-of-systems extension | gapped | 0.95 | GAP-SOS-001 |

</details>

## Active decisions

- `DEC-001` - Retain baseline-candidate status and project safety/scope constraints - **approved**.
- `DEC-002` - Select UAF terminology and version posture - **proposed**.

## Active architecture gaps

| Gap | Category | Severity | Affected model area |
|---|---|---|---|
| GAP-STD-001 | standards-version decision | moderate | DEC-002, SRC-EXT-003, CFG-REP, CFG-DOM, CFG-DIG, CFG-SOS |
| GAP-REC-001 | configuration mapping | major | CFG-REC, CFG-REP, CFG-DOM, CLM-REC-005 |
| GAP-SRC-001 | missing evidence | major | CFG-REC, SRC-GAP-001 |
| GAP-CFG-002 | unknown configuration applicability | moderate | HAZ-EXT-001, HAZ-EXT-002, HAZ-EXT-003 |
| GAP-TRC-001 | unallocated capability | major | CAP-003, REQ-DEF-004, TS-009 |
| GAP-TRC-002 | capability activity allocation | moderate | CAP-004 |
| GAP-HAZ-001 | unmitigated hazard | major | HAZ-001 |
| GAP-IFC-001 | interface verification | major | IFC-EXT-001, IFC-EXT-002, IFC-EXT-003, IFC-EXT-004, IFC-EXT-005 |
| GAP-SCN-001 | scenario activity mapping | moderate | SCN-001, OA-001 |
| GAP-SOS-001 | proposed system-of-systems thread | major | CFG-SOS, SCN-005, OP-004, IX-006, IX-007 |
| GAP-SOS-002 | proposed system-of-systems thread | major | CFG-DIG, CFG-SOS, SCN-006, IX-008 |
| GAP-SOS-003 | health and status coverage | moderate | IX-009, IFC-INT-006 |
| GAP-BUDGET-001 | mass-cost-endurance coupling | major | REQ-PER-001, REQ-PER-002, REQ-PER-003, REQ-PER-004, TS-001, TS-002, TS-003, TS-004, TS-006 |
| GAP-VER-001 | verification evidence | major | VER-001, VER-004, VER-005, VER-006, VER-007, VER-008 |

## Verification status

- Requirement allocations: blocked_by_tbd: 3, candidate: 8, candidate_analysis_only: 2, deferred: 8, intentional_deferral: 4, scope_control: 1, true_coverage_gap: 1.
- `VER-*` records are methods or planned activities unless an `EVD-*` execution record says otherwise.
- Physical verification evidence remains absent or deferred (`GAP-VER-001`).

## Concise traceability summary

- `NEED-001 -> CAP-001 -> SCN-003 -> OA-004 -> FUN-REL-01 -> CMP-COM-01 -> REQ-FUN-001 -> VER-001`.
- `HAZ-004 -> CTL-001 -> REQ-FUN-006 / REQ-SAF-002 -> VER-004 / VER-006 -> GAP-VER-001`.
- `HAZ-008 -> CTL-005 -> REQ-IFC-004 -> VER-005 / VER-008 -> GAP-VER-001`.
- Current platform-to-payload crossings are only `IFC-INT-003` and `IFC-INT-007`; `IFC-INT-010` is payload-internal.
- The complete relationship database remains in `model/traceability.yaml`.

## Items requiring owner attention

- `GAP-REC-001`: Perform element-by-element mapping between recovered-source records and generic CMP/IFC elements without assuming equivalence.
- `GAP-SRC-001`: Register the original evidence set if available; otherwise retain document-reported observations as internal-document evidence.
- `GAP-TRC-001`: Retain the gap unless a future in-scope architecture and evidence basis are approved.
- `GAP-HAZ-001`: Define the safety objective and authority before proposing controls.
- `GAP-IFC-001`: Define architecture-level acceptance criteria and an authority without adding implementation details.
- `GAP-SOS-001`: Formulate the UGV thread with the external-system owner before allocating requirements.
- `GAP-SOS-002`: Define authorized data consumers and architecture-level service criteria before allocation.
- `GAP-BUDGET-001`: Create an analysis-only budget model after source-backed inputs and configuration applicability are established.
- `GAP-VER-001`: Develop analysis and review evidence first; keep physical verification deferred and out of scope.

<details>
<summary>Intentional deferrals and secondary items</summary>

- `GAP-CFG-001` (deferred): The Cameo/MagicDraw HTML export remains unreconciled and is deferred future work outside this work package.
- `GAP-HAZ-002` (deferred): HAZ-009 is a preserved inactive identifier with no current architecture meaning.
- `GAP-IFC-002` (intentionally_out_of_scope): External communications interfaces intentionally retain unknown protocol, frequency, waveform, power, data-rate, and message-format attributes.

</details>

## Standards posture

The repository retains UAF 1.2 terminology. UAF 1.3 is the current OMG formal version. No conformance claim is made; `DEC-002` / `GAP-STD-001` remains unresolved.

## Approval statement

**This baseline remains a candidate and has not been approved.**
