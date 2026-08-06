# Requirements

Requirement IDs are referenced by `architecture.md`, `uaf-views.md`, and
`traceability.md`. Every requirement must trace upward to a capability and downward
to at least one component or explicitly deferred trade study.

> **Structured classification.** [`model/requirements.yaml`](model/requirements.yaml)
> preserves every existing requirement ID and text while adding configuration
> applicability, evidence basis, decision status, upstream rationale, allocation,
> verification, and TBD ownership. It is the authoritative structured requirement
> catalog for the baseline candidate. The requirements remain proposed unless an
> explicit decision record states otherwise.

## Conventions

- **Shall** statements only. One requirement per row.
- Verification methods: **A** analysis · **I** inspection · **D** demonstration · **T** test
- Requirements that cannot be verified without hardware are marked `Deferred` —
  expected, given this repository's scope.
- Bracketed `[TBD]` values are intentional and load-bearing. They mark quantities that
  a trade study must produce. Filling them with figures borrowed from comparable
  systems would create the appearance of derived requirements where none exist.

## Functional Requirements

| REQ ID | Requirement | Rationale | Traces To (CAP) | Allocated To (CMP/FUN) | Verify |
|---|---|---|---|---|---|
| REQ-FUN-001 | The system shall relay outbound traffic from a ground control node toward a remote UAS node. | Core relay function; half of the mission | CAP-001 | FUN-REL-01 / CMP-COM-01 | A |
| REQ-FUN-002 | The system shall relay return traffic from a remote UAS node toward a ground control node. | Control without telemetry return is not a usable link | CAP-001 | FUN-REL-02 / CMP-COM-01 | A |
| REQ-FUN-003 | The system shall maintain a commanded station position within [TBD] horizontal and [TBD] vertical tolerance. | Relay value is positional; drift degrades the geometry the node was placed to create | CAP-002 | FUN-FLT-03 / CMP-AVN-01 | A `Deferred` |
| REQ-FUN-004 | The system shall accept operator command input for transit, repositioning, and recovery. | The platform must be controllable independently of the payload it carries | — | FUN-CMD-01 / CMP-AVN-04 | A |
| REQ-FUN-005 | The system shall initiate return-to-launch on reaching a defined low-battery state. | Recovery of the reusable portion of the aircraft | CAP-004 | FUN-FLT-04, FUN-PWR-02 | D `Deferred` |
| REQ-FUN-006 | The system shall inhibit motor arming while in MODE-005 (Ground Safe). | Propeller contact is the dominant ground-handling injury path | — | FUN-PWR-01 / CMP-AVN-01 | D |
| REQ-FUN-007 | The system shall remain controllable and recoverable following loss of payload function (MODE-003). | An aircraft that has lost its payload is still an aircraft with stored energy aloft | CAP-004 | FUN-FLT-01, FUN-FLT-04 | D `Deferred` |

## Performance Requirements

| REQ ID | Requirement | Rationale | Traces To (CAP) | Allocated To | Verify |
|---|---|---|---|---|---|
| REQ-PER-001 | System unit cost shall not exceed [TBD]. | Attritability is a cost property before it is anything else | CAP-004 | All | A |
| REQ-PER-002 | The system shall provide at least [TBD] minutes of on-station endurance. | Below some dwell time the sortie costs more to fly than the link is worth | CAP-001 | CMP-PWR-01 | A `Deferred` |
| REQ-PER-003 | System gross mass shall not exceed [TBD]. | Bounds regulatory class and single-operator handling | CAP-004 | All | I |
| REQ-PER-004 | The payload bay shall accommodate a payload of up to [TBD] mass within a [TBD] volume envelope. | The platform is sized for an envelope, not a payload — see TS-006 | — | CMP-MNT-01 | I |
| REQ-PER-005 | The system shall be transportable and launched by a single operator without support equipment. | Dismounted employment; bounds mass and volume more tightly than performance does | CAP-004 | All | D `Deferred` |

## Interface Requirements

| REQ ID | Requirement | Rationale | Traces To | Allocated To | Verify |
|---|---|---|---|---|---|
| REQ-IFC-001 | The payload mount shall provide a standardized mechanical interface independent of payload type. | Modularity is the reason the black-box decomposition holds | CAP-004 | CMP-MNT-01 / IFC-INT-007 | I |
| REQ-IFC-002 | The power subsystem shall provide a regulated payload rail meeting a defined voltage and current envelope. | Payload-agnostic power; envelope rather than point value | — | CMP-PWR-03 / IFC-INT-003 | T `Deferred` |
| REQ-IFC-003 | The platform-to-payload interface shall be limited to power (IFC-INT-003) and mechanical retention (IFC-INT-007). | Constrains future platform coupling; payload-internal IFC-INT-010 is not a third platform interface | — | CMP-COM-01 | I |
| REQ-IFC-004 | The payload mount shall retain the payload under all flight loads with [TBD] margin. | In-flight separation is a falling-object hazard, not merely a mission loss | — | CMP-MNT-01 / IFC-INT-007 | T `Deferred` |

**Reconciliation note (2026-08-06):** `REQ-IFC-003` changed only from "payload
interface" to "platform-to-payload interface" so `IFC-INT-010`, which remains inside
the black-box payload envelope, cannot be misread as a third platform interface. The
requirement intent and ID are unchanged.

## Safety Requirements

> These mitigate identified hazards. They are ordinary engineering requirements, not
> evidence of a safety case — no safety standard is invoked and no risk acceptance
> authority exists for this project. See `hazard-analysis.md`.

| REQ ID | Requirement | Rationale | Mitigates | Allocated To | Verify |
|---|---|---|---|---|---|
| REQ-SAF-001 | The battery installation shall provide over-current protection and physical retention of the pack. | Battery thermal events are the most severe credible ground and flight hazard | HAZ-003 | CMP-PWR-01, CMP-PWR-02 | I `Deferred` |
| REQ-SAF-002 | The system shall provide an operator-visible indication of armed state. | Arming ambiguity is the precondition for propeller contact injury | HAZ-004 | CMP-AVN-01 | D |

## Design Constraints

| REQ ID | Requirement | Rationale | Traces To | Allocated To | Verify |
|---|---|---|---|---|---|
| REQ-CON-001 | The design shall use commercially available components in preference to custom-fabricated parts. | Cost and sustainment; custom parts carry tooling and lead time a cheap platform cannot absorb | CAP-004 | All | I |
| REQ-CON-002 | The flight controller shall run widely supported open-source firmware. | Cost, maintainability, no vendor lock | CAP-004 | CMP-AVN-01 | I |
| REQ-CON-003 | The system shall not integrate weapons or munitions of any kind. | Project scope constraint | — | All | I |
| REQ-CON-004 | The station-keeping design shall not assume continuous GNSS availability as a precondition. | The environments motivating an airborne relay are those where GNSS is least dependable | CAP-002 | CMP-AVN-03, FUN-FLT-03 | A |

`REQ-CON-003` is a proposed-design constraint and research-project scope control. It
does not apply retroactively to `CFG-REC` and is not a recovered-article observation.

## Deferred — Out of Scope

Recorded so the model is honest about what it does not resolve. These are not
requirements this repository attempts to satisfy.

`REQ-DEF-001` and `REQ-DEF-002` apply to proposed architecture configurations, not
`CFG-REC`. Unknown recovered payload and antenna characteristics remain evidence
claims and gaps (`CLM-REC-003`, `CLM-REC-004`, `GAP-REC-001`).

| REQ ID | Item | Disposition |
|---|---|---|
| REQ-DEF-001 | RF frequency, waveform, protocol, and link budget | Deferred to TS-009; requires RF engineering expertise |
| REQ-DEF-002 | Antenna type, gain, and pattern | Deferred to TS-009 |
| REQ-DEF-003 | Spectrum authorization for any radiating implementation | External; regulatory authority, not a design decision |
| REQ-DEF-004 | Contested-spectrum resilience mechanisms | Deferred; CAP-003 is stated qualitatively and remains unallocated |
| REQ-DEF-005 | Export control review of any resulting design | External; institutional compliance process |

## Requirement Health

| Check | Status |
|---|---|
| Every REQ traces to a CAP or is explicitly marked `—` | Pass |
| Every referenced CMP/FUN exists in `architecture.md` | Pass — verified by ID check |
| Every CAP has at least one REQ | **Fail — CAP-003 has none** (see note) |
| No duplicate REQ IDs | Pass |
| Every `[TBD]` has an owning trade study | Partial — REQ-FUN-003 tolerance depends on TS-009 |

**CAP-003 note.** The capability has no allocated requirement because every mechanism
that would satisfy it lives inside the deferred payload. This is a genuine coverage
gap, left visible rather than closed with a requirement the architecture cannot
support. See `traceability.md` coverage gaps.
