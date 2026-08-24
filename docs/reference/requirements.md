<!-- GENERATED VIEW - DO NOT EDIT. -->

# Requirements

[Overview](../../README.md) · [Architecture](../architecture.md) · [Feasibility](../feasibility.md) · [Engineering Status](../engineering-status.md) · [Reference index](README.md)

The current assurance set contains 23 system requirements. Neutral IDs are durable keys; classification remains metadata and names carry the human meaning.

Generated from `model/assurance.yaml`. The structured catalogs remain authoritative.

## Relay mission

| ID | Requirement | Status | Verification |
|---|---|---|---|
| REQ-001 | **Relay outbound traffic** — The system shall relay outbound traffic from a ground control node toward a remote UAS node. | proposed / candidate | A: VER-001, VER-004 |
| REQ-002 | **Relay return traffic** — The system shall relay return traffic from a remote UAS node toward a ground control node. | proposed / candidate | A: VER-001, VER-004 |

## Flight and positioning

| ID | Requirement | Status | Verification |
|---|---|---|---|
| REQ-003 | **Maintain commanded station position** — The system shall maintain a commanded station position within [TBD] horizontal and [TBD] vertical tolerance. | proposed / deferred | A: VER-001, VER-008 |
| REQ-010 | **Provide on-station endurance** — The system shall provide at least [TBD] minutes of on-station endurance. | proposed / deferred | A: VER-001, VER-008 |
| REQ-011 | **Limit system gross mass** — System gross mass shall not exceed [TBD]. | proposed / blocked_by_tbd | I: VER-005, VER-008 |
| REQ-023 | **Avoid continuous-GNSS dependency** — The station-keeping design shall not assume continuous GNSS availability as a precondition. | proposed / candidate | A: VER-001, VER-004 |

## Recovery and aircraft control

| ID | Requirement | Status | Verification |
|---|---|---|---|
| REQ-004 | **Accept operator aircraft commands** — The system shall accept operator command input for transit, repositioning, and recovery. | proposed / candidate | A: VER-001, VER-004 |
| REQ-005 | **Return on low-battery condition** — The system shall initiate return-to-launch on reaching a defined low-battery state. | proposed / deferred | D: VER-004, VER-006, VER-008 |
| REQ-006 | **Inhibit arming in Ground Safe** — The system shall inhibit motor arming while in MODE-005 (Ground Safe). | proposed / candidate_analysis_only | D: VER-004, VER-006 |
| REQ-007 | **Recover after payload loss** — The system shall remain controllable and recoverable following loss of payload function (MODE-003). | proposed / deferred | D: VER-004, VER-006, VER-008 |
| REQ-008 | **Provide mode and health/status** — The system shall make current operating mode and detected Relay-UAS health/status available to the operator. | proposed / deferred | I/D: VER-004, VER-005, VER-008, VER-009 |

## Payload support and interfaces

| ID | Requirement | Status | Verification |
|---|---|---|---|
| REQ-012 | **Accommodate payload envelope** — The payload bay shall accommodate a payload of up to [TBD] mass within a [TBD] volume envelope. | proposed / blocked_by_tbd | I: VER-005, VER-008 |
| REQ-014 | **Standardize payload mount** — The payload mount shall provide a standardized mechanical interface independent of payload type. | proposed / candidate | I: VER-005 |
| REQ-015 | **Provide regulated payload power** — The power subsystem shall provide a regulated payload rail meeting a defined voltage and current envelope. | proposed / deferred | T: VER-005, VER-008 |
| REQ-016 | **Limit platform-to-payload interfaces** — The platform-to-payload interface shall be limited to power (IFC-INT-003) and mechanical retention (IFC-INT-007). | proposed / candidate | I: VER-005 |
| REQ-017 | **Retain payload under flight loads** — The payload mount shall retain the payload under all flight loads with [TBD] margin. | proposed / deferred | T: VER-005, VER-006, VER-008 |

## Power and safety

| ID | Requirement | Status | Verification |
|---|---|---|---|
| REQ-018 | **Protect and retain battery** — The battery installation shall provide over-current protection and physical retention of the pack. | proposed / deferred | I: VER-005, VER-006, VER-008 |
| REQ-019 | **Indicate armed state to operator** — The system shall provide an operator-visible indication of armed state. | proposed / candidate_analysis_only | D: VER-004, VER-006 |
| REQ-022 | **Exclude weapons and munitions** — The system shall not integrate weapons or munitions of any kind. | proposed / scope_control | I: VER-003, VER-005 |

## Portability and affordability

| ID | Requirement | Status | Verification |
|---|---|---|---|
| REQ-009 | **Limit system unit cost** — System unit cost shall not exceed [TBD]. | proposed / blocked_by_tbd | A: VER-001 |
| REQ-013 | **Enable single-operator deployment** — The system shall be transportable and launched by a single operator without support equipment. | proposed / deferred | D: VER-004, VER-008 |
| REQ-020 | **Prefer commercial components** — The design shall use commercially available components in preference to custom-fabricated parts. | proposed / candidate | I: VER-005 |
| REQ-021 | **Use open-source flight firmware** — The flight controller shall run widely supported open-source firmware. | proposed / candidate | I: VER-005 |

## Deferred / externally owned topics

These records preserve scope, provenance, applicability, and ownership without presenting the topics as system requirements.

| ID | Topic | Disposition | Related model records |
|---|---|---|---|
| DEF-001 | **Define RF implementation** — RF frequency, waveform, protocol, and link budget | intentional_deferral | CLM-SCP-001, TS-009, IFC-EXT-001, IFC-EXT-002, IFC-EXT-003, IFC-EXT-004, IFC-EXT-005 |
| DEF-002 | **Define antenna characteristics** — Antenna type, gain, and pattern | intentional_deferral | CLM-SCP-001, TS-009, CMP-COM-02, IFC-INT-010 |
| DEF-003 | **Obtain spectrum authorization** — Spectrum authorization for any radiating implementation | intentional_deferral | CLM-SCP-001, OP-008, OP-008 |
| DEF-004 | **Define contested-spectrum resilience** — Contested-spectrum resilience mechanisms | true_coverage_gap | CLM-SCP-001, CAP-003, TS-009 |
| DEF-005 | **Complete export-control review** — Export control review of any resulting design | intentional_deferral | CLM-SCP-001 |

For allocation, provenance, applicability, TBD ownership, and source fields, inspect [`model/assurance.yaml`](../../model/assurance.yaml) and the [traceability reference](traceability.md).
