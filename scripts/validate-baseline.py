#!/usr/bin/env python3
"""Validate and render the baseline-candidate catalogs.

The catalogs use JSON-compatible YAML 1.2, so the validator intentionally uses only
the Python standard library. A structurally valid model may still contain documented
architecture gaps and intentional deferrals.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATHS = {
    "system": ROOT / "system.yaml",
    "sources": ROOT / ".seal" / "sources.yaml",
    "proof": ROOT / ".seal" / "proof.yaml",
    "configurations": ROOT / "model" / "configurations.yaml",
    "elements": ROOT / "model" / "elements.yaml",
    "claims": ROOT / "model" / "claims.yaml",
    "scenarios": ROOT / "model" / "operational-scenarios.yaml",
    "interfaces": ROOT / "model" / "interfaces.yaml",
    "requirements": ROOT / "model" / "requirements.yaml",
    "traceability": ROOT / "model" / "traceability.yaml",
}

REPORT_PATHS = [
    ROOT / "reports" / "baseline-candidate.md",
    ROOT / "reports" / "baseline-gaps.md",
    ROOT / "reports" / "baseline-traceability.md",
    ROOT / "reports" / "architecture-views.md",
]
VIEW_GENERATOR = ROOT / "scripts" / "generate-mermaid-views.py"

PREFIXES = (
    "CFG", "NEED", "CAP", "SCN", "OA", "OP", "IX", "FUN", "CMP", "IFC",
    "REQ", "HAZ", "CTL", "VER", "EVD", "TS", "MODE", "CLM", "SRC", "DEC",
)
ID_RE = re.compile(r"^(?:" + "|".join(PREFIXES) + r")-[A-Z0-9][A-Z0-9.-]*$")
ID_TOKEN_RE = re.compile(r"\b(?:" + "|".join(PREFIXES) + r")-[A-Z0-9]+(?:-[A-Z0-9]+)*\b")
MERMAID_ID_TOKEN_RE = re.compile(
    r"\b(?:(?:" + "|".join(PREFIXES) + r")-[A-Z0-9]+(?:-[A-Z0-9]+)*|GAP-[A-Z0-9]+(?:-[A-Z0-9]+)*)\b"
)
GAP_TOKEN_RE = re.compile(r"\bGAP-[A-Z0-9]+(?:-[A-Z0-9]+)*\b")
RECOGNIZED_MERMAID_HEADERS = {"flowchart", "sequenceDiagram", "stateDiagram-v2", "requirementDiagram"}

EXPECTED_EXISTING_IDS = {
    "CAP-000", "CAP-001", "CAP-002", "CAP-003", "CAP-004",
    "OA-001", "OA-002", "OA-003", "OA-004", "OA-005", "OA-006",
    "OP-001", "OP-002", "OP-003",
    "FUN-FLT-01", "FUN-FLT-02", "FUN-FLT-03", "FUN-FLT-04",
    "FUN-REL-01", "FUN-REL-02", "FUN-PWR-01", "FUN-PWR-02", "FUN-CMD-01",
    "CMP-AFR-01", "CMP-AFR-02", "CMP-AFR-03", "CMP-AFR-04", "CMP-AFR-05",
    "CMP-PRP-01", "CMP-PRP-02", "CMP-PRP-03",
    "CMP-PWR-01", "CMP-PWR-02", "CMP-PWR-03", "CMP-PWR-04",
    "CMP-AVN-01", "CMP-AVN-02", "CMP-AVN-03", "CMP-AVN-04",
    "CMP-COM-01", "CMP-COM-02", "CMP-MNT-01",
    "IFC-INT-001", "IFC-INT-002", "IFC-INT-003", "IFC-INT-004",
    "IFC-INT-005", "IFC-INT-006", "IFC-INT-007",
    "IFC-EXT-001", "IFC-EXT-002", "IFC-EXT-003", "IFC-EXT-004", "IFC-EXT-005",
    "REQ-FUN-001", "REQ-FUN-002", "REQ-FUN-003", "REQ-FUN-004",
    "REQ-FUN-005", "REQ-FUN-006", "REQ-FUN-007",
    "REQ-PER-001", "REQ-PER-002", "REQ-PER-003", "REQ-PER-004", "REQ-PER-005",
    "REQ-IFC-001", "REQ-IFC-002", "REQ-IFC-003", "REQ-IFC-004",
    "REQ-SAF-001", "REQ-SAF-002",
    "REQ-CON-001", "REQ-CON-002", "REQ-CON-003", "REQ-CON-004",
    "REQ-DEF-001", "REQ-DEF-002", "REQ-DEF-003", "REQ-DEF-004", "REQ-DEF-005",
    "HAZ-001", "HAZ-002", "HAZ-003", "HAZ-004", "HAZ-005", "HAZ-006",
    "HAZ-007", "HAZ-008", "HAZ-009", "HAZ-EXT-001", "HAZ-EXT-002", "HAZ-EXT-003",
    "TS-001", "TS-002", "TS-003", "TS-004", "TS-005", "TS-006",
    "TS-007", "TS-008", "TS-009", "TS-010", "TS-011",
    "MODE-001", "MODE-002", "MODE-003", "MODE-004", "MODE-005",
}

DEFINITION_CONTAINERS = {
    "sources": ("sources",),
    "configurations": ("configurations",),
    "elements": (
        "needs", "capabilities", "operational_activities", "functions", "components",
        "modes", "trade_studies", "hazards", "controls", "verifications", "decisions",
    ),
    "claims": ("claims",),
    "scenarios": ("performers", "information_exchanges", "scenarios"),
    "interfaces": ("interfaces",),
    "requirements": ("requirements",),
    "proof": ("evidence",),
}

REFERENCE_KEYS = {
    "subject_ids", "source_ids", "decision_ids", "applicable_configurations",
    "applicable_sources", "predecessor_ids", "performers", "activities",
    "information_exchanges", "related_requirements", "related_hazards",
    "verification_ids", "claim_ids", "operational_scenarios", "upstream_refs",
    "allocation_refs", "tbd_owner_ids", "contradicts", "supersedes", "mitigates",
    "implemented_by", "evidence_ids",
    "source_refs", "evidence_refs", "gap_refs", "counterevidence_refs", "blocks", "object_refs",
}
SINGULAR_REFERENCE_KEYS = {
    "claim_id", "decision_id", "gap_id", "endpoint_a", "endpoint_b", "from", "to"
}
REFERENCE_SENTINELS = {"TBD", "All", "External", "None"}


def load_catalog(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8-sig") as handle:
            data = json.load(handle)
    except FileNotFoundError as exc:
        raise ValueError(f"missing required catalog: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"{path.relative_to(ROOT)} is not valid JSON-compatible YAML: "
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
            value = catalog.get(container, [])
            if not isinstance(value, list):
                continue
            for index, record in enumerate(value):
                if isinstance(record, dict):
                    records.append((f"{catalog_name}.{container}[{index}]", record))
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
    if value is None or value == "":
        return "-"
    if isinstance(value, list):
        if not value:
            return "-"
        value = ", ".join(str(item) for item in value)
    return str(value).replace("|", "\\|").replace("\n", " ")


def generated_header(source_paths: list[str]) -> list[str]:
    joined = ", ".join(f"`{item}`" for item in source_paths)
    return [
        "<!-- GENERATED VIEW - DO NOT AUTHOR INDEPENDENT ARCHITECTURE FACTS HERE. -->",
        "",
        f"> Generated from {joined}. Regenerate with `python scripts/validate-baseline.py --write-reports`.",
        "> The structured catalogs are authoritative. This report is not an approval record.",
        "",
    ]


def extract_mermaid_blocks(markdown: str) -> tuple[list[tuple[str, str]], list[str]]:
    """Return titled Mermaid blocks and balanced-fence errors."""
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


def validate_maintained_mermaid_views(
    definitions: set[str],
    gap_codes: set[str],
) -> list[str]:
    """Apply repository-wide Mermaid hygiene rules to maintained root documents."""
    errors: list[str] = []
    for path in sorted(ROOT.glob("*.md")):
        text = path.read_text(encoding="utf-8-sig")
        if "```mermaid" not in text:
            continue
        blocks, fence_errors = extract_mermaid_blocks(text)
        errors.extend(f"{path.name}: {item}" for item in fence_errors)
        for title, block in blocks:
            lines = [line for line in block.splitlines() if line.strip()]
            if not lines:
                errors.append(f"{path.name}: Mermaid diagram {title!r} is empty")
                continue
            header = lines[0].split()[0]
            if header not in RECOGNIZED_MERMAID_HEADERS:
                errors.append(
                    f"{path.name}: Mermaid diagram {title!r} has unrecognized header {lines[0]!r}"
                )
            if not any("%% Configuration scope:" in line for line in lines[:4]):
                errors.append(
                    f"{path.name}: Mermaid diagram {title!r} lacks an explicit configuration scope"
                )
            if any(line.lstrip().startswith("click ") for line in lines):
                errors.append(f"{path.name}: Mermaid diagram {title!r} contains a prohibited clickable link")
            for match in MERMAID_ID_TOKEN_RE.finditer(block):
                token = match.group(0)
                if block[match.end():].startswith("-*"):
                    continue
                if token not in definitions and token not in gap_codes:
                    errors.append(
                        f"{path.name}: Mermaid diagram {title!r} references undefined model ID {token}"
                    )
    return errors


def validate_generated_views(
    catalogs: dict[str, dict[str, Any]],
    definitions: set[str],
    gap_codes: set[str],
) -> list[str]:
    """Validate generated-view structure, scope, IDs, and mandated mappings."""
    errors: list[str] = []
    path = ROOT / "reports" / "architecture-views.md"
    if not path.exists():
        return ["generated architecture view is missing: reports/architecture-views.md"]
    text = path.read_text(encoding="utf-8-sig")
    blocks, fence_errors = extract_mermaid_blocks(text)
    errors.extend(f"reports/architecture-views.md: {item}" for item in fence_errors)
    if len(blocks) < 12:
        errors.append(f"generated architecture view has {len(blocks)} Mermaid diagrams; at least 12 are required")

    allowed_generic_nodes = {"BASELINE"}
    for title, block in blocks:
        lines = [line for line in block.splitlines() if line.strip()]
        if not lines:
            errors.append(f"Mermaid diagram {title!r} is empty")
            continue
        header = lines[0].split()[0]
        if header not in RECOGNIZED_MERMAID_HEADERS:
            errors.append(f"Mermaid diagram {title!r} has unrecognized header {lines[0]!r}")
        if not any("%% Configuration scope:" in line for line in lines[:4]):
            errors.append(f"Mermaid diagram {title!r} lacks an explicit configuration scope")
        if any(line.lstrip().startswith("click ") for line in lines):
            errors.append(f"Mermaid diagram {title!r} contains a prohibited clickable link")
        for token in MERMAID_ID_TOKEN_RE.findall(block):
            if token not in definitions and token not in gap_codes:
                errors.append(f"Mermaid diagram {title!r} references undefined model ID {token}")
        for line in lines:
            normalized = line.lower().replace("not approved", "")
            if "proposed" in normalized and "approved" in normalized:
                errors.append(f"Mermaid diagram {title!r} labels a proposed element as approved")
            match = re.match(r"\s*([A-Za-z0-9_]+)\[\"", line)
            if match and match.group(1) not in allowed_generic_nodes:
                if not MERMAID_ID_TOKEN_RE.search(line):
                    errors.append(f"Mermaid diagram {title!r} has an architecture node without a model ID: {line.strip()}")
        if "CFG-REC" in block and re.search(r"\bCMP-[A-Z0-9-]+\b", block):
            errors.append(f"Mermaid diagram {title!r} silently mixes CFG-REC with proposed CMP resources")

    interface_ids = {item["id"] for item in catalogs["interfaces"]["interfaces"]}
    for interface_id in sorted(interface_ids):
        if text.count(interface_id) < 2:
            errors.append(
                f"{interface_id} must appear in the generated interface inventory and at least one diagram"
            )
    architecture_text = (ROOT / "architecture.md").read_text(encoding="utf-8-sig")
    for interface_id in sorted(interface_ids):
        if interface_id not in architecture_text:
            errors.append(f"architecture.md lacks human-readable coverage for {interface_id}")

    required_fragments = [
        'HAZ_004 -->|"mitigated by; candidate"| CTL_001',
        'CTL_001 -->|"implemented by; candidate"| REQ_FUN_006',
        'CTL_001 -->|"implemented by; candidate"| REQ_SAF_002',
        'HAZ_008 -->|"mitigated by; candidate"| CTL_005',
        'CTL_005 -->|"implemented by; candidate"| REQ_IFC_004',
    ]
    for fragment in required_fragments:
        if fragment not in text:
            errors.append(f"generated hazard mapping is missing {fragment}")

    payload_blocks = [block for _, block in blocks if "IFC-INT-010" in block]
    if not payload_blocks:
        errors.append("IFC-INT-010 is absent from generated diagrams")
    elif not any(
        "Relay-payload black-box envelope" in block
        and "payload-internal" in block
        and "CMP-COM-01" in block
        and "CMP-COM-02" in block
        for block in payload_blocks
    ):
        errors.append("IFC-INT-010 is not shown inside the relay-payload black-box envelope")
    return errors


def write_reports(catalogs: dict[str, dict[str, Any]]) -> None:
    reports_dir = ROOT / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    system = catalogs["system"]
    configs = catalogs["configurations"]["configurations"]
    claims = catalogs["claims"]["claims"]
    scenarios = catalogs["scenarios"]["scenarios"]
    interfaces = catalogs["interfaces"]["interfaces"]
    requirements = catalogs["requirements"]["requirements"]
    sources = catalogs["sources"]["sources"]
    trace = catalogs["traceability"]

    basis_counts = collections.Counter(claim["evidence_basis"] for claim in claims)
    candidate = generated_header([
        "system.yaml", "model/configurations.yaml", "model/claims.yaml",
        "model/operational-scenarios.yaml", "model/interfaces.yaml",
        "model/requirements.yaml", ".seal/sources.yaml", ".seal/proof.yaml",
    ])
    candidate.extend([
        "# Baseline Candidate - Not Approved",
        "",
        "## Baseline purpose",
        "",
        system["baseline"]["purpose"],
        "",
        "## Status and approval",
        "",
        f"- Model version: `{system['model_version']}`",
        f"- Baseline status: `{system['status']}`",
        f"- Approval state: `{system['baseline']['approval_state']}`",
        "",
        "**This is a baseline candidate. It has not been approved by the project owner.**",
        "",
        "## System boundaries",
        "",
    ])
    for key, boundary in system["system_boundaries"].items():
        candidate.extend([
            f"### {boundary['name']} ({key})",
            "",
            f"Role: {boundary['role']}. Evidence basis: `{boundary['evidence_basis']}`. "
            f"Decision status: `{boundary['decision_status']}`.",
            "",
            f"Configuration scope: {pipe(boundary['applicable_configurations'])}.",
            "",
            f"Includes: {pipe(boundary['includes'])}.",
            "",
        ])
    candidate.extend([
        "## Configuration summaries",
        "",
        "| Configuration | Name | Boundary | Maturity | Approval | Derivation |",
        "|---|---|---|---|---|---|",
    ])
    for config in configs:
        candidate.append(
            f"| {config['id']} | {pipe(config['name'])} | {pipe(config['system_boundary'])} | "
            f"{pipe(config['maturity'])} | {pipe(config['approval_status'])} | "
            f"{pipe(config['derivation_relationship'])} |"
        )
    candidate.extend([
        "",
        "## Evidence classification summary",
        "",
        "| Evidence basis | Claim count |",
        "|---|---:|",
    ])
    for basis in system["enumerations"]["evidence_basis"]:
        candidate.append(f"| `{basis}` | {basis_counts.get(basis, 0)} |")
    candidate.extend([
        "",
        "The register classifies repository inspection and reverse-engineering reports separately from "
        "engineering inference and proposed design. Physically observed claims are limited to visible-marking "
        "observations documented with embedded source imagery; the article was not re-inspected for this baseline.",
        "",
        "## Current architecture coverage",
        "",
        f"- Sources: {len(sources)}",
        f"- Claims: {len(claims)}",
        f"- Configurations: {len(configs)}",
        f"- Operational scenarios: {len(scenarios)}",
        f"- Interfaces: {len(interfaces)}",
        f"- Requirements classified: {len(requirements)}",
        f"- Recorded gaps: {len(trace['gaps'])}",
        "",
        "## Generated architecture views",
        "",
        "See [`architecture-views.md`](architecture-views.md) for deterministic configuration, context, "
        "resource, behavioral, hazard, traceability, and governance diagrams generated from the catalogs.",
        "",
        "## Standards-version posture",
        "",
        f"- Current repository claim: {system['standards_posture']['current_repository_claim']}",
        f"- Current OMG formal version: {system['standards_posture']['current_omg_formal_version']}",
        f"- Conformance claim: `{system['standards_posture']['conformance_claim']}`",
        f"- Owner decision: `{system['standards_posture']['decision_id']}` / `{system['standards_posture']['gap_id']}`",
        "",
        "## Major unresolved decisions",
        "",
    ])
    for config in configs:
        for question in config["unresolved_questions"]:
            candidate.append(f"- **{config['id']}:** {question}")
    candidate.extend([
        "",
        "## Approval statement",
        "",
        "This is a baseline candidate. It has not been approved by the project owner.",
        "",
    ])
    REPORT_PATHS[0].write_text("\n".join(candidate), encoding="utf-8", newline="\n")

    gaps_report = generated_header([
        "model/traceability.yaml", "model/requirements.yaml", "model/interfaces.yaml",
        "model/operational-scenarios.yaml", "model/elements.yaml", ".seal/sources.yaml",
    ])
    gaps_report.extend([
        "# Baseline Gaps",
        "",
        "> These gaps remain visible by design. Their presence does not make the structured baseline invalid.",
        "",
        "| Code | Category | Gap | Affected IDs | Disposition | Severity |",
        "|---|---|---|---|---|---|",
    ])
    for gap in trace["gaps"]:
        gaps_report.append(
            f"| {gap['code']} | {pipe(gap['category'])} | {pipe(gap['statement'])} | "
            f"{pipe(gap['affected_ids'])} | {pipe(gap['disposition'])} | {pipe(gap['severity'])} |"
        )

    unknown_config = [
        record["id"] for _, record in definition_records(catalogs)
        if record.get("applicable_configurations") == ["TBD"]
    ]
    missing_ifc_verification = [item["id"] for item in interfaces if not item.get("verification_ids")]
    missing_scenario_exchange = [
        item["id"] for item in scenarios
        if not item.get("information_exchanges") or item.get("information_exchanges") == ["TBD"]
    ]
    req_provenance_gaps = [item["id"] for item in requirements if item.get("provenance_gap")]
    proposed_sos = [
        item["id"] for item in scenarios
        if "CFG-SOS" in item.get("applicable_configurations", [])
        and item.get("decision_status") == "proposed"
    ]
    gaps_report.extend([
        "",
        "## Derived gap indexes",
        "",
        f"- Unknown configuration applicability: {pipe(unknown_config)}",
        f"- Interfaces without verification allocation: {pipe(missing_ifc_verification)}",
        f"- Scenarios without an information exchange: {pipe(missing_scenario_exchange)}",
        f"- Requirements with an explicit provenance gap: {pipe(req_provenance_gaps)}",
        f"- Proposed scenarios touching CFG-SOS: {pipe(proposed_sos)}",
        "",
        "## Interpretation",
        "",
        "External communications interfaces remain intentionally undefined at implementation level. "
        "UGV, radio-user, network-service, and broader sensor-data threads are proposals, not current "
        "three-node architecture capabilities. Mass, cost, power, endurance, capability allocation, "
        "hazard control, and verification evidence gaps remain open.",
        "",
    ])
    REPORT_PATHS[1].write_text("\n".join(gaps_report), encoding="utf-8", newline="\n")

    trace_report = generated_header([
        "model/traceability.yaml", "model/requirements.yaml", "model/operational-scenarios.yaml",
        "model/interfaces.yaml", ".seal/proof.yaml",
    ])
    trace_report.extend([
        "# Baseline Traceability",
        "",
        "Logical chain: Need -> Capability -> Scenario -> Performer/Activity -> Information Exchange -> "
        "Function -> Component -> Interface -> Requirement -> Hazard/Control -> Verification -> Evidence.",
        "",
        "A relationship may be absent at this maturity. `TBD` and gap codes are preserved rather than inferred.",
        "",
        "## Structured relationships",
        "",
        "| From | Relationship | To | Status | Gap |",
        "|---|---|---|---|---|",
    ])
    for relation in trace["relationships"]:
        trace_report.append(
            f"| {pipe(relation['from'])} | {pipe(relation['relation'])} | {pipe(relation['to'])} | "
            f"{pipe(relation['status'])} | {pipe(relation.get('gap'))} |"
        )
    trace_report.extend([
        "",
        "## Requirement mappings",
        "",
        "| Requirement | Classification | Upstream rationale | Allocation | Verification | TBD owner | Gap |",
        "|---|---|---|---|---|---|---|",
    ])
    for requirement in requirements:
        trace_report.append(
            f"| {requirement['id']} | {pipe(requirement['classification'])} | "
            f"{pipe(requirement['upstream_refs'])} | {pipe(requirement['allocation_refs'])} | "
            f"{pipe(requirement['verification_ids'])} | {pipe(requirement['tbd_owner_ids'])} | "
            f"{pipe(requirement.get('provenance_gap'))} |"
        )
    trace_report.append("")
    REPORT_PATHS[2].write_text("\n".join(trace_report), encoding="utf-8", newline="\n")


def validate(catalogs: dict[str, dict[str, Any]], ids_only: bool = False) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    documented_gaps: list[str] = []
    intentional_deferrals: list[str] = []
    records = definition_records(catalogs)

    definitions: dict[str, str] = {}
    for path, record in records:
        item_id = record.get("id")
        if not isinstance(item_id, str):
            errors.append(f"{path} has no string id")
            continue
        if not ID_RE.fullmatch(item_id):
            errors.append(f"{path} has invalid id {item_id!r}")
        if item_id in definitions:
            errors.append(f"duplicate id {item_id}: {definitions[item_id]} and {path}")
        else:
            definitions[item_id] = path

    missing_existing = sorted(EXPECTED_EXISTING_IDS - definitions.keys())
    if missing_existing:
        errors.append("existing IDs missing from structured catalogs: " + ", ".join(missing_existing))

    gap_codes = {
        item["code"] for item in catalogs["traceability"].get("gaps", [])
        if isinstance(item.get("code"), str)
    }
    for catalog_name, catalog in catalogs.items():
        for ref_path, reference in references_in(catalog, catalog_name):
            if reference in REFERENCE_SENTINELS:
                continue
            if reference.startswith("GAP-"):
                if reference not in gap_codes:
                    errors.append(f"{ref_path} references undefined gap {reference}")
                continue
            if ID_RE.fullmatch(reference) and reference not in definitions:
                errors.append(f"{ref_path} references undefined id {reference}")

    for markdown in ROOT.glob("*.md"):
        text = markdown.read_text(encoding="utf-8-sig")
        for match in ID_TOKEN_RE.finditer(text):
            if text[max(0, match.start() - 4):match.start()] == "GAP-":
                continue
            token = match.group(0)
            if token == "TS-XXX":
                continue
            if any(defined.startswith(token + "-") for defined in definitions):
                # Human-readable views use family labels such as CMP-AFR-* and
                # IFC-EXT-*; these are namespaces, not element definitions.
                continue
            if token not in definitions:
                errors.append(f"{markdown.name} references undefined id {token}")
        for gap_token in GAP_TOKEN_RE.findall(text):
            if gap_token not in gap_codes:
                errors.append(f"{markdown.name} references undefined gap {gap_token}")

    if ids_only:
        return errors, documented_gaps, intentional_deferrals

    system = catalogs["system"]
    evidence_values = set(system.get("enumerations", {}).get("evidence_basis", []))
    decision_values = set(system.get("enumerations", {}).get("decision_status", []))
    config_ids = {item["id"] for item in catalogs["configurations"]["configurations"]}

    for path, record in records:
        item_id = record.get("id", path)
        if item_id.startswith("CFG-"):
            continue
        configurations = record.get("applicable_configurations")
        if not isinstance(configurations, list) or not configurations:
            errors.append(f"{item_id} lacks configuration applicability")
        elif any(value != "TBD" and value not in config_ids for value in configurations):
            errors.append(f"{item_id} has invalid configuration applicability {configurations}")

        if "evidence_basis" in record and record["evidence_basis"] not in evidence_values:
            errors.append(f"{item_id} has invalid evidence_basis {record['evidence_basis']!r}")
        if "decision_status" in record and record["decision_status"] not in decision_values:
            errors.append(f"{item_id} has invalid decision_status {record['decision_status']!r}")
        if record.get("decision_status") == "approved":
            if item_id.startswith("DEC-"):
                if not record.get("source_ids"):
                    errors.append(f"approved decision {item_id} lacks a decision source")
            elif not record.get("decision_ids"):
                errors.append(f"approved record {item_id} lacks a DEC reference")

    claims = catalogs["claims"]["claims"]
    source_required = {
        "id", "title", "source_type", "location", "owner", "date", "revision",
        "accessed_date", "reliability", "applicable_configurations", "notes",
        "kind", "description", "authority_state", "approval_state", "confidence",
    }
    for source in catalogs["sources"]["sources"]:
        missing = sorted(source_required - source.keys())
        if missing:
            errors.append(f"{source.get('id', 'source')} lacks required source fields: {', '.join(missing)}")

    config_required = {
        "id", "name", "purpose", "system_boundary", "maturity", "approval_status",
        "predecessor_ids", "derivation_relationship", "applicable_sources",
        "known_exclusions", "unresolved_questions",
    }
    for config in catalogs["configurations"]["configurations"]:
        missing = sorted(config_required - config.keys())
        if missing:
            errors.append(f"{config.get('id', 'configuration')} lacks fields: {', '.join(missing)}")

    for claim in claims:
        if claim["evidence_basis"] not in evidence_values:
            errors.append(f"{claim['id']} has invalid claim evidence basis")
        if claim["decision_status"] not in decision_values:
            errors.append(f"{claim['id']} has invalid claim decision status")
        if claim["evidence_basis"] != "unknown" and not claim.get("source_ids"):
            errors.append(f"evidence-backed claim {claim['id']} has no source")

    proof_links = catalogs["proof"].get("claims", [])
    proof_counts = collections.Counter(item.get("id") for item in proof_links)
    proof_by_id = {item.get("id"): item for item in proof_links}
    for claim in claims:
        if proof_counts[claim["id"]] != 1:
            errors.append(f"{claim['id']} must have exactly one proof link, found {proof_counts[claim['id']]}")
        elif proof_by_id[claim["id"]].get("evidence_basis") != claim.get("evidence_basis"):
            errors.append(f"{claim['id']} evidence basis differs between claim and proof registers")

    baseline = system.get("baseline", {})
    if baseline.get("approval_state") == "approved" or system.get("status") == "approved":
        errors.append("system baseline is incorrectly marked approved")
    for config in catalogs["configurations"]["configurations"]:
        if config.get("approval_status") == "approved":
            errors.append(f"{config['id']} is incorrectly marked approved")

    inner_boundary = system.get("system_boundaries", {}).get("inner", {})
    if "CFG-REC" in inner_boundary.get("applicable_configurations", []):
        errors.append("CFG-REC must not inherit the proposed inner-boundary decomposition")
    recovered_config = next(
        item for item in catalogs["configurations"]["configurations"] if item["id"] == "CFG-REC"
    )
    if "descriptive evidence" not in recovered_config.get("boundary_semantics", "").lower():
        errors.append("CFG-REC lacks explicit descriptive-evidence boundary semantics")

    for requirement in catalogs["requirements"]["requirements"]:
        if "CFG-REC" in requirement.get("applicable_configurations", []):
            errors.append(
                f"{requirement['id']} incorrectly imposes a proposed requirement or deferral on CFG-REC"
            )
    for interface in catalogs["interfaces"]["interfaces"]:
        if "CFG-REC" in interface.get("applicable_configurations", []):
            errors.append(f"{interface['id']} incorrectly applies a proposed interface to CFG-REC")
    elements = catalogs["elements"]
    for record in elements.get("modes", []) + elements.get("controls", []):
        if "CFG-REC" in record.get("applicable_configurations", []):
            errors.append(f"{record['id']} incorrectly applies proposed design behavior to CFG-REC")
    ts_009 = next(item for item in elements["trade_studies"] if item["id"] == "TS-009")
    if "CFG-REC" in ts_009.get("applicable_configurations", []):
        errors.append("TS-009 must not treat unknown CFG-REC characteristics as a proposed design trade study")
    relay_performer = next(item for item in catalogs["scenarios"]["performers"] if item["id"] == "OP-002")
    if "CFG-REC" in relay_performer.get("applicable_configurations", []):
        errors.append("OP-002 must not impose the proposed operational-performer model on CFG-REC")
    for verification in elements.get("verifications", []):
        if "CFG-REC" in verification.get("applicable_configurations", []):
            scope = verification.get("applicability_scope", "").lower()
            if "not physical" not in scope and "evidence-record" not in scope:
                errors.append(
                    f"{verification['id']} applies to CFG-REC without distinguishing governance/evidence review from physical verification"
                )

    decisions = {item["id"]: item for item in elements.get("decisions", [])}
    std_decision = decisions.get("DEC-002", {})
    if std_decision.get("decision_status") != "proposed":
        errors.append("DEC-002 must remain an unapproved proposed standards-version decision")
    if "GAP-STD-001" not in gap_codes:
        errors.append("GAP-STD-001 must remain visible until DEC-002 is approved")
    standards = system.get("standards", [])
    if not any("UAF 1.2" in item for item in standards):
        errors.append("the current UAF 1.2 repository claim changed without an approved decision")
    posture = system.get("standards_posture", {})
    if "UAF 1.3" not in posture.get("current_omg_formal_version", ""):
        errors.append("standards posture does not record UAF 1.3 as the current OMG formal version")
    if posture.get("conformance_claim") != "none":
        errors.append("the baseline must not claim UAF conformance")

    for interface in catalogs["interfaces"]["interfaces"]:
        if not interface.get("endpoint_a") or not interface.get("endpoint_b"):
            errors.append(f"{interface['id']} must have two endpoints")

    for scenario in catalogs["scenarios"]["scenarios"]:
        if not scenario.get("performers"):
            errors.append(f"{scenario['id']} has no performer")

    for requirement in catalogs["requirements"]["requirements"]:
        if not requirement.get("upstream_refs") and not requirement.get("provenance_gap"):
            errors.append(f"{requirement['id']} lacks upstream rationale and a documented provenance gap")

    for report in REPORT_PATHS:
        if not report.exists():
            errors.append(f"generated report missing: {report.relative_to(ROOT)}")
        else:
            first_lines = "\n".join(report.read_text(encoding="utf-8-sig").splitlines()[:6])
            if "GENERATED VIEW" not in first_lines:
                errors.append(f"{report.relative_to(ROOT)} does not identify itself as generated")

    payload_resources = {"CMP-COM-01", "CMP-COM-02"}
    current_payload_crossings: set[str] = set()
    for interface in catalogs["interfaces"]["interfaces"]:
        endpoints = {interface["endpoint_a"], interface["endpoint_b"]}
        configs = set(interface.get("applicable_configurations", []))
        if interface["id"].startswith("IFC-INT-") and configs.intersection({"CFG-REP", "CFG-DOM"}):
            inside_count = len(endpoints.intersection(payload_resources))
            if inside_count == 1:
                current_payload_crossings.add(interface["id"])
    if current_payload_crossings != {"IFC-INT-003", "IFC-INT-007"}:
        errors.append(
            "CFG-REP/CFG-DOM platform-to-payload crossings must be exactly "
            f"IFC-INT-003 and IFC-INT-007, found {sorted(current_payload_crossings)}"
        )
    interface_010 = next(
        item for item in catalogs["interfaces"]["interfaces"] if item["id"] == "IFC-INT-010"
    )
    if {interface_010["endpoint_a"], interface_010["endpoint_b"]} != payload_resources:
        errors.append("IFC-INT-010 must remain wholly inside the relay-payload black-box envelope")
    if "payload-internal" not in interface_010.get("interface_type", ""):
        errors.append("IFC-INT-010 must be classified as payload-internal")

    component_002 = next(item for item in elements["components"] if item["id"] == "CMP-COM-02")
    if component_002.get("name") != "Antenna physical-resource envelope":
        errors.append("CMP-COM-02 must be named Antenna physical-resource envelope")
    requirement_ifc_003 = next(
        item for item in catalogs["requirements"]["requirements"] if item["id"] == "REQ-IFC-003"
    )
    expected_ifc_003 = (
        "The platform-to-payload interface shall be limited to power (IFC-INT-003) "
        "and mechanical retention (IFC-INT-007)."
    )
    if requirement_ifc_003.get("text") != expected_ifc_003:
        errors.append("REQ-IFC-003 wording does not preserve the reconciled two-interface boundary")

    relationships = {
        (item["from"], item["relation"], item["to"]): item
        for item in catalogs["traceability"].get("relationships", [])
    }
    required_relationships = {
        ("HAZ-004", "mitigated_by", "CTL-001"),
        ("CTL-001", "implemented_by", "REQ-FUN-006"),
        ("CTL-001", "implemented_by", "REQ-SAF-002"),
        ("HAZ-008", "mitigated_by", "CTL-005"),
        ("CTL-005", "implemented_by", "REQ-IFC-004"),
    }
    for relationship in required_relationships:
        if relationship not in relationships:
            errors.append("missing reconciled relationship: " + " -> ".join(relationship))
        elif relationships[relationship].get("gap"):
            errors.append("reconciled relationship still carries a stale conflict gap: " + " -> ".join(relationship))
    if {"GAP-CONFLICT-002", "GAP-CONFLICT-003"}.intersection(gap_codes):
        errors.append("resolved HAZ-004 or HAZ-008 contradiction gaps remain in the active gap catalog")

    hazard_text = (ROOT / "hazard-analysis.md").read_text(encoding="utf-8-sig")
    trace_text = (ROOT / "traceability.md").read_text(encoding="utf-8-sig")
    for token in ["CTL-001", "REQ-FUN-006", "REQ-SAF-002", "VER-006"]:
        if token not in hazard_text or token not in trace_text:
            errors.append(f"HAZ-004 human-readable reconciliation lacks {token}")
    for token in ["CTL-005", "REQ-IFC-004", "VER-008"]:
        if token not in hazard_text or token not in trace_text:
            errors.append(f"HAZ-008 human-readable reconciliation lacks {token}")
    if re.search(r"HAZ-004[^\n]*TODO|HAZ-008[^\n]*REQ-IFC-001\s*\|\s*TODO", hazard_text + "\n" + trace_text):
        errors.append("stale HAZ-004 or HAZ-008 TODO/mapping remains in human-readable views")

    errors.extend(validate_maintained_mermaid_views(set(definitions), gap_codes))
    errors.extend(validate_generated_views(catalogs, set(definitions), gap_codes))

    guarded_paths = [
        ROOT / "system.yaml", ROOT / ".seal", ROOT / "model", ROOT / "reports",
    ]
    implementation_patterns = [
        re.compile(r"\b\d+(?:\.\d+)?\s*(?:kHz|MHz|GHz|dBm|mW)\b", re.IGNORECASE),
        re.compile(r"\b(?:QPSK|QAM|OFDM|FHSS|DSSS)\b", re.IGNORECASE),
    ]
    for guarded in guarded_paths:
        files = [guarded] if guarded.is_file() else list(guarded.rglob("*"))
        for path in files:
            if not path.is_file() or path.suffix.lower() not in {".yaml", ".md"}:
                continue
            text = path.read_text(encoding="utf-8-sig")
            for pattern in implementation_patterns:
                if pattern.search(text):
                    errors.append(
                        f"{path.relative_to(ROOT)} contains prohibited RF implementation detail matching {pattern.pattern}"
                    )

    for gap in catalogs["traceability"].get("gaps", []):
        summary = f"{gap['code']}: {gap['statement']}"
        if gap.get("disposition") in {"intentionally_out_of_scope", "deferred"}:
            intentional_deferrals.append(summary)
        else:
            documented_gaps.append(summary)

    return errors, documented_gaps, intentional_deferrals


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-reports", action="store_true", help="regenerate derived Markdown reports")
    parser.add_argument("--ids-only", action="store_true", help="run ID and reference validation only")
    parser.add_argument(
        "--validate-mermaid",
        action="store_true",
        help="optionally validate diagrams with locally installed pinned Mermaid CLI",
    )
    args = parser.parse_args()

    try:
        catalogs = load_all()
    except ValueError as exc:
        print(f"MODEL-INVALID: {exc}")
        return 1

    if args.write_reports:
        write_reports(catalogs)
        generated = subprocess.run(
            [sys.executable, str(VIEW_GENERATOR)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if generated.stdout.strip():
            print(generated.stdout.strip())
        if generated.returncode:
            if generated.stderr.strip():
                print(generated.stderr.strip())
            print("MODEL-INVALID: architecture-view generation failed")
            return 1

    errors, gaps, deferrals = validate(catalogs, ids_only=args.ids_only)
    if not args.ids_only:
        view_command = [sys.executable, str(VIEW_GENERATOR), "--check"]
        if args.validate_mermaid:
            view_command.append("--validate-syntax")
        view_check = subprocess.run(
            view_command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if view_check.stdout.strip():
            print(view_check.stdout.strip())
        if view_check.returncode:
            errors.append("generated architecture views are stale or failed Mermaid syntax validation")
            if view_check.stderr.strip():
                errors.append("Mermaid validator error: " + view_check.stderr.strip())
    if errors:
        print("MODEL-INVALID FAILURES")
        for error in sorted(set(errors)):
            print(f"- {error}")
    else:
        print("MODEL-VALID: structured catalogs and references passed validation")

    if not args.ids_only:
        print(f"DOCUMENTED ARCHITECTURE GAPS: {len(gaps)}")
        for gap in gaps:
            print(f"- {gap}")
        print(f"INTENTIONAL DEFERRALS: {len(deferrals)}")
        for deferral in deferrals:
            print(f"- {deferral}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
