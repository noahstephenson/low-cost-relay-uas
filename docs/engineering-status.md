# Engineering Status

[Overview](../README.md) · [Architecture](architecture.md) · [Feasibility](feasibility.md) · **Engineering Status** · [Reference](reference/README.md)

The project has a coherent model-level architecture, complete logical interface inventory, explicit requirements and traceability, and a reproducible exploratory feasibility analysis. It does not yet have owner-approved quantitative targets, selected hardware, a physically verified aircraft, external conformance evidence, or an approved technical baseline.

![Engineering maturity separated into established work, scope limits, and missing evidence](figures/engineering-status.svg)

The current semantic model is `0.9.0-baseline-candidate`. The latest recorded model-review evidence remains tied to the 0.8.0 model and was not owner-accepted. The identifier and documentation migration does not rewrite that evidence or create a new approval record.

## Established

| Area | What is established | Boundary |
|---|---|---|
| System boundary | Carrier aircraft, black-box payload, external actors, and future context are separated. | Model definition only |
| Functional architecture | Current mission, aircraft-control, relay, health/status, power, and configuration functions are allocated. | Proposed candidate behavior |
| Physical architecture | Nineteen component roles are grouped into platform and payload responsibilities. | No component selection |
| Interfaces | Twenty-two logical interfaces have endpoints, direction, flow class, scenarios, failure meaning, and unknown attributes. | No external conformance |
| Requirements | Twenty-three requirements use neutral stable IDs and human-readable names. | Most retain TBD, physical, or external limitations |
| Deferred topics | Five external or deliberately deferred topics are explicit and separate from requirements. | No satisfaction claim |
| Traceability | Needs, capabilities, scenarios, functions, resources, interfaces, requirements, hazards, controls, verification, decisions, and gaps are connected. | Candidate relationships remain candidate |
| Feasibility | Coupled mass–power–battery–endurance–cost behavior is executable and reproducible. | Exploratory assumptions only |

Repository validation establishes structural consistency and generated-artifact freshness. It does not establish aircraft safety, performance, or approval.

## Proposed but unresolved

- Maintain commanded station position (REQ-003) has unresolved horizontal and vertical tolerances.
- Return on low-battery condition (REQ-005) has no approved threshold or reserve/recovery policy.
- Provide on-station endurance (REQ-010), limit system unit cost (REQ-009), and accommodate payload envelope (REQ-012) remain coupled owner targets.
- The regulated payload-power envelope, retention load basis, and retention margin remain undefined.
- Aircraft health/status purpose is modeled, but minimum content, transport, and owner acceptance remain open.
- The domestic-sourcing candidate preserves architecture roles but has no approved sourcing policy or substitutions.

## Requires owner decisions

| Decision | Current state | Why it matters |
|---|---|---|
| Select the standards terminology/version posture (DEC-002) | Proposed | Determines whether UAF 1.2 language is retained, made version-neutral, or migrated later; no conformance is claimed. |
| Select the architecture-level safety objective for uncontrolled descent (DEC-003) | Proposed | A control or mitigating requirement must not be invented before the objective is accepted. |
| Accept or revise the health/status thread (DEC-004) | Proposed | The current logical thread is coherent, but content and implementation remain undefined. |
| Confirm affordability/attritability as a cross-cutting constraint (DEC-005) | Proposed | Prevents creation of a synthetic mission activity while numerical targets remain open. |
| Set quantitative design targets | Not recorded | Payload, endurance, portability, cost, environment, reserve, and recovery targets drive the coupled design space. |

Only the project-scope and baseline-candidate constraint decision is approved. The remaining decisions are not.

## Requires physical evidence

No physical prototype verification has been performed. Future evidence must address, at minimum:

- measured mass and packaging fit;
- propulsion and hover performance;
- electrical loading, regulation, protection, and thermal behavior;
- payload retention under an approved load basis;
- station keeping and operation without assuming continuous GNSS;
- low-battery and payload-loss recovery behavior;
- armed-state indication and ground-safe arming behavior;
- transport and launch by one operator; and
- relevant safety behavior under defined conditions.

The recovered-reference mapping is role-level only. Missing original evidence and a known local source-checksum mismatch remain explicit; they are not repaired by changing a registry hash.

## Requires external authority or specifications

The seven external logical interfaces lack authoritative endpoint specifications and execution evidence. A future authority must define and accept the relevant basis before the project can claim platform-command, health/status, relay-endpoint, or maintenance-interface conformance.

Spectrum authorization, antenna characteristics, relay waveform/protocol/link-budget definition, contested-spectrum mechanisms, and export-control review are deferred or externally owned topics. They remain visible as DEF records without being counted as system requirements.

## Deliberate scope exclusions

The repository does not provide payload RF implementation, component selection, fabrication, assembly, operating procedures, flight-test instructions, weapon integration, or a deployable communications-system specification. Future ground-vehicle, video/sensor-data, digital-payload, and broad system-of-systems implementation remain outside the current candidate.

## Key engineering gaps

| Gap | Current disposition |
|---|---|
| Uncontrolled-descent hazard lacks an accepted control objective | Owner decision required |
| External interface authority and conformance evidence are missing | External evidence required |
| Mass, cost, endurance, payload, and power targets remain coupled and unapproved | Quantitatively narrowed; owner decision required |
| Physical performance and recovery evidence are absent | Physical evidence required |
| Exact recovered-article equivalence is unsupported | Role mapping complete; exact reconstruction unresolved |
| Future ground-vehicle and sensor-data threads are incomplete | Future configuration only |

See [Decisions and Gaps](reference/decisions-and-gaps.md) for every current gap and next action.

## Recommended next engineering work

1. Obtain owner dispositions for the four proposed decisions and the coupled quantitative target package.
2. Re-run the feasibility model against those authorized targets and supported component-class evidence.
3. Close payload packaging, electrical, retention, and environment envelopes before selecting hardware.
4. Develop a physical candidate and verification plan with explicit safety and external-authority roles.
5. Execute physical and external verification without using model-review evidence as a substitute.
6. Approve a technical baseline only after the required decisions and evidence exist.

For audit detail, use [Requirements](reference/requirements.md), [Verification](reference/verification.md), [Interfaces](reference/interfaces.md), the [generated baseline](reference/baseline.md), and the structured [source](../.seal/sources.yaml) and [proof](../.seal/proof.yaml) catalogs.

Next: return to the [Overview](../README.md) or enter the [Engineering Reference](reference/README.md).
