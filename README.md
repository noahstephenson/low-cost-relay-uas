# Low-Cost Attritable Communications Relay UAS

A small multirotor uncrewed aircraft system—the Relay UAS—carries a communications
relay to a useful airborne position, extending command and telemetry reach when
distance or terrain obstructs a direct link.

**Study result:** a plausible short-dwell, modest-payload design region exists under
exploratory assumptions; longer dwell creates a reinforcing battery–mass–power
penalty. **Current maturity:** coherent architecture and reproducible analysis, but
no verified or approved physical aircraft.

## The project in one picture

![The Relay UAS in one picture](reports/figures/project-in-one-picture.svg)

The aircraft has its own blue command-and-health path. Green mission traffic passes
through a separate black-box relay payload, so the payload does not control the
aircraft carrying it.

## What this project is

The aircraft positions the relay between ground control and a remote aircraft when
the direct path is too long or blocked by terrain.

The aircraft has its own command link so an operator can position and recover it.
That platform-control link is deliberately separate from the mission traffic passing
through the relay payload. Losing relay service therefore does not automatically
mean losing control of the relay aircraft.

This project defines the carrier aircraft, its boundary with the payload, its major
subsystems and interfaces, its mission behavior, and its feasibility. It deliberately
leaves the payload's internal radio design outside the current architecture.

## How the system works

1. The Relay UAS is prepared in a ground-safe state.
2. Its operator launches it and commands it to a useful airborne station.
3. The aircraft holds that position using its flight-control and navigation system.
4. Ground-originated remote-aircraft command passes through the black-box relay
   payload.
5. Remote-aircraft telemetry returns through the same payload in the opposite
   direction.
6. Aircraft health and operating status support repositioning or recovery decisions.
7. If relay service is degraded, the architecture intends to preserve the independent
   aircraft-control path and transition toward recovery. Exact recovery logic and
   physical performance are not yet established.

## What is on the drone

| Subsystem group | Plain-language role |
|---|---|
| Airframe and structure | Carries the aircraft, propulsion system, avionics, and payload support hardware. |
| Propulsion | Produces and controls lift through motors, controllers, and propellers. |
| Electrical power | Stores energy, distributes main-bus power, and provides regulated branches. |
| Flight avionics | Stabilizes and navigates the aircraft, receives platform command, and supports health/status reporting. |
| Payload support | Provides mechanical retention and regulated electrical power to the payload. |
| Relay payload | Passes mission communications between external endpoints; its internal RF design remains outside this project. |

The proposed platform-to-payload boundary has only two crossings: regulated power
and mechanical retention. No platform-to-payload data connection is part of the
current candidate.

## What the project learned

### Architecture result

The current candidate has a coherent boundary, mission thread, subsystem
decomposition, power and information paths, modes, requirements, and traceability.
Internal model review found no structural failure while keeping known gaps visible.

### Feasibility result

The concept appears physically and economically plausible in a limited region:
comparatively short dwell and modest payload under reference-or-better assumptions.
Increasing endurance creates a reinforcing battery–mass–power penalty. In the
reference analysis, the evaluated 45–60 minute cases fall outside the conditional
credible region.

![Conditional feasibility region](analysis/results/feasible-region.svg)

This is not an exact aircraft prediction. The boundaries are exploratory, owner
targets remain unset, packaging geometry is unresolved, and the model uses broad
component-class ranges rather than selected hardware.

## Engineering status at a glance

![What the project actually established](reports/figures/engineering-status.svg)

The architecture and analysis are established project results. Detailed radio design
and future system-of-systems concepts are deliberate scope limits. Physical aircraft
verification, external-interface conformance, owner targets, and baseline approval
still require future work.

## What comes next

### Requires decisions or evidence

- Set quantitative targets for payload service, endurance, affordability,
  portability, operating conditions, and recovery policy.
- Select and size hardware, then verify flight behavior, performance, power,
  retention, recovery, and safety-relevant claims on a physical aircraft.
- Obtain external specifications and authority before claiming endpoint or spectrum
  conformance.
- Approve a technical baseline only after those decisions and evidence exist.

### Deliberately outside the current project

- Internal relay waveform, radio-frequency, and antenna implementation.
- Future digital-payload, uncrewed-ground-vehicle, network-service, and broader
  command-and-control system-of-systems implementation.

---

## Technical detail and traceability

The sections above are the five-minute orientation. From here, names remain primary
but stable model identifiers are shown for engineering audit and handoff.

### Reference, current, and future configurations

- **Recovered reference:** evidence from the disassembled system; incomplete and not
  the design baseline.
- **Current candidates:** a functional-replica architecture and a domestic-sourcing
  variant. Both remain proposed and unapproved.
- **Future concepts:** digital-payload and wider command-and-control ecosystem
  extensions. They do not change the current candidate.

### Requirement intent

The detailed catalog contains 28 stable `REQ-*` records. At a glance, they require
the candidate to relay command and telemetry, maintain and recover the aircraft,
support a replaceable payload with power and retention, preserve independent
platform command and health/status, remain portable and affordable subject to
owner-set targets, and maintain basic ground and stored-energy safeguards. RF
implementation, spectrum authorization, contested-spectrum mechanisms, and export
review remain deferred or externally owned.

See [architecture.md](architecture.md#8-key-requirements) for the grouped translation
and `model/assurance.yaml` for authoritative wording and metadata.

### Traceability example

In plain language:

`Extend remote control reach → provide an airborne relay → relay outbound command → allocate that behavior to the black-box payload → cross the external relay path → review the architecture now and verify external compatibility later`

The corresponding audit trace is:

`NEED-001 → CAP-001 → SCN-003 → OA-004 → FUN-REL-01 → CMP-COM-01 → IFC-EXT-001/002 → REQ-FUN-001 → VER-001/009`

Two more representative threads appear in
[architecture.md](architecture.md#9-representative-traceability-threads). The full
relationship set remains in `model/traceability.yaml`.

## Where the authoritative model lives

`system.yaml` is the manifest. Structured catalogs are authoritative; Markdown and
generated figures are views. If a view disagrees with the catalogs, the view is
defective.

- [`model/architecture.yaml`](model/architecture.yaml): configurations, mission
  context, scenarios, functions, components, interfaces, and modes.
- [`model/assurance.yaml`](model/assurance.yaml): requirements, hazards, controls,
  verification methods, trade studies, and decisions.
- [`model/traceability.yaml`](model/traceability.yaml): relationships and explicit
  gaps.
- [`.seal/sources.yaml`](.seal/sources.yaml): source and authority registry.
- [`.seal/proof.yaml`](.seal/proof.yaml): claim and evidence registry.

## Human and generated views

- [`architecture.md`](architecture.md): progressive engineering explanation and the
  core communication figures.
- [`trade-studies.md`](trade-studies.md): substantive engineering trade reasoning.
- [`reports/feasibility-analysis.md`](reports/feasibility-analysis.md): detailed
  coupled feasibility model, assumptions, results, and limitations.
- [`reports/architecture-decision-target-package.md`](reports/architecture-decision-target-package.md):
  owner decision and target package; unresolved recommendations are not approvals.
- [`reports/architecture-views.md`](reports/architecture-views.md): generated
  ID-rich engineering audit views and complete interface inventory.
- [`reports/baseline.md`](reports/baseline.md): generated status, decisions, gaps,
  verification, and traceability summary.

## Reproduce and validate

```bash
python scripts/generate-communication-views.py
python scripts/generate-mermaid-views.py
python scripts/validate-baseline.py --check-generated
python analysis/feasibility.py --check
```

Continuous integration runs the same generated-file, model, and feasibility checks.

## Explicit scope boundaries

This repository does not provide RF implementation parameters, antenna design,
component selection, fabrication, assembly, integration, operating instructions,
flight-test instructions, weapons content, exact recovered-component replication,
or claims of Modular Open Systems Approach compliance, interoperability, resilience,
security, airworthiness, safety, operational readiness, or Unified Architecture
Framework conformance.

The model uses selected Unified Architecture Framework terminology but does not claim
full UAF or Department of Defense Architecture Framework conformance. The
terminology/version decision remains open.

## License

See [`LICENSE`](LICENSE).
