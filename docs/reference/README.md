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

## How the repository produces its evidence

Use this layer after the overview, architecture, feasibility, and engineering-status pages. IDs are stable lookup keys: `CMP` denotes a component, `IFC` an interface, `REQ` a requirement, `VER` a verification activity, and `GAP` an unresolved issue. An allocated verification activity is not evidence that a physical test passed.

| Source | Transformation | What to inspect |
|---|---|---|
| Architecture and assurance catalogs | View/report generators | Subsystem relationships, requirements, interfaces, and recorded dispositions |
| Carrier and mission assumptions | Executable analysis models | Conditional numerical results and classification flags |
| Source/evidence registers | Traceability and consistency checks | What supports a claim, and which gaps remain |

The architecture catalogs and numerical research form related evidence layers; they are not a fully integrated executable proof of mission performance. Generated views inherit their sources' limitations. Introductory prose explains the model and is maintained editorially; generated reports and figures are changed through their generators.

## Regenerate, then check

```bash
python scripts/generate-communication-views.py
python scripts/generate-mermaid-views.py
python analysis/feasibility.py
python analysis/mission_connectivity.py
python analysis/validation/validate_vehicle_scale.py
python scripts/validate-baseline.py --write-reports
python -B -m unittest discover -s tests -v
python scripts/validate-baseline.py --check-generated
```

For Mermaid syntax/render checks, use the repository-pinned Mermaid CLI 11.4.1 and `python scripts/generate-mermaid-views.py --check --validate-syntax`. A skipped parser is not a successful syntax check.

For the publication argument, read the [short argument test](paper-argument-test.md). For the scope and assumptions behind the results, return to [research status](../IEEE_AERO_2027_RESEARCH_STATUS.md). Historical work stays in the [archive](../archive/README.md); it does not supersede current model records.

The [readability review](readability-review.md) records diagram coverage, checks, and presentation limits.
