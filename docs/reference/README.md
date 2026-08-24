# Engineering Reference

[Overview](../../README.md) · [Architecture](../architecture.md) · [Feasibility](../feasibility.md) · [Engineering Status](../engineering-status.md) · **Reference**

Use this layer for complete inventories, identifiers, traceability, verification detail, model status, and source/evidence audit. The [structured model](../../model/) remains authoritative; these pages make it easier to inspect.

| Need to inspect… | Reference |
|---|---|
| System requirements and deferred topics | [Requirements](requirements.md) |
| External, internal, payload-boundary, and future interfaces | [Interfaces](interfaces.md) |
| Representative and complete model relationships | [Traceability](traceability.md) |
| Model review, analysis, physical verification, and conformance status | [Verification](verification.md) |
| Owner decisions, engineering gaps, deferrals, and next actions | [Decisions and Gaps](decisions-and-gaps.md) |
| Detailed trade reasoning | [Trade Studies](trade-studies.md) |
| Equations, sources, sweeps, convergence, and quantitative limitations | [Feasibility Analysis](feasibility-analysis.md) |
| ID-rich architecture diagrams and interface inventory | [Architecture Atlas](architecture-atlas.md) |
| Generated baseline state | [Baseline](baseline.md) |
| Old-to-new requirement key mapping | [Requirement ID Migration](requirement-id-migration.md) |
| Historical work packages and communication passes | [Archive](../archive/README.md) |

Direct authority and reproducibility links:

- [`model/system.yaml`](../../model/system.yaml) — scope, status, manifests, and ID scheme;
- [`model/architecture.yaml`](../../model/architecture.yaml) — configurations, behavior, resources, interfaces, and modes;
- [`model/assurance.yaml`](../../model/assurance.yaml) — requirements, deferred topics, hazards, controls, verification, trade studies, and decisions;
- [`model/traceability.yaml`](../../model/traceability.yaml) — complete relationships and gaps;
- [`.seal/sources.yaml`](../../.seal/sources.yaml) and [`.seal/proof.yaml`](../../.seal/proof.yaml) — source and evidence records; and
- [`analysis/`](../../analysis/) — executable feasibility inputs, model, and results.
