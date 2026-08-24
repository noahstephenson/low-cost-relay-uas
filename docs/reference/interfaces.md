<!-- GENERATED VIEW - DO NOT EDIT. -->

# Interfaces

[Overview](../../README.md) · [Architecture](../architecture.md) · [Feasibility](../feasibility.md) · [Engineering Status](../engineering-status.md) · [Reference index](README.md)

This inventory shows logical architecture interfaces. It does not establish connector design, electrical ratings, protocol compatibility, or external conformance.

Generated from `model/architecture.yaml`. The structured catalogs remain authoritative.

## External interfaces

| Interface | Endpoints | Flow | Configuration / maturity | Open attributes |
|---|---|---|---|---|
| **Ground-control outbound traffic to relay payload** (IFC-EXT-001) | Ground Control (OP-001) → Relay Payload (Black Box) (CMP-COM-01) | command and control; a_to_b | CFG-REP, CFG-DOM; proposed | frequency, waveform, protocol, power, data rate, message format, endpoint compatibility, verification authority |
| **Relay-payload outbound traffic to remote UAS** (IFC-EXT-002) | Relay Payload (Black Box) (CMP-COM-01) → Remote UAS (OP-003) | command and control; a_to_b | CFG-REP, CFG-DOM; proposed | frequency, waveform, protocol, power, data rate, message format, endpoint compatibility, verification authority |
| **Remote-UAS return traffic to relay payload** (IFC-EXT-003) | Remote UAS (OP-003) → Relay Payload (Black Box) (CMP-COM-01) | telemetry; a_to_b | CFG-REP, CFG-DOM; proposed | frequency, waveform, protocol, power, data rate, message format, endpoint compatibility, verification authority |
| **Relay-payload return traffic to ground control** (IFC-EXT-004) | Relay Payload (Black Box) (CMP-COM-01) → Ground Control (OP-001) | telemetry; a_to_b | CFG-REP, CFG-DOM; proposed | frequency, waveform, protocol, power, data rate, message format, endpoint compatibility, verification authority |
| **Relay-UAS platform command link** (IFC-EXT-005) | Operator (OP-010) → Platform Command Receiver (CMP-AVN-04) | command and control; a_to_b | CFG-REP, CFG-DOM; proposed | frequency, waveform, protocol, power, message format, failsafe behavior, verification authority |
| **Configuration and maintenance interface** (IFC-EXT-006) | Maintenance (OP-007) → Relay UAS (OP-002) | configuration and maintenance; bidirectional | CFG-REP, CFG-DOM, CFG-DIG, CFG-SOS; proposed | data set, format, transport, authorization, retention period, tool ownership |
| **Relay-UAS health and status return** (IFC-EXT-007) | Flight Controller (CMP-AVN-01) → Operator (OP-010) | health and status; a_to_b | CFG-REP, CFG-DOM; proposed | minimum status set, format, transport, update behavior, endpoint compatibility, conformance authority |

## Platform-to-payload interfaces

| Interface | Endpoints | Flow | Configuration / maturity | Open attributes |
|---|---|---|---|---|
| **Regulated relay-payload power** (IFC-INT-003) | Power Regulators (CMP-PWR-03) → Relay Payload (Black Box) (CMP-COM-01) | electrical power; a_to_b | CFG-REP, CFG-DOM; proposed | voltage envelope, current envelope, connector, protection, thermal allocation |
| **Relay-payload mechanical retention** (IFC-INT-007) | Modular Payload Bay (CMP-MNT-01) → Relay Payload (Black Box) (CMP-COM-01) | mechanical mounting; bidirectional_physical | CFG-REP, CFG-DOM; proposed | geometry, load envelope, retention margin, inspection criteria |

## Payload-internal interfaces

| Interface | Endpoints | Flow | Configuration / maturity | Open attributes |
|---|---|---|---|---|
| **Black-box antenna physical-resource coupling** (IFC-INT-010) | Relay Payload (Black Box) (CMP-COM-01) → Payload Antenna Envelope (CMP-COM-02) | physical-resource coupling; bidirectional_physical | CFG-REP, CFG-DOM; proposed | antenna count, role, placement, connector, all RF characteristics |

## Other internal interfaces

| Interface | Endpoints | Flow | Configuration / maturity | Open attributes |
|---|---|---|---|---|
| **Main bus power to propulsion controllers** (IFC-INT-001) | Main Power Distribution (CMP-PWR-02) → Motor Controllers (CMP-PRP-02) | electrical power; a_to_b | CFG-REP, CFG-DOM; proposed | voltage, current, connector, protection, wiring allocation |
| **Regulated avionics power** (IFC-INT-002) | Power Regulators (CMP-PWR-03) → Flight Controller (CMP-AVN-01) | electrical power; a_to_b | CFG-REP, CFG-DOM; proposed | voltage, current, connector, power-quality envelope |
| **Motor command signals** (IFC-INT-004) | Flight Controller (CMP-AVN-01) → Motor Controllers (CMP-PRP-02) | command and control; a_to_b | CFG-REP, CFG-DOM; proposed | signal format, timing, connector, fault response |
| **Platform control input** (IFC-INT-005) | Platform Command Receiver (CMP-AVN-04) → Flight Controller (CMP-AVN-01) | command and control; a_to_b | CFG-REP, CFG-DOM; proposed | protocol, connector, timing, failsafe behavior |
| **Battery-state telemetry** (IFC-INT-006) | Main Power Distribution (CMP-PWR-02) → Flight Controller (CMP-AVN-01) | health and status; a_to_b | CFG-REP, CFG-DOM; proposed | measurement set, accuracy, update rate, connector, fault indication |
| **Navigation and timing sensor data** (IFC-INT-009) | Flight Sensors (CMP-AVN-02) → Flight Controller (CMP-AVN-01) | navigation and timing; a_to_b | CFG-REP, CFG-DOM; proposed | sensor set, data format, timing, accuracy, fault detection, connector |
| **Battery source power to main distribution** (IFC-INT-011) | Battery (CMP-PWR-01) → Main Power Distribution (CMP-PWR-02) | electrical power; a_to_b | CFG-REP, CFG-DOM; proposed | voltage, current, polarity, protection, connector implementation, physical routing |
| **GNSS and heading sensor data** (IFC-INT-012) | Navigation Sensor (CMP-AVN-03) → Flight Controller (CMP-AVN-01) | navigation and timing; a_to_b | CFG-REP, CFG-DOM; proposed | data format, timing, accuracy, fault detection, connector |
| **Propulsion-controller output to motor** (IFC-INT-013) | Motor Controllers (CMP-PRP-02) → Motors (CMP-PRP-01) | controlled electrical propulsion power; a_to_b | CFG-REP, CFG-DOM; proposed | electrical characteristics, connector, wiring, fault response |
| **Motor mechanical drive to propeller** (IFC-INT-014) | Motors (CMP-PRP-01) → Propellers (CMP-PRP-03) | mechanical propulsion drive; a_to_b | CFG-REP, CFG-DOM; proposed | attachment method, rotation direction, torque envelope, retention criteria |
| **Main distribution power to regulators** (IFC-INT-015) | Main Power Distribution (CMP-PWR-02) → Power Regulators (CMP-PWR-03) | electrical power; a_to_b | CFG-REP, CFG-DOM; proposed | voltage, current, connector, protection, branch allocation |

## Future-only interfaces

| Interface | Endpoints | Flow | Configuration / maturity | Open attributes |
|---|---|---|---|---|
| **Candidate digital-payload management and status interface** (IFC-INT-008) | Flight Controller (CMP-AVN-01) → Relay Payload (Black Box) (CMP-COM-01) | payload management and health and status; bidirectional | CFG-DIG, CFG-SOS; proposed | adoption decision, data model, protocol, connector, timing, authority, failure response |
