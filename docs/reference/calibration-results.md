# Relay-UAS carrier calibration results

## Calibration data table

The five NASA rows are fit points. The three DJI hover-endurance rows are checks that were not used in the fit. Model errors are `(model - published) / published`. Mass in the NASA rows is the measured supported-thrust equivalent at the cited hover point, not a catalog takeoff mass. Blank battery entries mean that battery energy was not used for the power fit.

| Vehicle/test article | Source | Mass (kg) | Rotor diameter (m) | Battery energy (Wh) | Published condition and value | Model value | Error | Use |
|---|---|---:|---:|---:|---|---:|---:|---|
| 3DR SOLO NASA test article | Russell et al., NASA/TM-2018-219758, [raw run data](https://rotorcraft.arc.nasa.gov/Publications/files/Russell_1180_Final_TM_022218.pdf) | 1.510 | 0.2540 | — | Full-vehicle hover, run 28 point 11: 184.44 W electrical | 180.71 W | -2.02% | fit |
| DJI Phantom 3 Advanced NASA test article | Russell et al., NASA/TM-2018-219758, [raw run data](https://rotorcraft.arc.nasa.gov/Publications/files/Russell_1180_Final_TM_022218.pdf) | 1.223 | 0.2388 | — | Full-vehicle hover, run 27 point 9: 172.07 W electrical | 140.13 W | -18.56% | fit |
| 3DR Iris+ NASA test article | Russell et al., NASA/TM-2018-219758, [raw run data](https://rotorcraft.arc.nasa.gov/Publications/files/Russell_1180_Final_TM_022218.pdf) | 1.279 | 0.2438 | — | Full-vehicle hover, run 29 point 12: 142.90 W electrical | 146.62 W | +2.61% | fit |
| Drone America DAx8 NASA test article | Russell et al., NASA/TM-2018-219758, [raw run data](https://rotorcraft.arc.nasa.gov/Publications/files/Russell_1180_Final_TM_022218.pdf) | 5.592 | 0.2794 | — | Full-vehicle hover, run 97 point 9: 837.98 W electrical | 827.48 W | -1.25% | fit |
| Straight Up Imaging Endurance NASA test article | Russell et al., NASA/TM-2018-219758, [raw run data](https://rotorcraft.arc.nasa.gov/Publications/files/Russell_1180_Final_TM_022218.pdf) | 2.913 | 0.3810 | — | Full-vehicle hover, run 119 point 11: 281.52 W electrical | 322.73 W | +14.64% | fit |
| DJI Matrice 30 Series | DJI, [M30 specifications](https://enterprise.dji.com/matrice-30/specs) | 3.770 | 0.4064 | 263.2 | Manufacturer maximum hover time, two batteries, laboratory environment: 36.00 min | 33.57 min | -6.74% | check |
| DJI Matrice 4 Series | DJI, [Matrice 4 specifications](https://enterprise.dji.com/matrice-4-series/specs) | 1.219 | 0.2743 | 99.5 | Hover, windless sea level, 100% to 0%, standard propellers: 42.00 min | 40.80 min | -2.85% | check |
| DJI Mavic 3M | DJI, [Mavic 3M specifications](https://enterprise.dji.com/mavic-3-m/specs) | 0.951 | 0.2388 | 77.0 | Hover, wind-free sea level, to 0% remaining, standard hard propellers: 37.00 min | 38.17 min | +3.17% | check |
| DJI Matrice 350 RTK | DJI, [M350 specifications](https://enterprise.dji.com/matrice-350-rtk/specs) | 6.470 | 0.5334 | 526.4 | 55 min at about 8 m/s, no payload, windless, to 0% | — | — | excluded: forward-flight endurance, not hover |

NASA vehicle dimensions and propeller diameters are cross-checked against Russell et al., [NASA/AIAA 2016-374](https://rotorcraft.arc.nasa.gov/Publications/files/72-2016-374.pdf). The structural anchor uses the measured empty mass, 2.7216 kg, and calculated component masses for the Endurance article in Russell et al., [AHS 2018](https://rotorcraft.arc.nasa.gov/Publications/files/Russell_2018_TechMx.pdf), Table 1.

## Parameter table

Only three feasibility inputs changed. The calibration script fits the first two; the third is a direct current-production battery-pack selection, not another fitted degree of freedom.

| Parameter | Previous nominal | Calibrated nominal | Basis |
|---|---:|---:|---|
| Rotor figure of merit | 0.620000 | 0.620274 | Unweighted least-squares fit through the origin across five independent NASA full-vehicle hover points. With the unchanged motor/controller efficiency of 0.83 and environment multiplier of 1.15, this gives an effective `FM*eta/k_env` of 0.447676. |
| Structure base mass (kg) | 0.950000 | 0.163173 | Back-calculated from the NASA Endurance measured empty mass after subtracting the published calculated motor, ESC, propeller, battery, autopilot, and landing-gear masses; the existing load-fraction term is unchanged. |
| Battery specific energy (Wh/kg) | 170.000 | 192.117 | Direct ratio for one DJI Matrice 30 TB30 pack: 131.6 Wh / 0.685 kg. This is a selected carrier-battery technology anchor, not a hover-fit parameter. |

The machine-readable inputs retain `previous_nominal` and `calibration_source` fields in `analysis/feasibility-inputs.yaml`. Mission reserve, depth of discharge, payload, RF, and all other parameters remain unchanged.

## Held-out result

Across the three held-out DJI hover-endurance checks, error ranges from -6.74% to +3.17%; all three are inside the ±20% acceptance band, so there are no misses.

## New worked case

Primary payload `PAY-MESH-OEM`, obstructed-reference geometry, 10 km endpoint separation, 120 m relay altitude:

| Dwell (min) | Gross mass (kg) | Rotor diameter (m) | Battery branch | Energy slope | Mathematical closure | Practical constraint | Integrated label |
|---:|---:|---:|---|---:|---|---|---|
| 10 | 3.584 | 0.432 | power | 0.346 | finite | pass | `RELAY_BENEFICIAL_AND_FEASIBLE` |
| 20 | 3.584 | 0.432 | power | 0.500 | finite | pass | `RELAY_BENEFICIAL_AND_FEASIBLE` |
| 30 | 4.775 | 0.498 | energy | 0.654 | finite | pass | `RELAY_BENEFICIAL_AND_FEASIBLE` |
| 45 | 15.146 | 0.888 | energy | 0.885 | finite | fail | `MASS_CLOSED_PRACTICAL_CONSTRAINT_FAILURE` |
| 60 | — | — | none | 1.116 | nonclosure | fail | `RELAY_FUNCTIONAL_VEHICLE_RESOURCE_FAILURE` |

The 45-minute point remains mathematically finite but violates practical mass/span constraints. The 60-minute energy feedback slope exceeds one, so no finite carrier mass closes.

## New partitions

Primary-payload counts are shown in the order direct-sufficient / relay-beneficial-and-feasible / mass-closed-practical-failure / link-infeasible / vehicle-resource-failure.

| Scenario | Direct | Feasible relay | Practical failure | Link-infeasible | Resource failure | Total |
|---|---:|---:|---:|---:|---:|---:|
| `clear_reference` | 30 | 9 | 3 | 45 | 3 | 90 |
| `obstructed_reference` | 0 | 18 | 6 | 60 | 6 | 90 |
| `obstructed_adverse` | 0 | 6 | 2 | 80 | 2 | 90 |
| `obstruction_sensitivity_h60_x40` | 0 | 18 | 6 | 60 | 6 | 90 |
| `obstruction_sensitivity_h100_x40` | 0 | 9 | 3 | 75 | 3 | 90 |
| `obstruction_sensitivity_h80_x30` | 0 | 9 | 3 | 75 | 3 | 90 |
| `obstruction_sensitivity_h80_x45` | 0 | 18 | 6 | 60 | 6 | 90 |

Carrier-only counts before direct/connectivity gating are identical in each of the seven scenarios because the carrier inputs do not depend on screen geometry:

| Scenario scope | Finite practical pass | Finite practical failure | Mathematical nonclosure | Total |
|---|---:|---:|---:|---:|
| Each scenario | 54 | 18 | 18 | 90 |

## Boundaries

| Boundary | Result | Interpretation |
|---|---:|---|
| Clear link-limited endpoint separation | 25.049 km | Ground-to-relay hop limits first; symmetric midpoint placement and 120 m relay altitude. |
| Baseline link-limited endpoint separation | 25.049 km | Baseline RF assumptions have zero excess loss, so this equals the clear result. |
| +12 dB excess-loss link-limited endpoint separation | 6.288 km | Ground-to-relay hop limits first under the same geometry. |
| Favorable longest practical dwell | 126.913 min | Continuous practical-constraint boundary. |
| Favorable energy-slope-one dwell | 156.964 min | Mathematical nonclosure threshold. |
| Reference longest practical dwell | 42.116 min | Continuous practical-constraint boundary. |
| Reference energy-slope-one dwell | 52.443 min | Mathematical nonclosure threshold. |
| Adverse longest practical dwell | none | The power branch is already outside the practical constraints at zero dwell. |
| Adverse energy-slope-one dwell | 6.416 min | Mathematical nonclosure threshold. |

## Old vs. new comparison

The primary worked-case carrier shrank materially while preserving the intended distinction between finite-but-impractical and nonclosing cases.

| Dwell (min) | Old mass (kg) | New mass (kg) | Old rotor diameter (m) | New rotor diameter (m) | Old/new state |
|---:|---:|---:|---:|---:|---|
| 10 | 5.417 | 3.584 | 0.531 | 0.432 | practical / practical |
| 20 | 5.417 | 3.584 | 0.531 | 0.432 | practical / practical |
| 30 | 8.620 | 4.775 | 0.670 | 0.498 | practical / practical |
| 45 | 106.246 | 15.146 | 2.351 | 0.888 | finite but impractical / finite but impractical |
| 60 | — | — | — | — | nonclosure / nonclosure |

The primary baseline partition remained 18 feasible / 6 practical-failure / 6 vehicle-resource-failure / 60 link-infeasible before and after calibration. The +12 dB adverse partition likewise remained 6 / 2 / 2 / 80. Thus calibration changes the continuous carrier sizing and boundary values, not the sampled categorical counts at the existing grid points.

## What calibration does not establish

This calibration does not establish a production aircraft design, structural adequacy, component thermal margins, flight-control stability, manufacturability, supplier cost, lifecycle cost, regulatory compliance, or mission suitability. The fit is a compact class-level hover-power and empty-mass correction based on small multirotor data. Manufacturer endurance checks use idealized steady hover to 0% and therefore do not validate the mission reserve policy or adverse weather operation. The calibrated parameters should be revisited when a candidate rotor/propulsion set, battery pack, airframe layout, and payload integration are tested together.
