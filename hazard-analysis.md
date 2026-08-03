# Hazard Analysis

Preliminary hazard identification for the relay UAS concept.

> **Not a safety assessment.** No safety standard is invoked, no severity/probability
> matrix is claimed as authoritative, and no risk acceptance authority exists for this
> project. This file identifies hazards so the architecture can reason about them —
> it is not evidence of safety and would not survive review as such.

## Method

Hazards are identified per operating mode (`MODE-*` in `README.md`) and per subsystem.
Each hazard traces to a mitigating requirement or is recorded as unmitigated.

Severity and likelihood use a simple qualitative scale. Do **not** map these onto
MIL-STD-882E severity categories — that standard carries process obligations this
project does not meet.

| Scale | Severity | Likelihood |
|---|---|---|
| High | Injury to persons or loss of third-party property | Expected without mitigation |
| Medium | Loss of the platform or the relayed link | Plausible |
| Low | Degraded mission, recoverable | Unlikely |

## Hazard Log

| HAZ ID | Hazard | Mode(s) | Cause | Effect | Sev | Like | Mitigation | Traces To |
|---|---|---|---|---|---|---|---|---|
| HAZ-001 | Uncommanded descent / crash | MODE-001..004 | Power loss, control failure, structural failure | Platform loss; ground impact hazard | High | TODO | TODO | TODO |
| HAZ-002 | Flyaway (loss of platform command link) | MODE-001..003 | Platform command link loss (IFC-EXT-005) | Uncontrolled flight beyond operator area | High | TODO | REQ-FUN-005 (RTL) | FUN-FLT-04 |
| HAZ-003 | Battery thermal event | All | Cell damage, overcurrent, charge fault | Fire; injury; loss of platform | High | TODO | REQ-SAF-001 | CMP-PWR-01 |
| HAZ-004 | Propeller contact injury | MODE-005, ground handling | Inadvertent motor arming | Injury to personnel | High | TODO | REQ-SAF-002 | TODO |
| HAZ-005 | Loss of relay function while airborne | MODE-002 → MODE-003 | Payload failure, power rail loss | Relayed link drops; remote UAS may be stranded | Medium | TODO | TODO | FUN-REL-01, FUN-REL-02 |
| HAZ-006 | Station drift | MODE-002 | Position hold failure, wind, GNSS loss | Relay geometry degrades; link margin lost | Medium | TODO | REQ-FUN-003 | FUN-FLT-03 |
| HAZ-007 | Battery depletion before recovery | MODE-002, MODE-004 | Endurance overestimate, headwind | Platform loss | Medium | TODO | REQ-FUN-005 | FUN-PWR-02 |
| HAZ-008 | Payload separation in flight | MODE-001..004 | Mount failure (IFC-INT-007) | Falling object hazard; payload loss | High | TODO | REQ-IFC-001 | CMP-MNT-01 |
| HAZ-009 | TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO |

## Hazards Outside This Model

Recorded for completeness. These arise from the payload or its employment and cannot
be analyzed without the RF detail this project deliberately excludes.

| HAZ ID | Hazard | Why Deferred |
|---|---|---|
| HAZ-EXT-001 | RF exposure to personnel | Requires transmit power and antenna data — TS-009 |
| HAZ-EXT-002 | Interference with other spectrum users | Requires frequency plan and regulatory context — REQ-DEF-003 |
| HAZ-EXT-003 | Airspace conflict with crewed aircraft | Depends on employment context and applicable air regulations |

## Open Questions

<!-- STUB -->

- TODO — Does the concept assume operation over populated areas? That single
  assumption drives most of HAZ-001, HAZ-004, and HAZ-008.
- TODO — Is a flight termination or geofence function in scope?
