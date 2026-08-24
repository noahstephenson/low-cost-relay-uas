<!-- GENERATED VIEW - DO NOT EDIT. -->

> Generated from `model/system.yaml`, `model/architecture.yaml`, `model/assurance.yaml`, `model/traceability.yaml`, `.seal/sources.yaml`, `.seal/proof.yaml` with `python scripts/validate-baseline.py --write-reports`.
> This report is a model view, not an approval or verification record.

# Baseline Candidate - Not Approved

## Baseline status

- Model version: `0.9.0-baseline-candidate`
- Status: `baseline_candidate_not_approved`
- Approval: `not_approved`
- Model-valid means structurally consistent; it does not mean safe, verified, or ready.

## Internal verification work-package disposition

- Work package: `approved` for `0.7.0-baseline-candidate`.
- Accepted scope: model-level verification work and evidence records only.
- Authority record: `SRC-DEC-005`; acceptance evidence: `EVD-012`.
- Technical baseline: `not_approved`; physical verification and external-interface conformance: `not_established`; safety approval: `not_approved`.
- Unresolved decisions remain proposed: `DEC-002`, `DEC-003`, `DEC-004`, `DEC-005`.

## Model-review status

- Current semantic model: `0.9.0-baseline-candidate`.
- Latest recorded review: `0.8.0-baseline-candidate` with status `executed_not_owner_accepted` in `EVD-013` under `SRC-DEC-006`.
- The accepted 0.7.0 work package remains preserved; the 0.8.0 model-level review is not owner acceptance or technical-baseline approval. The 0.9.0 identifier and documentation refactor has no new evidence record.
- Physical verification, safety approval, and external-interface conformance remain not established.

## Configuration summary

| ID | Role | Maturity | Relationship | Approval |
|---|---|---|---|---|
| CFG-REC | Record the recovered or reference article as represented by available teardown records without treating inference as observation. | observed_record_with_gaps | reference configuration | not_approved |
| CFG-REP | Describe a non-deployable, architecture-level functional replica derived from the reference article while preserving black-box payload and safety constraints. | proposed_architecture | proposed functional derivation, not an exact clone | not_approved |
| CFG-DOM | Describe a domestically sourced low-cost relay-UAS architecture at system and interface level. | proposed_architecture | proposed substitution architecture | not_approved |
| CFG-DIG | Describe a future architecture-level digital relay capable of serving more than one external platform type. | concept_candidate | future concept branch | not_approved |
| CFG-SOS | Describe the complete architecture context connecting operator, ground control, relay UAS, remote UAS, UGV, radio users, services, authorities, and support infrastructure. | context_and_scenario_candidate | outer system-of-systems context containing the relay UAS as one constituent | not_approved |

## Recovered-evidence reconciliation

`CFG-REC` is descriptive evidence. The two-way mapping records role-level correspondence; it does not assert exact recovered-to-candidate equivalence, candidate identity, inheritance, or approval.

| Registered source | Integrity | Treatment |
|---|---|---|
| SRC-INT-001 | MATCH | Principal technical evidence used for architecture-relevant document-reported observations and clearly labeled engineering interpretation. |
| SRC-INT-002 | MATCH | Principal technical evidence used only for recovered item identity, quantity/class, unresolved status, and cross-source comparison; candidate substitutions were excluded. |
| SRC-INT-003 | MISMATCH | Current local file inspected structurally for change awareness only; not treated as the registered source revision and not used to strengthen technical claims. |

- Forward inventory: 24 recovered items and 10 recovered connections (34 total records).
- Forward classifications: CLASS_LEVEL_CORRESPONDENCE: 6, DIRECT_ROLE_CORRESPONDENCE: 9, ENGINEERING_INFERENCE: 2, PARTIAL_ROLE_CORRESPONDENCE: 11, UNKNOWN: 1, UNMATCHED_RECOVERED_ITEM: 5.
- Candidate component coverage: 19 of 19; DIRECT_SOURCE_SUPPORT: 10, ENGINEERING_INFERENCE: 2, INDIRECT_SOURCE_SUPPORT: 4, NO_RECOVERED_EVIDENCE: 2, PROPOSED_ARCHITECTURE_ONLY: 1.
- Candidate interface coverage: 22 of 22; DIRECT_SOURCE_SUPPORT: 3, ENGINEERING_INFERENCE: 4, INDIRECT_SOURCE_SUPPORT: 8, NOT_APPLICABLE: 1, NO_RECOVERED_EVIDENCE: 2, PROPOSED_ARCHITECTURE_ONLY: 4.
- Contradictions: 0. Unmatched recovered records: 5. Unknown recovered records: 1.
- `GAP-REC-001` is narrowed, not closed: the role mapping exists, while complete physical reconstruction and exact equivalence remain unsupported.
- In this repository, `physically_observed` means documented as an observation in an integrity-accepted registered record; it does not claim direct inspection by the model author or automation.

## Evidence and claim summary

- Claims: 14 (gapped: 10, proven: 4)
- Evidence records: 13
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

| Decision | Status | Current model-review evidence | Internal-consistency finding |
|---|---|---|---|
| DEC-001 - Retain baseline-candidate status and project safety/scope constraints | approved | - | - |
| DEC-002 - Select UAF terminology and version posture | proposed | EVD-013 | current architecture remains internally consistent while the terminology/version choice stays unresolved |
| DEC-003 - Select HAZ-001 architecture-level safety objective | proposed | EVD-013 | HAZ-001 is consistently visible, explicitly unmitigated, and governed by GAP-HAZ-001 rather than hidden |
| DEC-004 - Accept explicit Relay-UAS health/status architecture | proposed | EVD-013 | The proposed health/status thread is internally traceable across scenarios, functions, resources, interface, and requirement |
| DEC-005 - Confirm CAP-004 cross-cutting semantics | proposed | EVD-013 | CAP-004 remains internally consistent as a cross-cutting constraint with requirement and trade-study allocations rather than a synthetic mission activity |

## Active architecture gaps

| Gap | Category | Outcome | Severity | Affected model area |
|---|---|---|---|---|
| GAP-STD-001 | standards-version decision | OWNER DECISION REQUIRED | moderate | DEC-002, SRC-EXT-003, CFG-REP, CFG-DOM, CFG-DIG, CFG-SOS |
| GAP-REC-001 | configuration mapping | NARROWED | moderate | CFG-REC, CFG-REP, CFG-DOM, CLM-REC-005, EVD-006, EVD-007, EVD-013, IFC-INT-011 |
| GAP-SRC-001 | missing evidence | PHYSICAL EVIDENCE REQUIRED | major | CFG-REC, SRC-GAP-001, SRC-INT-003, EVD-005 |
| GAP-TRC-001 | unallocated capability | INTENTIONAL DEFERRAL | major | CAP-003, DEF-004, TS-009 |
| GAP-HAZ-001 | unmitigated hazard | OWNER DECISION REQUIRED | major | HAZ-001, DEC-003 |
| GAP-IFC-001 | interface verification | NARROWED | major | IFC-EXT-001, IFC-EXT-002, IFC-EXT-003, IFC-EXT-004, IFC-EXT-005, IFC-EXT-006, IFC-EXT-007, VER-005, VER-009 |
| GAP-SOS-001 | proposed system-of-systems thread | FUTURE CONFIGURATION | major | CFG-SOS, SCN-005, OP-004, IX-006, IX-007 |
| GAP-SOS-002 | proposed system-of-systems thread | FUTURE CONFIGURATION | major | CFG-DIG, CFG-SOS, SCN-006, IX-008 |
| GAP-BUDGET-001 | mass-cost-endurance coupling | QUANTITATIVELY_NARROWED | major | REQ-009, REQ-010, REQ-011, REQ-012, TS-001, TS-002, TS-003, TS-004, TS-006 |
| GAP-VER-001 | verification evidence | NARROWED | major | VER-001, VER-002, VER-003, VER-004, VER-005, VER-006, VER-007, VER-008, VER-009, EVD-008, EVD-009, EVD-010, EVD-011, EVD-012, EVD-013 |

## Remaining work by dependency

### Can be improved through model work now

- No accidental model-local completeness gap remains after this pass.

### Requires project-owner decision

- `GAP-STD-001` - **OWNER DECISION REQUIRED**: Project owner selects one DEC-002 option: retain UAF 1.2 terminology, adopt version-neutral terminology, or authorize a later UAF 1.3 migration. Retain no-conformance posture until then.
- `GAP-HAZ-001` - **OWNER DECISION REQUIRED**: Project owner selects one DEC-003 safety-objective option. Add a CTL/REQ path only after the exact generic objective is accepted.
- `GAP-BUDGET-001` - **QUANTITATIVELY_NARROWED**: Project owner supplies payload service, endurance, affordability, portability, environment, reserve, and recovery targets; engineering then reruns the coupled analysis and derives gross mass rather than treating it as an independent owner target.

### Requires physical or external evidence

- `GAP-REC-001` - **NARROWED**: Restore or register an authoritative DOCX revision, supply missing original evidence if available, and obtain owner review of REC-CHG-002 before adding any recovered-specific carrier-view architecture.
- `GAP-SRC-001` - **PHYSICAL EVIDENCE REQUIRED**: Project owner supplies and registers the original evidence set and either restores the registered SRC-INT-003 revision or explicitly registers the changed DOCX as a new source revision; otherwise retain document-reported observations at their current evidence level.
- `GAP-IFC-001` - **NARROWED**: Each external interface authority supplies an authoritative interface basis and accepts a future conformance method before compatibility evidence can be produced.
- `GAP-VER-001` - **NARROWED**: Preserve the accepted 0.7.0 trail and current 0.8.0 model-review evidence. Designated future physical and external authorities must supply performance, behavior, safety-relevant physical, and interface-conformance evidence before VER-008 or VER-009 can execute.

### Intentionally deferred or future configuration

- `GAP-CFG-002` - **INTENTIONAL DEFERRAL**: A designated external safety authority supplies employment assumptions, configuration applicability, and responsibility allocation before these hazards are activated.
- `GAP-TRC-001` - **INTENTIONAL DEFERRAL**: Retain CAP-003 as unsupported with DEF-004 and TS-009; only an explicitly authorized future payload scope may introduce a mechanism or satisfaction claim.
- `GAP-HAZ-002` - **INTENTIONAL DEFERRAL**: Keep the ID reserved; activate it only through an explicit owner decision supported by hazard content.
- `GAP-IFC-002` - **INTENTIONAL DEFERRAL**: Keep implementation attributes unknown in this repository and preserve TS-009 as intentionally deferred.
- `GAP-SOS-001` - **FUTURE CONFIGURATION**: A future CFG-SOS owner defines UGV responsibilities, authorized information classes, interface authority, and verification criteria before any current-system allocation.
- `GAP-SOS-002` - **FUTURE CONFIGURATION**: A future CFG-DIG/CFG-SOS owner identifies authorized consumers, service purpose, interface authority, and verification criteria before allocation.


## Verification execution matrix

| VER ID | Method | Readiness | Execution | Evidence | Result | Review-time residual gaps |
|---|---|---|---|---|---|---|
| VER-001 | analysis | model_verifiable_now | executed_with_open_gaps | EVD-013 | PASS_WITH_OPEN_GAPS | GAP-BUDGET-001, GAP-IFC-001, GAP-TRC-001, GAP-VER-001 |
| VER-002 | analysis | model_verifiable_now | executed_pass | EVD-013 | PASS | - |
| VER-003 | inspection | model_verifiable_now | executed_with_open_gaps | EVD-013 | PASS_WITH_OPEN_GAPS | GAP-CFG-001, GAP-REC-001, GAP-SRC-001 |
| VER-004 | analysis | model_verifiable_now | executed_with_open_gaps | EVD-013 | PASS_WITH_OPEN_GAPS | GAP-BUDGET-001, GAP-HAZ-001, GAP-IFC-001, GAP-SOS-001, GAP-SOS-002, GAP-VER-001 |
| VER-005 | inspection | model_verifiable_now | executed_with_open_gaps | EVD-013 | PASS_WITH_OPEN_GAPS | GAP-IFC-001, GAP-VER-001 |
| VER-006 | analysis | model_verifiable_now | executed_with_open_gaps | EVD-013 | PASS_WITH_OPEN_GAPS | GAP-CFG-002, GAP-HAZ-001, GAP-VER-001 |
| VER-007 | inspection | model_verifiable_now | executed_pass | EVD-013 | PASS | - |
| VER-008 | deferred demonstration or test | physical_evidence_required | deferred | - | NOT_EXECUTED | GAP-BUDGET-001, GAP-VER-001 |
| VER-009 | external-authority review and future conformance evidence | external_authority_required | blocked | - | BLOCKED | GAP-IFC-001, GAP-VER-001 |

Residual-gap lists record each verification's execution-time result. A referenced gap may have been closed later; current dispositions are listed in the gap sections below.

### Requirement-level review summary

- Requirements reviewed: 23; model-level review passed: 2 (`REQ-016`, `REQ-022`); architecture review passed with open limitations: 21.
- Readiness: analysis_blocked_by_tbd: 12, external_authority_required: 3, model_verifiable_now: 2, physical_evidence_required: 6.
- Deferred/external topics: 5; these `DEF-*` records are not counted as system requirements.
- `EVD-001` through `EVD-004` remain historical. `EVD-008` through `EVD-012` preserve the accepted 0.7.0 review and acceptance trail; `EVD-013` records the latest 0.8.0 model-level review without owner acceptance.
- Internal review does not establish physical requirement satisfaction, external conformance, safety, or technical approval (`GAP-VER-001`).

### Objective corrections from verification

| Evidence | Affected IDs | Problem | Correction | Architecture intent changed? |
|---|---|---|---|---|
| EVD-010 | SRC-INT-001, SRC-INT-002, SRC-INT-003 | Recovered-reference sources listed candidate configurations without an explicit source-record scope distinguishing lineage from physical equivalence or approval. | Each recovered-source record now states that lineage may inform candidate reasoning but does not establish candidate existence, equivalence, inheritance, or approval. | false |
| EVD-013 | IFC-INT-011, IFC-INT-012, IFC-INT-013, IFC-INT-014, IFC-INT-015 | Five necessary current-architecture energy, navigation, and propulsion relationships were absent from the interface catalog or appeared only as renderer associations. | Five implementation-neutral interfaces now state endpoints, purpose, behavior, unknowns, applicability, provenance, and verification allocation without selecting technical values. | false |
| EVD-013 | CMP-AFR-01, CMP-AFR-02, CMP-AFR-03, CMP-AFR-04, CMP-AFR-05, CMP-MNT-01, CMP-PWR-04, MODE-001, MODE-002, MODE-003, MODE-004, MODE-005 | Structural decomposition, passive connector participation, operating-mode transitions, and scenario-lifecycle transitions conveyed engineering meaning only in rendering code. | Resource relationships, mode transitions, and scenario transitions are structured model data and the renderer consumes those records. | false |

## Concise traceability summary

- Mission relay: `NEED-001 -> CAP-001 -> SCN-003 -> OA-004 -> IX-002 / IX-003 -> FUN-REL-01 -> CMP-COM-01 -> IFC-EXT-001 / IFC-EXT-002 -> REQ-001 -> VER-001 / VER-009`.
- Return telemetry: `SCN-004 -> OA-005 -> IX-004 / IX-005 -> FUN-REL-02 -> CMP-COM-01 -> IFC-EXT-003 / IFC-EXT-004 -> REQ-002 -> VER-001 / VER-009`.
- Station keeping: `CAP-002 -> SCN-002 -> OA-003 -> FUN-FLT-03 -> CMP-AVN-01 / CMP-AVN-02 / CMP-AVN-03 -> REQ-003 / REQ-023`.
- Setup and ground safety: `SCN-001 -> OA-007 -> MODE-005 -> HAZ-004 -> CTL-001 -> REQ-006 / REQ-019 -> VER-006`.
- Health/status: `SCN-007 -> IX-009 -> FUN-HLT-01 -> CMP-AVN-01 -> IFC-EXT-007 -> REQ-008 -> VER-005 / VER-008 / VER-009`.
- `HAZ-004 -> CTL-001 -> REQ-006 / REQ-019 -> VER-004 / VER-006 -> GAP-VER-001`.
- `HAZ-008 -> CTL-005 -> REQ-017 -> VER-005 / VER-008 -> GAP-VER-001`.
- Current platform-to-payload crossings are only `IFC-INT-003` and `IFC-INT-007`; `IFC-INT-010` is payload-internal.
- The complete relationship database remains in `model/traceability.yaml`.

## Items requiring owner attention

- `GAP-SRC-001`: Project owner supplies and registers the original evidence set and either restores the registered SRC-INT-003 revision or explicitly registers the changed DOCX as a new source revision; otherwise retain document-reported observations at their current evidence level.
- `GAP-TRC-001`: Retain CAP-003 as unsupported with DEF-004 and TS-009; only an explicitly authorized future payload scope may introduce a mechanism or satisfaction claim.
- `GAP-HAZ-001`: Project owner selects one DEC-003 safety-objective option. Add a CTL/REQ path only after the exact generic objective is accepted.
- `GAP-IFC-001`: Each external interface authority supplies an authoritative interface basis and accepts a future conformance method before compatibility evidence can be produced.
- `GAP-SOS-001`: A future CFG-SOS owner defines UGV responsibilities, authorized information classes, interface authority, and verification criteria before any current-system allocation.
- `GAP-SOS-002`: A future CFG-DIG/CFG-SOS owner identifies authorized consumers, service purpose, interface authority, and verification criteria before allocation.
- `GAP-BUDGET-001`: Project owner supplies payload service, endurance, affordability, portability, environment, reserve, and recovery targets; engineering then reruns the coupled analysis and derives gross mass rather than treating it as an independent owner target.
- `GAP-VER-001`: Preserve the accepted 0.7.0 trail and current 0.8.0 model-review evidence. Designated future physical and external authorities must supply performance, behavior, safety-relevant physical, and interface-conformance evidence before VER-008 or VER-009 can execute.

## Closed or reclassified gaps in this maturation pass

- `GAP-CFG-001` - **CLOSED_AS_HISTORICAL_ARTIFACT**: The legacy Cameo/MagicDraw report is preserved in the archive and explicitly classified as historical, non-authoritative, and inapplicable to current configurations.
- `GAP-TRC-002` - **RECLASSIFIED**: CAP-004 is explicitly modeled as a cross-cutting constraint on requirements, trade studies, configurations, and resources; a dedicated mission activity is not semantically required.
- `GAP-SCN-001` - **CLOSED**: SCN-001 now uses proposed OA-007 with FUN-CFG-01 and FUN-HLT-01 to represent architecture-level preparation and readiness without defining a procedure.
- `GAP-SOS-003` - **CLOSED**: IX-009 now has a proposed current-system chain through FUN-HLT-01, CMP-AVN-01, IFC-INT-006, IFC-EXT-007, REQ-008, and candidate verification methods.

<details>
<summary>Intentional deferrals and secondary items</summary>

- `GAP-CFG-002` (deferred): The external hazards do not yet have defensible configuration applicability.
- `GAP-HAZ-002` (deferred): HAZ-009 is a preserved inactive identifier with no current architecture meaning.
- `GAP-IFC-002` (intentionally_out_of_scope): External communications interfaces intentionally retain unknown protocol, frequency, waveform, power, data-rate, and message-format attributes.

</details>

## Standards posture

The repository retains UAF 1.2 terminology. UAF 1.3 is the current OMG formal version. No conformance claim is made; `DEC-002` / `GAP-STD-001` remains unresolved.

## Approval statement

**This baseline remains a candidate and has not been approved.**
