#!/usr/bin/env python3
"""Validate the consolidated baseline and generate its two derived reports.

Catalogs use the JSON-compatible subset of YAML 1.2, so validation and generation
require only the Python standard library. Model validity never implies approval,
verification completion, safety, or operational readiness.
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
VIEW_GENERATOR = ROOT / "scripts" / "generate-mermaid-views.py"
BASELINE_REPORT = ROOT / "reports" / "baseline.md"
ATLAS_REPORT = ROOT / "reports" / "architecture-views.md"

CATALOG_PATHS = {
    "system": ROOT / "system.yaml",
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
        "requirements", "hazards", "controls", "verifications",
        "trade_studies", "decisions",
    ),
}

PREFIXES = (
    "CFG", "NEED", "CAP", "SCN", "OA", "OP", "IX", "FUN", "CMP", "IFC",
    "REQ", "HAZ", "CTL", "VER", "EVD", "TS", "MODE", "CLM", "SRC", "DEC",
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
MERMAID_HEADERS = {"flowchart", "sequenceDiagram", "stateDiagram-v2", "requirementDiagram"}

# Exact prefix counts from the pre-refactor authoritative catalogs. Together with
# uniqueness and reference resolution, these guard the ID-preservation acceptance test.
PRESERVED_ID_COUNTS = {
    "CAP": 5, "CFG": 5, "CLM": 14, "CMP": 19, "CTL": 5, "DEC": 2,
    "EVD": 4, "FUN": 9, "HAZ": 12, "IFC": 16, "IX": 10, "MODE": 5,
    "NEED": 1, "OA": 6, "OP": 10, "REQ": 27, "SCN": 8, "SRC": 17,
    "TS": 11, "VER": 8,
}

REFERENCE_KEYS = {
    "subject_ids", "decision_ids", "applicable_configurations", "applicable_sources",
    "predecessor_ids", "performers", "activities", "information_exchanges",
    "related_requirements", "related_hazards", "verification_ids", "claim_ids",
    "operational_scenarios", "upstream_refs", "allocation_refs", "tbd_owner_ids",
    "contradicts", "supersedes", "mitigates", "implemented_by", "evidence_ids",
    "source_refs", "evidence_refs", "gap_refs", "counterevidence_refs", "blocks",
    "object_refs", "supports", "refutes", "source_ids",
}
SINGULAR_REFERENCE_KEYS = {
    "claim_id", "decision_id", "gap_id", "endpoint_a", "endpoint_b", "from", "to",
}
REFERENCE_SENTINELS = {"TBD", "All", "External", "None"}

AUTHORITY_RULE = (
    "system.yaml is the manifest. The structured catalogs referenced by it are "
    "authoritative model data. Markdown documents and generated reports are views of that model."
)

RETIRED_CORE_PATHS = {
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
        "system.yaml", "model/architecture.yaml", "model/assurance.yaml",
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
    lines.extend(["", "</details>", "", "## Active decisions", ""])
    for decision in assurance["decisions"]:
        lines.append(
            f"- `{decision['id']}` - {decision['name']} - **{decision['decision_status']}**."
        )

    active_gaps = [
        gap for gap in traceability["gaps"]
        if gap.get("disposition") not in {"deferred", "intentionally_out_of_scope"}
    ]
    deferred_gaps = [gap for gap in traceability["gaps"] if gap not in active_gaps]
    lines.extend([
        "",
        "## Active architecture gaps",
        "",
        "| Gap | Category | Severity | Affected model area |",
        "|---|---|---|---|",
    ])
    for gap in active_gaps:
        lines.append(
            f"| {gap['code']} | {pipe(gap['category'])} | {pipe(gap['severity'])} | "
            f"{pipe(gap['affected_ids'])} |"
        )

    verification_status = collections.Counter(
        item.get("verification_status", "unspecified") for item in assurance["requirements"]
    )
    lines.extend([
        "",
        "## Verification status",
        "",
        f"- Requirement allocations: {', '.join(f'{key}: {value}' for key, value in sorted(verification_status.items()))}.",
        "- `VER-*` records are methods or planned activities unless an `EVD-*` execution record says otherwise.",
        "- Physical verification evidence remains absent or deferred (`GAP-VER-001`).",
        "",
        "## Concise traceability summary",
        "",
        "- `NEED-001 -> CAP-001 -> SCN-003 -> OA-004 -> FUN-REL-01 -> CMP-COM-01 -> REQ-FUN-001 -> VER-001`.",
        "- `HAZ-004 -> CTL-001 -> REQ-FUN-006 / REQ-SAF-002 -> VER-004 / VER-006 -> GAP-VER-001`.",
        "- `HAZ-008 -> CTL-005 -> REQ-IFC-004 -> VER-005 / VER-008 -> GAP-VER-001`.",
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


def validate_mermaid_documents(definitions: set[str], gap_codes: set[str]) -> list[str]:
    errors: list[str] = []
    paths = [ROOT / "README.md", ROOT / "architecture.md", ATLAS_REPORT]
    for path in paths:
        if not path.exists():
            errors.append(f"missing Mermaid-bearing document: {path.relative_to(ROOT)}")
            continue
        blocks, fence_errors = extract_mermaid_blocks(path.read_text(encoding="utf-8-sig"))
        errors.extend(f"{path.relative_to(ROOT)}: {item}" for item in fence_errors)
        if path == ROOT / "README.md" and len(blocks) != 1:
            errors.append(f"README.md must contain exactly one Mermaid diagram, found {len(blocks)}")
        if path == ROOT / "architecture.md" and not 8 <= len(blocks) <= 10:
            errors.append(f"architecture.md must contain 8-10 Mermaid diagrams, found {len(blocks)}")
        if path == ATLAS_REPORT and not 14 <= len(blocks) <= 18:
            errors.append(f"architecture atlas must contain 14-18 Mermaid diagrams, found {len(blocks)}")
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
            if "…" in block or "â€¦" in block:
                errors.append(f"{path.name}: Mermaid diagram {title!r} contains a truncated label")
            if any(line.lstrip().startswith("click ") for line in lines):
                errors.append(f"{path.name}: Mermaid diagram {title!r} contains a clickable link")
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
    for prefix, expected in PRESERVED_ID_COUNTS.items():
        if prefix_counts[prefix] != expected:
            errors.append(f"preserved {prefix}- ID count is {prefix_counts[prefix]}, expected {expected}")

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

    for markdown in [
        ROOT / "README.md", ROOT / "architecture.md", ROOT / "trade-studies.md",
        BASELINE_REPORT, ATLAS_REPORT,
    ]:
        if not markdown.exists():
            continue
        text = markdown.read_text(encoding="utf-8-sig")
        for match in ID_TOKEN_RE.finditer(text):
            token = match.group(0)
            if (
                token == "TS-XXX"
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
        errors.append("system.yaml does not contain the single required authority rule")
    expected_catalogs = {
        "sources": ".seal/sources.yaml", "proof": ".seal/proof.yaml",
        "architecture": "model/architecture.yaml", "assurance": "model/assurance.yaml",
        "traceability": "model/traceability.yaml",
    }
    if system.get("catalogs") != expected_catalogs:
        errors.append("system.yaml catalog map does not match the consolidated authority model")
    if system.get("generated_reports") != ["reports/baseline.md", "reports/architecture-views.md"]:
        errors.append("system.yaml must name exactly the two generated reports")
    if system.get("human_readable_views") != ["README.md", "architecture.md", "trade-studies.md"]:
        errors.append("system.yaml must name exactly the three primary human-readable documents")

    if system.get("status") == "approved" or system.get("baseline", {}).get("approval_state") == "approved":
        errors.append("baseline is incorrectly marked approved")
    for config in architecture["configurations"]:
        if config.get("approval_status") == "approved":
            errors.append(f"{config['id']} is incorrectly marked approved")

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
    for scenario in architecture["scenarios"]:
        if not scenario.get("performers") or any(item not in performer_ids for item in scenario["performers"]):
            errors.append(f"{scenario['id']} has unresolved performers")
        if any(item not in exchange_ids and item != "TBD" for item in scenario.get("information_exchanges", [])):
            errors.append(f"{scenario['id']} has unresolved information exchanges")
        if any(item not in activity_ids and item != "TBD" for item in scenario.get("activities", [])):
            errors.append(f"{scenario['id']} has unresolved activities")

    classifications = set(system["enumerations"]["requirement_classification"])
    for requirement in assurance["requirements"]:
        if requirement.get("classification") not in classifications:
            errors.append(f"{requirement['id']} has invalid requirement classification")
        if not requirement.get("upstream_refs") and not requirement.get("provenance_gap"):
            errors.append(f"{requirement['id']} lacks provenance or a documented gap")

    relationships = {
        (item["from"], item["relation"], item["to"]): item
        for item in traceability["relationships"]
    }
    required_relationships = {
        ("HAZ-004", "mitigated_by", "CTL-001"),
        ("CTL-001", "implemented_by", "REQ-FUN-006"),
        ("CTL-001", "implemented_by", "REQ-SAF-002"),
        ("HAZ-008", "mitigated_by", "CTL-005"),
        ("CTL-005", "implemented_by", "REQ-IFC-004"),
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

    inner = system["system_boundaries"]["inner"]
    if "CFG-REC" in inner.get("applicable_configurations", []):
        errors.append("CFG-REC must not inherit the proposed inner-boundary decomposition")
    recovered = next(item for item in architecture["configurations"] if item["id"] == "CFG-REC")
    if "descriptive evidence" not in recovered.get("boundary_semantics", "").lower():
        errors.append("CFG-REC lacks descriptive-evidence boundary semantics")
    for record in assurance["requirements"] + assurance["controls"] + architecture["interfaces"] + architecture["modes"]:
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
    req_ifc_003 = next(item for item in assurance["requirements"] if item["id"] == "REQ-IFC-003")
    expected_requirement = (
        "The platform-to-payload interface shall be limited to power (IFC-INT-003) "
        "and mechanical retention (IFC-INT-007)."
    )
    if req_ifc_003.get("text") != expected_requirement:
        errors.append("REQ-IFC-003 wording changed")

    std_decision = next(item for item in assurance["decisions"] if item["id"] == "DEC-002")
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
    if cameo_source.get("applicability_scope") != "deferred_external_artifact":
        errors.append("Cameo source is not explicitly deferred")
    if cameo_gap.get("disposition") != "deferred" or cameo_gap.get("reporting_priority") != "secondary":
        errors.append("Cameo gap is not deferred secondary work")
    haz_009 = next(item for item in assurance["hazards"] if item["id"] == "HAZ-009")
    haz_009_gap = next(item for item in traceability["gaps"] if item["code"] == "GAP-HAZ-002")
    if haz_009.get("lifecycle_status") != "reserved_inactive" or haz_009_gap.get("disposition") != "deferred":
        errors.append("HAZ-009 must remain a reserved inactive ID")

    for relative in RETIRED_CORE_PATHS:
        if (ROOT / relative).exists():
            errors.append(f"retired architecture file still exists: {relative}")
    model_files = {path.name for path in (ROOT / "model").glob("*.yaml")}
    if model_files != {"architecture.yaml", "assurance.yaml", "traceability.yaml"}:
        errors.append(f"model catalog set is not consolidated: {sorted(model_files)}")
    report_files = {path.name for path in (ROOT / "reports").glob("*.md")}
    if report_files != {"architecture-views.md", "baseline.md"}:
        errors.append(f"generated report set is not consolidated: {sorted(report_files)}")
    script_files = {path.name for path in (ROOT / "scripts").glob("*.py")}
    if script_files != {"generate-mermaid-views.py", "validate-baseline.py"}:
        errors.append(f"supporting Python toolchain is not minimal: {sorted(script_files)}")

    for path in [BASELINE_REPORT, ATLAS_REPORT]:
        if not path.exists():
            errors.append(f"generated report missing: {path.relative_to(ROOT)}")
        elif "GENERATED VIEW" not in "\n".join(path.read_text(encoding="utf-8-sig").splitlines()[:6]):
            errors.append(f"{path.relative_to(ROOT)} lacks generated-view marker")

    atlas_text = ATLAS_REPORT.read_text(encoding="utf-8-sig") if ATLAS_REPORT.exists() else ""
    for interface in architecture["interfaces"]:
        if atlas_text.count(interface["id"]) < 2:
            errors.append(f"{interface['id']} lacks atlas diagram and inventory coverage")
    errors.extend(validate_mermaid_documents(set(definitions), gap_codes))

    implementation_patterns = [
        re.compile(r"\b\d+(?:\.\d+)?\s*(?:kHz|MHz|GHz|dBm|mW)\b", re.IGNORECASE),
        re.compile(r"\b(?:QPSK|QAM|OFDM|FHSS|DSSS)\b", re.IGNORECASE),
    ]
    guarded = [
        ROOT / "system.yaml", ROOT / "model", ROOT / ".seal",
        ROOT / "README.md", ROOT / "architecture.md", ROOT / "trade-studies.md", ROOT / "reports",
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
        if gap.get("disposition") in {"deferred", "intentionally_out_of_scope"}:
            deferred.append(summary)
        else:
            active.append(summary)
    return errors, active, deferred


def generated_outputs_current(catalogs: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    expected_baseline = render_baseline(catalogs)
    if not BASELINE_REPORT.exists() or BASELINE_REPORT.read_text(encoding="utf-8-sig") != expected_baseline:
        errors.append("reports/baseline.md is stale; run --write-reports")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-reports", action="store_true", help="regenerate both derived reports")
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
        BASELINE_REPORT.parent.mkdir(parents=True, exist_ok=True)
        BASELINE_REPORT.write_text(render_baseline(catalogs), encoding="utf-8", newline="\n")
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
        print("GENERATED-BASELINE-WRITTEN: reports/baseline.md")

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

    if errors:
        print("MODEL-INVALID FAILURES")
        for error in sorted(set(errors)):
            print(f"- {error}")
    else:
        print("MODEL-VALID: consolidated catalogs, references, reports, and guards passed")
    print(f"ACTIVE ARCHITECTURE GAPS: {len(active_gaps)}")
    for gap in active_gaps:
        print(f"- {gap}")
    print(f"INTENTIONAL OR SECONDARY DEFERRALS: {len(deferrals)}")
    for gap in deferrals:
        print(f"- {gap}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
