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

## Architecture Overview

The decomposition is a conventional quadrotor split into five platform subsystems
(airframe, propulsion, power, avionics, payload mount) plus the relay payload. The
arrangement is unremarkable by design: novelty in the platform would cost money the
concept does not have, and the interesting decisions here are about cost allocation
and interface discipline rather than configuration.

Two choices shape everything downstream.

**The payload is isolated behind two interfaces.** `CMP-COM-01` connects to the rest
of the system through `IFC-INT-003` (regulated power) and `IFC-INT-007` (mechanical
retention), and nothing else. No data path, no control signal, no shared structure.
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
| CMP-COM-02 | Antenna interface | TBD | Physical RF interface only. Type, count, and placement deferred | TS-009 |

`CMP-COM-02` is listed separately from `CMP-COM-01` because antenna *placement* is a
platform concern even when antenna *design* is not — mounting location, clearance from
structure, and mass distribution affect the airframe regardless of what the antenna
turns out to be. The platform can reserve volume and mass for it without characterising it.

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

Internal interfaces (`IFC-INT-`) are within the system boundary; external
(`IFC-EXT-`) cross it.

| IFC ID | From | To | Data / Flow | Type |
|---|---|---|---|---|
| IFC-INT-001 | CMP-PWR-02 | CMP-PRP-02 (x4) | Main bus power | Electrical |
| IFC-INT-002 | CMP-PWR-03 | CMP-AVN-01 | Regulated avionics power | Electrical |
| IFC-INT-003 | CMP-PWR-03 | CMP-COM-01 | Regulated payload power | Electrical |
| IFC-INT-004 | CMP-AVN-01 | CMP-PRP-02 (x4) | Motor commands | Signal |
| IFC-INT-005 | CMP-AVN-04 | CMP-AVN-01 | Platform control input | Signal |
| IFC-INT-006 | CMP-PWR-02 | CMP-AVN-01 | Battery state telemetry | Signal |
| IFC-INT-007 | CMP-MNT-01 | CMP-COM-01 | Mechanical retention | Mechanical |
| IFC-EXT-001 | Ground control node | CMP-COM-01 | Relayed traffic (outbound) | RF — **undefined** |
| IFC-EXT-002 | CMP-COM-01 | Remote UAS node | Relayed traffic (outbound) | RF — **undefined** |
| IFC-EXT-003 | Remote UAS node | CMP-COM-01 | Relayed traffic (return) | RF — **undefined** |
| IFC-EXT-004 | CMP-COM-01 | Ground control node | Relayed traffic (return) | RF — **undefined** |
| IFC-EXT-005 | Platform operator | CMP-AVN-04 | Platform command and control | RF — **undefined** |

> **RF interfaces are intentionally left undefined.** `IFC-EXT-001` through
> `IFC-EXT-004` are declared as existing with a direction and traffic class only;
> characterising them is TS-009 and is out of scope for this repository. `IFC-EXT-005`
> is a different question — the platform's own command link is a conventional sUAS
> control problem (TS-008), not a relay-payload problem, and is undefined here only
> because the trade study has not been worked.

`IFC-INT-003` and `IFC-INT-007` are the entire payload coupling. Any proposal that
adds a third payload interface — a data line, a control signal, shared cooling —
should be treated as a change to the architecture's central assumption, not a detail.

## Budgets

| Budget | Target | Allocated | Margin | Notes |
|---|---|---|---|---|
| Mass | [TBD] | [TBD] | [TBD] | Blocked on TS-001, TS-002, TS-003; payload entry is an envelope, not a value |
| Unit cost | [TBD] | [TBD] | [TBD] | Blocked on the same three; CMP-PWR-01 expected to dominate reusable cost |
| Power | [TBD] | [TBD] | [TBD] | Hover draw dominates; payload allocation is an envelope per TS-004 |
| Endurance | [TBD] | — | — | Derived, not allocated. See REQ-PER-002 |

Budgets are deliberately empty. Populating them requires TS-001 through TS-003, and
filling them with plausible figures beforehand would make the model appear more
resolved than it is. Endurance is marked *derived* because it is an output of the mass
and power budgets rather than an independent allocation — writing a number there
before the others are closed would invert the dependency.

<!-- When TS-001..003 close: consider a script that parses the component tables and
     computes these rollups, so the budget cannot silently drift from the
     decomposition. Candidate CI check alongside scripts/check-ids.py. -->
