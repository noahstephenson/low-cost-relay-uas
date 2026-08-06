<!-- GENERATED VIEW - DO NOT AUTHOR INDEPENDENT ARCHITECTURE FACTS HERE. -->

> Generated from `system.yaml`, `model/configurations.yaml`, `model/claims.yaml`, `model/operational-scenarios.yaml`, `model/interfaces.yaml`, `model/requirements.yaml`, `.seal/sources.yaml`, `.seal/proof.yaml`. Regenerate with `python scripts/validate-baseline.py --write-reports`.
> The structured catalogs are authoritative. This report is not an approval record.

# Baseline Candidate - Not Approved

## Baseline purpose

Reconcile the existing exploratory architecture with configuration, evidence, decision, and traceability records without adding implementation detail.

## Status and approval

- Model version: `0.2.0-baseline-candidate`
- Baseline status: `baseline_candidate_not_approved`
- Approval state: `not_approved`

**This is a baseline candidate. It has not been approved by the project owner.**

## System boundaries

### Relay UAS (inner)

Role: product boundary. Evidence basis: `proposed_design`. Decision status: `proposed`.

Includes: airframe, structure, propulsion, electrical power, flight control, platform command link, relay payload as a black box, payload management at architecture level, antennas as black-box physical resources, payload mounting, configuration and maintenance interfaces.

### C2 Ecosystem (outer)

Role: system-of-systems context boundary. Evidence basis: `proposed_design`. Decision status: `proposed`.

Includes: operator, ground-control system, relay UAS, remote UAS, UGV, radio users, network services, maintenance personnel, spectrum-management authority, supporting infrastructure.

## Configuration summaries

| Configuration | Name | Boundary | Maturity | Approval | Derivation |
|---|---|---|---|---|---|
| CFG-REC | Recovered Reference Article | Relay UAS | observed_record_with_gaps | not_approved | reference configuration |
| CFG-REP | Safe Functional-Replica Architecture | Relay UAS | proposed_architecture | not_approved | proposed functional derivation, not an exact clone |
| CFG-DOM | Domestic Low-Cost Relay-UAS Architecture | Relay UAS | proposed_architecture | not_approved | proposed substitution architecture |
| CFG-DIG | Future Digital Multi-Platform Relay Architecture | Relay UAS | concept_candidate | not_approved | future concept branch |
| CFG-SOS | UAS-UGV-Radio C2 System-of-Systems Architecture | C2 Ecosystem | context_and_scenario_candidate | not_approved | outer system-of-systems context containing the relay UAS as one constituent |

## Evidence classification summary

| Evidence basis | Claim count |
|---|---:|
| `physically_observed` | 2 |
| `internal_document` | 1 |
| `external_source` | 0 |
| `engineering_inference` | 3 |
| `proposed_design` | 7 |
| `unknown` | 1 |

The register classifies repository inspection and reverse-engineering reports separately from engineering inference and proposed design. Physically observed claims are limited to visible-marking observations documented with embedded source imagery; the article was not re-inspected for this baseline.

## Current architecture coverage

- Sources: 16
- Claims: 14
- Configurations: 5
- Operational scenarios: 8
- Interfaces: 16
- Requirements classified: 27
- Recorded gaps: 18

## Major unresolved decisions

- **CFG-REC:** Exact battery architecture
- **CFG-REC:** Propulsion component ratings and corner mapping
- **CFG-REC:** Relay-module identities and internal behavior
- **CFG-REC:** Antenna roles
- **CFG-REC:** Functions of auxiliary modules
- **CFG-REC:** Complete standalone teardown evidence set
- **CFG-REP:** Extent to which the current generic component model represents the recovered article
- **CFG-REP:** Mass, cost, power, endurance, and payload envelopes
- **CFG-REP:** Platform command-link architecture
- **CFG-REP:** Verification evidence
- **CFG-DOM:** Domestic-content criteria and approval authority
- **CFG-DOM:** Component substitutions
- **CFG-DOM:** Interface conformance criteria
- **CFG-DOM:** Cost and logistics evidence
- **CFG-DIG:** Payload-management boundary
- **CFG-DIG:** Supported platform classes
- **CFG-DIG:** Information-assurance requirements
- **CFG-DIG:** Interface standards and conformance evidence
- **CFG-SOS:** External-system ownership and approval authorities
- **CFG-SOS:** UGV and radio-user information exchanges
- **CFG-SOS:** Network-service dependencies
- **CFG-SOS:** Cross-system safety and assurance responsibilities
- **CFG-SOS:** System-of-systems verification strategy

## Approval statement

This is a baseline candidate. It has not been approved by the project owner.
