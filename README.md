# Low-Cost Communications Relay UAS

This repository studies a small multirotor communications relay UAS: its mission role, subsystem responsibilities, payload interfaces, and resource limits. Executable models assess the architecture under declared mission assumptions.

**Paper title:** System Architecture and Mission Feasibility of a Multirotor Communications Relay

The study targets IEEE Aerospace 2027, Track 13.01. Examination of a recovered relay aircraft provides background motivation only. The paper does not reconstruct that aircraft or depend on its provenance or measured performance.

**Research question:** What architecture lets a small multirotor support airborne relay service, and under what declared mission demands does that architecture remain plausible?

![System concept showing logically separate aircraft control and relayed mission traffic](docs/figures/project-in-one-picture.svg)

## The problem

Ground systems do not always have a useful direct communications path to a remote aircraft. Terrain, distance, and line-of-sight geometry can block or weaken that path. An airborne relay can improve the geometry by carrying a communications payload above the obstruction or between the endpoints.

The engineering question is whether a small, portable aircraft can do that without becoming too heavy, power-hungry, costly, or difficult to recover.

## What the system does

The Relay UAS carries the black-box relay payload to a useful position and holds that position while the payload passes mission traffic between ground control and a remote aircraft. The carrier supplies lift, navigation, electrical power, payload retention, and its own recovery capability.

Two information paths are intentionally separate:

| Path | Purpose |
|---|---|
| Aircraft command and control | Lets the operator launch, position, monitor, and recover the Relay UAS. |
| Relayed mission traffic | Passes remote-aircraft commands outward and telemetry back through the payload. |

Three commitments define the proposed architecture: a black-box relay payload, explicit mechanical and electrical payload support, and logically separate carrier control and relay traffic. The carrier does not use relayed mission traffic to fly itself. Separation is architectural intent, not demonstrated failure isolation: shared power, physical dependencies, and control-link performance remain unresolved.

## Mission

The operating concept is deliberately simple: **Prepare → Launch → Transit → Establish relay position → Relay → Monitor → Recover.**

This is an architecture sequence, not an operating procedure. The quantitative assessment covers only stationary Ground → Relay → Remote service during hover dwell. Transit, recovery energy, reverse-link service, and carrier-control performance are not quantitatively established.

## Architecture

The aircraft allocates lift, energy, navigation, carrier control, and payload-support responsibilities. Quantitative owner targets and component selections remain open. Read [Architecture](docs/architecture.md) for subsystem roles, interfaces, and the evidence supporting them.

## Why endurance is coupled

More dwell requires more battery energy; added battery mass raises hover power and battery demand again. The model treats gross mass as an output, using branch-consistent analytical closure and numerical iteration as a verification diagnostic.

## What the study found

The primary relay-UAS study evaluates 90 separation × dwell × altitude cases with a 0.20 kg payload and a constant 14 W electrical sizing allowance. Its baseline screen scenario produces **18 relay-beneficial physical-boundary passes, 6 finite practical exclusions, 6 mathematical nonclosures, and 60 connectivity failures**. The +12 dB sensitivity produces **6 / 2 / 2 / 80**, respectively. These hierarchical counts describe the declared grid, not success probabilities.

At 10 km endpoint separation and 120 m relay altitude in the baseline scenario, 30-minute dwell gives an 8.6203 kg analytical carrier that passes exploratory physical bounds; 45 minutes gives a finite 106.2456 kg result outside those bounds; 60 minutes has no finite closure. The large finite result is an extrapolation, not a proposed aircraft.

The outcomes distinguish connectivity failure, finite carrier burden, and mathematical nonclosure. The broader carrier sweep provides supporting sensitivity analysis. Affordability and operational performance remain unestablished.

Read the [architecture-to-evidence assessment](docs/architecture.md#architecture-to-evidence-assessment), [feasibility interpretation](docs/feasibility.md), and [paper research status](docs/IEEE_AERO_2027_RESEARCH_STATUS.md).

## What remains unresolved

- The owner must set the payload service, endurance, portability, affordability, environment, reserve, and recovery targets together.
- Payload packaging, electrical-service, and retention-load envelopes remain open.
- No hardware has been selected, and no prototype, physical verification, or external-interface conformance evidence exists.
- A low-order link budget uses declared service and antenna-gain assumptions to screen connectivity. Radio implementation, waveform/protocol design, installed antenna performance, and spectrum authorization remain outside the demonstrated evidence.

## Engineering status

| Area | Current position |
|---|---|
| Architecture, functions, and logical interfaces | Defined at the model level |
| Feasibility analysis | Reproducible and exploratory |
| Quantitative design targets and hardware | Not established |
| Physical verification and external conformance | Not performed or not available |
| Technical baseline | Not approved |

Automated checks confirm the model is internally consistent and its generated files are current. They do not establish safety, airworthiness, endpoint compatibility, operational readiness, or approval.

## Explore the engineering

| If you want to know… | Read |
|---|---|
| How the system works | [Architecture](docs/architecture.md) |
| Whether the concept closes quantitatively | [Feasibility](docs/feasibility.md) |
| What is established and what the next phase must do | [Engineering Status](docs/engineering-status.md) |
| Detailed requirements, interfaces, traceability, decisions, verification, and evidence | [Engineering Reference](docs/reference/README.md) |
| The structured source of record | [Model catalogs](model/) |
| The executable feasibility model and results | [Analysis](analysis/) |

## Reproduce and validate

The model and views use Python's standard library. From the repository root:

```bash
python scripts/generate-communication-views.py
python scripts/generate-mermaid-views.py
python analysis/feasibility.py
python analysis/validation/validate_vehicle_scale.py
python analysis/mission_connectivity.py
python -m unittest discover -s tests -v
python scripts/validate-baseline.py --write-reports
python scripts/validate-baseline.py --check-generated
```

## Scope note

This study defines a relay-aircraft architecture and a conditional feasibility envelope. It does not select components, define payload radio details, provide fabrication, flight-test, or operating instructions, or claim interoperability, spectrum authorization, safety certification, airworthiness, operational readiness, standards conformance, or an approved technical baseline. See [Engineering Status](docs/engineering-status.md) for the remaining work and [`LICENSE`](LICENSE) for licensing.
