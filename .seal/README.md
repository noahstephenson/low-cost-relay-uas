# SEAL Baseline Workspace

> **Baseline Candidate - Not Approved.** This workspace records source authority,
> claims, proof links, gaps, and human decisions. It does not approve the architecture.

`system.yaml` is the model manifest. The catalogs referenced by that manifest are the
authoritative structured records for this reconciliation work package. Root Markdown
files are human-readable architecture views, and files under `reports/` are generated
views. A disagreement is recorded as a reconciliation issue rather than resolved
silently.

## Catalog syntax

The `.yaml` catalogs use the JSON-compatible subset of YAML 1.2. This keeps the files
valid YAML while allowing `scripts/validate-baseline.py` to use Python's standard
library without adding a YAML-parser dependency. `.seal/sources.yaml` and
`.seal/proof.yaml` conform to SEAL's upstream v2 schemas and use permitted extension
fields for this project's configuration, evidence-basis, and decision-status data.

## Independent classification dimensions

- `evidence_basis` describes why a statement is believed.
- `decision_status` describes whether a human authority has accepted a decision.

Evidence does not imply approval. Approval does not convert an inference into an
observation. Unknowns and intentional deferrals remain visible.

## Safe use of SEAL

SEAL is used here as an assurance and configuration-governance layer. It does not
replace the UAF architecture, infer missing technical values, or authorize physical
testing. The communications payload remains a black box outside architecture-level
interfaces and information exchanges.
