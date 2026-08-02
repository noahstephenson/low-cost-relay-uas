# Low-Cost Attritable Communications Relay UAS

> **Status: exploratory draft.** Independent concept study. Not affiliated with any
> program of record, and not a build specification. See [Scope Boundaries](#scope-boundaries).

## Overview

<!-- STUB: 2-3 paragraphs. What the system is, why the concept exists, what the
     three-node relay arrangement looks like at a glance. Keep factual; avoid
     claiming performance this model does not substantiate. -->

TODO — A small, deliberately inexpensive rotary-wing platform whose sole mission is to
carry a communications-relay payload to altitude and hold station, extending the
control and telemetry link between a ground control node and a separate remote UAS
operating beyond direct line of sight.

The design driver is unit cost. The concept assumes the platform is attritable —
cheap enough that loss is tolerable — which inverts the usual optimization from
capability-per-airframe toward capability-per-dollar.

## Scope Boundaries

This repository models **capability justification and system architecture**.

**In scope**

- Capability gap articulation and operational concept
- Platform architecture: airframe, propulsion, power, avionics
- Interface definition, cost and mass budget allocation
- Requirements, hazard identification, and end-to-end traceability

**Out of scope — deliberately**

- RF waveform, frequency plan, protocol, modulation, or link budget
- Antenna design, gain patterns, or transmit power
- Electronic warfare technique or counter-EW design
- Weapons or munitions integration of any kind
- Hardware build, flight test, or any spectrum-radiating experimentation

The communications payload (`CMP-COM-01`) is modeled as a **black box** throughout:
defined by its function and interfaces, not its implementation. Moving toward
hardware would require RF engineering expertise, spectrum authorization, and — in a
defense-affiliated context — export control review. None of that is addressed here.

## Repository Structure

| File | Contents |
|---|---|
| `system.yaml` | Machine-readable metadata, scope, ID scheme |
| `architecture.md` | Components (`CMP-`), functions (`FUN-`), interfaces (`IFC-`) |
| `requirements.md` | Requirements (`REQ-`) with rationale and verification method |
| `uaf-views.md` | Capability, operational, and resource viewpoints (Mermaid) |
| `hazard-analysis.md` | Hazards (`HAZ-`) and mitigations |
| `trade-studies.md` | Open decisions (`TS-`) this model does not resolve |
| `traceability.md` | Cross-reference matrices linking every ID |

## System Boundary

**Inside the system boundary**

- Airframe and payload mount structure (`CMP-AFR-*`, `CMP-MNT-01`)
- Propulsion — motors, ESCs, propellers (`CMP-PRP-*`)
- Power — battery, distribution, regulation (`CMP-PWR-*`)
- Avionics — flight controller, sensors, platform command receiver (`CMP-AVN-*`)
- Relay payload as a black box (`CMP-COM-01`, `CMP-COM-02`)

**Outside the system boundary**

- Ground control node (`OP-001`) — originates traffic; independently operated
- Remote UAS node (`OP-003`) — the system being relayed for; independently operated
- Platform operator and their control equipment
- Spectrum management authority — governs any real implementation
- Launch and recovery handling, transport, and field sustainment equipment

## Operational Environment

<!-- STUB: describe the intended employment environment. Candidates below —
     replace with your own analysis and delete what does not apply. -->

TODO — Notional employment is dismounted small-unit operation from unimproved sites.
Environmental envelope (temperature, wind, precipitation) is **not yet specified**;
setting it is TS-010. No environmental qualification standard is invoked — this is a
concept study, not a qualification program.

## Operating Modes

Mode IDs are referenced by `requirements.md` and `hazard-analysis.md`.

| Mode ID | Name | Description | Active Functions | Constraints |
|---|---|---|---|---|
| MODE-001 | Transit | Climb and fly to station | FUN-FLT-01, FUN-FLT-02, FUN-CMD-01 | Payload may be inactive |
| MODE-002 | Station Keeping | Loiter at relay altitude, payload active | FUN-FLT-01, FUN-FLT-03, FUN-REL-01, FUN-REL-02 | Primary mission mode |
| MODE-003 | Relay Degraded | Partial or failed payload function; platform airborne | FUN-FLT-01, FUN-FLT-03 | TODO — define degraded criteria |
| MODE-004 | Return / Recovery | Return to launch on low battery or command | FUN-FLT-01, FUN-FLT-04, FUN-PWR-02 | Relay function ends |
| MODE-005 | Ground Safe | Powered on ground; payload and motors inhibited | FUN-PWR-01 | Motor arming inhibited |

## Key Technical Challenges

<!-- STUB: each item should become a short paragraph of real analysis. -->

1. **Endurance versus unit cost.** TODO — Endurance drives battery mass, which drives
   airframe and propulsion sizing, which drives cost. The concept lives or dies on
   where this curve is cut.

2. **Station-keeping without heavy dependence on GNSS.** TODO — A relay is only useful
   if it holds a stable position, but GNSS availability cannot be assumed in the
   environments that motivate the concept.

3. **Payload mass fraction on a deliberately cheap airframe.** TODO

4. **Attritability versus recoverability.** TODO — If the platform is cheap enough to
   lose, how much design effort should go into recovering it?

5. **Payload-agnostic mount and power interface.** TODO — Keeping `CMP-COM-01` a true
   black box requires the mechanical and power interfaces to be genuinely generic.

## Stakeholders

| Stakeholder | Role |
|---|---|
| Small-unit operator | Employs and recovers the relay platform |
| Remote UAS operator | Consumer of the extended link; drives relay requirements |
| Sustainment / logistics | Handles battery supply, spares, and unit replacement |
| Spectrum management authority | External; governs any radiating implementation |
| Research advisor / reviewer | Evaluates the concept and its assumptions |

## Standards Applicability

| Standard | Applicability |
|---|---|
| UAF 1.2 | Architecture framework; Strategic, Operational, Resources viewpoints |
| SysML 1.6 | Structural decomposition, applied informally in markdown |
| INCOSE SE Handbook v5 | Process reference for requirements and traceability practice |

> No MIL-STD, airworthiness, or safety-certification standard is invoked. This is an
> exploratory concept study with no assurance framework, no certification basis, and
> no safety integrity level. Any such claim would be unearned.

## Disclaimer

All content is derived from publicly available information and original analysis. No
export-controlled, classified, or proprietary content is included. The communications
payload is intentionally left unspecified. Nothing here constitutes a design suitable
for fabrication, and any physical implementation would require appropriate
engineering review, spectrum authorization, and regulatory compliance.

## License

TODO — MIT or CC-BY-4.0 recommended for an open concept study.
