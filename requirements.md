# Requirements

Requirement IDs are referenced by `architecture.md`, `uaf-views.md`, and
`traceability.md`. Every requirement must trace upward to a capability and downward
to at least one component or explicitly deferred trade study.

## Conventions

- **Shall** statements only. One requirement per row.
- Verification methods: **A** analysis · **I** inspection · **D** demonstration · **T** test
- Requirements that cannot be verified without hardware are marked `Deferred` —
  expected, given this repository's scope.

## Functional Requirements

| REQ ID | Requirement | Rationale | Traces To (CAP) | Allocated To (CMP/FUN) | Verify |
|---|---|---|---|---|---|
| REQ-FUN-001 | The system shall relay outbound traffic from a ground control node toward a remote UAS node. | Core relay function | CAP-001 | FUN-REL-01 | A |
| REQ-FUN-002 | The system shall relay return traffic from a remote UAS node toward a ground control node. | Bidirectional link | CAP-001 | FUN-REL-02 | A |
| REQ-FUN-003 | The system shall maintain a commanded station position. | Relay geometry must be stable | CAP-002 | FUN-FLT-03 | A |
| REQ-FUN-004 | The system shall accept command input for transit and recovery. | Platform must be controllable | — | FUN-CMD-01 | A |
| REQ-FUN-005 | The system shall initiate return-to-launch on low battery state. | Recovery of a reusable airframe | CAP-004 | FUN-FLT-04, FUN-PWR-02 | D `Deferred` |
| REQ-FUN-006 | TODO | TODO | TODO | TODO | TODO |

## Performance Requirements

| REQ ID | Requirement | Rationale | Traces To (CAP) | Allocated To | Verify |
|---|---|---|---|---|---|
| REQ-PER-001 | The system unit cost shall not exceed [TBD]. | Attritability depends on cost | CAP-004 | All | A |
| REQ-PER-002 | The system shall provide at least [TBD] minutes of on-station endurance. | Mission utility floor | CAP-001 | CMP-PWR-01 | A `Deferred` |
| REQ-PER-003 | System gross mass shall not exceed [TBD]. | Group 1 sUAS classification | CAP-004 | All | I |
| REQ-PER-004 | The payload bay shall accommodate a payload of at least [TBD] mass. | Payload-agnostic design | — | CMP-MNT-01 | I |
| REQ-PER-005 | TODO | TODO | TODO | TODO | TODO |

> Bracketed `[TBD]` values are intentional. Setting them requires trade studies
> (TS-002, TS-003) not performed in this repository. Do not populate them with
> figures borrowed from reporting on fielded systems — those are not derived
> requirements for this design.

## Interface Requirements

| REQ ID | Requirement | Rationale | Traces To | Allocated To | Verify |
|---|---|---|---|---|---|
| REQ-IFC-001 | The payload mount shall provide a standardized mechanical interface independent of payload type. | Modularity | CAP-004 | CMP-MNT-01, IFC-INT-007 | I |
| REQ-IFC-002 | The power subsystem shall provide a regulated payload rail. | Payload-agnostic power | — | CMP-PWR-03, IFC-INT-003 | T `Deferred` |
| REQ-IFC-003 | TODO | TODO | TODO | TODO | TODO |

## Design Constraints

| REQ ID | Requirement | Rationale | Traces To | Allocated To | Verify |
|---|---|---|---|---|---|
| REQ-CON-001 | The design shall use commercially available components in preference to custom-fabricated parts. | Cost and sustainment | CAP-004 | All | I |
| REQ-CON-002 | The flight controller shall run widely supported open-source firmware. | Cost, maintainability, no vendor lock | CAP-004 | CMP-AVN-01 | I |
| REQ-CON-003 | The system shall not integrate weapons or munitions of any kind. | Project scope constraint | — | All | I |
| REQ-CON-004 | TODO | TODO | TODO | TODO | TODO |

## Deferred — Out of Scope

These are recorded so the model is honest about what it does *not* resolve. They are
not requirements this repository attempts to satisfy.

| REQ ID | Item | Disposition |
|---|---|---|
| REQ-DEF-001 | RF frequency, waveform, protocol, and link budget | Deferred to TS-009; requires RF engineering expertise |
| REQ-DEF-002 | Antenna type, gain, and pattern | Deferred to TS-009 |
| REQ-DEF-003 | Spectrum authorization for any radiating implementation | External; regulatory authority, not a design decision |
| REQ-DEF-004 | Contested-spectrum resilience mechanisms | Deferred; CAP-003 is stated qualitatively only |
| REQ-DEF-005 | Export control review of any resulting design | External; institutional compliance process |

## Requirement Health

<!-- STUB: a linter over these tables could check that every REQ traces to a CAP,
     every CMP referenced exists in architecture.md, and no ID is orphaned.
     Candidate CI check. -->

| Check | Status |
|---|---|
| Every REQ traces to a CAP or is explicitly marked `—` | TODO |
| Every referenced CMP/FUN exists in `architecture.md` | TODO |
| Every CAP has at least one REQ | TODO |
| No duplicate REQ IDs | TODO |
