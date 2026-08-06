# Architecture

Physical decomposition, functional allocation, and interfaces for the relay UAS
concept. IDs defined here are referenced by `requirements.md`, `uaf-views.md`, and
`traceability.md`.

> **Baseline authority.** This file is a human-readable architecture view. The
> configuration-aware element and interface records in
> [`model/elements.yaml`](model/elements.yaml) and
> [`model/interfaces.yaml`](model/interfaces.yaml) are the authoritative structured
> data for the baseline candidate. The decomposition below maps provisionally to
> `CFG-REP` and `CFG-DOM`; it is not asserted to be the as-built `CFG-REC` article.
> The Relay UAS is the inner product boundary; the broader C2 Ecosystem remains an
> outer, proposed system-of-systems context.
> Generated configuration, context, resource, sequence, hazard, and governance
> diagrams are maintained in
> [`reports/architecture-views.md`](reports/architecture-views.md).

## Architecture Overview

The decomposition is a conventional quadrotor split into five platform subsystems
(airframe, propulsion, power, avionics, payload mount) plus the relay payload. The
arrangement is unremarkable by design: novelty in the platform would cost money the
concept does not have, and the interesting decisions here are about cost allocation
and interface discipline rather than configuration.

Two choices shape everything downstream.

**The payload is isolated behind two platform interfaces.** `CMP-COM-01` connects to
the rest of the platform through `IFC-INT-003` (regulated power) and `IFC-INT-007`
(mechanical retention), and nothing else in `CFG-REP`/`CFG-DOM`. No platform data
path or payload-control signal is defined in those configurations.
This is what lets the platform architecture proceed while TS-009 stays deferred — and
it also means a payload change is a mount-and-rail question rather than a redesign.
The cost is that the platform must be sized for a payload envelope rather than a
known payload, which pushes uncertainty into the mass and power budgets.

**The platform command link is separate from the relay function.** `CMP-AVN-04`
receives commands for *this aircraft*; `CMP-COM-01` relays traffic for a *different*
aircraft. They are unrelated systems that happen to share an airframe. Conflating them
is the most likely modeling error here, so they carry separate IDs, separate
interfaces (`IFC-EXT-005` versus `IFC-EXT-001..004`), and separate trade studies
(TS-008 versus TS-009).

Four-corner propulsion sets are treated as identical by design. Unlike a
reverse-engineered article, there is no reason for asymmetry, so `C1`–`C4` differ only
in propeller rotation direction.

## Component Breakdown

Subsystem prefixes: `AFR` airframe · `PRP` propulsion · `PWR` power · `AVN` avionics
· `COM` communications payload · `MNT` payload mount.

### Airframe

| CMP ID | Component | Qty | Description | Trade Study |
|---|---|---|---|---|
| CMP-AFR-01 | Center frame plate | 1 | Primary structure; carries arm loads into the payload mount and battery cradle | TS-001 |
| CMP-AFR-02 | Arm assembly | 4 | Motor standoff structure; length sets propeller clearance and therefore diameter limit | TS-001 |
| CMP-AFR-03 | Landing gear | 4 | Ground contact and payload ground clearance; robustness is a recovery feature, see TS-011 | TS-011 |
| CMP-AFR-04 | Payload mount interface | 1 | Structural half of the payload attachment; mates CMP-MNT-01 | TS-006 |
| CMP-AFR-05 | Fastener and hardware set | lot | Commodity COTS hardware; no unique parts intended | — |

### Propulsion

Four identical corner sets, `C1`–`C4`, differing only in propeller rotation direction.

| CMP ID | Component | Qty | Description | Trade Study |
|---|---|---|---|---|
| CMP-PRP-01 | Brushless motor | 4 | Class and KV follow from all-up mass and propeller selection | TS-002 |
| CMP-PRP-02 | Electronic speed controller | 4 | Current rating follows motor selection; sized for hover draw plus thrust margin | TS-002 |
| CMP-PRP-03 | Propeller | 4 | Diameter and pitch bounded by CMP-AFR-02 arm length; CW/CCW alternating | TS-002 |

Propulsion sizing is where the endurance-versus-cost loop is actually resolved. Larger
propellers hover more efficiently but demand longer arms and more structure; the
optimum depends on the mass budget, which depends on the battery, which depends on the
endurance requirement. TS-002 and TS-003 must be worked together rather than in
sequence.

### Power

| CMP ID | Component | Qty | Description | Trade Study |
|---|---|---|---|---|
| CMP-PWR-01 | Battery pack | 1 | Chemistry, cell count, capacity TBD; likely the highest-value single reusable component | TS-003 |
| CMP-PWR-02 | Power distribution board | 1 | Main bus distribution to four ESCs; current sensing supports FUN-PWR-02 | — |
| CMP-PWR-03 | Step-down regulator(s) | TBD | Separate rails for avionics and payload; count depends on whether rails are shared | TS-004 |
| CMP-PWR-04 | Battery connector | 1 | Class follows peak current; also the field-replaceable interface for battery reuse | TS-011 |

### Avionics

| CMP ID | Component | Qty | Description | Trade Study |
|---|---|---|---|---|
| CMP-AVN-01 | Flight controller | 1 | COTS board capable of running widely supported open-source firmware | TS-005 |
| CMP-AVN-02 | IMU / sensor suite | 1 | Attitude and barometric altitude; typically integrated on CMP-AVN-01 | — |
| CMP-AVN-03 | GNSS / compass module | 0–1 | Optional. Presence depends on the station-keeping approach selected in TS-007 | TS-007 |
| CMP-AVN-04 | Control link receiver | 1 | Command link for **this platform only** — not the relay payload | TS-008 |

`CMP-AVN-03` is deliberately `0–1`. Whether the platform carries GNSS at all is an
open architectural question, not a detail: a design that requires it inherits a
dependency the concept's own justification argues against (see README challenge 2).

### Communications Payload — black box

> Modeled by function and interface only. No internal decomposition, no RF
> parameters. See [Scope Boundaries](README.md#scope-boundaries).

| CMP ID | Component | Qty | Description | Trade Study |
|---|---|---|---|---|
| CMP-COM-01 | Relay payload module | 1 | Black box. Accepts regulated power and mechanical retention; performs FUN-REL-01 and FUN-REL-02 | TS-009 |
| CMP-COM-02 | Antenna physical-resource envelope | TBD | Black-box physical-resource envelope; count, type, placement, and all characteristics remain undefined | TS-009 |

`CMP-COM-02` is a resource, not an interface. `IFC-INT-010` represents only the
existence of physical coupling between that resource envelope and `CMP-COM-01`, wholly
inside the relay-payload black-box envelope. It does not expose another
platform-to-payload interface and defines no count, type, connector, location, role,
or RF characteristic.

### Payload Mount

| CMP ID | Component | Qty | Description | Trade Study |
|---|---|---|---|---|
| CMP-MNT-01 | Modular payload bay | 1 | Mates to CMP-AFR-04; payload-agnostic retention and volume envelope | TS-006 |

## Function Allocation

| FUN ID | Function | Allocated To | Operational Activity |
|---|---|---|---|
| FUN-FLT-01 | Maintain stable flight | CMP-AVN-01, CMP-AVN-02, CMP-PRP-01..03 | OA-001 |
| FUN-FLT-02 | Navigate to station | CMP-AVN-01, CMP-AVN-03 | OA-002 |
| FUN-FLT-03 | Hold station | CMP-AVN-01, CMP-AVN-02, CMP-AVN-03 | OA-003 |
| FUN-FLT-04 | Return to launch | CMP-AVN-01 | OA-006 |
| FUN-REL-01 | Relay outbound traffic (ground → remote) | CMP-COM-01 | OA-004 |
| FUN-REL-02 | Relay return traffic (remote → ground) | CMP-COM-01 | OA-005 |
| FUN-PWR-01 | Distribute and regulate power | CMP-PWR-02, CMP-PWR-03 | — |
| FUN-PWR-02 | Report battery state | CMP-PWR-02, CMP-AVN-01 | OA-006 |
| FUN-CMD-01 | Receive platform command link | CMP-AVN-04 | OA-002, OA-006 |

`FUN-PWR-01` has no operational activity because power distribution is an enabling
function rather than a mission activity — it supports every activity without being one.
Recorded explicitly rather than left blank, so the gap is visibly intentional.

## Interfaces

The tables below are configuration-specific views of the authoritative interface
catalog. `proposed` and `candidate` are maturity labels, not approval. `VER-008` is a
deferred physical method, not executed evidence.

### Current candidate platform interfaces - CFG-REP / CFG-DOM

| IFC ID | Endpoints | Direction | Flow class | Maturity | Verification | Unknown attributes |
|---|---|---|---|---|---|---|
| IFC-INT-001 | CMP-PWR-02 to CMP-PRP-02 | A to B | electrical power | proposed design / proposed | VER-005; VER-008 deferred | voltage; current; connector; protection; wiring allocation |
| IFC-INT-002 | CMP-PWR-03 to CMP-AVN-01 | A to B | electrical power | proposed design / proposed | VER-005; VER-008 deferred | voltage; current; connector; power-quality envelope |
| IFC-INT-003 | CMP-PWR-03 to CMP-COM-01 | A to B | electrical power; platform-to-payload crossing | proposed design / proposed | VER-005; VER-008 deferred | voltage/current envelopes; connector; protection; thermal allocation |
| IFC-INT-004 | CMP-AVN-01 to CMP-PRP-02 | A to B | command and control | proposed design / proposed | VER-005; VER-008 deferred | signal format; timing; connector; fault response |
| IFC-INT-005 | CMP-AVN-04 to CMP-AVN-01 | A to B | command and control | proposed design / proposed | VER-005; VER-008 deferred | protocol; connector; timing; failsafe behavior |
| IFC-INT-006 | CMP-PWR-02 to CMP-AVN-01 | A to B | health and status | proposed design / proposed | VER-005; VER-008 deferred | measurement set; accuracy; update rate; connector; fault indication |
| IFC-INT-007 | CMP-MNT-01 to CMP-COM-01 | bidirectional physical | mechanical mounting; platform-to-payload crossing | proposed design / proposed | VER-005; VER-008 deferred | geometry; load envelope; retention margin; inspection criteria |
| IFC-INT-009 | CMP-AVN-02 to CMP-AVN-01 | A to B | navigation and timing | engineering inference / proposed | VER-005; VER-008 deferred | sensor set; data format; timing; accuracy; fault detection; connector |

### Relay-payload black-box internal interface - CFG-REP / CFG-DOM

| IFC ID | Endpoints | Direction | Flow class | Maturity | Verification | Unknown attributes |
|---|---|---|---|---|---|---|
| IFC-INT-010 | CMP-COM-01 to CMP-COM-02 | bidirectional physical | physical-resource coupling inside payload envelope | proposed design / proposed | none allocated - GAP-IFC-001 | count; type; role; placement; connector; all RF characteristics |

`IFC-INT-010` is not a platform boundary crossing. The only
platform-to-payload interfaces in `CFG-REP` and `CFG-DOM` are `IFC-INT-003` and
`IFC-INT-007`.

### Future digital interface - CFG-DIG / CFG-SOS only

| IFC ID | Endpoints | Direction | Flow class | Maturity | Verification | Unknown attributes |
|---|---|---|---|---|---|---|
| IFC-INT-008 | CMP-AVN-01 to CMP-COM-01 | bidirectional | payload management and health/status | proposed design / proposed future interface | VER-004; VER-005; VER-007 candidate | adoption decision; data model; protocol; connector; timing; authority; failure response |

`IFC-INT-008` is omitted from current `CFG-REP`/`CFG-DOM` resource views because it
would violate their two-interface platform-to-payload boundary. Its presence in a
future view does not approve it.

### Current external traffic and platform command - CFG-REP / CFG-DOM

| IFC ID | Endpoints | Direction | Flow class | Maturity | Verification | Unknown attributes |
|---|---|---|---|---|---|---|
| IFC-EXT-001 | OP-001 to CMP-COM-01 | A to B | command and control | proposed design / proposed; intentionally undefined path | none allocated - GAP-IFC-001 | frequency; waveform; protocol; power; data rate; message format; compatibility; authority |
| IFC-EXT-002 | CMP-COM-01 to OP-003 | A to B | command and control | proposed design / proposed; intentionally undefined path | none allocated - GAP-IFC-001 | frequency; waveform; protocol; power; data rate; message format; compatibility; authority |
| IFC-EXT-003 | OP-003 to CMP-COM-01 | A to B | telemetry | proposed design / proposed; intentionally undefined path | none allocated - GAP-IFC-001 | frequency; waveform; protocol; power; data rate; message format; compatibility; authority |
| IFC-EXT-004 | CMP-COM-01 to OP-001 | A to B | telemetry | proposed design / proposed; intentionally undefined path | none allocated - GAP-IFC-001 | frequency; waveform; protocol; power; data rate; message format; compatibility; authority |
| IFC-EXT-005 | OP-010 to CMP-AVN-04 | A to B | command and control; separate platform command | proposed design / proposed; intentionally undefined path | none allocated - GAP-IFC-001 | frequency; waveform; protocol; power; message format; failsafe behavior; authority |

External implementation attributes remain intentionally undefined. `IFC-EXT-005`
is independent of `IFC-EXT-001` through `IFC-EXT-004`; it controls the relay
platform rather than carrying relayed mission traffic.

### Support and governance - CFG-REP / CFG-DOM / CFG-DIG / CFG-SOS

| IFC ID | Endpoints | Direction | Flow class | Maturity | Verification | Unknown attributes |
|---|---|---|---|---|---|---|
| IFC-EXT-006 | OP-007 to OP-002 | bidirectional | configuration and maintenance | proposed design / proposed support interface | VER-004; VER-005; VER-007 candidate | data set; format; transport; authorization; retention period; tool ownership |

`IFC-EXT-006` is a support/governance interface, not a mission-traffic interface.
The generated resource diagrams show why it is omitted from the airborne relay
traffic view.

## Budgets

| Budget | Target | Allocated | Margin | Notes |
|---|---|---|---|---|
| Mass | [TBD] — bounded below by dry mass (airframe + propulsion hardware + avionics + payload mount + payload envelope; TS-001/TS-006), bounded above by battery mass, which is coupled to REQ-PER-002 and TS-002's hover efficiency, not independently settable | [TBD] | [TBD] | Coupled loop, not yet closed — see TS-002/TS-003 for the iteration and finding. Payload entry is an envelope, not a value |
| Unit cost | [TBD] | [TBD] | [TBD] | CMP-PWR-01 (battery) is the dominant, least cost-elastic driver — see TS-002/TS-003 finding. Coupled to the same endurance target as Mass, not an independent number |
| Power | [TBD] | [TBD] | [TBD] | Hover draw dominates; set jointly by AUW (see Mass row) and TS-002's disk-loading choice. Payload allocation is an envelope per TS-004 |
| Endurance | [TBD] | — | — | Derived, not allocated. See REQ-PER-002. TS-002/TS-003 finding: no candidate value is risk-free — a short-dwell target plausibly converges to a small, cheap design of marginal operational utility; a mission-useful-dwell target risks pricing the platform out of CAP-004. Not resolved here |

Budgets are deliberately empty, and as of TS-002/TS-003 that emptiness is no longer
just "blocked on more component data." Working the propulsion/battery loop showed the
three quantities above are not independent `[TBD]`s that TS-001 through TS-003 will
fill in one at a time — they are three views of a single unresolved coupling, and the
iteration (see `trade-studies.md`) suggests the loop does not obviously close
favorably at every candidate endurance target. Filling these cells with plausible
figures now would make the model appear more resolved than it is, and in this case
would also paper over a real, load-bearing open question rather than an ordinary gap
in component data. Endurance is marked *derived* because it is an output of the mass
and power budgets rather than an independent allocation — writing a number there
before the others are closed would invert the dependency.

<!-- When TS-001..003 close: consider a script that parses the component tables and
     computes these rollups, so the budget cannot silently drift from the
     decomposition. Candidate CI check alongside scripts/check-ids.py. -->
