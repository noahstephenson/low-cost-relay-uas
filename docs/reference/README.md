# Engineering Reference

[Overview](../../README.md) · [Architecture](../architecture.md) · [Feasibility](../feasibility.md) · [Engineering Status](../engineering-status.md) · **Reference**

The primary documents explain the study in plain language. Use this layer when you need complete inventories, identifiers, evidence records, or the full reasoning behind a decision. The structured [model](../../model/) is the source of record; these pages make it easier to inspect.

## Start with the engineering question

| Question | Reference |
|---|---|
| What must the current system do, and which targets are still open? | [Requirements](requirements.md) |
| How do commands, telemetry, power, and payload support cross the architecture? | [Interfaces](interfaces.md) |
| What trade has been studied, what remains open, and why? | [Trade Studies](trade-studies.md) |
| What does the quantitative model include and where does it stop? | [Detailed Feasibility Analysis](feasibility-analysis.md) |
| What owner decisions, evidence needs, and future branches remain? | [Decisions and Gaps](decisions-and-gaps.md) |

## Audit and model detail

| Need to inspect… | Reference |
|---|---|
| Requirement, function, component, interface, and evidence relationships | [Traceability](traceability.md) |
| Model review, analysis, physical verification, and conformance status | [Verification](verification.md) |
| ID-rich architecture diagrams and interface inventory | [Architecture Atlas](architecture-atlas.md) |
| Generated baseline state | [Baseline](baseline.md) |
| Old-to-new requirement key mapping | [Requirement ID Migration](requirement-id-migration.md) |
| Historical work packages and communication passes | [Archive](../archive/README.md) |

The model and executable sources are available directly:

- [model/system.yaml](../../model/system.yaml) — scope, status, and generated-view manifest.
- [model/architecture.yaml](../../model/architecture.yaml) — configurations, behavior, resources, and interfaces.
- [model/assurance.yaml](../../model/assurance.yaml) — requirements, deferred topics, hazards, verification, trade studies, and decisions.
- [model/traceability.yaml](../../model/traceability.yaml) — relationship and gap registers.
- [.seal/sources.yaml](../../.seal/sources.yaml) and [.seal/proof.yaml](../../.seal/proof.yaml) — source and evidence records.
- [analysis/](../../analysis/) — feasibility inputs, executable model, and generated results.
