<!-- GENERATED VIEW - DO NOT EDIT. -->

# Decisions and Gaps

[Overview](../../README.md) · [Architecture](../architecture.md) · [Feasibility](../feasibility.md) · [Engineering Status](../engineering-status.md) · [Reference index](README.md)

This page consolidates unresolved owner choices, evidence dependencies, deliberate deferrals, and future-configuration work without changing their model dispositions.

Generated from `model/assurance.yaml`, `model/traceability.yaml`. The structured catalogs remain authoritative.

## Decisions

| Decision | Status | Authority | Remaining issue |
|---|---|---|---|
| **Retain baseline-candidate status and project safety/scope constraints** (DEC-001) | approved | project owner | The baseline shall remain not approved, and the existing restrictions on RF detail, fabrication, physical testing, deployable communications specifications, and weapons integration shall remain in force. |
| **Select UAF terminology and version posture** (DEC-002) | proposed | project owner | Owner selection among intentional retention, version-neutral wording, or later migration. |
| **Select HAZ-001 architecture-level safety objective** (DEC-003) | proposed | project owner | The architecture-level recovery or containment objective and any designated safety authority. |
| **Accept explicit Relay-UAS health/status architecture** (DEC-004) | proposed | project owner | Minimum status content, implementation, physical behavior, endpoint authority, and external conformance. |
| **Confirm CAP-004 cross-cutting semantics** (DEC-005) | proposed | project owner | Owner confirmation and all numeric affordability, mass, endurance, and payload targets. |

## Requires project-owner decision

| Gap | Outcome | Meaning | Next action |
|---|---|---|---|
| GAP-STD-001 | OWNER DECISION REQUIRED | UAF 1.3 is the current OMG formal version, while this repository still names UAF 1.2; the owner has not selected intentional retention, version-neutral terminology, or later migration. | Project owner selects one DEC-002 option: retain UAF 1.2 terminology, adopt version-neutral terminology, or authorize a later UAF 1.3 migration. Retain no-conformance posture until then. |
| GAP-HAZ-001 | OWNER DECISION REQUIRED | HAZ-001 has no defined control or mitigating requirement. | Project owner selects one DEC-003 safety-objective option. Add a CTL/REQ path only after the exact generic objective is accepted. |
| GAP-BUDGET-001 | QUANTITATIVELY_NARROWED | The dependency structure among payload envelope, dry mass, gross mass, propulsion demand, power, battery requirement, endurance, and cost is explicit and has been executed as a reproducible conditional feasibility sweep. Owner targets, packaging geometry, component-class evidence, and physical evidence remain unresolved. | Project owner supplies payload service, endurance, affordability, portability, environment, reserve, and recovery targets; engineering then reruns the coupled analysis and derives gross mass rather than treating it as an independent owner target. |

## Requires physical or external evidence

| Gap | Outcome | Meaning | Next action |
|---|---|---|---|
| GAP-REC-001 | NARROWED | A controlled two-way architecture-role mapping now exists, but source limitations prevent complete recovered-article reconstruction or exact equivalence with CFG-REP / CFG-DOM. | Restore or register an authoritative DOCX revision, supply missing original evidence if available, and obtain owner review of REC-CHG-002 before adding any recovered-specific carrier-view architecture. |
| GAP-SRC-001 | PHYSICAL EVIDENCE REQUIRED | Original standalone teardown photographs, measurements, and inspection records remain unavailable, and the current local SRC-INT-003 file does not match its registered checksum. | Project owner supplies and registers the original evidence set and either restores the registered SRC-INT-003 revision or explicitly registers the changed DOCX as a new source revision; otherwise retain document-reported observations at their current evidence level. |
| GAP-IFC-001 | NARROWED | IFC-EXT-001 through IFC-EXT-007 have complete architecture-level definitions and internal model-review allocation, but external conformance authority, specifications, and execution evidence remain unavailable. | Each external interface authority supplies an authoritative interface basis and accepts a future conformance method before compatibility evidence can be produced. |
| GAP-VER-001 | NARROWED | VER-001 through VER-007 have an accepted 0.7.0 review trail in EVD-008 through EVD-012 and a current 0.8.0 model-level execution record in EVD-013. Physical behavior, performance evidence, and external conformance evidence remain unavailable; VER-008 is deferred and VER-009 is blocked. | Preserve the accepted 0.7.0 trail and current 0.8.0 model-review evidence. Designated future physical and external authorities must supply performance, behavior, safety-relevant physical, and interface-conformance evidence before VER-008 or VER-009 can execute. |

## Deliberately deferred

| Gap | Outcome | Meaning | Next action |
|---|---|---|---|
| GAP-CFG-002 | INTENTIONAL DEFERRAL | The external hazards do not yet have defensible configuration applicability. | A designated external safety authority supplies employment assumptions, configuration applicability, and responsibility allocation before these hazards are activated. |
| GAP-TRC-001 | INTENTIONAL DEFERRAL | CAP-003 has no allocated operational activity, function, component, or supported requirement mechanism. | Retain CAP-003 as unsupported with DEF-004 and TS-009; only an explicitly authorized future payload scope may introduce a mechanism or satisfaction claim. |
| GAP-HAZ-002 | INTENTIONAL DEFERRAL | HAZ-009 is a preserved inactive identifier with no current architecture meaning. | Keep the ID reserved; activate it only through an explicit owner decision supported by hazard content. |
| GAP-IFC-002 | INTENTIONAL DEFERRAL | External communications interfaces intentionally retain unknown protocol, frequency, waveform, power, data-rate, and message-format attributes. | Keep implementation attributes unknown in this repository and preserve TS-009 as intentionally deferred. |

## Future configuration

| Gap | Outcome | Meaning | Next action |
|---|---|---|---|
| GAP-SOS-001 | FUTURE CONFIGURATION | UGV command and telemetry exchanges have no allocated activity, system function, interface, requirement, hazard set, or verification authority. | A future CFG-SOS owner defines UGV responsibilities, authorized information classes, interface authority, and verification criteria before any current-system allocation. |
| GAP-SOS-002 | FUTURE CONFIGURATION | Video or sensor-data return has no allocated current interface, function, requirement, hazard set, or verification authority. | A future CFG-DIG/CFG-SOS owner identifies authorized consumers, service purpose, interface authority, and verification criteria before allocation. |

## Closed or reclassified model work

| Gap | Outcome | Meaning | Next action |
|---|---|---|---|
| GAP-CFG-001 | CLOSED_AS_HISTORICAL_ARTIFACT | The legacy Cameo/MagicDraw report is preserved in the archive and explicitly classified as historical, non-authoritative, and inapplicable to current configurations. | No current action. Re-open only if the project owner authorizes a detailed cross-model reconciliation. |
| GAP-TRC-002 | RECLASSIFIED | CAP-004 is explicitly modeled as a cross-cutting constraint on requirements, trade studies, configurations, and resources; a dedicated mission activity is not semantically required. | Project owner reviews DEC-005 and confirms or rejects the proposed cross-cutting treatment; do not create a synthetic mission activity. |
| GAP-SCN-001 | CLOSED | SCN-001 now uses proposed OA-007 with FUN-CFG-01 and FUN-HLT-01 to represent architecture-level preparation and readiness without defining a procedure. | Project owner reviews OA-007 and its candidate allocations; no operating checklist or startup procedure is authorized. |
| GAP-SOS-003 | CLOSED | IX-009 now has a proposed current-system chain through FUN-HLT-01, CMP-AVN-01, IFC-INT-006, IFC-EXT-007, REQ-008, and candidate verification methods. | Project owner reviews DEC-004. Physical behavior and external conformance remain under GAP-VER-001 and GAP-IFC-001. |

The earlier detailed owner-target package is retained in the [archive](../archive/architecture-decision-target-package.md) as project history. Current dispositions come from the structured catalogs above.
