# Architecture

Physical decomposition, functional allocation, and interfaces for the relay UAS
concept. IDs defined here are referenced by `requirements.md`, `uaf-views.md`, and
`traceability.md`.

## Architecture Overview

<!-- STUB: 1-2 paragraphs describing the decomposition rationale — why these six
     subsystems, and why the payload is isolated behind a single mount and power
     interface. -->

TODO

## Component Breakdown

Subsystem prefixes: `AFR` airframe · `PRP` propulsion · `PWR` power · `AVN` avionics
· `COM` communications payload · `MNT` payload mount.

### Airframe

| CMP ID | Component | Qty | Description | Trade Study |
|---|---|---|---|---|
| CMP-AFR-01 | Center frame plate | 1 | TODO | TS-001 |
| CMP-AFR-02 | Arm assembly | 4 | TODO | TS-001 |
| CMP-AFR-03 | Landing gear | 4 | TODO | — |
| CMP-AFR-04 | Payload mount interface | 1 | Standardized bolt pattern; see CMP-MNT-01 | TS-006 |
| CMP-AFR-05 | Fastener and hardware set | lot | Commodity COTS hardware | — |

### Propulsion

Four identical corner sets, `C1`–`C4`.

| CMP ID | Component | Qty | Description | Trade Study |
|---|---|---|---|---|
| CMP-PRP-01 | Brushless motor | 4 | Class and KV TBD | TS-002 |
| CMP-PRP-02 | Electronic speed controller | 4 | Current rating follows motor selection | TS-002 |
| CMP-PRP-03 | Propeller | 4 | Diameter/pitch TBD; CW/CCW alternating | TS-002 |

### Power

| CMP ID | Component | Qty | Description | Trade Study |
|---|---|---|---|---|
| CMP-PWR-01 | Battery pack | 1 | Chemistry, cell count, capacity TBD | TS-003 |
| CMP-PWR-02 | Power distribution board | 1 | COTS, with current sensing | — |
| CMP-PWR-03 | Step-down regulator(s) | TBD | Avionics and payload low-voltage rails | TS-004 |
| CMP-PWR-04 | Battery connector | 1 | Class follows current budget | — |

### Avionics

| CMP ID | Component | Qty | Description | Trade Study |
|---|---|---|---|---|
| CMP-AVN-01 | Flight controller | 1 | Open-source-firmware-capable COTS board | TS-005 |
| CMP-AVN-02 | IMU / sensor suite | 1 | Typically integrated on CMP-AVN-01 | — |
| CMP-AVN-03 | GNSS / compass module | 0–1 | Optional; depends on station-keeping approach | TS-007 |
| CMP-AVN-04 | Control link receiver | 1 | For the relay platform's *own* command link | TS-008 |

### Communications Payload — black box

> Modeled by function and interface only. No internal decomposition, no RF
> parameters. See [Scope Boundaries](README.md#scope-boundaries).

| CMP ID | Component | Qty | Description | Trade Study |
|---|---|---|---|---|
| CMP-COM-01 | Relay payload module | 1 | Black box. Accepts power and a mount; performs FUN-REL-01/02 | TS-009 |
| CMP-COM-02 | Antenna interface | TBD | Physical RF interface only; type/count deferred | TS-009 |

### Payload Mount

| CMP ID | Component | Qty | Description | Trade Study |
|---|---|---|---|---|
| CMP-MNT-01 | Modular payload bay | 1 | Mates to CMP-AFR-04; payload-agnostic | TS-006 |

## Function Allocation

| FUN ID | Function | Allocated To | Operational Activity |
|---|---|---|---|
| FUN-FLT-01 | Maintain stable flight | CMP-AVN-01, CMP-PRP-01..03 | OA-001 |
| FUN-FLT-02 | Navigate to station | CMP-AVN-01, CMP-AVN-03 | OA-002 |
| FUN-FLT-03 | Hold station | CMP-AVN-01 | OA-003 |
| FUN-FLT-04 | Return to launch | CMP-AVN-01 | OA-006 |
| FUN-REL-01 | Relay outbound traffic (ground → remote) | CMP-COM-01 | OA-004 |
| FUN-REL-02 | Relay return traffic (remote → ground) | CMP-COM-01 | OA-005 |
| FUN-PWR-01 | Distribute and regulate power | CMP-PWR-02, CMP-PWR-03 | — |
| FUN-PWR-02 | Report battery state | CMP-PWR-02, CMP-AVN-01 | OA-006 |
| FUN-CMD-01 | Receive platform command link | CMP-AVN-04 | OA-002, OA-006 |

## Interfaces

Internal interfaces (`IFC-INT-`) are within the system boundary; external
(`IFC-EXT-`) cross it.

| IFC ID | From | To | Data / Flow | Type |
|---|---|---|---|---|
| IFC-INT-001 | CMP-PWR-02 | CMP-PRP-02 (x4) | Main bus power | Electrical |
| IFC-INT-002 | CMP-PWR-03 | CMP-AVN-01 | Regulated power | Electrical |
| IFC-INT-003 | CMP-PWR-03 | CMP-COM-01 | Regulated payload power | Electrical |
| IFC-INT-004 | CMP-AVN-01 | CMP-PRP-02 (x4) | Motor commands | Signal |
| IFC-INT-005 | CMP-AVN-04 | CMP-AVN-01 | Platform control input | Signal |
| IFC-INT-006 | CMP-PWR-02 | CMP-AVN-01 | Battery telemetry | Signal |
| IFC-INT-007 | CMP-MNT-01 | CMP-COM-01 | Mechanical retention | Mechanical |
| IFC-EXT-001 | Ground control node | CMP-COM-01 | Relayed traffic (outbound) | RF — **undefined** |
| IFC-EXT-002 | CMP-COM-01 | Remote UAS node | Relayed traffic (outbound) | RF — **undefined** |
| IFC-EXT-003 | Remote UAS node | CMP-COM-01 | Relayed traffic (return) | RF — **undefined** |
| IFC-EXT-004 | CMP-COM-01 | Ground control node | Relayed traffic (return) | RF — **undefined** |
| IFC-EXT-005 | Platform operator | CMP-AVN-04 | Platform command and control | RF — **undefined** |

> **RF interfaces are intentionally left undefined.** `IFC-EXT-001` through
> `IFC-EXT-005` are declared as existing with a direction and a payload class only.
> Characterizing them (band, bandwidth, protocol, power) is TS-009 and is out of
> scope for this repository.

## Budgets

| Budget | Target | Allocated | Margin | Notes |
|---|---|---|---|---|
| Mass | TODO | TODO | TODO | Rolls up from component table |
| Unit cost | TODO | TODO | TODO | Rolls up from component table |
| Power | TODO | TODO | TODO | Drives CMP-PWR-01 sizing |
| Endurance | TODO | — | — | Derived; see REQ-PER-002 |

<!-- STUB: consider a small script that parses the component tables and computes
     these rollups so the budget cannot silently drift from the decomposition. -->
