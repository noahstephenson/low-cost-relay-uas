<!-- GENERATED VIEW - DO NOT EDIT. -->

# Verification

[Overview](../../README.md) · [Architecture](../architecture.md) · [Feasibility](../feasibility.md) · [Engineering Status](../engineering-status.md) · [Reference index](README.md)

Model verification, quantitative analysis, physical verification, and external conformance are separate evidence classes. A passing repository check is not a verified aircraft.

Generated from `model/assurance.yaml`, `.seal/proof.yaml`. The structured catalogs remain authoritative.

## Evidence boundary

| Evidence class | What it can establish | Current position |
|---|---|---|
| Internal model review | Structure, reference integrity, allocation, and consistency | Latest recorded review is 0.8.0; not owner acceptance |
| Reproducible analysis | Conditional mass, power, endurance, and cost behavior | Executed with exploratory assumptions |
| Physical verification | Aircraft behavior and measured performance | Not performed |
| External conformance | Endpoint, spectrum, and authority-controlled compatibility | Blocked by missing authority/specifications |
| Technical baseline approval | Owner acceptance of a design baseline | Not approved |

## Verification activities

| Activity | Method | Readiness | Execution | Evidence | Residual gaps |
|---|---|---|---|---|---|
| **Requirement and architecture analysis** (VER-001) | analysis | model_verifiable_now | executed_with_open_gaps | EVD-013 | GAP-BUDGET-001, GAP-IFC-001, GAP-TRC-001, GAP-VER-001 |
| **Structured traceability audit** (VER-002) | analysis | model_verifiable_now | executed_pass | EVD-013 | - |
| **Source and evidence-record inspection** (VER-003) | inspection | model_verifiable_now | executed_with_open_gaps | EVD-013 | GAP-CFG-001, GAP-REC-001, GAP-SRC-001 |
| **Operational-scenario walkthrough** (VER-004) | analysis | model_verifiable_now | executed_with_open_gaps | EVD-013 | GAP-BUDGET-001, GAP-HAZ-001, GAP-IFC-001, GAP-SOS-001, GAP-SOS-002, GAP-VER-001 |
| **Interface-catalog inspection** (VER-005) | inspection | model_verifiable_now | executed_with_open_gaps | EVD-013 | GAP-IFC-001, GAP-VER-001 |
| **Hazard-control-requirement cross-reference** (VER-006) | analysis | model_verifiable_now | executed_with_open_gaps | EVD-013 | GAP-CFG-002, GAP-HAZ-001, GAP-VER-001 |
| **Configuration-applicability review** (VER-007) | inspection | model_verifiable_now | executed_pass | EVD-013 | - |
| **Deferred physical verification method** (VER-008) | deferred demonstration or test | physical_evidence_required | deferred | - | GAP-BUDGET-001, GAP-VER-001 |
| **External interface conformance verification** (VER-009) | external-authority review and future conformance evidence | external_authority_required | blocked | - | GAP-IFC-001, GAP-VER-001 |

The current semantic model is `0.9.0-baseline-candidate`. The latest recorded review evidence remains tied to `0.8.0-baseline-candidate`; the identifier/documentation migration does not rewrite that evidence.
