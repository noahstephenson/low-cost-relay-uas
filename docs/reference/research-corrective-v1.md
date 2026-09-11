# Corrective successor record

Working title: **System Architecture and Mission Feasibility of a Multirotor Communications Relay**

Baseline: `2eb84259573cf7e0f216bc11002d65dbdb0f32f3`, tag `relay-uas-research-freeze-v1`. This corrective successor preserves that tag and the research scope. Recommended successor tag: `relay-uas-research-corrective-v1`.

## Corrections and rationale

- Finite analytical closure now determines standalone burden and conditional class independently of numerical convergence. Previously a finite solution could receive an arbitrary burden of 10 and fail classification solely because iteration timed out. Numerical convergence and guard events remain diagnostics; nonclosure still has no physical state.
- Primary PAY-MESH-OEM DC demand changes from 5 W to 14 W for all dwell and battery-power calculations. The [manufacturer product page](https://doodlelabs.com/product/oem/) (checked 2026-09-11) identifies 5 W as receive consumption and 14 W as peak consumption. Constant 14 W is an upper-load sizing assumption, not measured relay average power or validation of a simultaneous RF/DC operating point. The source receive value remains recorded. RF output, payload mass, and all other scenario inputs are unchanged. Secondary payload assumptions remain exploratory.
- Existing machine state names are retained for compatibility, with explicit definitions and first-applicable-gate precedence. Integrated physical-boundary pass differs from standalone cost/battery-fraction acceptance. JSON now reports carrier counts before connectivity gating; CSV includes the violated practical bounds.
- The architecture map now has distinct cell codes and correctly placed separation labels and units. The dependency diagram depicts the implemented shared-payload screening, not an unimplemented link-margin-to-payload-sizing loop, and is generated and freshness-checked with mission outputs. Sensitivity and mass-growth figure captions distinguish conditional rankings and finite mathematical extrapolations from realizable aircraft.
- Research documentation distinguishes the sampled battery branch switch (20–30 minutes) from the later mass-growth knee, corrects stale costs and sensitivity prose, and explains redundant exploratory rotor/span limits. The vehicle-scale generator wording now agrees with its checked-in report; it remains a sanity comparison, not predictive validation.
- Regression tests exercise truncated numerical iteration, classification precedence, unique cases, primary electrical loading, and headline counts. CI now runs the scientific tests as well as baseline checks.

## Frozen versus corrected results

Order below: relay-beneficial physical pass / finite practical exclusion / mathematical nonclosure / connectivity failure.

| Primary scenario | Frozen | Corrected |
|---|---|---|
| Baseline obstructed reference | 18 / 6 / 6 / 60 | 18 / 6 / 6 / 60 |
| Baseline screen +12 dB | 6 / 2 / 2 / 80 | 6 / 2 / 2 / 80 |

No architecture state changes in any of the 1,890 existing rows. The 90 primary cases remain unique separation × dwell × altitude combinations. Before connectivity gating, each primary scenario has 54 finite physical passes, 18 finite exclusions, and 18 nonclosures; these are not additional mission cases or failure probabilities.

| Primary dwell | Frozen mass at 5 W | Corrected mass at 14 W |
|---|---:|---:|
| 10 or 20 min | 5.3827 kg | 5.4170 kg |
| 30 min | 8.4551 kg | 8.6203 kg |
| 45 min | 103.3074 kg | 106.2456 kg |
| 60 min | no finite closure | no finite closure |

The 45-minute masses are extrapolations outside exploratory vehicle boundaries, not design proposals. The correction changes the affine intercept, not the endurance-driven slope or nonclosure boundary.

All 225 standalone grid classes are unchanged; 15 finite-case burden values change. The 4,096-candidate sensitivity study retains 2,605 finite closures and excludes 1,491 nonclosures. Corrected aggregate scores still rank endurance, battery specific power, and payload mass first through third. Rankings are conditional on finite closure and combine mass, cost, and burden correlations; they do not rank causes of nonclosure.

## Verification

Run from the repository root:

```text
python -B -m unittest discover -s tests -v
python -B scripts/validate-baseline.py --check-generated
git diff --check
```

Affected outputs were regenerated with `analysis/feasibility.py`, `analysis/mission_connectivity.py`, and `analysis/validation/validate_vehicle_scale.py`. Old/new comparison uses `git show` at the frozen commit, checks matching row keys, and compares all architecture states and standalone classes. Changed figures were rendered for visual review.

## Remaining publication risks and stop gate

The defensible contribution remains an architecture screening case study with distinct failure mechanisms. Fixed payload assumptions connect two largely separable models; this is not joint radio/vehicle sizing or optimization. Mission feasibility means stationary one-way service within the declared assumptions. It excludes transit/recovery, reverse-link and carrier-control performance, operational propagation, throughput, physical aircraft validation, and success probability. The common service threshold is an assumption; coarse grids do not establish robustness at continuous boundaries.

Exploratory physical limits are not owner requirements. The public-vehicle table cannot establish prediction accuracy, and the formal architecture catalogs are historical governance/traceability artifacts, not a fully integrated executable mission-evidence chain. These limits must remain visible in the paper. No added modeling is necessary for that narrow claim; broader full-mission or validated-performance claims remain unsupported. No terrain, optimization, transit model, new payload family, or expanded experiment was added.
