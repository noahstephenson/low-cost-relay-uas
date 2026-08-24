# Architecture

[Overview](../README.md) · **Architecture** · [Feasibility](feasibility.md) · [Engineering Status](engineering-status.md) · [Reference](reference/README.md)

The Relay UAS is a small multirotor carrier for a separately bounded communications payload. The aircraft positions the payload where airborne geometry can extend a blocked or distant link. Its own control path remains separate from the mission traffic passing through the relay.

## System concept

Ground control sends remote-aircraft command toward the Relay UAS. The relay payload passes that traffic onward, then returns remote-aircraft telemetry in the opposite direction. The carrier aircraft supplies position, lift, electrical power, payload retention, and recovery support; it does not process the relayed mission traffic at this architecture level.

The architecture is intentionally payload-agnostic. It defines what the carrier needs from a payload—mass and volume accommodation, regulated power, and mechanical retention—without defining the payload’s internal radio implementation.

## System boundary

The product boundary contains the aircraft platform, payload support, and relay payload as a black box. It includes:

- airframe and load-bearing structure;
- four-corner propulsion;
- stored energy, main distribution, and regulated power;
- flight control, navigation, and aircraft health/status support;
- the independent platform-command receiver;
- payload mounting and regulated payload power; and
- the relay payload and antenna resources as bounded physical resources.

Operators, ground-control equipment, the remote aircraft, maintenance personnel, external network services, spectrum authorities, and other future platforms remain outside the product boundary. Their presence in the broader context does not assign responsibility or establish compatibility.

The recovered article is evidence for role correspondence, not an inherited design. The functional-replica and domestic-sourcing configurations are current candidates. Digital-payload and wider system-of-systems branches remain future concepts. None is an approved technical baseline.

The complete boundary and configuration views are available in the [Architecture Atlas](reference/architecture-atlas.md).

## Major physical subsystems

![Grouped physical architecture of the Relay UAS](figures/physical-architecture.svg)

The structured model contains 19 component records, grouped here by engineering role:

| Subsystem | Responsibility |
|---|---|
| Airframe and structure | Carry aircraft loads and support propulsion, avionics, energy storage, and payload mounting. |
| Propulsion | Convert controlled electrical power into lift through controllers, motors, and propellers. |
| Electrical power | Store energy, distribute the main bus, and provide regulated avionics and payload branches. |
| Flight avionics | Stabilize, navigate, hold station, manage aircraft modes, and support health/status reporting. |
| Platform communications | Receive commands for the Relay UAS independently of the relay payload. |
| Payload support | Retain the payload and provide its regulated electrical interface. |
| Relay payload | Pass mission command and telemetry between external endpoints as a black box. |

The diagram groups components to show responsibility rather than every physical part. No motor, controller, propeller, battery, frame, flight computer, mount, radio, or antenna has been selected.

## Platform control and mission relay

![Two information lanes separating aircraft control from relayed traffic](figures/command-data-flow.svg)

The upper lane controls the carrier aircraft. The operator sends platform command through the aircraft’s dedicated receiver to flight avionics. Proposed mode and health/status information returns toward the operator.

The lower lane carries remote-aircraft mission traffic. Ground-originated command enters the black-box relay payload and exits toward the remote aircraft. Return telemetry follows the reverse path. The aircraft carries and powers the payload but does not use that traffic to control itself.

The current platform-to-payload boundary has exactly two crossings:

1. **Regulated payload power** supplies a payload-agnostic electrical envelope.
2. **Mechanical retention** secures the payload to the carrier.

Limit platform-to-payload interfaces (REQ-016) preserves this separation. A payload-internal antenna connection remains inside the payload envelope, and a possible digital management connection belongs only to a future configuration.

## Power architecture

Stored battery energy feeds main power distribution. The main bus supplies propulsion controllers and also feeds regulated branches. One regulated branch supports flight avionics; another supports the relay payload. Motor controllers drive the motors, and the motors drive the propellers mechanically.

This architecture establishes connectivity and failure meaning without assigning voltage, current, connector, wire, protection, thermal, or power-quality values. Loss of payload power can remove relay service while leaving platform control available. Loss of avionics power is more severe because it can remove flight control and recovery capability.

See [Interfaces](reference/interfaces.md) for the complete logical inventory and the atlas’s reference power view for detailed connectivity.

## Mission behavior

The normal mission is an architecture sequence, not an operating procedure:

1. **Prepare.** Establish the candidate configuration and a Ground Safe state.
2. **Launch and transit.** Use the independent platform-command path to move to a useful position.
3. **Hold station.** Flight avionics and navigation maintain the commanded relay geometry.
4. **Relay outbound traffic.** The payload passes command toward the remote aircraft.
5. **Relay return traffic.** The payload passes telemetry back toward ground control.
6. **Monitor.** Aircraft mode and detected health/status support repositioning and recovery decisions.
7. **Recover.** Normal completion or a defined low-battery condition moves the aircraft toward return, landing, and Ground Safe.

Maintain commanded station position (REQ-003) retains horizontal and vertical tolerance as owner-controlled values. Return on low-battery condition (REQ-005) retains the threshold and reserve policy as unresolved. The behavior exists in the architecture without pretending those criteria are known.

## Degraded behavior and recovery intent

![Mode flow showing relay degradation and recovery intent](figures/degraded-behavior.svg)

Relay degradation is distinct from loss of aircraft control. The model moves from station keeping to a relay-degraded state when payload service is impaired. If the independent platform-control path remains available, the intended next state is return and recovery. Recover after payload loss (REQ-007) captures that objective.

The model does not define detection thresholds, detailed flight-control logic, containment behavior, or physical recovery performance. If platform control is also impaired, the architecture stops at an explicit safety gap rather than inventing a response. Physical recovery evidence has not been produced.

## Deliberate architecture boundaries

The current architecture does not define:

- relay frequency, waveform, modulation, protocol, transmit power, or link budget;
- antenna type, gain, or radiation pattern;
- connector families, electrical ratings, or packaging geometry;
- component selections or fabrication details;
- detailed readiness, flight, or recovery procedures;
- endpoint compatibility, spectrum authorization, or external conformance;
- future ground-vehicle, video, sensor-data, or broader network implementation; or
- safety, airworthiness, operational-readiness, standards-conformance, or baseline approval.

These are controlled omissions. Deferred and externally owned topics remain visible in [Requirements](reference/requirements.md), while unresolved owner choices and evidence dependencies are consolidated in [Decisions and Gaps](reference/decisions-and-gaps.md).

## Inspect the detailed model

Use the reference layer when the engineering question requires identifiers and complete catalogs:

- [Interfaces](reference/interfaces.md) for external, internal, payload-boundary, and future interfaces;
- [Traceability](reference/traceability.md) for representative and complete relationship chains;
- [Architecture Atlas](reference/architecture-atlas.md) for ID-rich audit diagrams;
- [`model/architecture.yaml`](../model/architecture.yaml) for authoritative structured architecture data; and
- [`model/system.yaml`](../model/system.yaml) for scope, status, manifests, and presentation-view metadata.

Next: read [Feasibility](feasibility.md) to see where the coupled aircraft concept appears plausible, or [Engineering Status](engineering-status.md) to see what remains unresolved.
