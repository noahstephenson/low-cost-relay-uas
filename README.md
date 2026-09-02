# Low-Cost Communications Relay UAS

This repository is a model-based systems engineering study of a small uncrewed aircraft that carries a modular communications relay to an advantageous airborne location. It explores the aircraft around the payload; it does not design the payload's radio implementation.

![System concept showing independent aircraft control and relayed mission traffic](docs/figures/project-in-one-picture.svg)

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

The aircraft does not interpret the relayed mission traffic. The current platform-to-payload boundary is limited to regulated power and mechanical retention, so a loss of relay service need not remove aircraft control.

## Mission

The operating concept is deliberately simple: **Prepare → Launch → Transit → Establish relay position → Relay → Monitor → Recover.**

This is an architecture sequence, not an operating procedure. It describes the behavior the study must support while leaving detailed readiness criteria, flight-control logic, and recovery thresholds for later engineering.

## What the system must accomplish

The requirements are organized around relay service, station keeping, aircraft control and recovery, payload support, power and safety, and portability and affordability. The requirements that most strongly shape the design are the payload envelope, useful on-station endurance, gross mass, cost, battery reserve and recovery behavior, and single-operator handling.

Several of those targets are intentionally still open. The study uses ranges to understand their consequences; it does not convert those ranges into approved requirements.

## Architecture

The physical architecture combines an airframe, four-corner propulsion, stored energy and power distribution, flight avionics and navigation, a dedicated platform-command path, payload support, and the relay payload. The payload remains a black box, while the carrier architecture makes its support and control responsibilities explicit.

Read [Architecture](docs/architecture.md) for the system boundary, mission behavior, information paths, power flow, and degraded behavior.

## The engineering problem

Endurance is not a simple battery-capacity choice. Payload mass and power affect aircraft mass and electrical demand. More endurance requires more battery energy; the larger battery increases gross mass; greater mass increases hover power; and that extra power increases the battery demand again.

The feasibility model iterates this feedback loop. It treats gross mass as an output of the coupled design problem rather than a number chosen independently at the start.

## What the study found

The analysis identifies a limited plausible region for modest payloads and short on-station dwell under exploratory, component-class assumptions. In the reference 50 W payload slice, shorter dwell cases are generally feasible or marginal, 30-minute cases reach a payload-sensitive transition, and every evaluated 45- and 60-minute case is infeasible under the model's analysis boundaries.

This is a conditional feasibility result, not a selected aircraft or proof that an owner requirement has been met. The main conclusion is straightforward: longer hover time becomes increasingly difficult because of the battery–mass–power feedback.

## What remains unresolved

- The owner must set the payload service, endurance, portability, affordability, environment, reserve, and recovery targets together.
- Payload packaging, electrical-service, and retention-load envelopes remain open.
- No hardware has been selected, and no prototype, physical verification, or external-interface conformance evidence exists.
- Relay frequency, waveform, protocol, link budget, antenna design, and spectrum authorization are outside this study.

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
python scripts/validate-baseline.py --write-reports
python scripts/validate-baseline.py --check-generated
```

## Scope note

This study defines a relay-aircraft architecture and a conditional feasibility envelope. It does not select components; define payload radio details; provide fabrication, flight-test, or operating instructions; or claim interoperability, spectrum authorization, safety certification, airworthiness, operational readiness, standards conformance, or an approved technical baseline. See [Engineering Status](docs/engineering-status.md) for the remaining work and [`LICENSE`](LICENSE) for licensing.
