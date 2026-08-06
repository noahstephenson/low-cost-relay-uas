# Hazard Analysis

Preliminary hazard identification for the relay UAS concept.

> **Structured reconciliation.** Hazard, control, requirement, verification, and gap
> relationships are maintained in [`model/elements.yaml`](model/elements.yaml),
> [`model/requirements.yaml`](model/requirements.yaml), and
> [`model/traceability.yaml`](model/traceability.yaml). This human-readable view is
> reconciled to those candidate relationships; unresolved evidence and coverage gaps
> remain explicit.

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
| HAZ-001 | Uncommanded descent / crash | MODE-001..004 | Power loss, control failure, structural failure | Platform loss; ground impact hazard | High | Medium | **Unmitigated** - no consequence-management requirement exists in the current architecture | Unresolved - GAP-HAZ-001 |
| HAZ-002 | Flyaway (loss of platform command link) | MODE-001..003 | Platform command link loss (IFC-EXT-005) | Uncontrolled flight beyond operator area | High | Medium | REQ-FUN-005 (RTL) | FUN-FLT-04 |
| HAZ-003 | Battery thermal event | All | Cell damage, overcurrent, charge fault | Fire; injury; loss of platform | High | Medium | REQ-SAF-001 | CMP-PWR-01 |
| HAZ-004 | Propeller contact injury | MODE-005, ground handling | Inadvertent motor arming | Injury to personnel | High | High | CTL-001: REQ-FUN-006 provides the Ground Safe arming inhibit; REQ-SAF-002 provides operator-visible armed-state indication | VER-004 scenario walkthrough and VER-006 cross-reference are candidate analysis only; no physical evidence |
| HAZ-005 | Loss of relay function while airborne | MODE-002 → MODE-003 | Payload failure, power rail loss | Relayed link drops; remote UAS may be stranded | Medium | High | REQ-FUN-007 (platform safety only — MODE-003 keeps the aircraft controllable/recoverable; does not restore relay function, which is a black-box payload concern per TS-009) | FUN-REL-01, FUN-REL-02 |
| HAZ-006 | Station drift | MODE-002 | Position hold failure, wind, GNSS loss | Relay geometry degrades; link margin lost | Medium | Medium | REQ-FUN-003 | FUN-FLT-03 |
| HAZ-007 | Battery depletion before recovery | MODE-002, MODE-004 | Endurance overestimate, headwind | Platform loss | Medium | Medium | REQ-FUN-005 | FUN-PWR-02 |
| HAZ-008 | Payload separation in flight | MODE-001..004 | Mount failure (IFC-INT-007) | Falling object hazard; payload loss | High | Low | CTL-005 implemented by REQ-IFC-004; REQ-IFC-001 supports standardization but is not the primary retention mitigation | CMP-MNT-01; IFC-INT-007; VER-008 physical verification deferred |
| HAZ-009 | Reserved — no hazard identified | — | — | — | — | — | Not applicable — no hazard defined | — |

## Hazards Outside This Model

Recorded for completeness. These arise from the payload or its employment and cannot
be analyzed without the RF detail this project deliberately excludes.

| HAZ ID | Hazard | Why Deferred |
|---|---|---|
| HAZ-EXT-001 | RF exposure to personnel | Requires transmit power and antenna data — TS-009 |
| HAZ-EXT-002 | Interference with other spectrum users | Requires frequency plan and regulatory context — REQ-DEF-003 |
| HAZ-EXT-003 | Airspace conflict with crewed aircraft | Depends on employment context and applicable air regulations |

## Open Questions

**Does the concept assume operation over populated areas?** No — the model's working
assumption is austere, non-populated employment. README's Operational Environment
section describes "dismounted small-unit operation from unimproved sites: hand
launch, no support equipment, no prepared surface, no ground infrastructure," and
nothing in the Stakeholders table or operational concept (`uaf-views.md` Op-Tx)
mentions a public or bystander population. This is consistent with the tactical
small-unit employment picture the whole model is built around, not an urban-ops or
BVLOS-over-people concept.

This answer is a **stated assumption, not a verified design constraint**. No
requirement in `requirements.md` currently bars transit over or staging near
populated areas — the assumption lives in the operational narrative, not in an
enforceable `REQ-`. It is recorded here because the Hazard Log needs one coherent
answer to reason about third-party exposure consistently across HAZ-001, HAZ-004,
and HAZ-008; if a future revision of this concept extends employment to populated
areas, this assumption — and the severity/likelihood ratings that depend on it —
would need to be revisited, and the assumption should probably graduate into an
actual `REQ-CON-` constraint at that point.

**Is a flight termination or geofence function in scope?** No — and this is a
genuine "not modeled" finding, not a considered exclusion. There is no `CMP-`, `FUN-`,
or `REQ-` anywhere in the model for flight termination or geofencing, and unlike
every other open architectural question in this repository (station keeping, battery
chemistry, recovery approach, environmental envelope, ...) it does not even have a
`TS-` entry in `trade-studies.md` — meaning nobody has scoped it as a decision to be
made. `system.yaml` and README both explicitly disclaim any certification or
assurance framework ("no MIL-STD, airworthiness, or safety-certification standard is
invoked... no assurance framework, no certification basis, no safety integrity
level"), and flight termination is typically a requirement that gets pulled in by
exactly that kind of framework (e.g., a certificate of authorization for BVLOS or
overflight of people), which this project deliberately does not carry.

The direct consequence: HAZ-001's mitigation cannot cite a flight-termination or
geofence-based control, because the architecture does not contain one. See the
Hazard Log disposition for HAZ-001 below.
