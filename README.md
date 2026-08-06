# Low-Cost Attritable Communications Relay UAS

> **Status: exploratory draft.** Independent concept study. Not affiliated with any
> program of record, and not a build specification. See [Scope Boundaries](#scope-boundaries).

> **Baseline Candidate - Not Approved.** The reconciled structured baseline is
> governed by [`system.yaml`](system.yaml), the catalogs under [`model/`](model/),
> and the source/proof records under [`.seal/`](.seal/). This candidate has not been
> approved by the project owner.

## Baseline Reconciliation

This repository distinguishes the recovered reference article (`CFG-REC`) from the
safe functional-replica (`CFG-REP`), domestic (`CFG-DOM`), future digital
(`CFG-DIG`), and complete system-of-systems (`CFG-SOS`) architecture candidates.
Existing prose is not approved truth merely because it predates the reconciliation.
Each structured claim records its evidence basis separately from its decision status.

The structured model uses two boundaries: the **Relay UAS** is the inner product
boundary, while the **C2 Ecosystem** is the outer system-of-systems context. External
vehicles, users, services, authorities, and infrastructure remain independently
managed unless a source establishes otherwise. See the generated
[`baseline-candidate.md`](reports/baseline-candidate.md) and
[`baseline-gaps.md`](reports/baseline-gaps.md) views. The generated diagram suite is
in [`architecture-views.md`](reports/architecture-views.md).

## Overview

A small rotary-wing platform whose sole mission is to carry a communications-relay
payload to altitude and hold station, extending the control and telemetry link
between a ground control node and a separate remote UAS operating beyond direct line
of sight.

The concept's organizing assumption is that the relay function deserves its own
airframe. The prevailing alternative is to treat relay as one mission among several
for a general-purpose small UAS — which works, but means every relay sortie ties up a
platform sized and priced for a harder job. A purpose-built relay node can shed
everything the relay mission does not need and spend the savings on unit cost. If the
platform is cheap enough, losing one stops being an incident and becomes a
consumable.

That inversion — optimizing for capability-per-dollar rather than
capability-per-airframe — is the hypothesis this model exists to structure. It is not
a demonstrated finding, and this repository does not claim to have validated it.

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
defined by its function and interfaces, not its implementation. In `CFG-REP` and
`CFG-DOM`, it crosses into the rest of the platform through exactly two interfaces -
`IFC-INT-003` (power) and `IFC-INT-007` (mechanical retention). `IFC-INT-010` is
wholly internal to the payload envelope and only records physical coupling to
`CMP-COM-02`, the antenna physical-resource envelope; it is not a third platform
interface and defines no RF characteristics. Moving toward
hardware would require RF engineering expertise, spectrum authorization, and, in a
defense-affiliated context, export control review. None of that is addressed here.

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
| `model/*.yaml` | Authoritative configuration, element, claim, scenario, interface, requirement, and relationship catalogs |
| `.seal/*.yaml` | Source-authority and proof records |
| `reports/*.md` | Generated baseline views; no independent architecture authority |
| `scripts/validate-baseline.py` | Standard-library structural validation and report generation |
| `scripts/generate-mermaid-views.py` | Deterministic generation and freshness checks for `reports/architecture-views.md` |

## Relay UAS Product Boundary (Inner)

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

The boundary is drawn so the relay payload sits *inside* it physically but *outside*
it analytically. The platform is specified to carry an unspecified payload within a
defined mass, power, and volume envelope. This is what allows the architecture to
proceed while TS-009 remains deferred.

This proposed inner-boundary decomposition applies to `CFG-REP`, `CFG-DOM`,
`CFG-DIG`, and the Relay-UAS constituent inside `CFG-SOS`. `CFG-REC` is a descriptive
evidence configuration and does not automatically inherit the proposed component,
interface, requirement, mode, control, or verification structure.

## C2 Ecosystem Context Boundary (Outer)

The outer boundary adds the operator, ground-control system, remote UAS, UGV, radio
users, network services, maintenance personnel, spectrum-management authority, and
supporting infrastructure as a proposed system-of-systems context. The existing
three-node operational concept remains the current candidate thread for `CFG-REP`
and `CFG-DOM`; it does not establish that the UGV, radio-user, or broader data-return
threads are supported. Those candidate threads and their explicit TBDs are maintained
in [`model/operational-scenarios.yaml`](model/operational-scenarios.yaml).

## Operational Environment

Notional employment is dismounted small-unit operation from unimproved sites: hand
launch, no support equipment, no prepared surface, no ground infrastructure beyond
what the unit already carries. The platform is transported by the same personnel who
employ it, which bounds mass and volume more tightly than any performance requirement
does.

The environmental envelope — temperature, wind, precipitation limits — is **not yet
specified**. Setting it is TS-010, and it matters more than it might appear: wind
tolerance during station keeping drives thrust margin, which drives propulsion sizing
and therefore much of the unit cost. A concept that holds station in calm air and
drifts in moderate wind is a different, and considerably cheaper, system than one that
does not.

No environmental qualification standard is invoked. This is a concept study, not a
qualification program.

## Operating Modes

Mode IDs are referenced by `requirements.md` and `hazard-analysis.md`.

| Mode ID | Name | Description | Active Functions | Constraints |
|---|---|---|---|---|
| MODE-001 | Transit | Climb and fly to station | FUN-FLT-01, FUN-FLT-02, FUN-CMD-01 | Payload may be inactive |
| MODE-002 | Station Keeping | Loiter at relay altitude, payload active | FUN-FLT-01, FUN-FLT-03, FUN-REL-01, FUN-REL-02 | Primary mission mode |
| MODE-003 | Relay Degraded | Payload function lost or partial; platform airborne and controllable | FUN-FLT-01, FUN-FLT-03, FUN-CMD-01 | Entered on loss of payload power or operator declaration; exit is to MODE-004 |
| MODE-004 | Return / Recovery | Return to launch on low battery or command | FUN-FLT-01, FUN-FLT-04, FUN-PWR-02 | Relay function ends on entry |
| MODE-005 | Ground Safe | Powered on ground; payload and motors inhibited | FUN-PWR-01 | Motor arming inhibited (REQ-FUN-006) |

MODE-003 exists because the platform outliving its payload is the expected partial
failure, not an edge case. A relay that has lost its payload is still an aircraft with
stored energy in the air, and the mode makes explicit that it must still be flown home
rather than treated as expendable the moment it stops being useful.

## Key Technical Challenges

1. **Endurance versus unit cost.** These are coupled through a loop that does not close
   easily on a cheap airframe. Rotary-wing hover is power-hungry, so endurance comes
   from battery mass; but added battery mass raises hover power, so returns diminish
   and eventually reverse. Structural efficiency is what buys margin in that loop, and
   structural efficiency is exactly what an inexpensive airframe gives up. The concept
   therefore has a real possibility of failing on its own terms — of needing enough
   battery and structure to hold useful station time that it prices itself out of
   attritability. Establishing where that curve sits is the most load-bearing open
   question in the model (TS-001, TS-002, TS-003).

2. **Station keeping without assuming GNSS.** The environments that motivate an
   airborne relay are the same environments where satellite navigation is least
   dependable, so a design that silently assumes GNSS has assumed away part of its own
   justification. The mitigating observation is that relay geometry is far more
   tolerant than precision hover: a relay node needs to stay roughly where it was put,
   not hold a survey point. If the acceptable drift box is tens of metres rather than
   metres, the sensing burden drops substantially. Quantifying that tolerance requires
   the link characterisation this project defers (TS-009), so TS-007 has to be framed
   as a range of approaches rather than a single decision.

3. **Payload mass fraction on a deliberately cheap airframe.** Treating the payload as
   a black box is analytically clean but pushes a real problem into the mass budget:
   the platform must be sized for a payload *envelope* rather than a payload. Size the
   envelope generously and the airframe grows to carry mass that may never be
   installed; size it tightly and the architecture stops being payload-agnostic, which
   was the point. This is the clearest cost of the black-box decision, and it is worth
   stating plainly rather than absorbing quietly (TS-004, TS-006).

4. **Attritability versus recoverability.** Below some unit cost, features that exist
   to recover the platform cost more than the platform. Robust landing gear,
   return-to-launch, and the navigation needed to support it are all recovery
   features. The complication is that cost is not uniformly distributed: the battery is
   typically the most expensive reusable component, so "attritable airframe,
   recoverable battery" may be the coherent position rather than treating the whole
   aircraft as consumable. TS-011 should resolve this, and it will move REQ-FUN-005 in
   one direction or the other.

5. **Keeping the payload interface genuinely generic.** The black-box treatment only
   holds if `IFC-INT-003` and `IFC-INT-007` are specified without reference to what is
   on the other side. The failure mode is subtle: a power rail sized for one
   anticipated payload, or a mount whose bolt pattern reflects one anticipated form
   factor, produces an architecture that claims a modularity it does not have.
   Guarding against this means specifying an envelope and accepting the
   overprovisioning that comes with it (TS-004, TS-006).

## Stakeholders

| Stakeholder | Role |
|---|---|
| Small-unit operator | Employs, launches, and recovers the relay platform |
| Remote UAS operator | Consumer of the extended link; their tolerance for link loss drives relay requirements |
| Sustainment / logistics | Battery supply, spares, unit replacement; bears the consequence of attritability |
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

OMG lists UAF 1.3 (April 2026) as the current formal version. This repository retains
its existing UAF 1.2 terminology pending owner review of `DEC-002` and
`GAP-STD-001`. It does not claim conformance to UAF 1.2 or UAF 1.3; the open decision
is whether to intentionally retain 1.2 terminology, use version-neutral concepts, or
plan a later migration.

## Disclaimer

All content is derived from publicly available information and original analysis. No
export-controlled, classified, or proprietary content is included. The communications
payload is intentionally left unspecified. Nothing here constitutes a design suitable
for fabrication, and any physical implementation would require appropriate engineering
review, spectrum authorization, and regulatory compliance.

## License

[CC BY 4.0](LICENSE) — Creative Commons Attribution 4.0 International. Chosen
over MIT because the repository's content is primarily analysis and
documentation (a concept study), not software; attribution licensing fits
that better than a permissive software license. The one script in this
repo (`scripts/check-ids.py`) is covered by the same terms.
