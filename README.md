# Low-Cost Communications Relay UAS

This project studies a small multirotor uncrewed aircraft that carries a communications relay to an airborne position. Elevation can restore a path that terrain or distance blocks at ground level. The relay is treated as a black-box payload, while the carrier aircraft keeps its own independent command-and-control path.

![System concept showing independent aircraft control and relayed mission traffic](docs/figures/project-in-one-picture.svg)

## What the system does

An operator launches and positions the Relay UAS between ground control and a remote aircraft. Ground-originated command passes through the relay payload toward the remote aircraft, and telemetry returns through the payload in the opposite direction.

The carrier does not interpret that mission traffic at this architecture level. Its flight avionics, navigation, electrical power, propulsion, and platform communications support the aircraft itself. The payload receives regulated power and mechanical retention from the platform, but no platform-to-payload data connection is part of the current candidate.

That separation is deliberate. Loss of relay service should not automatically remove control of the aircraft carrying it. The architecture defines a degraded relay state and recovery intent, while leaving detection thresholds, detailed recovery logic, and physical performance for later engineering and test.

## What the study found

The concept appears plausible in a limited short-dwell, modest-payload region under exploratory component-class assumptions. The result is driven by a coupled loop: more endurance needs more battery energy; more battery increases mass; more mass increases hover power; and higher power demands still more battery.

The reference analysis found feasible or marginal cases at shorter dwell times, with a payload-sensitive transition around the middle of the evaluated range. All evaluated 45- and 60-minute reference cases fell outside the conditional credible region. This is a design-space result, not a prediction for selected hardware and not proof that an owner requirement has been met.

## Engineering status

| Area | Current status |
|---|---|
| System architecture | Established at model level |
| Functional decomposition | Established |
| Interface architecture | Established at logical level |
| Feasibility analysis | Reproducible and exploratory |
| Quantitative design targets | Pending owner decisions |
| Hardware selection | Not established |
| Physical prototype verification | Not performed |
| External interoperability or conformance | Not verified |
| Technical baseline | Not approved |

The repository distinguishes a structurally valid model from a verified aircraft. Passing the automated checks confirms internal consistency and generated-artifact freshness; it does not establish safety, airworthiness, endpoint compatibility, operational readiness, or approval.

## Explore the engineering

| If you want to know… | Read |
|---|---|
| How the system is designed and behaves | [Architecture](docs/architecture.md) |
| Whether the concept appears physically plausible | [Feasibility](docs/feasibility.md) |
| What is established, unresolved, or unverified | [Engineering Status](docs/engineering-status.md) |
| Requirements, interfaces, traceability, verification, decisions, and evidence | [Engineering Reference](docs/reference/README.md) |
| The authoritative structured definition | [Model catalogs](model/) |
| The executable quantitative work | [Analysis](analysis/) |

## Reproduce and validate

The model and views use Python’s standard library. From the repository root:

```bash
python scripts/generate-communication-views.py
python scripts/generate-mermaid-views.py
python analysis/feasibility.py
python scripts/validate-baseline.py --write-reports
python scripts/validate-baseline.py --check-generated
```

Continuous integration runs the generated-file, model, and feasibility checks. The commands regenerate deterministic Markdown, SVG, CSV, and JSON artifacts from the versioned model and analysis inputs.

## Scope note

The current project defines the relay-aircraft architecture and a conditional feasibility envelope. It does not select components; define payload frequency, waveform, protocol, transmit power, link budget, or antenna design; provide fabrication or flight-test instructions; or claim interoperability, spectrum authorization, safety certification, airworthiness, operational readiness, Modular Open Systems Approach compliance, Unified Architecture Framework conformance, or an approved technical baseline. See [Engineering Status](docs/engineering-status.md) for the remaining work and [`LICENSE`](LICENSE) for licensing.
