# Feasibility

[Overview](../README.md) · [Architecture](architecture.md) · **Feasibility** · [Engineering Status](engineering-status.md) · [Reference](reference/README.md)

The analysis asks whether a small multirotor can carry the relay payload, hover for a useful dwell, and remain within exploratory mass, power, discharge, portability, and cost boundaries. It evaluates a design space, not a selected aircraft.

## Why the problem is coupled

Hover endurance cannot be sized one subsystem at a time:

1. Payload and dry-aircraft mass set an initial gross mass.
2. Gross mass and rotor loading set hover power.
3. Hover power and dwell time set required battery energy.
4. Battery energy and discharge demand set battery mass.
5. Battery mass increases gross mass, which raises hover power again.

The model iterates that loop until mass converges or the case diverges. Longer dwell increases the loop gain: the battery must carry energy not only for the original aircraft, but also for the extra battery mass introduced by the endurance target.

## What the model includes

The executable model combines:

- payload mass and electrical demand;
- multirotor induced-power and efficiency terms;
- rotor disk loading and environmental power margin;
- installed propulsion, structure, avionics, power electronics, and mount mass;
- battery energy and continuous-power sizing;
- energy reserve and usable depth of discharge;
- broad component-class cost relationships; and
- conditional portability, cost, battery-fraction, and discharge boundaries.

The solver evaluates 225 deterministic grid cases and uses 4,096 low-discrepancy samples to rank sensitivities. Those implementation details support the result; they are not the result itself.

## Primary assumptions

| Input | Evaluated range | Meaning |
|---|---|---|
| Payload mass | 0.25–2.0 kg | Owner-controlled sensitivity, not an approved payload envelope |
| Payload power | 0–120 W | Black-box electrical demand, not a selected radio |
| On-station endurance | 10–60 min | Owner-controlled sensitivity, not an approved requirement |
| Installed battery specific energy | 130–220 Wh/kg | Component-class evidence range; upper end is optimistic |
| Rotor disk loading | 40–100 N/m² | Architecture design variable |
| Environmental power margin | 1.0–1.3 multiplier | Unapproved sensitivity for operating conditions |

Other structure, propulsion, efficiency, reserve, discharge, and cost terms are versioned in [`analysis/feasibility-inputs.yaml`](../analysis/feasibility-inputs.yaml). None represents selected hardware.

## Principal result

The study found a bounded plausible region for short dwell and modest payload under reference-or-better assumptions. Endurance is the dominant sensitivity. As dwell rises, the battery–mass–power feedback rapidly increases gross mass, installed energy, propulsion demand, and cost.

In the deterministic grid:

- the favorable regime produced 73 feasible and 2 marginal cases;
- the reference regime produced 20 feasible, 21 marginal, and 34 infeasible cases; and
- the adverse regime produced 75 infeasible cases.

Within the reference 50 W payload-power slice, shorter-dwell cases are generally feasible or marginal, 30-minute cases cross a payload-sensitive knee, and every evaluated 45- and 60-minute case is infeasible under the analysis boundaries.

![Conditional feasibility region across payload mass and endurance](../analysis/results/feasible-region.svg)

“Feasible,” “marginal,” and “infeasible” are conditional analysis classes. They do not dispose any owner requirement because quantitative owner targets have not been approved.

## Dominant sensitivities

The global ranking identifies these leading drivers:

1. on-station endurance;
2. rotor figure of merit;
3. disk loading;
4. environmental power margin;
5. installed battery specific energy;
6. installed battery specific power; and
7. motor/controller efficiency.

Payload mass and power still matter, especially near the transition between marginal and infeasible cases. The ranking says where evidence and design effort have the greatest leverage; it does not select a rotor, motor, controller, battery, structure, or payload.

## Engineering implications

- Set payload service, endurance, portability, affordability, environment, reserve, and recovery targets together.
- Treat gross mass as a coupled output, not an independent value that can be chosen without consequence.
- Evaluate propulsion and battery classes together because disk loading, efficiency, specific energy, and specific power interact.
- Resolve packaging geometry before treating the mass-only feasible region as a physical design region.
- Re-run the same model with owner-authorized targets and supported component-class evidence before selecting hardware.

The analysis suggests that a short-dwell demonstration or limited service concept may close. It also shows why extending hover duration is not a simple battery-capacity upgrade.

## What the model does not establish

The model does not establish a point design, exact flight time, selected hardware, packaging fit, structural adequacy, thermal behavior, wind performance, battery safety, payload compatibility, spectrum authority, unit production cost, physical verification, or technical-baseline approval. The middle representative point is marginal under the analysis boundaries; it is not a recommended aircraft.

For equations, source treatment, convergence behavior, all limitations, and detailed results, read the [Feasibility Analysis](reference/feasibility-analysis.md). To reproduce the artifacts, run [`analysis/feasibility.py`](../analysis/feasibility.py).

Next: read [Engineering Status](engineering-status.md) for the decisions and evidence required before this design space can become a physical candidate.
