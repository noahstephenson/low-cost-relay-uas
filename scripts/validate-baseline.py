#!/usr/bin/env python3
"""Validate the consolidated baseline and generate its derived reports.

Catalogs use the JSON-compatible subset of YAML 1.2, so validation and generation
require only the Python standard library. Model validity never implies approval,
verification completion, safety, or operational readiness.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
VIEW_GENERATOR = ROOT / "scripts" / "generate-mermaid-views.py"
COMMUNICATION_GENERATOR = ROOT / "scripts" / "generate-communication-views.py"
BASELINE_REPORT = ROOT / "docs" / "reference" / "baseline.md"
ATLAS_REPORT = ROOT / "docs" / "reference" / "architecture-atlas.md"
DECISIONS_REFERENCE = ROOT / "docs" / "reference" / "decisions-and-gaps.md"
FEASIBILITY_REPORT = ROOT / "docs" / "reference" / "feasibility-analysis.md"
REQUIREMENTS_REFERENCE = ROOT / "docs" / "reference" / "requirements.md"
INTERFACES_REFERENCE = ROOT / "docs" / "reference" / "interfaces.md"
TRACEABILITY_REFERENCE = ROOT / "docs" / "reference" / "traceability.md"
VERIFICATION_REFERENCE = ROOT / "docs" / "reference" / "verification.md"
FEASIBILITY_MODEL = ROOT / "analysis" / "feasibility.py"
MISSION_MODEL = ROOT / "analysis" / "mission_connectivity.py"

CATALOG_PATHS = {
    "system": ROOT / "model" / "system.yaml",
    "sources": ROOT / ".seal" / "sources.yaml",
    "proof": ROOT / ".seal" / "proof.yaml",
    "architecture": ROOT / "model" / "architecture.yaml",
    "assurance": ROOT / "model" / "assurance.yaml",
    "traceability": ROOT / "model" / "traceability.yaml",
}

DEFINITION_CONTAINERS = {
    "sources": ("sources",),
    "proof": ("claims", "evidence"),
    "architecture": (
        "configurations", "needs", "capabilities", "performers",
        "operational_activities", "information_exchanges", "scenarios",
        "functions", "components", "interfaces", "modes",
    ),
    "assurance": (
        "requirements", "deferred_topics", "hazards", "controls", "verifications",
        "trade_studies", "decisions",
    ),
}

PREFIXES = (
    "CFG", "NEED", "CAP", "SCN", "OA", "OP", "IX", "FUN", "CMP", "IFC",
    "REQ", "DEF", "HAZ", "CTL", "VER", "EVD", "TS", "MODE", "CLM", "SRC", "DEC",
)
ID_RE = re.compile(r"^(?:" + "|".join(PREFIXES) + r")-[A-Z0-9][A-Z0-9.-]*$")
ID_TOKEN_RE = re.compile(
    r"\b(?:" + "|".join(PREFIXES) + r")-[A-Z0-9]+(?:-[A-Z0-9]+)*\b"
)
MODEL_OR_GAP_TOKEN_RE = re.compile(
    r"\b(?:(?:" + "|".join(PREFIXES) + r")-[A-Z0-9]+(?:-[A-Z0-9]+)*"
    r"|GAP-[A-Z0-9]+(?:-[A-Z0-9]+)*)\b"
)
GAP_RE = re.compile(r"^GAP-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
GAP_TOKEN_RE = re.compile(r"\bGAP-[A-Z0-9]+(?:-[A-Z0-9]+)*\b")
REQUIREMENT_ID_RE = re.compile(r"^REQ-\d{3}$")
DEFERRED_TOPIC_ID_RE = re.compile(r"^DEF-\d{3}$")
LEGACY_REQUIREMENT_ID_RE = re.compile(r"\bREQ-(?:FUN|PER|IFC|SAF|CON|DEF)-\d+\b")
MERMAID_HEADERS = {"flowchart", "sequenceDiagram", "stateDiagram-v2"}

# Minimum prefix counts from the accepted consolidated baseline. New proposed elements
# may be added, but no accepted identifier family may silently lose records.
PRESERVED_ID_MINIMUMS = {
    "CAP": 5, "CFG": 5, "CLM": 14, "CMP": 19, "CTL": 5, "DEC": 2,
    "EVD": 4, "FUN": 9, "HAZ": 12, "IFC": 16, "IX": 10, "MODE": 5,
    "NEED": 1, "OA": 6, "OP": 10, "REQ": 23, "DEF": 5, "SCN": 8, "SRC": 17,
    "TS": 11, "VER": 8,
}

REFERENCE_KEYS = {
    "subject_ids", "decision_ids", "applicable_configurations", "applicable_sources",
    "predecessor_ids", "performers", "activities", "information_exchanges",
    "system_functions", "related_modes", "related_requirements", "related_hazards",
    "verification_ids", "claim_ids", "constrains_requirement_ids", "trade_study_ids",
    "operational_scenarios", "upstream_refs", "allocation_refs", "tbd_owner_ids",
    "contradicts", "supersedes", "mitigates", "implemented_by", "evidence_ids",
    "source_refs", "evidence_refs", "gap_refs", "counterevidence_refs", "blocks",
    "object_refs", "supports", "refutes", "source_ids", "affected_ids", "control_refs", "owner_ids",
    "dependency_ids", "internal_model_verification_ids",
    "external_conformance_verification_ids",
    "candidate_target_ids",
    "residual_gap_ids",
    "trigger_refs", "interface_refs",
}
SINGULAR_REFERENCE_KEYS = {
    "claim_id", "decision_id", "gap_id", "endpoint_a", "endpoint_b", "from", "to",
    "requirement_id", "deferred_topic_id", "subject_id", "initial_mode",
}
REFERENCE_SENTINELS = {"TBD", "All", "External", "None"}

AUTHORITY_RULE = (
    "model/system.yaml is the manifest. The structured catalogs referenced by it are "
    "authoritative model data. Markdown documents and generated reports are views of that model."
)

RETIRED_CORE_PATHS = {
    "system.yaml", "architecture.md", "trade-studies.md", "reports",
    ".seal/README.md",
    "model/configurations.yaml", "model/elements.yaml", "model/claims.yaml",
    "model/operational-scenarios.yaml", "model/interfaces.yaml", "model/requirements.yaml",
    "uaf-views.md", "requirements.md", "hazard-analysis.md", "traceability.md",
    "reports/baseline-candidate.md", "reports/baseline-gaps.md",
    "reports/baseline-traceability.md", "scripts/check-ids.py", "scripts/migrate_catalogs.py",
}


def load_catalog(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing required catalog: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"{path.relative_to(ROOT)} is not JSON-compatible YAML: "
            f"line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a top-level object")
    return data


def load_all() -> dict[str, dict[str, Any]]:
    return {name: load_catalog(path) for name, path in CATALOG_PATHS.items()}


def definition_records(catalogs: dict[str, dict[str, Any]]) -> list[tuple[str, dict[str, Any]]]:
    records: list[tuple[str, dict[str, Any]]] = []
    for catalog_name, containers in DEFINITION_CONTAINERS.items():
        catalog = catalogs[catalog_name]
        for container in containers:
            value = catalog.get(container)
            if not isinstance(value, list):
                records.append((f"{catalog_name}.{container}", {}))
                continue
            for index, record in enumerate(value):
                if isinstance(record, dict):
                    records.append((f"{catalog_name}.{container}[{index}]", record))
                else:
                    records.append((f"{catalog_name}.{container}[{index}]", {}))
    return records


def references_in(value: Any, path: str = "") -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            if key in REFERENCE_KEYS and isinstance(child, list):
                for index, item in enumerate(child):
                    if isinstance(item, str):
                        yield f"{child_path}[{index}]", item
            elif key in SINGULAR_REFERENCE_KEYS and isinstance(child, str):
                yield child_path, child
            yield from references_in(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from references_in(child, f"{path}[{index}]")


def pipe(value: Any) -> str:
    if value is None or value == "" or value == []:
        return "-"
    if isinstance(value, list):
        value = ", ".join(str(item) for item in value)
    return str(value).replace("|", "\\|").replace("\n", " ")


def generated_header(source_paths: list[str]) -> list[str]:
    sources = ", ".join(f"`{path}`" for path in source_paths)
    return [
        "<!-- GENERATED VIEW - DO NOT EDIT. -->",
        "",
        f"> Generated from {sources} with `python scripts/validate-baseline.py --write-reports`.",
        "> This report is a model view, not an approval or verification record.",
        "",
    ]


def render_baseline(catalogs: dict[str, dict[str, Any]]) -> str:
    system = catalogs["system"]
    architecture = catalogs["architecture"]
    assurance = catalogs["assurance"]
    proof = catalogs["proof"]
    traceability = catalogs["traceability"]

    lines = generated_header([
        "model/system.yaml", "model/architecture.yaml", "model/assurance.yaml",
        "model/traceability.yaml", ".seal/sources.yaml", ".seal/proof.yaml",
    ])
    lines.extend([
        "# Baseline Candidate - Not Approved",
        "",
        "## Baseline status",
        "",
        f"- Model version: `{system['model_version']}`",
        f"- Status: `{system['status']}`",
        f"- Approval: `{system['baseline']['approval_state']}`",
        "- Model-valid means structurally consistent; it does not mean safe, verified, or ready.",
        "",
        "## Internal verification work-package disposition",
        "",
        f"- Work package: `{system['internal_verification_baseline']['work_package_status']}` for `{system['internal_verification_baseline']['model_version']}`.",
        f"- Accepted scope: {system['internal_verification_baseline']['approval_scope']}.",
        f"- Authority record: `{system['internal_verification_baseline']['source_refs'][0]}`; acceptance evidence: `{system['internal_verification_baseline']['evidence_refs'][0]}`.",
        "- Technical baseline: `not_approved`; physical verification and external-interface conformance: `not_established`; safety approval: `not_approved`.",
        f"- Unresolved decisions remain proposed: {', '.join(f'`{item}`' for item in system['internal_verification_baseline']['unresolved_decisions'])}.",
        "",
        "## Model-review status",
        "",
        f"- Current semantic model: `{system['model_version']}`.",
        f"- Latest recorded review: `{system['latest_recorded_model_review']['model_version']}` with status `{system['latest_recorded_model_review']['review_status']}` in `{system['latest_recorded_model_review']['evidence_refs'][0]}` under `{system['latest_recorded_model_review']['source_refs'][0]}`.",
        "- The accepted 0.7.0 work package remains preserved; the 0.8.0 model-level review is not owner acceptance or technical-baseline approval. The 0.9.0 identifier and documentation refactor has no new evidence record.",
        "- Physical verification, safety approval, and external-interface conformance remain not established.",
        "",
        "## Configuration summary",
        "",
        "| ID | Role | Maturity | Relationship | Approval |",
        "|---|---|---|---|---|",
    ])
    for config in architecture["configurations"]:
        lines.append(
            f"| {config['id']} | {pipe(config['purpose'])} | {pipe(config['maturity'])} | "
            f"{pipe(config['derivation_relationship'])} | {pipe(config['approval_status'])} |"
        )

    reconciliation = architecture["configuration_reconciliation"]
    forward = reconciliation["recovered_to_candidate"]
    recovered_items = [item for item in forward if item["record_id"].startswith("REC-MAP-")]
    recovered_connections = [item for item in forward if item["record_id"].startswith("REC-CON-")]
    forward_counts = collections.Counter(item["mapping_classification"] for item in forward)
    component_counts = collections.Counter(
        item["mapping_classification"]
        for item in reconciliation["candidate_components_to_recovered"]
    )
    interface_counts = collections.Counter(
        item["mapping_classification"]
        for item in reconciliation["candidate_interfaces_to_recovered"]
    )
    lines.extend([
        "",
        "## Recovered-evidence reconciliation",
        "",
        "`CFG-REC` is descriptive evidence. The two-way mapping records role-level correspondence; it does not assert exact recovered-to-candidate equivalence, candidate identity, inheritance, or approval.",
        "",
        "| Registered source | Integrity | Treatment |",
        "|---|---|---|",
    ])
    for item in reconciliation["source_integrity"]:
        lines.append(
            f"| {item['source_id']} | {item['status']} | {pipe(item['treatment'])} |"
        )
    lines.extend([
        "",
        f"- Forward inventory: {len(recovered_items)} recovered items and {len(recovered_connections)} recovered connections ({len(forward)} total records).",
        f"- Forward classifications: {', '.join(f'{key}: {value}' for key, value in sorted(forward_counts.items()))}.",
        f"- Candidate component coverage: {len(reconciliation['candidate_components_to_recovered'])} of {len(architecture['components'])}; {', '.join(f'{key}: {value}' for key, value in sorted(component_counts.items()))}.",
        f"- Candidate interface coverage: {len(reconciliation['candidate_interfaces_to_recovered'])} of {len(architecture['interfaces'])}; {', '.join(f'{key}: {value}' for key, value in sorted(interface_counts.items()))}.",
        "- Contradictions: 0. Unmatched recovered records: 5. Unknown recovered records: 1.",
        "- `GAP-REC-001` is narrowed, not closed: the role mapping exists, while complete physical reconstruction and exact equivalence remain unsupported.",
        "- In this repository, `physically_observed` means documented as an observation in an integrity-accepted registered record; it does not claim direct inspection by the model author or automation.",
    ])

    claim_status = collections.Counter(item.get("status", "unknown") for item in proof["claims"])
    evidence_basis = collections.Counter(item.get("evidence_basis", "unknown") for item in proof["claims"])
    lines.extend([
        "",
        "## Evidence and claim summary",
        "",
        f"- Claims: {len(proof['claims'])} ({', '.join(f'{key}: {value}' for key, value in sorted(claim_status.items()))})",
        f"- Evidence records: {len(proof['evidence'])}",
        f"- Claim evidence basis: {', '.join(f'{key}: {value}' for key, value in sorted(evidence_basis.items()))}",
        "- Evidence supports claims; it does not approve the candidate architecture.",
        "",
        "<details>",
        "<summary>Claim register summary</summary>",
        "",
        "| Claim | Subject | Status | Confidence | Gaps |",
        "|---|---|---|---|---|",
    ])
    for claim in proof["claims"]:
        lines.append(
            f"| {claim['id']} | {pipe(claim['subject'])} | {pipe(claim['status'])} | "
            f"{pipe(claim['confidence'])} | {pipe(claim.get('gap_refs'))} |"
        )
    lines.extend([
        "", "</details>", "", "## Active decisions", "",
        "| Decision | Status | Current model-review evidence | Internal-consistency finding |",
        "|---|---|---|---|",
    ])
    for decision in assurance["decisions"]:
        review = decision.get("verification_review", {})
        lines.append(
            f"| {decision['id']} - {pipe(decision['name'])} | {decision['decision_status']} | "
            f"{pipe(review.get('evidence_ids'))} | {pipe(review.get('consistency_result'))} |"
        )

    active_gaps = [
        gap for gap in traceability["gaps"]
        if gap.get("disposition") not in {"closed", "deferred", "intentionally_out_of_scope"}
    ]
    closed_gaps = [gap for gap in traceability["gaps"] if gap.get("disposition") == "closed"]
    deferred_gaps = [
        gap for gap in traceability["gaps"]
        if gap.get("disposition") in {"deferred", "intentionally_out_of_scope"}
    ]
    lines.extend([
        "",
        "## Active architecture gaps",
        "",
        "| Gap | Category | Outcome | Severity | Affected model area |",
        "|---|---|---|---|---|",
    ])
    for gap in active_gaps:
        lines.append(
            f"| {gap['code']} | {pipe(gap['category'])} | {pipe(gap.get('work_package_outcome'))} | "
            f"{pipe(gap['severity'])} | "
            f"{pipe(gap['affected_ids'])} |"
        )

    practical_gap_groups = [
        (
            "Can be improved through model work now",
            {"A_closeable_by_model_work"},
            "No accidental model-local completeness gap remains after this pass.",
        ),
        (
            "Requires project-owner decision",
            {"B_project_owner_decision"},
            "No owner decision is currently recorded.",
        ),
        (
            "Requires physical or external evidence",
            {"C_physical_or_external_evidence"},
            "No physical or external-evidence dependency is currently recorded.",
        ),
        (
            "Intentionally deferred or future configuration",
            {"D_intentional_deferral", "E_future_configuration"},
            "No deferred or future item is currently recorded.",
        ),
    ]
    lines.extend(["", "## Remaining work by dependency", ""])
    for heading, classifications, empty_text in practical_gap_groups:
        grouped = [
            gap for gap in traceability["gaps"]
            if gap.get("audit_classification") in classifications
            and gap.get("disposition") != "closed"
        ]
        lines.extend([f"### {heading}", ""])
        if not grouped:
            lines.append(f"- {empty_text}")
        else:
            for gap in grouped:
                lines.append(
                    f"- `{gap['code']}` - **{gap['work_package_outcome']}**: {gap['next_action']}"
                )
        lines.append("")

    verification_status = collections.Counter(
        item.get("verification_readiness", "unspecified")
        for item in assurance["requirement_quality_audit"]
    )
    execution_labels = {
        "executed_pass": "PASS",
        "executed_with_open_gaps": "PASS_WITH_OPEN_GAPS",
        "failed": "FAIL",
        "blocked": "BLOCKED",
        "deferred": "NOT_EXECUTED",
        "not_executed": "NOT_EXECUTED",
    }
    lines.extend([
        "",
        "## Verification execution matrix",
        "",
        "| VER ID | Method | Readiness | Execution | Evidence | Result | Review-time residual gaps |",
        "|---|---|---|---|---|---|---|",
    ])
    for verification in assurance["verifications"]:
        execution = verification["execution_status"]
        lines.append(
            f"| {verification['id']} | {pipe(verification['method'])} | {verification['readiness']} | "
            f"{execution} | {pipe(verification['evidence_ids'])} | {execution_labels[execution]} | "
            f"{pipe(verification['residual_gap_ids'])} |"
        )
    lines.extend([
        "",
        "Residual-gap lists record each verification's execution-time result. A referenced gap may have been closed later; current dispositions are listed in the gap sections below.",
        "",
        "### Requirement-level review summary",
        "",
        f"- Requirements reviewed: {len(assurance['requirements'])}; model-level review passed: 2 (`REQ-016`, `REQ-022`); architecture review passed with open limitations: {len(assurance['requirements']) - 2}.",
        f"- Readiness: {', '.join(f'{key}: {value}' for key, value in sorted(verification_status.items()))}.",
        f"- Deferred/external topics: {len(assurance['deferred_topics'])}; these `DEF-*` records are not counted as system requirements.",
        "- `EVD-001` through `EVD-004` remain historical. `EVD-008` through `EVD-012` preserve the accepted 0.7.0 review and acceptance trail; `EVD-013` records the latest 0.8.0 model-level review without owner acceptance.",
        "- Internal review does not establish physical requirement satisfaction, external conformance, safety, or technical approval (`GAP-VER-001`).",
    ])
    objective_corrections = [
        (evidence["id"], correction)
        for evidence in proof["evidence"]
        for correction in evidence.get("objective_corrections", [])
    ]
    lines.extend([
        "",
        "### Objective corrections from verification",
        "",
        "| Evidence | Affected IDs | Problem | Correction | Architecture intent changed? |",
        "|---|---|---|---|---|",
    ])
    for evidence_id, correction in objective_corrections:
        lines.append(
            f"| {evidence_id} | {pipe(correction['affected_ids'])} | {pipe(correction['problem'])} | "
            f"{pipe(correction['new_state'])} | {str(correction['architecture_intent_changed']).lower()} |"
        )
    if not objective_corrections:
        lines.append("| - | - | No objective correction was required. | - | false |")
    lines.extend([
        "",
        "## Concise traceability summary",
        "",
        "- Mission relay: `NEED-001 -> CAP-001 -> SCN-003 -> OA-004 -> IX-002 / IX-003 -> FUN-REL-01 -> CMP-COM-01 -> IFC-EXT-001 / IFC-EXT-002 -> REQ-001 -> VER-001 / VER-009`.",
        "- Return telemetry: `SCN-004 -> OA-005 -> IX-004 / IX-005 -> FUN-REL-02 -> CMP-COM-01 -> IFC-EXT-003 / IFC-EXT-004 -> REQ-002 -> VER-001 / VER-009`.",
        "- Station keeping: `CAP-002 -> SCN-002 -> OA-003 -> FUN-FLT-03 -> CMP-AVN-01 / CMP-AVN-02 / CMP-AVN-03 -> REQ-003 / REQ-023`.",
        "- Setup and ground safety: `SCN-001 -> OA-007 -> MODE-005 -> HAZ-004 -> CTL-001 -> REQ-006 / REQ-019 -> VER-006`.",
        "- Health/status: `SCN-007 -> IX-009 -> FUN-HLT-01 -> CMP-AVN-01 -> IFC-EXT-007 -> REQ-008 -> VER-005 / VER-008 / VER-009`.",
        "- `HAZ-004 -> CTL-001 -> REQ-006 / REQ-019 -> VER-004 / VER-006 -> GAP-VER-001`.",
        "- `HAZ-008 -> CTL-005 -> REQ-017 -> VER-005 / VER-008 -> GAP-VER-001`.",
        "- Current platform-to-payload crossings are only `IFC-INT-003` and `IFC-INT-007`; `IFC-INT-010` is payload-internal.",
        "- The complete relationship database remains in `model/traceability.yaml`.",
        "",
        "## Items requiring owner attention",
        "",
    ])
    for gap in active_gaps:
        if gap.get("severity") in {"major", "blocker"}:
            lines.append(f"- `{gap['code']}`: {gap['next_action']}")

    lines.extend([
        "",
        "## Closed or reclassified gaps in this maturation pass",
        "",
    ])
    for gap in closed_gaps:
        lines.append(
            f"- `{gap['code']}` - **{gap.get('work_package_outcome', 'CLOSED')}**: {gap['statement']}"
        )

    lines.extend([
        "",
        "<details>",
        "<summary>Intentional deferrals and secondary items</summary>",
        "",
    ])
    for gap in deferred_gaps:
        lines.append(f"- `{gap['code']}` ({gap['disposition']}): {gap['statement']}")
    lines.extend([
        "",
        "</details>",
        "",
        "## Standards posture",
        "",
        "The repository retains UAF 1.2 terminology. UAF 1.3 is the current OMG formal version. "
        "No conformance claim is made; `DEC-002` / `GAP-STD-001` remains unresolved.",
        "",
        "## Approval statement",
        "",
        "**This baseline remains a candidate and has not been approved.**",
        "",
    ])
    return "\n".join(lines)


def reference_header(title: str, purpose: str, sources: list[str]) -> list[str]:
    return [
        "<!-- GENERATED VIEW - DO NOT EDIT. -->", "", f"# {title}", "",
        "[Overview](../../README.md) · [Architecture](../architecture.md) · "
        "[Feasibility](../feasibility.md) · [Engineering Status](../engineering-status.md) · "
        "[Reference index](README.md)", "", purpose, "",
        "Generated from " + ", ".join(f"`{source}`" for source in sources) + ". "
        "The structured catalogs remain authoritative.", "",
    ]


def render_requirements(catalogs: dict[str, dict[str, Any]]) -> str:
    assurance = catalogs["assurance"]
    requirements = {item["id"]: item for item in assurance["requirements"]}
    groups = [
        ("Relay mission", ["REQ-001", "REQ-002"]),
        ("Flight and positioning", ["REQ-003", "REQ-010", "REQ-011", "REQ-023"]),
        ("Recovery and aircraft control", ["REQ-004", "REQ-005", "REQ-006", "REQ-007", "REQ-008"]),
        ("Payload support and interfaces", ["REQ-012", "REQ-014", "REQ-015", "REQ-016", "REQ-017"]),
        ("Power and safety", ["REQ-018", "REQ-019", "REQ-022"]),
        ("Portability and affordability", ["REQ-009", "REQ-013", "REQ-020", "REQ-021"]),
    ]
    lines = reference_header(
        "Requirements",
        "The requirements below describe what the current carrier must accomplish. Some values are deliberately [TBD] because owner targets and physical evidence are not yet available; those placeholders are not settled design values.",
        ["model/assurance.yaml"],
    )
    lines.extend([
        "## Design-driving requirements", "",
        "The payload envelope, on-station endurance, gross mass, cost, payload power, recovery behavior, and single-operator handling are coupled. Changing one changes the practical range of the others.", "",
    ])
    for heading, identifiers in groups:
        lines.extend([f"## {heading}", "", "| ID | Requirement | Status | Verification |", "|---|---|---|---|"])
        for item_id in identifiers:
            item = requirements[item_id]
            requirement = f"**{pipe(item['display_name'])}** — {pipe(item['text'])}"
            status = f"{item['decision_status']} / {item['verification_status']}"
            verification = f"{item['verification_method']}: {pipe(item['verification_ids'])}"
            lines.append(f"| {item_id} | {requirement} | {status} | {verification} |")
        lines.append("")
    lines.extend([
        "## Deferred / externally owned topics", "",
        "These records preserve scope, provenance, applicability, and ownership without presenting the topics as system requirements.", "",
        "| ID | Topic | Disposition | Related model records |", "|---|---|---|---|",
    ])
    for topic in assurance["deferred_topics"]:
        related = topic.get("upstream_refs", []) + topic.get("allocation_refs", [])
        lines.append(
            f"| {topic['id']} | **{pipe(topic['display_name'])}** — {pipe(topic['text'])} | "
            f"{topic['verification_status']} | {pipe(related)} |"
        )
    lines.extend([
        "", "For allocation, provenance, applicability, TBD ownership, and source fields, inspect "
        "[`model/assurance.yaml`](../../model/assurance.yaml) and the [traceability reference](traceability.md).",
    ])
    return "\n".join(lines).rstrip() + "\n"


def render_interfaces(catalogs: dict[str, dict[str, Any]]) -> str:
    architecture = catalogs["architecture"]
    index = {
        item["id"]: item.get("display_name") or item.get("name") or item["id"]
        for collection in ("components", "performers") for item in architecture[collection]
    }
    groups: dict[str, list[dict[str, Any]]] = collections.OrderedDict((
        ("External interfaces", []), ("Platform-to-payload interfaces", []),
        ("Payload-internal interfaces", []), ("Other internal interfaces", []),
        ("Future-only interfaces", []),
    ))
    current = {"CFG-REP", "CFG-DOM"}
    for interface in architecture["interfaces"]:
        configs = set(interface.get("applicable_configurations", []))
        if not current.intersection(configs):
            group = "Future-only interfaces"
        elif interface["id"] in {"IFC-INT-003", "IFC-INT-007"}:
            group = "Platform-to-payload interfaces"
        elif "payload-internal" in interface.get("interface_type", ""):
            group = "Payload-internal interfaces"
        elif interface["id"].startswith("IFC-EXT-"):
            group = "External interfaces"
        else:
            group = "Other internal interfaces"
        groups[group].append(interface)
    lines = reference_header(
        "Interfaces",
        "This inventory shows logical architecture interfaces. It does not establish connector design, electrical ratings, protocol compatibility, or external conformance.",
        ["model/architecture.yaml"],
    )
    for heading, interfaces in groups.items():
        lines.extend([
            f"## {heading}", "", "| Interface | Endpoints | Flow | Configuration / maturity | Open attributes |",
            "|---|---|---|---|---|",
        ])
        for interface in interfaces:
            a = f"{index.get(interface['endpoint_a'], interface['endpoint_a'])} ({interface['endpoint_a']})"
            b = f"{index.get(interface['endpoint_b'], interface['endpoint_b'])} ({interface['endpoint_b']})"
            maturity = f"{pipe(interface['applicable_configurations'])}; {interface['decision_status']}"
            lines.append(
                f"| **{pipe(interface['name'])}** ({interface['id']}) | {pipe(a)} → {pipe(b)} | "
                f"{pipe(interface['flow_class'])}; {pipe(interface['direction'])} | {maturity} | "
                f"{pipe(interface.get('unknown_attributes'))} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_traceability(catalogs: dict[str, dict[str, Any]]) -> str:
    relationships = catalogs["traceability"]["relationships"]
    lines = reference_header(
        "Traceability",
        "Representative traces explain engineering cause and effect first. The complete relationship register follows for audit.",
        ["model/architecture.yaml", "model/assurance.yaml", "model/traceability.yaml"],
    )
    lines.extend([
        "## Representative traces", "",
        "**Extend remote command reach**", "",
        "Need → airborne-relay capability → outbound-relay scenario → relay behavior → black-box payload → external relay path → **Relay outbound traffic (REQ-001)** → architecture review now; external conformance later.", "",
        "**Return remote-aircraft telemetry**", "",
        "Relay scenario → return-traffic behavior → black-box payload → return external path → **Relay return traffic (REQ-002)** → architecture review now; external conformance later.", "",
        "**Hold a useful relay position**", "",
        "Station-keeping capability → position-and-hold scenario → flight behavior → avionics and navigation → **Maintain commanded station position (REQ-003)** → analysis after owner tolerance; physical evidence later.", "",
        "**Recover after payload loss**", "",
        "Degraded scenario → independent aircraft control → recovery mode → **Recover after payload loss (REQ-007)** → model review recorded; physical recovery evidence absent.", "",
        "## Complete relationship register", "", f"The model contains {len(relationships)} explicit relationships.", "",
        "<details>", "<summary>Open complete relationship table</summary>", "",
        "| From | Relationship | To | Status | Gap |", "|---|---|---|---|---|",
    ])
    for relationship in relationships:
        lines.append(
            f"| {relationship['from']} | {pipe(relationship['relation'])} | {relationship['to']} | "
            f"{pipe(relationship['status'])} | {pipe(relationship.get('gap'))} |"
        )
    lines.extend(["", "</details>", "", "See [Decisions & gaps](decisions-and-gaps.md) for the human interpretation of unresolved relationships."])
    return "\n".join(lines).rstrip() + "\n"


def render_verification(catalogs: dict[str, dict[str, Any]]) -> str:
    assurance = catalogs["assurance"]
    system = catalogs["system"]
    lines = reference_header(
        "Verification",
        "Model verification, quantitative analysis, physical verification, and external conformance are separate evidence classes. A passing repository check is not a verified aircraft.",
        ["model/assurance.yaml", ".seal/proof.yaml"],
    )
    lines.extend([
        "## Evidence boundary", "", "| Evidence class | What it can establish | Current position |", "|---|---|---|",
        "| Internal model review | Structure, reference integrity, allocation, and consistency | Latest recorded review is 0.8.0; not owner acceptance |",
        "| Reproducible analysis | Conditional mass, power, endurance, and cost behavior | Executed with exploratory assumptions |",
        "| Physical verification | Aircraft behavior and measured performance | Not performed |",
        "| External conformance | Endpoint, spectrum, and authority-controlled compatibility | Blocked by missing authority/specifications |",
        "| Technical baseline approval | Owner acceptance of a design baseline | Not approved |", "",
        "## Verification activities", "", "| Activity | Method | Readiness | Execution | Evidence | Review-time residual gaps |",
        "|---|---|---|---|---|---|",
    ])
    for verification in assurance["verifications"]:
        lines.append(
            f"| **{pipe(verification['name'])}** ({verification['id']}) | {pipe(verification['method'])} | "
            f"{pipe(verification['readiness'])} | {pipe(verification['execution_status'])} | "
            f"{pipe(verification['evidence_ids'])} | {pipe(verification['residual_gap_ids'])} |"
        )
    lines.extend([
        "", "Residual-gap lists preserve the result recorded when each verification ran. See [Decisions & gaps](decisions-and-gaps.md) for current dispositions.",
        "", "The current semantic model is `" + system["model_version"] + "`. The latest recorded review evidence remains tied to `" + system["latest_recorded_model_review"]["model_version"] + "`; the identifier/documentation migration does not rewrite that evidence.",
    ])
    return "\n".join(lines).rstrip() + "\n"


def render_decisions_and_gaps(catalogs: dict[str, dict[str, Any]]) -> str:
    assurance = catalogs["assurance"]
    gaps = catalogs["traceability"]["gaps"]
    lines = reference_header(
        "Decisions and Gaps",
        "Use this page to see which owner decisions, evidence needs, and future branches block the next phase. It reports model dispositions; it does not change them.",
        ["model/assurance.yaml", "model/traceability.yaml"],
    )
    lines.extend(["## Decisions", "", "| Decision | Status | Authority | Remaining issue |", "|---|---|---|---|"])
    for decision in assurance["decisions"]:
        review = decision.get("verification_review", {})
        remaining = review.get("remaining_unresolved") or decision.get("statement")
        lines.append(
            f"| **{pipe(decision['name'])}** ({decision['id']}) | {pipe(decision['decision_status'])} | "
            f"{pipe(decision['authority'])} | {pipe(remaining)} |"
        )
    groups = collections.OrderedDict((
        ("Requires project-owner decision", {"B_project_owner_decision"}),
        ("Requires physical or external evidence", {"C_physical_or_external_evidence"}),
        ("Deliberately deferred", {"D_intentional_deferral"}),
        ("Future configuration", {"E_future_configuration"}),
        ("Closed or reclassified model work", {"A_closeable_by_model_work", "F_false_positive_model_health_gap"}),
    ))
    for heading, classifications in groups.items():
        lines.extend(["", f"## {heading}", "", "| Gap | Outcome | Meaning | Next action |", "|---|---|---|---|"])
        for gap in gaps:
            if gap.get("audit_classification") in classifications:
                lines.append(
                    f"| {gap['code']} | {pipe(gap['work_package_outcome'])} | {pipe(gap['statement'])} | {pipe(gap['next_action'])} |"
                )
    lines.extend([
        "", "The earlier detailed owner-target package is retained in the "
        "[archive](../archive/architecture-decision-target-package.md) as project history. Current dispositions come from the structured catalogs above.",
    ])
    return "\n".join(lines).rstrip() + "\n"


def extract_mermaid_blocks(markdown: str) -> tuple[list[tuple[str, str]], list[str]]:
    blocks: list[tuple[str, str]] = []
    errors: list[str] = []
    title = "untitled diagram"
    body: list[str] = []
    in_mermaid = False
    start_line = 0
    for line_number, line in enumerate(markdown.splitlines(), start=1):
        if not in_mermaid and line.startswith("### "):
            title = line[4:].strip()
        if line == "```mermaid":
            if in_mermaid:
                errors.append(f"nested Mermaid fence at line {line_number}")
            in_mermaid = True
            start_line = line_number
            body = []
        elif in_mermaid and line == "```":
            blocks.append((title, "\n".join(body)))
            in_mermaid = False
            body = []
        elif in_mermaid:
            body.append(line)
    if in_mermaid:
        errors.append(f"unclosed Mermaid fence beginning at line {start_line}")
    return blocks, errors


MARKDOWN_LINK_RE = re.compile(
    r"!?\[[^\]]*\]\((?P<target><[^>]+>|[^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)"
)


def markdown_anchors(text: str) -> set[str]:
    anchors: set[str] = set()
    counts: collections.Counter[str] = collections.Counter()
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*$", text, flags=re.MULTILINE):
        plain = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", heading)
        plain = re.sub(r"[`*_~]", "", plain).strip().lower()
        slug = re.sub(r"[^\w\s-]", "", plain, flags=re.UNICODE)
        slug = re.sub(r"[\s-]+", "-", slug).strip("-")
        suffix = counts[slug]
        counts[slug] += 1
        anchors.add(f"{slug}-{suffix}" if suffix else slug)
    return anchors


def validate_markdown_links() -> list[str]:
    """Validate local Markdown targets and heading anchors across active and archive docs."""
    errors: list[str] = []
    markdown_files = [ROOT / "README.md"] + sorted((ROOT / "docs").rglob("*.md"))
    anchor_cache: dict[Path, set[str]] = {}
    for source in markdown_files:
        text = source.read_text(encoding="utf-8-sig")
        for match in MARKDOWN_LINK_RE.finditer(text):
            raw_target = match.group("target").strip("<>")
            if raw_target.startswith(("http://", "https://", "mailto:")):
                continue
            path_part, separator, anchor = raw_target.partition("#")
            target = source if not path_part else (source.parent / unquote(path_part)).resolve()
            try:
                target.relative_to(ROOT)
            except ValueError:
                errors.append(f"{source.relative_to(ROOT)} link escapes the repository: {raw_target}")
                continue
            if not target.exists():
                errors.append(f"{source.relative_to(ROOT)} has missing link target {raw_target}")
                continue
            if separator and target.suffix.lower() == ".md":
                anchors = anchor_cache.setdefault(
                    target, markdown_anchors(target.read_text(encoding="utf-8-sig"))
                )
                if unquote(anchor).lower() not in anchors:
                    errors.append(f"{source.relative_to(ROOT)} has missing anchor {raw_target}")
    return errors


def validate_mermaid_documents(definitions: set[str], gap_codes: set[str]) -> list[str]:
    errors: list[str] = []
    paths = [ROOT / "README.md", ROOT / "docs" / "architecture.md", ATLAS_REPORT]
    for path in paths:
        if not path.exists():
            errors.append(f"missing Mermaid-bearing document: {path.relative_to(ROOT)}")
            continue
        blocks, fence_errors = extract_mermaid_blocks(path.read_text(encoding="utf-8-sig"))
        errors.extend(f"{path.relative_to(ROOT)}: {item}" for item in fence_errors)
        if path == ROOT / "README.md" and blocks:
            errors.append(f"README.md must use canonical generated figures rather than Mermaid, found {len(blocks)} Mermaid diagrams")
        if path == ROOT / "docs" / "architecture.md" and blocks:
            errors.append(f"docs/architecture.md must use canonical generated figures rather than Mermaid, found {len(blocks)} Mermaid diagrams")
        if path == ATLAS_REPORT and not 10 <= len(blocks) <= 16:
            errors.append(f"architecture atlas must contain 10-16 selected audit diagrams, found {len(blocks)}")
        for title, block in blocks:
            lines = [line for line in block.splitlines() if line.strip()]
            if not lines:
                errors.append(f"{path.name}: Mermaid diagram {title!r} is empty")
                continue
            header = lines[0].split()[0]
            if header not in MERMAID_HEADERS:
                errors.append(f"{path.name}: Mermaid diagram {title!r} uses unsupported header {header}")
            if not any("%% Configuration scope:" in line for line in lines[:4]):
                errors.append(f"{path.name}: Mermaid diagram {title!r} lacks configuration scope")
            if ";" in block:
                errors.append(
                    f"{path.name}: Mermaid diagram {title!r} contains a raw semicolon; "
                    "use a dash, comma, or line break"
                )
            if "…" in block or "â€¦" in block:
                errors.append(f"{path.name}: Mermaid diagram {title!r} contains a truncated label")
            if any(line.lstrip().startswith("click ") for line in lines):
                errors.append(f"{path.name}: Mermaid diagram {title!r} contains a clickable link")
            for line in lines:
                stripped = line.strip()
                if re.search(r"\bend\b", stripped) and stripped not in {"end", "end note"}:
                    errors.append(
                        f"{path.name}: Mermaid diagram {title!r} uses reserved lowercase 'end' "
                        "outside a structural closing line"
                    )
            for match in MODEL_OR_GAP_TOKEN_RE.finditer(block):
                token = match.group(0)
                if block[match.end():].startswith("-*"):
                    continue
                if token.startswith("GAP-"):
                    if token not in gap_codes:
                        errors.append(f"{path.name}: diagram {title!r} references undefined gap {token}")
                elif token not in definitions:
                    errors.append(f"{path.name}: diagram {title!r} references undefined ID {token}")
            if header == "sequenceDiagram":
                participants = sum(1 for line in lines if line.strip().startswith("participant "))
                if participants > 6:
                    errors.append(f"{path.name}: sequence {title!r} has {participants} participants; maximum is 6")
            elif header == "flowchart":
                node_keys = {
                    match.group(1)
                    for line in lines
                    for match in [re.match(r"\s*([A-Za-z0-9_]+)\[\"", line)]
                    if match
                }
                if len(node_keys) > 12:
                    errors.append(f"{path.name}: diagram {title!r} has {len(node_keys)} major nodes; split it")
    return errors


def validate_communication_figures(
    catalogs: dict[str, dict[str, Any]], definitions: set[str], gap_codes: set[str]
) -> list[str]:
    """Check deterministic outsider views without policing subjective layout."""
    errors: list[str] = []
    system = catalogs["system"]
    manifest = system.get("communication_views", [])
    generated = system.get("generated_figures", [])
    expected_slugs = {
        "project-in-one-picture", "system-boundary", "physical-architecture",
        "power-resource-flow", "command-data-flow", "mission-sequence",
        "degraded-behavior", "configuration-evolution", "engineering-status",
    }
    slugs = [item.get("slug") for item in manifest]
    if set(slugs) != expected_slugs or len(slugs) != len(set(slugs)):
        errors.append("communication-view manifest must contain exactly the nine canonical view slugs")
    primary_views = [item for item in manifest if item.get("tier") == "primary"]
    if len(primary_views) != 5:
        errors.append(f"communication-view manifest must identify five primary views, found {len(primary_views)}")
    expected_paths = {f"docs/figures/{slug}.svg" for slug in expected_slugs}
    if set(generated) != expected_paths:
        errors.append("generated_figures must match the nine canonical communication views")

    display_records = (
        catalogs["architecture"].get("configurations", [])
        + catalogs["architecture"].get("performers", [])
        + catalogs["architecture"].get("components", [])
        + catalogs["assurance"].get("requirements", [])
        + catalogs["assurance"].get("deferred_topics", [])
    )
    for record in display_records:
        alias = record.get("display_name")
        if alias is None:
            continue
        if not isinstance(alias, str) or not alias.strip() or len(alias) > 36:
            errors.append(f"{record['id']} has an invalid human-readable display_name")
        if ID_TOKEN_RE.search(alias) or GAP_TOKEN_RE.search(alias):
            errors.append(f"{record['id']} display_name leaks a technical identifier")

    for view in manifest:
        slug = view.get("slug", "<missing>")
        required = {"title", "audience", "question", "object_refs", "tier", "major_node_count"}
        if not required.issubset(view):
            errors.append(f"communication view {slug} lacks presentation or provenance fields")
            continue
        tier = view.get("tier")
        if tier not in {"primary", "reference"}:
            errors.append(f"communication view {slug} has invalid tier {tier!r}")
        if tier == "primary" and not 1 <= view.get("major_node_count", 0) <= 8:
            errors.append(f"primary communication view {slug} exceeds the eight-node comprehension limit")
        path = ROOT / "docs" / "figures" / f"{slug}.svg"
        if not path.exists():
            errors.append(f"canonical communication figure missing: {path.relative_to(ROOT)}")
            continue
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as exc:
            errors.append(f"{path.relative_to(ROOT)} is not valid SVG XML: {exc}")
            continue
        namespace = {"svg": "http://www.w3.org/2000/svg"}
        title = root.find("svg:title", namespace)
        desc = root.find("svg:desc", namespace)
        metadata = root.find("svg:metadata", namespace)
        if title is None or not (title.text or "").strip():
            errors.append(f"{path.relative_to(ROOT)} lacks an accessible title")
        if desc is None or not (desc.text or "").strip():
            errors.append(f"{path.relative_to(ROOT)} lacks an accessible description")
        metadata_text = "" if metadata is None else "".join(metadata.itertext())
        for item_id in view["object_refs"]:
            if item_id.startswith("GAP-"):
                known = item_id in gap_codes
            else:
                known = item_id in definitions
            if not known:
                errors.append(f"communication view {slug} references unknown record {item_id}")
            if item_id not in metadata_text:
                errors.append(f"{path.relative_to(ROOT)} metadata omits source record {item_id}")
        visible_text = " ".join(
            "".join(element.itertext()) for element in root.findall(".//svg:text", namespace)
        )
        if tier == "primary" and (ID_TOKEN_RE.search(visible_text) or GAP_TOKEN_RE.search(visible_text)):
            errors.append(f"{path.relative_to(ROOT)} exposes raw model IDs in primary visible labels")
        metadata_lower = metadata_text.lower()
        if f"view tier: {tier}" not in metadata_lower or view["audience"].lower() not in metadata_lower:
            errors.append(f"{path.relative_to(ROOT)} metadata omits declared tier or audience")
        if tier == "primary":
            width = int(root.get("width", "0"))
            height = int(root.get("height", "0"))
            if width < 1200 or height < 600:
                errors.append(f"{path.relative_to(ROOT)} has unexpectedly small primary-view dimensions")
            sizes = [int(value) for value in re.findall(r"font-size:\s*(\d+)px", path.read_text(encoding="utf-8-sig"))]
            if not sizes or min(sizes) < 15:
                errors.append(f"{path.relative_to(ROOT)} uses primary-view text below 15 px")

    readme = (ROOT / "README.md").read_text(encoding="utf-8-sig")
    architecture = (ROOT / "docs" / "architecture.md").read_text(encoding="utf-8-sig")
    feasibility = (ROOT / "docs" / "feasibility.md").read_text(encoding="utf-8-sig")
    engineering_status = (ROOT / "docs" / "engineering-status.md").read_text(encoding="utf-8-sig")
    if "docs/figures/project-in-one-picture.svg" not in readme:
        errors.append("README.md lacks the primary system-concept figure")
    if len(re.findall(r"!\[[^\]]*\]\([^)]*\)", readme)) != 1:
        errors.append("README.md must contain exactly one hero figure")
    for relative in (
        "figures/physical-architecture.svg",
        "figures/command-data-flow.svg",
        "figures/degraded-behavior.svg",
    ):
        if relative not in architecture:
            errors.append(f"docs/architecture.md lacks primary communication figure {relative}")
    if "../analysis/results/feasible-region.svg" not in feasibility:
        errors.append("docs/feasibility.md lacks the primary feasibility result")
    if "figures/engineering-status.svg" not in engineering_status:
        errors.append("docs/engineering-status.md lacks the primary engineering-status figure")
    if ID_TOKEN_RE.search(readme) or GAP_TOKEN_RE.search(readme):
        errors.append("README orientation exposes raw architecture identifiers")
    return errors


def validate(catalogs: dict[str, dict[str, Any]]) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    records = definition_records(catalogs)
    definitions: dict[str, str] = {}

    for path, record in records:
        item_id = record.get("id")
        if not isinstance(item_id, str):
            errors.append(f"{path} lacks a string ID")
            continue
        if not ID_RE.fullmatch(item_id):
            errors.append(f"{path} has invalid ID {item_id!r}")
        if item_id in definitions:
            errors.append(f"duplicate ID {item_id}: {definitions[item_id]} and {path}")
        definitions[item_id] = path

    prefix_counts = collections.Counter(item_id.split("-", 1)[0] for item_id in definitions)
    for prefix, minimum in PRESERVED_ID_MINIMUMS.items():
        if prefix_counts[prefix] < minimum:
            errors.append(
                f"preserved {prefix}- ID count is {prefix_counts[prefix]}, minimum is {minimum}"
            )

    gap_codes: set[str] = set()
    for index, gap in enumerate(catalogs["traceability"].get("gaps", [])):
        code = gap.get("code")
        if not isinstance(code, str) or not GAP_RE.fullmatch(code):
            errors.append(f"traceability.gaps[{index}] has invalid code {code!r}")
        elif code in gap_codes:
            errors.append(f"duplicate gap code {code}")
        else:
            gap_codes.add(code)

    for catalog_name, catalog in catalogs.items():
        for ref_path, reference in references_in(catalog, catalog_name):
            if reference in REFERENCE_SENTINELS:
                continue
            if reference.startswith("GAP-"):
                if reference not in gap_codes:
                    errors.append(f"{ref_path} references undefined gap {reference}")
            elif ID_RE.fullmatch(reference) and reference not in definitions:
                errors.append(f"{ref_path} references undefined ID {reference}")

    active_markdown = [ROOT / "README.md"] + sorted((ROOT / "docs").rglob("*.md"))
    for markdown in active_markdown:
        if not markdown.exists():
            continue
        text = markdown.read_text(encoding="utf-8-sig")
        for match in ID_TOKEN_RE.finditer(text):
            token = match.group(0)
            if (
                token == "TS-XXX"
                or markdown.name == "requirement-id-migration.md" and LEGACY_REQUIREMENT_ID_RE.fullmatch(token)
                or text[match.end():].startswith("-*")
                or text[max(0, match.start() - 4):match.start()] == "GAP-"
            ):
                continue
            if token not in definitions:
                errors.append(f"{markdown.relative_to(ROOT)} references undefined ID {token}")
        for match in GAP_TOKEN_RE.finditer(text):
            gap_token = match.group(0)
            if text[max(0, match.start() - 4):match.start()] == "SRC-":
                continue
            if gap_token not in gap_codes:
                errors.append(f"{markdown.relative_to(ROOT)} references undefined gap {gap_token}")

    system = catalogs["system"]
    architecture = catalogs["architecture"]
    assurance = catalogs["assurance"]
    proof = catalogs["proof"]
    sources = catalogs["sources"]
    traceability = catalogs["traceability"]
    config_ids = {item["id"] for item in architecture["configurations"]}
    evidence_values = set(system["enumerations"]["evidence_basis"])
    decision_values = set(system["enumerations"]["decision_status"])

    if system.get("authority") != {"rule": AUTHORITY_RULE}:
        errors.append("model/system.yaml does not contain the single required authority rule")
    expected_catalogs = {
        "sources": ".seal/sources.yaml", "proof": ".seal/proof.yaml",
        "architecture": "model/architecture.yaml", "assurance": "model/assurance.yaml",
        "traceability": "model/traceability.yaml",
    }
    if system.get("catalogs") != expected_catalogs:
        errors.append("model/system.yaml catalog map does not match the consolidated authority model")
    expected_generated_reports = [
        "docs/reference/baseline.md", "docs/reference/architecture-atlas.md",
        "docs/reference/requirements.md", "docs/reference/interfaces.md",
        "docs/reference/traceability.md", "docs/reference/verification.md",
        "docs/reference/decisions-and-gaps.md",
    ]
    if system.get("generated_reports") != expected_generated_reports:
        errors.append("model/system.yaml generated-reference manifest is incomplete or out of order")
    expected_human_views = [
        "README.md", "docs/architecture.md", "docs/feasibility.md",
        "docs/engineering-status.md", "docs/reference/README.md",
    ]
    if system.get("human_readable_views") != expected_human_views:
        errors.append("model/system.yaml must name the orientation, primary narrative, and reference index")

    if system.get("status") != "baseline_candidate_not_approved":
        errors.append("baseline status must remain baseline_candidate_not_approved")
    if system.get("model_version") != "0.9.0-baseline-candidate":
        errors.append("model version must match the 0.9.0 identifier-migration baseline candidate")
    if system.get("baseline", {}).get("approval_state") != "not_approved":
        errors.append("technical baseline approval must remain not_approved")
    if sources.get("baseline_status") != "candidate_not_approved" or proof.get("baseline_status") != "candidate_not_approved":
        errors.append("source and proof catalogs must preserve candidate_not_approved status")
    for config in architecture["configurations"]:
        if config.get("approval_status") == "approved":
            errors.append(f"{config['id']} is incorrectly marked approved")

    internal_verification = system.get("internal_verification_baseline", {})
    expected_internal_verification = {
        "model_version": "0.7.0-baseline-candidate",
        "work_package_status": "approved",
        "approval_scope": "model-level verification work and evidence records only",
        "approval_date": "2026-08-11",
        "source_refs": ["SRC-DEC-005"],
        "evidence_refs": ["EVD-012"],
        "technical_baseline_approval": "not_approved",
        "physical_verification": "not_established",
        "safety_approval": "not_approved",
        "external_interface_conformance": "not_established",
        "unresolved_decisions": ["DEC-002", "DEC-003", "DEC-004", "DEC-005"],
    }
    if internal_verification != expected_internal_verification:
        errors.append("internal verification work-package disposition or approval boundary changed")
    expected_latest_review = {
        "model_version": "0.8.0-baseline-candidate",
        "review_status": "executed_not_owner_accepted",
        "review_date": "2026-08-11",
        "source_refs": ["SRC-DEC-006"],
        "evidence_refs": ["EVD-013"],
        "relationship_to_accepted_baseline": (
            "The accepted 0.7.0 internal-verification baseline remains preserved. "
            "EVD-013 records the fresh model-level review of 0.8.0 changes but is not "
            "project-owner acceptance or technical-baseline approval."
        ),
        "technical_baseline_approval": "not_approved",
        "physical_verification": "not_established",
        "safety_approval": "not_approved",
        "external_interface_conformance": "not_established",
    }
    if system.get("latest_recorded_model_review") != expected_latest_review:
        errors.append("latest recorded model review or its non-approval boundary changed")

    reconciliation = architecture.get("configuration_reconciliation")
    if not isinstance(reconciliation, dict):
        errors.append("architecture lacks configuration_reconciliation")
        reconciliation = {}
    forward_values = set(system["enumerations"]["recovered_to_candidate_mapping"])
    reverse_values = set(system["enumerations"]["candidate_to_recovered_mapping"])
    cross_source_values = set(system["enumerations"]["cross_source_support"])
    common_mapping_fields = {
        "source_item_description", "source_refs", "evidence_refs", "evidence_basis",
        "mapping_classification", "candidate_target_ids", "confidence", "limitation",
        "applicable_configurations",
    }
    mapping_groups = (
        ("recovered_to_candidate", forward_values, True),
        ("candidate_components_to_recovered", reverse_values, False),
        ("candidate_interfaces_to_recovered", reverse_values, False),
    )
    all_definition_records = {record.get("id"): record for _, record in records if record.get("id")}
    mapping_record_ids: set[str] = set()
    for group_name, allowed_values, is_forward in mapping_groups:
        group = reconciliation.get(group_name, [])
        if not isinstance(group, list):
            errors.append(f"configuration_reconciliation.{group_name} must be a list")
            continue
        for index, record in enumerate(group):
            label = record.get("record_id") or record.get("candidate_id") or f"{group_name}[{index}]"
            missing = common_mapping_fields - record.keys()
            if missing:
                errors.append(f"{label} lacks reconciliation fields: {', '.join(sorted(missing))}")
            if is_forward:
                record_id = record.get("record_id")
                if not isinstance(record_id, str) or not re.fullmatch(r"REC-(?:MAP|CON)-\d{3}", record_id):
                    errors.append(f"{label} has invalid reconciliation record ID")
                elif record_id in mapping_record_ids:
                    errors.append(f"duplicate reconciliation record ID {record_id}")
                else:
                    mapping_record_ids.add(record_id)
                if record.get("cross_source_support") not in cross_source_values:
                    errors.append(f"{label} has invalid cross-source support")
                if "CFG-REC" not in record.get("applicable_configurations", []):
                    errors.append(f"{label} lacks CFG-REC scope")
            if record.get("mapping_classification") not in allowed_values:
                errors.append(f"{label} has invalid mapping classification")
            if record.get("evidence_basis") not in evidence_values:
                errors.append(f"{label} has invalid reconciliation evidence basis")
            confidence = record.get("confidence")
            if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
                errors.append(f"{label} has invalid confidence")
            if not isinstance(record.get("source_item_description"), str) or not record.get("source_item_description"):
                errors.append(f"{label} lacks a source item description")
            if not isinstance(record.get("limitation"), str) or not record.get("limitation"):
                errors.append(f"{label} lacks a limitation")
            targets = record.get("candidate_target_ids", [])
            if not targets and not record.get("unmatched_status"):
                errors.append(f"{label} lacks a candidate target or explicit unmatched status")
            for target in targets:
                if target not in definitions:
                    errors.append(f"{label} has undefined candidate target {target}")
                if is_forward:
                    target_record = all_definition_records.get(target, {})
                    target_configs = set(target_record.get("applicable_configurations", []))
                    if target_configs and target_configs.issubset({"CFG-DIG", "CFG-SOS"}):
                        errors.append(f"{label} falsely presents future-only {target} as recovered evidence")
            if record.get("decision_status") == "approved" or record.get("approval_status") == "approved":
                errors.append(f"{label} incorrectly approves a reconciliation result")
            if record.get("mapping_classification") in {"CONTRADICTORY", "CONTRADICTED"}:
                if not record.get("gap_refs") and not record.get("owner_review_status"):
                    errors.append(f"{label} has an unmanaged contradiction")

    expected_components = {
        item["id"] for item in architecture["components"]
        if set(item.get("applicable_configurations", [])).intersection({"CFG-REP", "CFG-DOM"})
    }
    reverse_component_ids = [
        item.get("candidate_id")
        for item in reconciliation.get("candidate_components_to_recovered", [])
    ]
    if set(reverse_component_ids) != expected_components or len(reverse_component_ids) != len(set(reverse_component_ids)):
        errors.append("candidate component reconciliation must cover every current component exactly once")
    interface_ids = {item["id"] for item in architecture["interfaces"]}
    reverse_interface_ids = [
        item.get("candidate_id")
        for item in reconciliation.get("candidate_interfaces_to_recovered", [])
    ]
    if set(reverse_interface_ids) != interface_ids or len(reverse_interface_ids) != len(set(reverse_interface_ids)):
        errors.append("candidate interface reconciliation must cover every interface exactly once")
    integrity_by_source = {
        item.get("source_id"): item for item in reconciliation.get("source_integrity", [])
    }
    expected_integrity = {
        "SRC-INT-001": ("EF32AF40F1AE48CA631249B76EE85B6F726FCB4BCFE3796FD388D2C3DA3033BC", "MATCH"),
        "SRC-INT-002": ("577F5FD4B6662E7982CDB73663A2534C829627E5ABFC3FEE3FB68D6837271BFA", "MATCH"),
        "SRC-INT-003": ("4D28858FD484E94B086ADBC186452B1BD3F4222E50BFF6779C89661298570EF1", "MISMATCH"),
    }
    if set(integrity_by_source) != set(expected_integrity):
        errors.append("source integrity reconciliation must cover exactly SRC-INT-001 through SRC-INT-003")
    for source_id, (expected_hash, expected_status) in expected_integrity.items():
        record = integrity_by_source.get(source_id, {})
        if record.get("expected_sha256") != expected_hash or record.get("status") != expected_status:
            errors.append(f"{source_id} integrity disposition changed without source registration")
        if not record.get("actual_sha256") or not record.get("treatment"):
            errors.append(f"{source_id} lacks actual checksum or treatment")

    for path, record in records:
        item_id = record.get("id", path)
        if item_id.startswith("CFG-"):
            continue
        configurations = record.get("applicable_configurations")
        scope = record.get("applicability_scope")
        inactive = record.get("lifecycle_status") == "reserved_inactive"
        if not isinstance(configurations, list):
            errors.append(f"{item_id} lacks configuration applicability")
        elif not configurations and not scope and not inactive:
            errors.append(f"{item_id} has empty configuration applicability without an explicit scope")
        elif any(value != "TBD" and value not in config_ids for value in configurations):
            errors.append(f"{item_id} has invalid configuration applicability {configurations}")
        if record.get("evidence_basis") not in evidence_values and "evidence_basis" in record:
            errors.append(f"{item_id} has invalid evidence_basis {record.get('evidence_basis')!r}")
        if record.get("decision_status") not in decision_values and "decision_status" in record:
            errors.append(f"{item_id} has invalid decision_status {record.get('decision_status')!r}")

    source_required = {
        "id", "title", "source_type", "location", "owner", "date", "revision",
        "accessed_date", "reliability", "notes", "kind", "description",
        "authority_state", "approval_state", "confidence", "applicable_configurations",
    }
    for source in sources["sources"]:
        missing = source_required - source.keys()
        if missing:
            errors.append(f"{source.get('id', 'source')} lacks source fields: {', '.join(sorted(missing))}")
    for source_id in ("SRC-EXT-001", "SRC-EXT-002"):
        source = next(item for item in sources["sources"] if item["id"] == source_id)
        if source.get("applicability_scope") != "project_methodology" or source["applicable_configurations"]:
            errors.append(f"{source_id} must be project-level methodology with no CFG-* applicability")
    for source_id in ("SRC-INT-001", "SRC-INT-002", "SRC-INT-003"):
        source = next(item for item in sources["sources"] if item["id"] == source_id)
        scope = source.get("applicability_scope", "").lower()
        if "lineage" not in scope or "does not establish" not in scope:
            errors.append(f"{source_id} does not distinguish candidate lineage from physical equivalence")
    source_by_id = {item["id"]: item for item in sources["sources"]}
    acceptance_source = source_by_id.get("SRC-DEC-005", {})
    acceptance_source_text = " ".join(
        str(acceptance_source.get(field, ""))
        for field in ("description", "applicability_scope", "notes")
    ).lower()
    for boundary in (
        "technical baseline", "physical", "safety", "external-interface conformance",
        "dec-002 through dec-005", "baseline_candidate_not_approved",
    ):
        if boundary not in acceptance_source_text:
            errors.append(f"SRC-DEC-005 does not preserve the {boundary} acceptance boundary")
    completion_source = source_by_id.get("SRC-DEC-006", {})
    completion_source_text = " ".join(
        str(completion_source.get(field, ""))
        for field in ("description", "applicability_scope", "notes")
    ).lower()
    for boundary in (
        "model-local architecture completeness", "without selecting technical values",
        "dec", "ver-008", "ver-009", "ts-009", "baseline_candidate_not_approved",
    ):
        if boundary not in completion_source_text:
            errors.append(f"SRC-DEC-006 does not preserve the {boundary} work-package boundary")

    claim_ids = {item["id"] for item in proof["claims"]}
    for claim in proof["claims"]:
        for required in (
            "subject", "statement", "subject_ids", "source_refs", "evidence_refs",
            "evidence_basis", "confidence", "decision_status", "applicable_configurations",
            "rationale", "contradicts", "supersedes",
        ):
            if required not in claim:
                errors.append(f"{claim['id']} lacks consolidated claim field {required}")
        if claim.get("evidence_basis") != "unknown" and not claim.get("source_refs"):
            errors.append(f"{claim['id']} has an evidence basis but no source")
    for evidence in proof["evidence"]:
        for supported in evidence.get("supports", []):
            if supported not in claim_ids:
                errors.append(f"{evidence['id']} supports undefined claim {supported}")
    freshness_values = set(system["enumerations"]["claim_freshness_review"])
    freshness_reviews = proof.get("claim_freshness_review", [])
    freshness_claim_ids = [item.get("claim_id") for item in freshness_reviews]
    if set(freshness_claim_ids) != claim_ids or len(freshness_claim_ids) != len(set(freshness_claim_ids)):
        errors.append("claim freshness review must cover every claim exactly once")
    claim_by_id = {item["id"]: item for item in proof["claims"]}
    for review in freshness_reviews:
        claim_id = review.get("claim_id")
        classification = review.get("classification")
        if classification not in freshness_values:
            errors.append(f"{claim_id} has invalid freshness-review classification")
        if review.get("reviewed_model_version") != system["latest_recorded_model_review"]["model_version"]:
            errors.append(f"{claim_id} freshness review does not identify the latest recorded review version")
        if classification == "CURRENT_MODEL_CLAIM_REVIEWED":
            if not review.get("evidence_ids"):
                errors.append(f"{claim_id} current-model freshness review lacks evidence")
            if claim_by_id.get(claim_id, {}).get("freshness", {}).get("checked_at") != review.get("review_date"):
                errors.append(f"{claim_id} current-model freshness date is inconsistent")
        if classification == "UNCHANGED_SOURCE_CLAIM" and review.get("evidence_ids"):
            errors.append(f"{claim_id} unchanged-source review incorrectly adds current evidence")

    endpoint_types = {"CMP", "OP"}
    for interface in architecture["interfaces"]:
        for key in ("endpoint_a", "endpoint_b"):
            endpoint = interface.get(key)
            if endpoint not in definitions:
                errors.append(f"{interface['id']} has undefined {key} {endpoint}")
            elif endpoint.split("-", 1)[0] not in endpoint_types:
                errors.append(f"{interface['id']} has invalid endpoint type {endpoint}")
    performer_ids = {item["id"] for item in architecture["performers"]}
    exchange_ids = {item["id"] for item in architecture["information_exchanges"]}
    activity_ids = {item["id"] for item in architecture["operational_activities"]}
    function_ids = {item["id"] for item in architecture["functions"]}
    mode_ids = {item["id"] for item in architecture["modes"]}
    current_configs = {"CFG-REP", "CFG-DOM"}
    required_interface_fields = {
        "endpoint_a", "endpoint_b", "direction", "flow_class", "interface_type", "owner",
        "applicable_configurations", "operational_scenarios", "normal_behavior",
        "failure_behavior", "security_concerns", "safety_concerns", "verification_ids",
        "source_ids", "claim_ids", "evidence_basis", "decision_status", "unknown_attributes",
    }
    for interface in architecture["interfaces"]:
        if current_configs.intersection(interface.get("applicable_configurations", [])):
            missing = required_interface_fields - interface.keys()
            if missing:
                errors.append(
                    f"current interface {interface['id']} lacks fields: {', '.join(sorted(missing))}"
                )
            for field in (
                "operational_scenarios", "normal_behavior", "failure_behavior",
                "verification_ids", "source_ids", "unknown_attributes",
            ):
                if not interface.get(field):
                    errors.append(f"current interface {interface['id']} lacks meaningful {field}")
            if "VER-005" not in interface.get("verification_ids", []):
                errors.append(f"current interface {interface['id']} lacks interface-catalog review allocation")

    resource_relationships = architecture.get("resource_relationships", [])
    if not isinstance(resource_relationships, list):
        errors.append("architecture.resource_relationships must be a list")
        resource_relationships = []
    resource_relationship_keys: set[tuple[str, str, str]] = set()
    resource_relationship_fields = {
        "from", "relation", "to", "label", "purpose", "relationship_type", "status",
        "evidence_basis", "decision_status", "applicable_configurations", "source_ids",
        "verification_ids", "view_groups",
    }
    for index_number, relationship in enumerate(resource_relationships):
        label = f"architecture.resource_relationships[{index_number}]"
        missing = resource_relationship_fields - relationship.keys()
        if missing:
            errors.append(f"{label} lacks fields: {', '.join(sorted(missing))}")
        key = (
            relationship.get("from", ""), relationship.get("relation", ""),
            relationship.get("to", ""),
        )
        if key in resource_relationship_keys:
            errors.append(f"duplicate resource relationship {key}")
        resource_relationship_keys.add(key)
        if relationship.get("from") not in definitions or relationship.get("to") not in definitions:
            errors.append(f"{label} has undefined endpoints")
        if relationship.get("relationship_type") not in {"structural", "interface_participation"}:
            errors.append(f"{label} has unsupported relationship type")
        if relationship.get("status") not in set(system["enumerations"]["relationship_status"]):
            errors.append(f"{label} has invalid status")
        if relationship.get("evidence_basis") not in evidence_values:
            errors.append(f"{label} has invalid evidence basis")
        if relationship.get("decision_status") not in decision_values:
            errors.append(f"{label} has invalid decision status")
        if not current_configs.intersection(relationship.get("applicable_configurations", [])):
            errors.append(f"{label} does not apply to the current architecture")

    initial_mode = architecture.get("initial_mode")
    if initial_mode not in mode_ids:
        errors.append("architecture initial_mode is undefined")
    mode_transition_keys: set[tuple[str, str]] = set()
    for transition in architecture.get("mode_transitions", []):
        key = (transition.get("from", ""), transition.get("to", ""))
        if key in mode_transition_keys:
            errors.append(f"duplicate mode transition {key}")
        mode_transition_keys.add(key)
        if key[0] not in mode_ids or key[1] not in mode_ids:
            errors.append(f"mode transition {key} has undefined endpoint")
        for field in (
            "label", "trigger_refs", "status", "evidence_basis", "decision_status",
            "applicable_configurations", "source_ids", "verification_ids",
        ):
            if not transition.get(field):
                errors.append(f"mode transition {key} lacks {field}")
        if not current_configs.intersection(transition.get("applicable_configurations", [])):
            errors.append(f"mode transition {key} leaks outside the current architecture")
    if len(mode_transition_keys) != 6:
        errors.append(f"current mode-transition set must contain 6 explicit records, found {len(mode_transition_keys)}")

    scenario_ids = {item["id"] for item in architecture["scenarios"]}
    scenario_transition_keys: set[tuple[str, str]] = set()
    for transition in architecture.get("scenario_transitions", []):
        key = (transition.get("from", ""), transition.get("to", ""))
        if key in scenario_transition_keys:
            errors.append(f"duplicate scenario transition {key}")
        scenario_transition_keys.add(key)
        if key[0] not in scenario_ids or key[1] not in scenario_ids:
            errors.append(f"scenario transition {key} has undefined endpoint")
        if transition.get("transition_type") not in {"current", "future"}:
            errors.append(f"scenario transition {key} lacks controlled transition_type")
        if transition.get("transition_type") == "future":
            if current_configs.intersection(transition.get("applicable_configurations", [])):
                errors.append(f"future scenario transition {key} leaks into current configurations")
            if not transition.get("gap_refs"):
                errors.append(f"future scenario transition {key} lacks a controlled gap")
        elif not current_configs.intersection(transition.get("applicable_configurations", [])):
            errors.append(f"current scenario transition {key} lacks current applicability")
    if len(scenario_transition_keys) != 10:
        errors.append(
            f"scenario-transition set must contain 10 explicit current/future records, found {len(scenario_transition_keys)}"
        )

    for scenario in architecture["scenarios"]:
        if not scenario.get("performers") or any(item not in performer_ids for item in scenario["performers"]):
            errors.append(f"{scenario['id']} has unresolved performers")
        if any(item not in exchange_ids and item != "TBD" for item in scenario.get("information_exchanges", [])):
            errors.append(f"{scenario['id']} has unresolved information exchanges")
        if any(item not in activity_ids and item != "TBD" for item in scenario.get("activities", [])):
            errors.append(f"{scenario['id']} has unresolved activities")
        if any(item not in function_ids for item in scenario.get("system_functions", [])):
            errors.append(f"{scenario['id']} has unresolved system functions")
        if any(item not in mode_ids for item in scenario.get("related_modes", [])):
            errors.append(f"{scenario['id']} has unresolved modes")
        if current_configs.intersection(scenario.get("applicable_configurations", [])):
            for field in (
                "activities", "information_exchanges", "system_functions", "related_modes",
                "related_requirements", "related_hazards", "verification_ids",
            ):
                if not scenario.get(field):
                    errors.append(f"current scenario {scenario['id']} lacks {field}")
            for field in ("evidence_ids", "gap_refs"):
                if field not in scenario:
                    errors.append(f"current scenario {scenario['id']} lacks explicit {field}")
        elif not scenario.get("activities") and scenario.get("activity_allocation_disposition") != "future_configuration_gap":
            errors.append(f"future scenario {scenario['id']} lacks an activity-allocation disposition")

    classifications = set(system["enumerations"]["requirement_classification"])
    readiness_values = set(system["enumerations"]["verification_readiness"])
    requirements = assurance["requirements"]
    deferred_topics = assurance.get("deferred_topics", [])
    requirement_ids = {item["id"] for item in requirements}
    deferred_topic_ids = {item["id"] for item in deferred_topics}
    expected_requirement_ids = {f"REQ-{number:03d}" for number in range(1, 24)}
    expected_deferred_topic_ids = {f"DEF-{number:03d}" for number in range(1, 6)}
    if requirement_ids != expected_requirement_ids or len(requirements) != 23:
        errors.append("active requirements must be exactly REQ-001 through REQ-023")
    if deferred_topic_ids != expected_deferred_topic_ids or len(deferred_topics) != 5:
        errors.append("deferred topics must be exactly DEF-001 through DEF-005")
    for catalog_name in ("system", "architecture", "assurance", "traceability", "sources", "proof"):
        serialized = json.dumps(catalogs[catalog_name], sort_keys=True)
        match = LEGACY_REQUIREMENT_ID_RE.search(serialized)
        if match:
            errors.append(f"{catalog_name} contains prohibited legacy requirement ID {match.group(0)}")
    quality_audits = assurance.get("requirement_quality_audit", [])
    audit_ids = [item.get("requirement_id") for item in quality_audits]
    if set(audit_ids) != requirement_ids or len(audit_ids) != len(set(audit_ids)):
        errors.append("requirement quality audit must contain exactly one entry for every requirement")
    audit_by_requirement = {item.get("requirement_id"): item for item in quality_audits}
    requirement_names: set[str] = set()
    for requirement in requirements:
        if not REQUIREMENT_ID_RE.fullmatch(requirement.get("id", "")):
            errors.append(f"{requirement.get('id')} does not use the neutral REQ-NNN scheme")
        display_name = requirement.get("display_name")
        if not isinstance(display_name, str) or not display_name.strip():
            errors.append(f"{requirement['id']} lacks a human-readable display_name")
        elif display_name.casefold() in requirement_names:
            errors.append(f"duplicate requirement display_name {display_name!r}")
        else:
            requirement_names.add(display_name.casefold())
        for field in ("text", "classification", "applicable_configurations", "verification_ids"):
            if not requirement.get(field):
                errors.append(f"{requirement['id']} lacks required field {field}")
        if requirement.get("classification") not in classifications:
            errors.append(f"{requirement['id']} has invalid requirement classification")
        if not requirement.get("upstream_refs") and not requirement.get("provenance_gap"):
            errors.append(f"{requirement['id']} lacks provenance or a documented gap")
        if not requirement.get("verification_ids"):
            errors.append(f"{requirement['id']} lacks verification allocation")
        audit = audit_by_requirement.get(requirement["id"], {})
        if audit.get("verification_readiness") not in readiness_values:
            errors.append(f"{requirement['id']} lacks controlled verification readiness")
        if "[TBD]" in requirement.get("text", ""):
            governance = audit.get("tbd_governance")
            required_tbd_fields = {"category", "owner_ids", "dependency", "reason", "verification_implication"}
            if not isinstance(governance, dict) or not required_tbd_fields.issubset(governance):
                errors.append(f"{requirement['id']} has an ungoverned substantive TBD")
        if not requirement.get("allocation_refs") and audit.get("quality_result") not in {
            "cross_cutting_constraint", "scope_control", "pass_with_open_tbd",
        }:
            errors.append(f"{requirement['id']} lacks downward allocation or a semantic exception")

    deferred_audits = assurance.get("deferred_topic_quality_audit", [])
    deferred_audit_ids = [item.get("deferred_topic_id") for item in deferred_audits]
    if set(deferred_audit_ids) != deferred_topic_ids or len(deferred_audit_ids) != len(set(deferred_audit_ids)):
        errors.append("deferred-topic quality audit must contain exactly one entry per deferred topic")
    deferred_names: set[str] = set()
    for topic in deferred_topics:
        if not DEFERRED_TOPIC_ID_RE.fullmatch(topic.get("id", "")):
            errors.append(f"{topic.get('id')} does not use the DEF-NNN scheme")
        display_name = topic.get("display_name")
        if not isinstance(display_name, str) or not display_name.strip():
            errors.append(f"{topic['id']} lacks a human-readable display_name")
        elif display_name.casefold() in deferred_names:
            errors.append(f"duplicate deferred-topic display_name {display_name!r}")
        else:
            deferred_names.add(display_name.casefold())
        for field in ("text", "classification", "applicable_configurations", "decision_status"):
            if not topic.get(field):
                errors.append(f"{topic['id']} lacks required field {field}")
        if topic.get("classification") not in classifications:
            errors.append(f"{topic['id']} has invalid deferred-topic classification")
        if topic.get("decision_status") != "not_applicable":
            errors.append(f"{topic['id']} must remain explicitly non-requirement scope")

    execution_values = set(system["enumerations"]["verification_execution_status"])
    evidence_by_id = {item["id"]: item for item in proof["evidence"]}
    verification_by_id = {item["id"]: item for item in assurance["verifications"]}
    acceptance_evidence = evidence_by_id.get("EVD-012", {})
    if acceptance_evidence.get("source_refs") != ["SRC-DEC-005"]:
        errors.append("EVD-012 must derive only from SRC-DEC-005")
    if acceptance_evidence.get("evidence_level") != "work_package_acceptance_only":
        errors.append("EVD-012 must remain work-package acceptance evidence only")
    if acceptance_evidence.get("verification_ids"):
        errors.append("EVD-012 must not be presented as verification execution evidence")
    expected_preserved_gaps = {
        "GAP-VER-001", "GAP-IFC-001", "GAP-HAZ-001", "GAP-BUDGET-001",
        "GAP-TRC-001", "GAP-SOS-001", "GAP-SOS-002",
    }
    if not expected_preserved_gaps.issubset(set(acceptance_evidence.get("object_refs", []))):
        errors.append("EVD-012 does not reference every explicitly preserved verification or future-scope gap")
    acceptance_text = " ".join(
        [str(acceptance_evidence.get("result", ""))]
        + [str(item) for item in acceptance_evidence.get("limitations", [])]
        + [str(acceptance_evidence.get("applicability_scope", ""))]
    ).lower()
    for boundary in (
        "technical baseline", "physical verification", "safety approval",
        "external-interface conformance", "dec-002 through dec-005 remain proposed",
    ):
        if boundary not in acceptance_text:
            errors.append(f"EVD-012 does not preserve the {boundary} acceptance boundary")
    latest_review = system["latest_recorded_model_review"]
    latest_review_evidence = evidence_by_id.get("EVD-013", {})
    if latest_review_evidence.get("source_refs", [None])[0] != "SRC-DEC-006":
        errors.append("EVD-013 must derive from SRC-DEC-006")
    if latest_review_evidence.get("reviewed_model_version") != latest_review["model_version"]:
        errors.append("EVD-013 must preserve the latest recorded model-review version")
    if latest_review_evidence.get("evidence_level") != "model_level_only":
        errors.append("EVD-013 must remain model-level evidence only")
    if set(latest_review_evidence.get("verification_ids", [])) != {
        "VER-001", "VER-002", "VER-003", "VER-004", "VER-005", "VER-006", "VER-007"
    }:
        errors.append("EVD-013 must record the full current internal model-review cycle")
    review_limitations = " ".join(latest_review_evidence.get("limitations", [])).lower()
    for boundary in (
        "not owner-accepted", "does not establish physical", "does not approve dec-002 through dec-005",
    ):
        if boundary not in review_limitations:
            errors.append(f"EVD-013 does not preserve the {boundary} boundary")
    for verification in assurance["verifications"]:
        if verification.get("readiness") not in readiness_values:
            errors.append(f"{verification['id']} lacks controlled readiness")
        if not verification.get("readiness_note"):
            errors.append(f"{verification['id']} lacks readiness rationale")
        for field in (
            "execution_status", "execution_date", "reviewed_model_version",
            "evidence_ids", "result_summary", "residual_gap_ids",
        ):
            if field not in verification:
                errors.append(f"{verification['id']} lacks execution field {field}")
        execution_status = verification.get("execution_status")
        if execution_status not in execution_values:
            errors.append(f"{verification['id']} has invalid execution status")
        if execution_status in {"executed_pass", "executed_with_open_gaps"}:
            if not verification.get("execution_date") or verification.get("reviewed_model_version") != latest_review["model_version"]:
                errors.append(f"{verification['id']} executed review lacks latest recorded date/version metadata")
            if not verification.get("evidence_ids"):
                errors.append(f"{verification['id']} executed review lacks evidence")
            for evidence_id in verification.get("evidence_ids", []):
                evidence = evidence_by_id.get(evidence_id, {})
                if verification["id"] not in evidence.get("verification_ids", []):
                    errors.append(f"{verification['id']} evidence {evidence_id} does not record its execution")
                if evidence.get("reviewed_model_version") != latest_review["model_version"]:
                    errors.append(f"{verification['id']} evidence {evidence_id} targets another model version")
                if execution_status == "executed_pass" and "fail" in evidence.get("result", "").lower():
                    errors.append(f"{verification['id']} is executed_pass but {evidence_id} reports failure")
        elif verification.get("evidence_ids"):
            errors.append(f"{verification['id']} is not executed but cites execution evidence")
    for verification_id in ("VER-001", "VER-002", "VER-003", "VER-004", "VER-005", "VER-006", "VER-007"):
        if verification_by_id[verification_id].get("execution_status") not in {"executed_pass", "executed_with_open_gaps"}:
            errors.append(f"{verification_id} lacks an executed current-model disposition")
    if verification_by_id["VER-008"].get("execution_status") != "deferred" or verification_by_id["VER-008"].get("evidence_ids"):
        errors.append("VER-008 must remain deferred without model-only execution evidence")
    if verification_by_id["VER-009"].get("execution_status") != "blocked" or verification_by_id["VER-009"].get("evidence_ids"):
        errors.append("VER-009 must remain blocked without external-authority execution evidence")
    for evidence_id in ("EVD-008", "EVD-009", "EVD-010", "EVD-011"):
        evidence = evidence_by_id[evidence_id]
        if evidence.get("reviewed_model_version") != "0.7.0-baseline-candidate":
            errors.append(f"{evidence_id} no longer preserves the accepted 0.7.0 execution trail")
        if evidence.get("evidence_level") != "model_level_only":
            errors.append(f"{evidence_id} is not explicitly model-level evidence only")
    physical_requirement_ids = {
        item["requirement_id"] for item in quality_audits
        if item.get("verification_readiness") == "physical_evidence_required"
    }
    for requirement in requirements:
        if requirement["id"] in physical_requirement_ids and any(
            requirement.get(field) is True for field in ("verified", "satisfied", "compliant")
        ):
            errors.append(f"{requirement['id']} is falsely marked satisfied by model-level evidence")

    for hazard in assurance["hazards"]:
        if not hazard.get("control_disposition"):
            errors.append(f"{hazard['id']} lacks an explicit control disposition")
        if "control_refs" not in hazard:
            errors.append(f"{hazard['id']} lacks explicit control references")
    for control in assurance["controls"]:
        if not control.get("implemented_by"):
            errors.append(f"{control['id']} has no implementing requirement")

    relationships = {
        (item["from"], item["relation"], item["to"]): item
        for item in traceability["relationships"]
    }
    if len(relationships) != len(traceability["relationships"]):
        errors.append("traceability relationships contain a duplicate from/relation/to triple")
    current_components = [
        item for item in architecture["components"]
        if current_configs.intersection(item.get("applicable_configurations", []))
    ]
    requirement_allocations = {
        allocation
        for requirement in assurance["requirements"]
        for allocation in requirement.get("allocation_refs", [])
    }
    function_allocations = {
        item["to"]
        for item in traceability["relationships"]
        if item.get("relation") == "allocated_to" and item.get("from", "").startswith("FUN-")
    }
    interface_participants = {
        endpoint
        for interface in architecture["interfaces"]
        if current_configs.intersection(interface.get("applicable_configurations", []))
        for endpoint in (interface.get("endpoint_a"), interface.get("endpoint_b"))
    }
    resource_participants = {
        endpoint
        for relationship in resource_relationships
        for endpoint in (relationship.get("from"), relationship.get("to"))
    }
    for component in current_components:
        component_id = component["id"]
        if not component.get("architecture_role"):
            errors.append(f"current component {component_id} lacks an architecture role")
        participates = component_id in (
            requirement_allocations | function_allocations | interface_participants | resource_participants
        )
        if not participates and not component.get("passive_rationale"):
            errors.append(
                f"current component {component_id} has no function, interface, resource relationship, "
                "requirement allocation, or passive rationale"
            )

    current_scenarios = [
        item for item in architecture["scenarios"]
        if current_configs.intersection(item.get("applicable_configurations", []))
    ]
    scenario_functions = {
        function_id for scenario in current_scenarios for function_id in scenario.get("system_functions", [])
    }
    activity_functions = {
        item["to"]
        for item in traceability["relationships"]
        if item.get("relation") == "performed_by_function"
    }
    for function in architecture["functions"]:
        if not current_configs.intersection(function.get("applicable_configurations", [])):
            continue
        function_id = function["id"]
        if not function.get("purpose"):
            errors.append(f"current function {function_id} lacks an explicit purpose")
        if (
            function_id not in scenario_functions
            and function_id not in activity_functions
            and not function.get("activity_rationale")
        ):
            errors.append(f"current function {function_id} lacks scenario or activity rationale")
        requirement_trace = any(
            function_id in requirement.get("allocation_refs", [])
            for requirement in assurance["requirements"]
        )
        if not requirement_trace and not function.get("traceability_rationale"):
            errors.append(
                f"current function {function_id} lacks requirement/verification trace or explicit rationale"
            )
    for exchange in architecture["information_exchanges"]:
        if current_configs.intersection(exchange.get("applicable_configurations", [])):
            realized = any(
                relation["from"] == exchange["id"]
                and relation["relation"] == "realized_by"
                and not relation.get("gap")
                for relation in traceability["relationships"]
            )
            if not realized:
                errors.append(f"current exchange {exchange['id']} lacks an ungapped interface realization")
    for function in architecture["functions"]:
        if current_configs.intersection(function.get("applicable_configurations", [])):
            allocated = any(
                relation["from"] == function["id"]
                and relation["relation"] == "allocated_to"
                and not relation.get("gap")
                for relation in traceability["relationships"]
            )
            if not allocated:
                errors.append(f"current function {function['id']} lacks resource allocation")
    required_relationships = {
        ("HAZ-004", "mitigated_by", "CTL-001"),
        ("CTL-001", "implemented_by", "REQ-006"),
        ("CTL-001", "implemented_by", "REQ-019"),
        ("HAZ-008", "mitigated_by", "CTL-005"),
        ("CTL-005", "implemented_by", "REQ-017"),
    }
    for relation in required_relationships:
        if relation not in relationships or relationships[relation].get("gap"):
            errors.append("missing or gapped reconciled relationship: " + " -> ".join(relation))
    relation_statuses = set(system["enumerations"]["relationship_status"])
    gap_dispositions = set(system["enumerations"]["gap_disposition"])
    for relation in traceability["relationships"]:
        if relation.get("status") not in relation_statuses:
            errors.append(f"invalid relationship status in {relation}")
    for gap in traceability["gaps"]:
        if gap.get("disposition") not in gap_dispositions:
            errors.append(f"{gap['code']} has invalid disposition")
        if gap.get("audit_classification") not in set(system["enumerations"]["gap_audit_classification"]):
            errors.append(f"{gap['code']} lacks a controlled audit classification")
        if not gap.get("work_package_outcome") or not gap.get("next_action"):
            errors.append(f"{gap['code']} lacks an outcome or concrete next action")

    for interface in architecture["interfaces"]:
        if not interface["id"].startswith("IFC-EXT-"):
            continue
        if interface.get("logical_definition_status") != "complete_at_architecture_level":
            errors.append(f"{interface['id']} lacks logical-definition completeness status")
        if "VER-005" not in interface.get("internal_model_verification_ids", []):
            errors.append(f"{interface['id']} lacks internal interface-catalog review")
        if interface.get("external_conformance_verification_ids") != ["VER-009"]:
            errors.append(f"{interface['id']} lacks separated external-conformance verification")
        if interface.get("external_conformance_status") != "external_authority_and_execution_evidence_required":
            errors.append(f"{interface['id']} obscures external authority or evidence status")

    inner = system["system_boundaries"]["inner"]
    if "CFG-REC" in inner.get("applicable_configurations", []):
        errors.append("CFG-REC must not inherit the proposed inner-boundary decomposition")
    recovered = next(item for item in architecture["configurations"] if item["id"] == "CFG-REC")
    if "descriptive evidence" not in recovered.get("boundary_semantics", "").lower():
        errors.append("CFG-REC lacks descriptive-evidence boundary semantics")
    for record in requirements + deferred_topics + assurance["controls"] + architecture["interfaces"] + architecture["modes"]:
        if "CFG-REC" in record.get("applicable_configurations", []):
            errors.append(f"{record['id']} incorrectly applies proposed design semantics to CFG-REC")
    ts_009 = next(item for item in assurance["trade_studies"] if item["id"] == "TS-009")
    if "CFG-REC" in ts_009.get("applicable_configurations", []):
        errors.append("TS-009 must not impose a proposed trade study on CFG-REC")
    op_002 = next(item for item in architecture["performers"] if item["id"] == "OP-002")
    if "CFG-REC" in op_002.get("applicable_configurations", []):
        errors.append("OP-002 must not impose proposed performer semantics on CFG-REC")

    payload_resources = {"CMP-COM-01", "CMP-COM-02"}
    crossings: set[str] = set()
    for interface in architecture["interfaces"]:
        endpoints = {interface["endpoint_a"], interface["endpoint_b"]}
        configs = set(interface.get("applicable_configurations", []))
        if interface["id"].startswith("IFC-INT-") and configs.intersection({"CFG-REP", "CFG-DOM"}):
            if len(endpoints.intersection(payload_resources)) == 1:
                crossings.add(interface["id"])
    if crossings != {"IFC-INT-003", "IFC-INT-007"}:
        errors.append(f"current platform-to-payload crossings are {sorted(crossings)}")
    ifc_010 = next(item for item in architecture["interfaces"] if item["id"] == "IFC-INT-010")
    if {ifc_010["endpoint_a"], ifc_010["endpoint_b"]} != payload_resources:
        errors.append("IFC-INT-010 must remain inside the payload envelope")
    if "payload-internal" not in ifc_010.get("interface_type", ""):
        errors.append("IFC-INT-010 lacks payload-internal classification")
    component = next(item for item in architecture["components"] if item["id"] == "CMP-COM-02")
    if component.get("name") != "Antenna physical-resource envelope":
        errors.append("CMP-COM-02 display name changed")
    req_ifc_003 = next(item for item in requirements if item["id"] == "REQ-016")
    expected_requirement = (
        "The platform-to-payload interface shall be limited to power (IFC-INT-003) "
        "and mechanical retention (IFC-INT-007)."
    )
    if req_ifc_003.get("text") != expected_requirement:
        errors.append("REQ-016 wording changed")

    expected_completion_interfaces = {
        "IFC-INT-011": ("CMP-PWR-01", "CMP-PWR-02", "a_to_b"),
        "IFC-INT-012": ("CMP-AVN-03", "CMP-AVN-01", "a_to_b"),
        "IFC-INT-013": ("CMP-PRP-02", "CMP-PRP-01", "a_to_b"),
        "IFC-INT-014": ("CMP-PRP-01", "CMP-PRP-03", "a_to_b"),
        "IFC-INT-015": ("CMP-PWR-02", "CMP-PWR-03", "a_to_b"),
    }
    interface_by_identifier = {item["id"]: item for item in architecture["interfaces"]}
    for interface_id, expected in expected_completion_interfaces.items():
        interface = interface_by_identifier.get(interface_id, {})
        actual = (
            interface.get("endpoint_a"), interface.get("endpoint_b"), interface.get("direction")
        )
        if actual != expected:
            errors.append(f"{interface_id} no longer preserves its model-completion determination")
    expected_resource_relationships = {
        ("CMP-AFR-01", "structurally_supports", "CMP-AFR-02"),
        ("CMP-AFR-01", "structurally_supports", "CMP-AFR-03"),
        ("CMP-AFR-01", "structurally_supports", "CMP-AFR-04"),
        ("CMP-AFR-01", "uses_retention_hardware", "CMP-AFR-05"),
        ("CMP-AFR-04", "structurally_supports", "CMP-MNT-01"),
        ("CMP-PWR-04", "participates_in_source_connection", "CMP-PWR-02"),
    }
    if resource_relationship_keys != expected_resource_relationships:
        errors.append("current resource-relationship set changed without an explicit model disposition")
    budget_view_relationships = [
        item for item in traceability["relationships"]
        if item.get("view_group") == "mass_cost_power_endurance"
    ]
    if len(budget_view_relationships) != 10:
        errors.append("mass-cost-power-endurance view must derive from 10 controlled relationships")

    decision_by_id = {item["id"]: item for item in assurance["decisions"]}
    for decision_id in ("DEC-002", "DEC-003", "DEC-004", "DEC-005"):
        if decision_by_id.get(decision_id, {}).get("decision_status") != "proposed":
            errors.append(f"{decision_id} must remain proposed after work-package acceptance")
        review = decision_by_id.get(decision_id, {}).get("verification_review", {})
        if review.get("reviewed_model_version") != latest_review["model_version"] or review.get("evidence_ids") != ["EVD-013"]:
            errors.append(f"{decision_id} lacks the latest recorded non-approval consistency review")
    std_decision = decision_by_id["DEC-002"]
    if std_decision.get("decision_status") != "proposed" or "GAP-STD-001" not in gap_codes:
        errors.append("DEC-002 / GAP-STD-001 standards decision must remain unresolved")
    if not any("UAF 1.2" in item for item in system.get("standards", [])):
        errors.append("UAF 1.2 terminology was removed without approval")
    if "UAF 1.3" not in system.get("standards_posture", {}).get("current_omg_formal_version", ""):
        errors.append("UAF 1.3 current-version fact is missing")
    if system.get("standards_posture", {}).get("conformance_claim") != "none":
        errors.append("repository must not claim UAF conformance")

    cameo_source = next(item for item in sources["sources"] if item["id"] == "SRC-REPO-009")
    cameo_gap = next(item for item in traceability["gaps"] if item["code"] == "GAP-CFG-001")
    cameo_path = ROOT / cameo_source.get("location", "")
    cameo_integrity = cameo_source.get("integrity_check", {})
    expected_cameo_hash = "C38F99CBF4B5CA11BEDEC11D060D961F4C42E4ED8AC7875F605F3238F3AFB9F6"
    if cameo_source.get("applicability_scope") != "historical_unreconciled_reference":
        errors.append("Cameo source is not explicitly classified as historical")
    if cameo_source.get("applicable_configurations"):
        errors.append("historical Cameo source must not apply to a current configuration")
    if not cameo_path.is_file():
        errors.append("historical Cameo source is missing from the archive")
    else:
        actual_cameo_hash = hashlib.sha256(cameo_path.read_bytes()).hexdigest().upper()
        if actual_cameo_hash != expected_cameo_hash:
            errors.append("historical Cameo source checksum changed")
    if (
        cameo_integrity.get("expected_sha256") != expected_cameo_hash
        or cameo_integrity.get("actual_sha256") != expected_cameo_hash
        or cameo_integrity.get("status") != "MATCH"
    ):
        errors.append("historical Cameo source lacks its verified archive checksum")
    if cameo_gap.get("disposition") != "closed" or cameo_gap.get("reporting_priority") != "secondary":
        errors.append("Cameo repository conflict is not closed as secondary historical material")
    haz_009 = next(item for item in assurance["hazards"] if item["id"] == "HAZ-009")
    haz_009_gap = next(item for item in traceability["gaps"] if item["code"] == "GAP-HAZ-002")
    if haz_009.get("lifecycle_status") != "reserved_inactive" or haz_009_gap.get("disposition") != "deferred":
        errors.append("HAZ-009 must remain a reserved inactive ID")

    for relative in RETIRED_CORE_PATHS:
        if (ROOT / relative).exists():
            errors.append(f"retired architecture file still exists: {relative}")
    model_files = {path.name for path in (ROOT / "model").glob("*.yaml")}
    if model_files != {"system.yaml", "architecture.yaml", "assurance.yaml", "traceability.yaml"}:
        errors.append(f"model catalog set is not consolidated: {sorted(model_files)}")
    required_reference_files = {
        "README.md", "requirements.md", "interfaces.md", "traceability.md",
        "verification.md", "decisions-and-gaps.md", "trade-studies.md",
        "feasibility-analysis.md", "architecture-atlas.md", "baseline.md",
        "requirement-id-migration.md",
    }
    reference_files = {path.name for path in (ROOT / "docs" / "reference").glob("*.md")}
    if not required_reference_files.issubset(reference_files):
        errors.append(f"technical reference layer is incomplete: {sorted(reference_files)}")
    script_files = {path.name for path in (ROOT / "scripts").glob("*.py")}
    if script_files != {
        "generate-communication-views.py", "generate-mermaid-views.py", "validate-baseline.py",
    }:
        errors.append(f"supporting Python toolchain is not minimal: {sorted(script_files)}")

    for path in [
        BASELINE_REPORT, ATLAS_REPORT, REQUIREMENTS_REFERENCE, INTERFACES_REFERENCE,
        TRACEABILITY_REFERENCE, VERIFICATION_REFERENCE, DECISIONS_REFERENCE,
    ]:
        if not path.exists():
            errors.append(f"generated report missing: {path.relative_to(ROOT)}")
        elif "GENERATED VIEW" not in "\n".join(path.read_text(encoding="utf-8-sig").splitlines()[:6]):
            errors.append(f"{path.relative_to(ROOT)} lacks generated-view marker")

    atlas_text = ATLAS_REPORT.read_text(encoding="utf-8-sig") if ATLAS_REPORT.exists() else ""
    for interface in architecture["interfaces"]:
        if atlas_text.count(interface["id"]) < 2:
            errors.append(f"{interface['id']} lacks atlas diagram and inventory coverage")

    generator_text = VIEW_GENERATOR.read_text(encoding="utf-8-sig")
    forbidden_renderer_semantics = (
        "source association - IFC not allocated",
        "resource association - IFC not allocated",
        "mount relationship [UNRESOLVED]",
        "navigation resource - IFC unresolved",
        "propulsion association",
        "MODE_005 --> MODE_001: SCN-002 transition",
        'SCN_001 -->|"progression"| SCN_002',
        'TS_006 -->|"defines payload envelope"| REQ_012',
        "future relationship unresolved",
    )
    for semantic_literal in forbidden_renderer_semantics:
        if semantic_literal in generator_text:
            errors.append(
                f"Mermaid generator still defines architecture semantics directly: {semantic_literal}"
            )
    for required_model_input in (
        'get("resource_relationships", [])',
        'architecture["mode_transitions"]',
        'catalogs["architecture"]["scenario_transitions"]',
        'relationship.get("view_group")',
    ):
        if required_model_input not in generator_text:
            errors.append(f"Mermaid generator does not consume structured semantic input {required_model_input}")

    readme_text = (ROOT / "README.md").read_text(encoding="utf-8-sig")
    required_readme_sections = (
        "## What the system does",
        "## What the study found",
        "## Engineering status",
        "## Explore the engineering",
        "## Reproduce and validate",
        "## Scope note",
    )
    section_positions = [readme_text.find(section) for section in required_readme_sections]
    if any(position < 0 for position in section_positions) or section_positions != sorted(section_positions):
        errors.append("README orientation sections are missing or out of order")
    word_count = len(re.findall(r"\b[\w’-]+\b", re.sub(r"```.*?```", "", readme_text, flags=re.DOTALL)))
    if not 500 <= word_count <= 1000:
        errors.append(f"README orientation length is {word_count} words; expected approximately 600-900")
    workflow = ROOT / ".github" / "workflows" / "check.yml"
    workflow_text = workflow.read_text(encoding="utf-8-sig") if workflow.exists() else ""
    if not re.search(r"python-version:\s*['\"]3\.12['\"]", workflow_text) or "python scripts/validate-baseline.py --check-generated" not in workflow_text:
        errors.append("CI workflow no longer runs the pinned generated-baseline validation")
    errors.extend(validate_mermaid_documents(set(definitions), gap_codes))
    errors.extend(validate_communication_figures(catalogs, set(definitions), gap_codes))
    errors.extend(validate_markdown_links())

    implementation_patterns = [
        re.compile(r"\b\d+(?:\.\d+)?\s*(?:kHz|MHz|GHz|dBm|mW)\b", re.IGNORECASE),
        re.compile(r"\b(?:QPSK|QAM|OFDM|FHSS|DSSS)\b", re.IGNORECASE),
    ]
    guarded = [
        ROOT / "model", ROOT / ".seal", ROOT / "README.md", ROOT / "docs",
    ]
    for root in guarded:
        paths = [root] if root.is_file() else list(root.rglob("*"))
        for path in paths:
            if not path.is_file() or path.suffix.lower() not in {".yaml", ".md"}:
                continue
            text = path.read_text(encoding="utf-8-sig")
            for pattern in implementation_patterns:
                if pattern.search(text):
                    errors.append(f"{path.relative_to(ROOT)} contains prohibited implementation detail")

    active = []
    deferred = []
    for gap in traceability["gaps"]:
        summary = f"{gap['code']}: {gap['statement']}"
        if gap.get("disposition") in {"closed", "deferred", "intentionally_out_of_scope"}:
            deferred.append(summary)
        else:
            active.append(summary)
    return errors, active, deferred


def generated_outputs_current(catalogs: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    outputs = {
        BASELINE_REPORT: render_baseline(catalogs),
        REQUIREMENTS_REFERENCE: render_requirements(catalogs),
        INTERFACES_REFERENCE: render_interfaces(catalogs),
        TRACEABILITY_REFERENCE: render_traceability(catalogs),
        VERIFICATION_REFERENCE: render_verification(catalogs),
        DECISIONS_REFERENCE: render_decisions_and_gaps(catalogs),
    }
    for path, expected in outputs.items():
        if not path.exists() or path.read_text(encoding="utf-8-sig") != expected:
            errors.append(f"{path.relative_to(ROOT)} is stale; run --write-reports")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-reports", action="store_true", help="regenerate derived reports and canonical figures")
    parser.add_argument(
        "--check-generated", action="store_true",
        help="explicitly check generated freshness (also performed by the default command)",
    )
    parser.add_argument(
        "--validate-mermaid", action="store_true",
        help="use locally installed pinned Mermaid CLI when available",
    )
    args = parser.parse_args()

    try:
        catalogs = load_all()
    except ValueError as exc:
        print(f"MODEL-INVALID: {exc}")
        return 1

    if args.write_reports:
        reference_outputs = {
            BASELINE_REPORT: render_baseline(catalogs),
            REQUIREMENTS_REFERENCE: render_requirements(catalogs),
            INTERFACES_REFERENCE: render_interfaces(catalogs),
            TRACEABILITY_REFERENCE: render_traceability(catalogs),
            VERIFICATION_REFERENCE: render_verification(catalogs),
            DECISIONS_REFERENCE: render_decisions_and_gaps(catalogs),
        }
        for path, content in reference_outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
        generated = subprocess.run(
            [sys.executable, str(VIEW_GENERATOR)], cwd=ROOT,
            capture_output=True, text=True, check=False,
        )
        if generated.stdout.strip():
            print(generated.stdout.strip())
        if generated.returncode:
            if generated.stderr.strip():
                print(generated.stderr.strip())
            print("MODEL-INVALID: architecture-view generation failed")
            return 1
        communication_generated = subprocess.run(
            [sys.executable, str(COMMUNICATION_GENERATOR)], cwd=ROOT,
            capture_output=True, text=True, check=False,
        )
        if communication_generated.stdout.strip():
            print(communication_generated.stdout.strip())
        if communication_generated.returncode:
            if communication_generated.stderr.strip():
                print(communication_generated.stderr.strip())
            print("MODEL-INVALID: communication-view generation failed")
            return 1
        print(f"GENERATED-REFERENCE-VIEWS-WRITTEN: {len(reference_outputs) + 1} documents")

    errors, active_gaps, deferrals = validate(catalogs)
    errors.extend(generated_outputs_current(catalogs))

    view_command = [sys.executable, str(VIEW_GENERATOR), "--check"]
    if args.validate_mermaid:
        view_command.append("--validate-syntax")
    view_check = subprocess.run(
        view_command, cwd=ROOT, capture_output=True, text=True, check=False,
    )
    if view_check.stdout.strip():
        print(view_check.stdout.strip())
    if view_check.returncode:
        errors.append("architecture atlas is stale or failed optional syntax validation")
        if view_check.stderr.strip():
            errors.append("Mermaid validator error: " + view_check.stderr.strip())

    communication_check = subprocess.run(
        [sys.executable, str(COMMUNICATION_GENERATOR), "--check"], cwd=ROOT,
        capture_output=True, text=True, check=False,
    )
    if communication_check.stdout.strip():
        print(communication_check.stdout.strip())
    if communication_check.returncode:
        errors.append("canonical communication figures are stale or invalid")
        if communication_check.stderr.strip():
            errors.append("Communication-view validator error: " + communication_check.stderr.strip())

    if not FEASIBILITY_MODEL.exists():
        errors.append("analysis/feasibility.py is missing")
    else:
        feasibility_check = subprocess.run(
            [sys.executable, str(FEASIBILITY_MODEL), "--check"], cwd=ROOT,
            capture_output=True, text=True, check=False,
        )
        if feasibility_check.stdout.strip():
            print(feasibility_check.stdout.strip())
        if feasibility_check.returncode:
            errors.append("feasibility analysis artifacts are stale or invalid")
            if feasibility_check.stderr.strip():
                errors.append("Feasibility validator error: " + feasibility_check.stderr.strip())

    if not MISSION_MODEL.exists():
        errors.append("analysis/mission_connectivity.py is missing")
    else:
        mission_check = subprocess.run(
            [sys.executable, str(MISSION_MODEL), "--check"], cwd=ROOT,
            capture_output=True, text=True, check=False,
        )
        if mission_check.stdout.strip():
            print(mission_check.stdout.strip())
        if mission_check.returncode:
            errors.append("mission analysis artifacts are stale or invalid")
            if mission_check.stderr.strip():
                errors.append("Mission validator error: " + mission_check.stderr.strip())
    if errors:
        print("MODEL-INVALID FAILURES")
        for error in sorted(set(errors)):
            print(f"- {error}")
    else:
        print("MODEL-VALID: consolidated catalogs, references, reports, and guards passed")
    print(f"ACTIVE ARCHITECTURE GAPS: {len(active_gaps)}")
    for gap in active_gaps:
        print(f"- {gap}")
    print(f"CLOSED, DEFERRED, OR SECONDARY ITEMS: {len(deferrals)}")
    for gap in deferrals:
        print(f"- {gap}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
