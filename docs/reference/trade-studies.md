# Trade Studies

[Overview](../../README.md) · [Architecture](../architecture.md) · [Feasibility](../feasibility.md) · [Engineering Status](../engineering-status.md) · [Reference index](README.md)

Trade studies turn open engineering questions into visible choices. This page explains what each choice affects, what the current analysis has shown, and what must happen before a design decision is made. The structured trade-study records in [model/assurance.yaml](../../model/assurance.yaml) remain the complete register.

## How to read status

| Status | Meaning |
|---|---|
| Open | The decision still needs bounds, authority, or evidence before it can be evaluated. |
| Scoped | The architecture or analysis clarifies the decision, but does not justify a selection. |
| Resolved | A decision has been made and recorded. |
| Deferred | The decision is deliberately outside this study. |

## Trade-study register

| Trade | Question | Why it matters | Current result |
|---|---|---|---|
| TS-001 — Airframe construction | What structural approach can carry the aircraft and payload? | Structure mass and cost reinforce the endurance loop. | Scoped; structure must be evaluated with battery, propulsion, and payload mass. |
| TS-002 — Propulsion sizing | What propulsion class and rotor geometry are appropriate? | Rotor efficiency and disk loading strongly affect hover power. | Scoped; no motors, propellers, or controllers selected. |
| TS-003 — Battery architecture | What pack characteristics are needed? | Battery energy and continuous power drive mass, cost, and endurance. | Scoped; no chemistry, topology, or capacity selected. |
| TS-004 — Payload power | What regulated electrical service must the carrier provide? | It affects rail capacity, power-conversion mass, and mission energy. | Scoped; payload electrical envelope remains open. |
| TS-005 — Flight controller | What flight-control capability is needed? | It depends on navigation, command, I/O, and authority needs. | Open. |
| TS-006 — Payload mount | What mechanical interface supports modular payloads? | The mount affects mass, volume, retention, and portability. | Scoped; geometry and load basis remain open. |
| TS-007 — Station keeping | How should the aircraft hold relay position without assuming continuous GNSS? | It affects navigation, control, energy, and mission usefulness. | Open. |
| TS-008 — Platform command link | How is the carrier aircraft controlled independently of the payload? | It preserves the separation between aircraft control and relayed traffic. | Open; external interface authority is needed. |
| TS-009 — Relay payload characterization | What is inside the relay payload? | The carrier must accommodate the payload, but does not design its radio implementation. | Deferred; outside this study. |
| TS-010 — Operating environment | What conditions must the aircraft tolerate? | Environmental burden changes power demand and available feasibility margin. | Open. |
| TS-011 — Recovery approach | What recovery and loss policy is acceptable? | It drives reserve, recovery behavior, cost, and safety work. | Open. |

## The central coupled trade: propulsion and battery

### Question

What propulsion and battery characteristics could support useful relay dwell without making the carrier too large, expensive, or difficult to handle?

### Why it matters

Payload mass and electrical demand add to the carrier. More dwell requires more battery energy. The heavier battery raises gross mass, which raises hover power and therefore requires still more battery. Propulsion efficiency, rotor disk loading, battery specific energy, and battery specific power determine how sharply that loop grows.

### Options

- Smaller rotors and a more compact airframe can help packaging and structure, but higher disk loading tends to increase hover power.
- Larger rotor area can improve hover efficiency, but longer arms and larger structure can cost mass, money, and portability.
- A battery class with stronger continuous-power capability can help short dwell, while greater specific energy matters more as dwell increases.
- Pack topology, power regulation, and payload demand must remain compatible, but no electrical implementation is selected here.

### Key trade

There is no independent “best battery” or “best propulsion set.” A battery cannot be sized until hover power is estimated, and hover power cannot be estimated until the aircraft mass—including battery mass—is known. Improving one part of the loop can move the burden to structure, packaging, cost, or portability.

### Current result

The executable feasibility analysis finds a limited short-dwell, modest-payload region under reference-or-better assumptions. Endurance is the dominant sensitivity; rotor figure of merit, disk loading, environmental power margin, battery specific energy and power, and motor/controller efficiency follow. In the reference 50 W payload slice, 30-minute cases reach a payload-sensitive knee, while all evaluated 45- and 60-minute cases are infeasible under the analysis boundaries.

The directional lesson is clear: efficient, lower-disk-loading propulsion improves the available design space, but its structural and portability consequences must be evaluated at the same time. The analysis does not select a rotor, motor, controller, battery chemistry, capacity, or topology.

### Status

**Scoped.** The model bounds the question and shows which variables matter most. Owner targets, packaging geometry, environmental conditions, and supported component-class evidence are still needed before a candidate comparison is appropriate.

## Other important decisions

| Decision area | Key trade | What the analysis or architecture establishes | What is still needed |
|---|---|---|---|
| Airframe construction | Low structural mass versus stiffness, durability, cost, and portability | Structural growth amplifies the mass–power loop. | Load basis, portability envelope, payload geometry, and sourcing policy. |
| Payload power | Sufficient support versus unnecessary mass and energy use | Payload demand consumes mission energy and rail capacity, even though propulsion dominates the reference station load. | Voltage, current, transient, protection, thermal, and connector envelope. |
| Payload mount | Modularity versus retention, mass, and package size | Mount and structural penalties must scale with payload load. | Payload volume, geometry, retention margin, inspection basis, and physical loads. |
| Flight control and station keeping | Capability versus complexity, energy use, and authority | The architecture requires station keeping without assuming continuous GNSS. | Station tolerance, navigation concept, command needs, and acceptance authority. |
| Platform command | Independent aircraft control versus external-interface uncertainty | Aircraft control stays separate from relay traffic. | Endpoint specification, interface authority, and conformance method. |
| Operating environment | Mission usefulness versus power and recovery margin | The generic environmental power margin is a leading sensitivity. | Authorized temperature, wind, precipitation, and operating conditions. |
| Recovery approach | Recoverability versus unit cost and reserve burden | Reserve changes the coupled feasibility region, but no safety credit is assumed. | Recovery/loss policy and accepted safety objective. |

## Deliberate payload boundary

TS-009 is different from the open trades. The relay payload's internal communications implementation is deliberately outside the project boundary. The carrier architecture only needs a payload accommodation envelope, regulated power, and mechanical retention. Keeping that boundary stable lets the carrier be studied without implying a radio design, endpoint compatibility, spectrum authorization, or payload selection.

## Next decision-quality step

Before the project compares actual components, the owner needs to set the payload service, endurance, portability, affordability, operating environment, reserve, and recovery targets together. Engineering can then rerun the feasibility model over that authorized region, define component-class evidence needs, and decide whether a later candidate comparison is justified.

For calculations, representative points, sensitivity rankings, equations, and limitations, read the [detailed feasibility analysis](feasibility-analysis.md). For all current owner decisions and evidence gaps, read [Decisions and Gaps](decisions-and-gaps.md).
