# Research Status

> **Superseded.** This status page predates the carrier calibration (commit `4f9e2cd`, branch `codex/carrier-calibration-v1`) and the finished manuscript. The submitted paper in `submission/relay_uas_aeroconf.tex` (local, intentionally untracked; see `.gitignore`) is the sole authority for claims and numbers; its title is "System Architecture and Service Envelope of a Multirotor Communications Relay." Treat everything below as historical drafting context.

Working title: **System Architecture and Mission Feasibility of a Multirotor Communications Relay**

Corrective successor to commit `2eb84259573cf7e0f216bc11002d65dbdb0f32f3`, tag `relay-uas-research-freeze-v1`. The original frozen tag is preserved. See [corrective record](reference/research-corrective-v1.md).

## Aircraft-centered research question

What architecture lets a small multirotor support airborne relay service, and under what declared mission demands does that architecture remain plausible?

The subject is the relay aircraft: its mission role, subsystem responsibilities, payload-support interfaces, and resource limitations. The existing connectivity and carrier models provide a conditional assessment of that architecture. This framing update follows corrective commit `2d19310abc4df22e6a662ec03436c6938c1751a6` without changing its equations, inputs, grids, classifications, or results.

Examination of a recovered relay aircraft is background motivation only. No paper claim depends on provenance, exact reconstruction, or measured performance of that article. Historical replica and domestic-sourcing configuration identifiers and evidence records remain intact; the paper is organized around the general relay-UAS architecture.

## Proposed contributions and evidence

1. **An explicit small relay-UAS architecture:** black-box relay payload, mechanical/electrical payload support, and logically separate carrier control and relay traffic. This is a documented architecture allocation, not demonstrated fault isolation or a claim that these established principles are new.
2. **A conditional service envelope for that architecture:** the existing geometry/link screen and carrier resource closure jointly identify where the declared outbound hover-dwell service passes exploratory physical bounds. This is shared-payload screening, not joint radio/vehicle optimization or full-mission validation.
3. **Decision-relevant failure distinctions:** connectivity failure, finite closure outside physical bounds, and mathematical nonclosure identify different limitations on the small aircraft. Their value is in explaining which assumptions would need to change, not in treating standard equations as novel methods.

The [architecture-to-evidence table](architecture.md#architecture-to-evidence-assessment) separates modeled responsibilities from quantitative support and remaining gaps. The [worked dwell example](feasibility.md#primary-relay-uas-result) uses the existing 30-, 45-, and 60-minute cases. The full prepare-to-recover mission remains a conceptual responsibility sequence; only stationary one-way dwell is quantitatively assessed.

## Current experiment

The primary experiment contains 90 unique mission cases: 6 endpoint separations × 5 dwell values × 3 relay altitudes. The headline payload is PAY-MESH-OEM. The Helix Nano and SC4200 Plus records are secondary SWaP sensitivity cases; they do not multiply mission counts and no payload-selection claim is made.

The reference service is declared in `analysis/mission-connectivity-inputs.yaml`: a common analysis band, service bandwidth, receiver threshold, ground transmit basis, endpoint and relay gains, and miscellaneous-loss allowance. These are analysis assumptions, not authorization, waveform, or hardware-performance claims. Manufacturer receiver sensitivities are not mixed across incompatible bandwidth/MCS conditions.

The mission-feasibility analysis covers the Ground → Relay → Remote direction, stationary hover dwell, constant atmospheric density, declared stylized visibility and link assumptions, and declared exploratory vehicle boundaries. It does not demonstrate transit, climb, descent, return, reverse-link service, full mission energy, bidirectional operational performance, or physical aircraft validation.

The primary payload uses 14 W continuously for carrier energy and power sizing: the manufacturer lists 5 W for receive and 14 W peak. This replaces the freeze's receive-only 5 W assumption with an upper-load allowance; no duty cycle or measured RF/DC operating pair is claimed. Secondary payload DC assumptions remain exploratory; their peak-power fields are source metadata, not separate solver inputs.

The implemented connection is a shared-payload architecture screening: payload mass/DC demand and dwell drive carrier closure; geometry and RF assumptions drive connectivity; the classifier intersects their results. Link margin does not resize radio hardware or electrical demand, and altitude does not alter constant-density hover power.

## Visibility and propagation scenarios

The classifier accepts free-space margins only for clear segments. Exported margins for blocked segments are hypothetical unobstructed-path values, not predictions through the screen. The visibility mechanism is an opaque vertical screen, deliberately declared as a stylized clearance scenario rather than terrain prediction, ray tracing, or an operational terrain claim. The direct Ground → Remote path is blocked in every screen case. The Relay → Remote segment is not evaluated against a screen located before the midpoint relay because that segment does not cross it.

The baseline screen is 80 m at 40% of endpoint separation. Four one-factor geometry sensitivities retain the same separation, dwell, altitude, payload, link, and carrier inputs:

| Screen scenario | Midpoint-relay clearance threshold | 60 m | 120 m | 240 m |
|---|---:|---|---|---|
| 80 m at 40% baseline (baseline) | 100 m | blocked | clear | clear |
| 60 m at 40% baseline | 75 m | blocked | clear | clear |
| 100 m at 40% baseline | 125 m | blocked | blocked | clear |
| 80 m at 30% baseline | 133.333 m | blocked | blocked | clear |
| 80 m at 45% baseline | 88.889 m | blocked | clear | clear |

The thresholds are computed from the first-hop line geometry; they were not fitted to the classifier. The existing clear-reference and baseline-screen +12 dB bounded adverse-loss runs remain separate propagation scenarios.

## Results

Baseline obstructed-reference result, counted once per separation × dwell × altitude mission case:

| State | Unique cases |
|---|---:|
| DIRECT_SUFFICIENT | 0 |
| RELAY_BENEFICIAL_AND_FEASIBLE | 18 |
| MASS_CLOSED_PRACTICAL_CONSTRAINT_FAILURE | 6 |
| RELAY_FUNCTIONAL_VEHICLE_RESOURCE_FAILURE | 6 |
| RELAY_CONNECTIVITY_INFEASIBLE | 60 |

The compact primary-only obstruction sensitivity is written to `analysis/results/obstruction-sensitivity.csv`.

| Screen scenario | Feasible | Practical-boundary failure | Resource failure | Connectivity infeasible |
|---|---:|---:|---:|---:|
| 80 m at 40% baseline | 18 | 6 | 6 | 60 |
| 60 m at 40% baseline | 18 | 6 | 6 | 60 |
| 100 m at 40% baseline | 9 | 3 | 3 | 75 |
| 80 m at 30% baseline | 9 | 3 | 3 | 75 |
| 80 m at 45% baseline | 18 | 6 | 6 | 60 |

The modeled altitude outcomes shift exactly with the calculated threshold ordering. A threshold below 120 m leaves the 120 m and 240 m state boundaries unchanged; a threshold above 120 m blocks that altitude and leaves only the 240 m layer link-functional. This is a useful null finding: lower-height or later-position screens still leave 60 m below the clearance threshold, so the tested altitude grid does not distinguish them from the baseline.

At cleared relay altitudes, 30/40/60 km fail relay link margin. At 5/10/20 km, 10–30 minute dwell is relay-beneficial with modeled carrier feasibility; 45-minute dwell has finite analytical model closure but lies outside exploratory vehicle-class analysis boundaries; 60-minute dwell has mathematical nonclosure.

The baseline-obstructed +12 dB sensitivity leaves 6 feasible cases, 2 finite/practical failures, 2 nonclosures, and 80 connectivity failures. This is a bounded deterministic stress case, not a propagation prediction.

Secondary payload sensitivity produces the same coarse baseline state boundaries for all three payload cases. This supports only the narrow null result that payload SWaP did not move these coarse boundaries under the declared service assumptions.

## Classification and counting

First applicable gate wins: direct sufficient, relay connectivity failure, mathematical nonclosure, finite closure outside practical boundaries, then relay benefit with physical-boundary pass. The retained `RELAY_BENEFICIAL_AND_FEASIBLE` identifier means only the last of these; it is not the standalone carrier `FEASIBLE` class (which also tests cost and battery fraction), approved requirements compliance, or operational mission success. `RELAY_FUNCTIONAL_VEHICLE_RESOURCE_FAILURE` means mathematical nonclosure of this model.

Counts partition 90 deterministic grid cases, not probabilities or independent observations. Connectivity failure can conceal a simultaneous carrier failure. Before connectivity gating, each primary scenario has 54 physical-boundary passes, 18 finite practical exclusions, and 18 nonclosures; the baseline gate exposes only 6 finite exclusions and 6 nonclosures. JSON reports these separate counts and CSV retains carrier flags. The 1,890 rows include secondary payloads and scenario repetitions.

## Carrier reporting and boundaries

The carrier solver distinguishes numerical convergence, finite analytical model closure, nonclosure, guard events, and practical-boundary failure. A valid affine closure is reported as the analytical model state even if relaxation has not reached tolerance. Nonclosing cases have no finite model state and no reported mass, power, energy, battery, rotor, or cost result; the explicitly named last iterate is a numerical diagnostic only.

Numerical timeout cannot change finite-state burden or either classifier. Sensitivity scores combine three Spearman correlations (mass, cost, burden) by RMS, conditional on the 2,605 finite closures out of 4,096 candidates; they do not rank causes of nonclosure.

The 15 kg gross-mass ceiling, 0.75 m equivalent rotor-diameter ceiling, and 1.5 m footprint proxy remain explicitly exploratory analysis boundaries, not vehicle requirements, selected-design limits, or validation results.

Span is defined as twice equivalent rotor diameter: the 1.5 m span and 0.75 m rotor limits are redundant, not independent constraints. At reference disk loading the rotor bound implies approximately 10.81 kg, tighter than the 15 kg ceiling. Large finite masses near the affine singularity are mathematical extrapolations, not proposed aircraft.

## Validation status

The public-aircraft comparison is a vehicle-scale sanity check, not aircraft validation. It has no matched mission, calibration, residual, or endurance-prediction basis.

## Findings supported by calculations

- In the declared stylized screen family, relay clearance altitude moves according to screen height and location rather than being unique to the baseline screen.
- The transition from blocked to clear visibility can be an architecture decision boundary; after clearance, link margin and endurance/practical boundaries determine the remaining feasible region.
- Under the declared baseline assumptions, 120 m and 240 m restore visibility whereas 60 m does not; in the two higher-threshold variants, 120 m does not restore visibility and 240 m does.
- Endurance and exploratory practical vehicle boundaries materially shrink the link-functional region.
- The bounded adverse-loss case materially shrinks the declared reference result.

## Claims not supported

- Terrain restoration in real geography, general propagation performance, real-world availability, selected payloads, aircraft validation, authorization, interoperability, airworthiness, or mission-success probability.
- Optimal altitude, relay position, screen geometry, payload selection, or a universal low-cost claim.
- A claim that the selected screen cases represent observed terrain, obstacles, or obstacle prevalence.

## Stop gate

The existing research scope remains frozen. The paper framing now centers the relay aircraft and uses the completed analyses as evidence. No terrain data, higher-fidelity RF model, optimization, new vehicle or payload families, or parameter tuning is needed for this bounded argument. Affordability, physical validation, operational performance, and broader mission-feasibility claims remain unresolved.
