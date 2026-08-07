<!-- GENERATED VIEW - DO NOT EDIT. -->

> Generated from `system.yaml`, `model/architecture.yaml`, `model/assurance.yaml`, `model/traceability.yaml`, `.seal/sources.yaml`, `.seal/proof.yaml` with `python scripts/validate-baseline.py --write-reports`.
> This report is a model view, not an approval or verification record.

# Baseline Candidate - Not Approved

## Baseline status

- Model version: `0.5.0-baseline-candidate`
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
- `DEC-003` - Select HAZ-001 architecture-level safety objective - **proposed**.
- `DEC-004` - Accept explicit Relay-UAS health/status architecture - **proposed**.
- `DEC-005` - Confirm CAP-004 cross-cutting semantics - **proposed**.

## Active architecture gaps

| Gap | Category | Outcome | Severity | Affected model area |
|---|---|---|---|---|
| GAP-STD-001 | standards-version decision | OWNER DECISION REQUIRED | moderate | DEC-002, SRC-EXT-003, CFG-REP, CFG-DOM, CFG-DIG, CFG-SOS |
| GAP-REC-001 | configuration mapping | INTENTIONAL DEFERRAL | major | CFG-REC, CFG-REP, CFG-DOM, CLM-REC-005 |
| GAP-SRC-001 | missing evidence | PHYSICAL EVIDENCE REQUIRED | major | CFG-REC, SRC-GAP-001 |
| GAP-TRC-001 | unallocated capability | INTENTIONAL DEFERRAL | major | CAP-003, REQ-DEF-004, TS-009 |
| GAP-HAZ-001 | unmitigated hazard | OWNER DECISION REQUIRED | major | HAZ-001, DEC-003 |
| GAP-IFC-001 | interface verification | NARROWED | major | IFC-EXT-001, IFC-EXT-002, IFC-EXT-003, IFC-EXT-004, IFC-EXT-005, IFC-EXT-006, IFC-EXT-007, VER-005, VER-009 |
| GAP-SOS-001 | proposed system-of-systems thread | FUTURE CONFIGURATION | major | CFG-SOS, SCN-005, OP-004, IX-006, IX-007 |
| GAP-SOS-002 | proposed system-of-systems thread | FUTURE CONFIGURATION | major | CFG-DIG, CFG-SOS, SCN-006, IX-008 |
| GAP-BUDGET-001 | mass-cost-endurance coupling | NARROWED | major | REQ-PER-001, REQ-PER-002, REQ-PER-003, REQ-PER-004, TS-001, TS-002, TS-003, TS-004, TS-006 |
| GAP-VER-001 | verification evidence | NARROWED | major | VER-001, VER-004, VER-005, VER-006, VER-007, VER-008, VER-009 |

## Verification status

- Requirement readiness: analysis_blocked_by_tbd: 12, external_authority_required: 5, intentionally_deferred: 3, model_verifiable_now: 2, physical_evidence_required: 6.
- `VER-*` records are methods or planned activities unless an `EVD-*` execution record says otherwise.
- Physical verification evidence remains absent or deferred (`GAP-VER-001`).

## Concise traceability summary

- Mission relay: `NEED-001 -> CAP-001 -> SCN-003 -> OA-004 -> IX-002 / IX-003 -> FUN-REL-01 -> CMP-COM-01 -> IFC-EXT-001 / IFC-EXT-002 -> REQ-FUN-001 -> VER-001 / VER-009`.
- Return telemetry: `SCN-004 -> OA-005 -> IX-004 / IX-005 -> FUN-REL-02 -> CMP-COM-01 -> IFC-EXT-003 / IFC-EXT-004 -> REQ-FUN-002 -> VER-001 / VER-009`.
- Station keeping: `CAP-002 -> SCN-002 -> OA-003 -> FUN-FLT-03 -> CMP-AVN-01 / CMP-AVN-02 / CMP-AVN-03 -> REQ-FUN-003 / REQ-CON-004`.
- Setup and ground safety: `SCN-001 -> OA-007 -> MODE-005 -> HAZ-004 -> CTL-001 -> REQ-FUN-006 / REQ-SAF-002 -> VER-006`.
- Health/status: `SCN-007 -> IX-009 -> FUN-HLT-01 -> CMP-AVN-01 -> IFC-EXT-007 -> REQ-FUN-008 -> VER-005 / VER-008 / VER-009`.
- `HAZ-004 -> CTL-001 -> REQ-FUN-006 / REQ-SAF-002 -> VER-004 / VER-006 -> GAP-VER-001`.
- `HAZ-008 -> CTL-005 -> REQ-IFC-004 -> VER-005 / VER-008 -> GAP-VER-001`.
- Current platform-to-payload crossings are only `IFC-INT-003` and `IFC-INT-007`; `IFC-INT-010` is payload-internal.
- The complete relationship database remains in `model/traceability.yaml`.

## Items requiring owner attention

- `GAP-REC-001`: Under a separately authorized recovered-reference work package, perform source-by-source mapping between CFG-REC evidence and candidate CMP/IFC elements without assuming equivalence.
- `GAP-SRC-001`: Project owner supplies and registers the original photograph, measurement, and inspection set if available; otherwise retain document-reported observations at their current evidence level.
- `GAP-TRC-001`: Retain CAP-003 as unsupported with REQ-DEF-004 and TS-009; only an explicitly authorized future payload scope may introduce a mechanism or satisfaction claim.
- `GAP-HAZ-001`: Project owner selects one DEC-003 safety-objective option. Add a CTL/REQ path only after the exact generic objective is accepted.
- `GAP-IFC-001`: Each external interface authority supplies an authoritative interface basis and accepts a future conformance method before compatibility evidence can be produced.
- `GAP-SOS-001`: A future CFG-SOS owner defines UGV responsibilities, authorized information classes, interface authority, and verification criteria before any current-system allocation.
- `GAP-SOS-002`: A future CFG-DIG/CFG-SOS owner identifies authorized consumers, service purpose, interface authority, and verification criteria before allocation.
- `GAP-BUDGET-001`: Project owner selects candidate cost, endurance, mass, and payload target ranges; source-backed component inputs are then required before executing the coupled TS-001/002/003/004/006 analysis.
- `GAP-VER-001`: Execute and capture the model-review methods as EVD records; designated future physical and external authorities must supply all performance, behavior, and conformance evidence.

## Closed or reclassified gaps in this maturation pass

- `GAP-TRC-002` - **RECLASSIFIED**: CAP-004 is explicitly modeled as a cross-cutting constraint on requirements, trade studies, configurations, and resources; a dedicated mission activity is not semantically required.
- `GAP-SCN-001` - **CLOSED**: SCN-001 now uses proposed OA-007 with FUN-CFG-01 and FUN-HLT-01 to represent architecture-level preparation and readiness without defining a procedure.
- `GAP-SOS-003` - **CLOSED**: IX-009 now has a proposed current-system chain through FUN-HLT-01, CMP-AVN-01, IFC-INT-006, IFC-EXT-007, REQ-FUN-008, and candidate verification methods.

<details>
<summary>Intentional deferrals and secondary items</summary>

- `GAP-CFG-001` (deferred): The Cameo/MagicDraw HTML export remains unreconciled and is deferred future work outside this work package.
- `GAP-CFG-002` (deferred): The external hazards do not yet have defensible configuration applicability.
- `GAP-HAZ-002` (deferred): HAZ-009 is a preserved inactive identifier with no current architecture meaning.
- `GAP-IFC-002` (intentionally_out_of_scope): External communications interfaces intentionally retain unknown protocol, frequency, waveform, power, data-rate, and message-format attributes.

</details>

## Standards posture

The repository retains UAF 1.2 terminology. UAF 1.3 is the current OMG formal version. No conformance claim is made; `DEC-002` / `GAP-STD-001` remains unresolved.

## Approval statement

**This baseline remains a candidate and has not been approved.**
