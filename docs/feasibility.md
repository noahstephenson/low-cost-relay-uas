# Feasibility

[Overview](../README.md) · [Architecture](architecture.md) · **Feasibility** · [Engineering Status](engineering-status.md) · [Reference](reference/README.md)

## The question

Can a small multirotor carry the relay payload and remain airborne for a useful time without mass, power, battery size, cost, or portability becoming unreasonable? The executable analysis explores that question across a range of assumptions. It does not size a selected aircraft.

## Why endurance is coupled

Longer hover time is not a battery-only problem:

1. Payload and dry-aircraft mass set a starting gross mass.
2. Gross mass and rotor loading determine hover power.
3. Hover power and dwell time determine required battery energy.
4. Battery energy and continuous-power demand determine battery mass.
5. The larger battery increases gross mass, so hover power and battery demand rise again.

The model repeats this loop until mass converges or the case diverges. As dwell time grows, the feedback becomes stronger: the battery must carry energy for both the aircraft and the additional battery mass caused by the endurance target.

## What goes into the model

The analysis varies payload mass and electrical demand, on-station endurance, battery performance, rotor loading and efficiency, environmental power margin, reserve, structural and propulsion allowances, and broad carrier-cost factors. It also checks conditional mass, cost, battery-fraction, and discharge boundaries.

| Input | Evaluated range | Interpretation |
|---|---|---|
| Payload mass | 0.25–2.0 kg | Unapproved payload sensitivity range |
| Payload power | 0–120 W | Black-box demand, not a selected radio |
| On-station endurance | 10–60 min | Unapproved mission sensitivity range |
| Installed battery specific energy | 130–220 Wh/kg | Component-class range; the upper end is optimistic |
| Rotor disk loading | 40–100 N/m² | Architecture variable |
| Environmental power margin | 1.0–1.3 | Generic operating-condition sensitivity |

The versioned [analysis inputs](../analysis/feasibility-inputs.yaml) identify the other assumptions, sources, and limitations. None is selected hardware or an approved target.

## What comes out

The model calculates disk area, hover power, required and installed battery energy, battery mass, propulsion and structure allowances, gross mass, cost, convergence behavior, and a conditional feasibility class. It evaluates 225 deterministic grid cases and uses 4,096 low-discrepancy samples to rank sensitivities.

## Main result

The study finds a bounded plausible region for short dwell and modest payload under reference-or-better assumptions. Endurance is the strongest driver. As dwell rises, the battery–mass–power feedback increases gross mass, installed energy, propulsion demand, and cost rapidly.

| Assumption bundle | Feasible | Marginal | Infeasible |
|---|---:|---:|---:|
| Favorable | 73 | 2 | 0 |
| Reference | 20 | 21 | 34 |
| Adverse | 0 | 0 | 75 |

In the reference 50 W payload-power slice, shorter dwell cases are generally feasible or marginal, 30-minute cases reach a payload-sensitive knee, and every evaluated 45- and 60-minute case is infeasible under the model's analysis boundaries.

![Conditional feasibility region across payload mass and endurance](../analysis/results/feasible-region.svg)

“Feasible,” “marginal,” and “infeasible” are conditional analysis classes. They do not show compliance with an owner requirement, because no quantitative owner targets have been approved.

## What changes the region

The leading sensitivities are on-station endurance, rotor figure of merit, disk loading, environmental power margin, installed battery specific energy, installed battery specific power, and motor/controller efficiency. Payload mass and power matter most near the transition between marginal and infeasible cases.

![How longer dwell drives mass and cost in the reference analysis](../analysis/results/endurance-mass-cost.svg)

The analysis shows two battery regimes. At short dwell, the pack can be limited by the continuous power needed to hover. At longer dwell, energy capacity dominates. The transition near 30 to 45 minutes is a feature of these explored assumptions, not a universal aircraft limit.

## Engineering implications

- Set payload service, endurance, portability, affordability, operating environment, reserve, and recovery policy together.
- Treat gross mass as a coupled output, not an independent value chosen before propulsion and battery sizing.
- Consider propulsion and battery classes together; efficiency, disk loading, specific energy, and specific power interact.
- Close packaging geometry and payload electrical and retention envelopes before treating the mass-only region as a physical design.
- Re-run the model with authorized targets and supported component-class evidence before selecting hardware.

The analysis supports a short-dwell demonstration or limited-service concept as a possibility. It also shows why longer hover duration cannot be assumed to follow from a simple battery-capacity increase.

## What this does not establish

The model does not establish a point design, exact flight time, packaging fit, structural adequacy, thermal behavior, wind performance, battery safety, payload compatibility, spectrum authority, production cost, physical verification, or technical-baseline approval. The representative points are illustrations of the design space, not recommended aircraft.

For equations, sources, convergence behavior, detailed results, and limitations, read the [detailed feasibility analysis](reference/feasibility-analysis.md). To reproduce the artifacts, run [analysis/feasibility.py](../analysis/feasibility.py).

Next: read [Engineering Status](engineering-status.md) for the decisions and evidence needed before this design space can become a physical candidate.
