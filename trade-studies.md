# Trade Studies

Open decisions this model does not resolve. Each `TS-` ID is referenced from
`architecture.md` where it gates a component selection.

The point of this file is to make the model's ignorance explicit. A `TODO` in a
component table is a gap; a `TS-` reference is a *known* gap with a defined shape.

## Status Legend

**Open** — not started · **Scoped** — criteria defined, not evaluated · **Resolved** — decision made and recorded · **Deferred** — out of scope for this project

## Register

| TS ID | Decision | Drives | Criteria | Status |
|---|---|---|---|---|
| TS-001 | Airframe material and construction method | CMP-AFR-01, CMP-AFR-02 | Cost, mass, manufacturability, damage tolerance | Open |
| TS-002 | Propulsion sizing (motor class, prop diameter/pitch, ESC rating) | CMP-PRP-01..03 | Thrust margin, efficiency at loiter, cost | Open |
| TS-003 | Battery chemistry, cell count, capacity | CMP-PWR-01 | Endurance vs. mass vs. cost; REQ-PER-002 | Open |
| TS-004 | Payload power rail voltage and current allocation | CMP-PWR-03 | Payload-agnostic support without overprovisioning | Open |
| TS-005 | Flight controller selection | CMP-AVN-01 | Open-source firmware support, cost, I/O | Open |
| TS-006 | Payload mount interface standard | CMP-MNT-01, CMP-AFR-04 | Modularity, mass, retention under vibration | Open |
| TS-007 | Station-keeping approach and GNSS dependence | CMP-AVN-03, FUN-FLT-03 | Position hold accuracy without assuming GNSS availability | Open |
| TS-008 | Platform command link approach | CMP-AVN-04, IFC-EXT-005 | Range, cost — **platform control only, not the relay payload** | Open |
| TS-009 | Relay payload characterization | CMP-COM-01, CMP-COM-02, all `IFC-EXT-001..004` | — | **Deferred — out of scope** |
| TS-010 | Environmental envelope | All | Temperature, wind, precipitation limits | Open |
| TS-011 | Recovery approach (recoverable vs. genuinely attritable) | CMP-AFR-03, FUN-FLT-04 | Cost of recovery features vs. unit replacement cost | Open |

## TS-009 — Note on Deferral

TS-009 covers frequency, waveform, protocol, modulation, transmit power, antenna type
and gain, and link budget. It is deferred rather than open because resolving it is
outside this project's scope by design, not merely unfinished.

Anyone picking this up should treat it as a separate effort requiring RF engineering
expertise, and — before any radiating hardware exists — spectrum authorization from
the relevant national authority. In a defense-affiliated context it would also
require export control review. See `REQ-DEF-001` through `REQ-DEF-005`.

The architecture is deliberately built so that TS-009 can be resolved independently:
`CMP-COM-01` touches the rest of the system through exactly two interfaces
(`IFC-INT-003` power, `IFC-INT-007` mechanical), so a payload decision does not
ripple into the platform design.

## Template

<!-- Copy this block when working a trade study. -->

```
### TS-XXX — <decision>

**Question.**
**Options.**
**Evaluation criteria.**
**Analysis.**
**Decision.**
**Consequences / affected IDs.**
```
