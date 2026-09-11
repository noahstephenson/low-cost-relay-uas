#!/usr/bin/env python3
"""Generate deterministic GitHub-renderable Mermaid architecture views.

The authoritative catalogs are JSON-compatible YAML 1.2, so this script uses only
the Python standard library. It does not infer implementation detail or approve any
candidate relationship.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "reference" / "architecture-atlas.md"
PINNED_MERMAID_CLI = "11.4.1"

CATALOG_PATHS = {
    "system": ROOT / "model" / "system.yaml",
    "sources": ROOT / ".seal" / "sources.yaml",
    "proof": ROOT / ".seal" / "proof.yaml",
    "architecture": ROOT / "model" / "architecture.yaml",
    "assurance": ROOT / "model" / "assurance.yaml",
    "traceability": ROOT / "model" / "traceability.yaml",
}

SHORT_LABELS = {
    "CFG-REC": "Reference evidence",
    "CFG-REP": "Replica candidate",
    "CFG-DOM": "Domestic candidate",
    "CFG-DIG": "Digital extension",
    "CFG-SOS": "C2 Ecosystem context",
    "NEED-001": "Extend mission reach",
    "SRC-INT-001": "Recovered-article research report",
    "GAP-STD-001": "UAF version decision unresolved",
    "GAP-REC-001": "Role mapping complete - exact equivalence unresolved",
    "GAP-HAZ-001": "HAZ-001 has no defined control",
    "GAP-VER-001": "Physical and external evidence missing",
    "GAP-BUDGET-001": "Coupled targets and evidence unresolved",
    "GAP-IFC-001": "External conformance authority missing",
    "OA-007": "Prepare Relay UAS",
    "FUN-CFG-01": "Establish configuration and readiness",
    "FUN-HLT-01": "Monitor and report health/status",
    "IFC-EXT-007": "Health/status return",
    "REQ-001": "Relay outbound traffic",
    "REQ-006": "Inhibit arming in Ground Safe",
    "REQ-007": "Recover after payload loss",
    "REQ-008": "Provide mode and health/status",
    "REQ-017": "Retain payload under flight loads",
    "REQ-018": "Protect and retain battery",
    "REQ-019": "Show armed state to operator",
    "VER-009": "External conformance verification",
    "DEC-003": "Select HAZ-001 safety objective",
    "DEC-004": "Accept health/status architecture",
    "DEC-005": "Confirm CAP-004 semantics",
}


def load_catalogs() -> dict[str, dict[str, Any]]:
    return {
        name: json.loads(path.read_text(encoding="utf-8-sig"))
        for name, path in CATALOG_PATHS.items()
    }


def build_index(catalogs: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    collections = [
        catalogs["sources"].get("sources", []),
        catalogs["proof"].get("claims", []),
        catalogs["proof"].get("evidence", []),
    ]
    for catalog_name in ("architecture", "assurance"):
        for key, values in catalogs[catalog_name].items():
            if key != "schema_version" and isinstance(values, list):
                collections.append(values)
    for collection in collections:
        for record in collection:
            if isinstance(record, dict) and isinstance(record.get("id"), str):
                index[record["id"]] = record
    for gap in catalogs["traceability"].get("gaps", []):
        index[gap["code"]] = {"id": gap["code"], "name": gap["statement"], **gap}
    return index


def mermaid_key(item_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", item_id)


def clean_label(value: Any, _legacy_limit: int | None = None) -> str:
    text = str(value or "").replace("\n", " ").replace('"', "'")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def record_name(record: dict[str, Any]) -> str:
    if record.get("id") in SHORT_LABELS:
        return SHORT_LABELS[record["id"]]
    return clean_label(
        record.get("display_name")
        or record.get("name")
        or record.get("title")
        or record.get("subject")
        or record.get("text")
        or record.get("statement")
        or record.get("id")
    )


def node(index: dict[str, dict[str, Any]], item_id: str, extra: str = "") -> str:
    record = index[item_id]
    parts = [item_id, record_name(record)]
    if extra:
        parts.append(clean_label(extra))
    return f'{mermaid_key(item_id)}["' + "<br/>".join(parts) + '"]'


def status_of(index: dict[str, dict[str, Any]], item_id: str) -> str:
    record = index[item_id]
    if item_id.startswith("GAP-"):
        if record.get("disposition") == "closed":
            return "[CLOSED]"
        return "[DEFERRED]" if record.get("disposition") == "deferred" else "[UNRESOLVED]"
    status = record.get("execution_status") or record.get("decision_status") or record.get("status") or "unverified"
    labels = {
        "executed_pass": "[EXECUTED PASS]",
        "executed_with_open_gaps": "[EXECUTED WITH OPEN GAPS]",
        "failed": "[FAILED]",
        "blocked": "[BLOCKED]",
        "not_executed": "[NOT EXECUTED]",
        "proposed": "[PROPOSED]",
        "deferred": "[DEFERRED]",
        "unknown": "[UNRESOLVED]",
        "candidate": "[PROPOSED]",
        "unverified": "[UNVERIFIED]",
    }
    return labels.get(str(status), clean_label(status))


def flow_diagram(number: str, title: str, scope: str, body: Iterable[str], note: str = "") -> list[str]:
    """Keep relationships in the picture and full labels in a companion table."""
    details = []
    compact = []
    for line in body:
        def compact_node(match):
            key, label = match.groups()
            parts = label.split("<br/>")
            if key in {"OUTER", "INNER", "PAYLOAD"}:
                details.append((key, label))
                return f'{key}["{dict(OUTER="External context", INNER="Relay UAS", PAYLOAD="Payload boundary")[key]}"]'
            details.append((key, label.replace("<br/>", "; ")))
            if len(parts) > 1:
                headings = {"ACCEPTED": "Accepted review", "EXECUTED": "Latest model review", "PASS": "Review pass", "OPEN": "Review with gaps", "PHYSICAL": "Physical evidence needed", "EXTERNAL": "External authority needed", "DEFERRED": "Deferred scope"}
                parts[0] = headings.get(key, parts[0])
                name = textwrap.shorten(parts[1], width=48, placeholder="...")
                label = parts[0] + "<br/>" + "<br/>".join(textwrap.wrap(name, width=25))
            else:
                label = "<br/>".join(textwrap.wrap(label, width=25))
            return f'{key}["{label}"]'
        line = re.sub(r'(\w+)\["([^"\n]+)"\]', compact_node, line)
        def compact_edge(match):
            label = match.group(1)
            if len(label.split()) <= 4 and "<br/>" not in label:
                return match.group(0)
            ref = f"R{sum(k.startswith('R') and k[1:].isdigit() for k, _ in details) + 1}"
            details.append((ref, label.replace("<br/>", "; ")))
            return f'|"{ref}"|'
        compact.append(re.sub(r'\|"([^"\n]+)"\|', compact_edge, line))
    lines = [f"### {number}. {title}", "", f"Configuration scope: `{scope}`."]
    if note:
        lines.extend(["", note])
    lines.extend(["", "<details>", f"<summary>Open {title.lower()} diagram and detail table</summary>", "", "```mermaid",
                  '%%{init: {"theme": "neutral", "htmlLabels": false, "themeVariables": {"fontSize": "18px"}, "flowchart": {"htmlLabels": false, "nodeSpacing": 35, "rankSpacing": 45}}}%%',
                  ("flowchart TB" if number in {"2", "4B", "9B", "11A", "11B"} else "flowchart LR"), f"    %% Configuration scope: {scope}"])
    lines.extend(compact)
    lines.extend(["```", "", "The picture shows connections. Full names, status qualifiers, and numbered relationship labels are below.", "", "| Diagram key | Full description |", "|---|---|"])
    lines.extend(f"| `{key}` | {label.replace('|', '/')} |" for key, label in details)
    lines.extend(["", "</details>", ""])
    return lines


def sequence_diagram(number: str, title: str, scope: str, body: Iterable[str], note: str = "") -> list[str]:
    lines = [f"### {number}. {title}", "", f"Configuration scope: `{scope}`."]
    if note:
        lines.extend(["", note])
    lines.extend(["", "<details>", f"<summary>Open {title.lower()} diagram</summary>", "", "```mermaid", '%%{init: {"theme": "neutral"}}%%', "sequenceDiagram", f"    %% Configuration scope: {scope}"])
    for line in body:
        if " as " in line:
            prefix, label = line.split(" as ", 1)
            line = prefix + " as " + "<br/>".join(textwrap.wrap(label, width=20))
        elif ":" in line:
            prefix, label = line.split(":", 1)
            line = prefix + ": " + "<br/>".join(textwrap.wrap(label.strip(), width=42))
        lines.append(line)
    lines.extend(["```", "", "</details>", ""])
    return lines


def state_diagram(number: str, title: str, scope: str, body: Iterable[str], note: str = "") -> list[str]:
    lines = [f"### {number}. {title}", "", f"Configuration scope: `{scope}`."]
    if note:
        lines.extend(["", note])
    lines.extend(["", "<details>", f"<summary>Open {title.lower()} diagram</summary>", "", "```mermaid", '%%{init: {"htmlLabels": false, "theme": "neutral"}}%%', "stateDiagram-v2", f"    %% Configuration scope: {scope}"])
    lines.extend(body)
    lines.extend(["```", "", "</details>", ""])
    return lines


def relation_map(catalogs: dict[str, dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    return {
        (item["from"], item["to"]): item
        for item in catalogs["traceability"].get("relationships", [])
    }


def interface_by_id(catalogs: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in catalogs["architecture"]["interfaces"]}


def edge_for_interface(
    interface: dict[str, Any],
    *,
    indent: str = "    ",
    label_suffix: str = "",
) -> str:
    arrow = "<-->" if interface["direction"].startswith("bidirectional") else "-->"
    label = f"{interface['id']}<br/>{clean_label(interface['flow_class'], 38)}"
    if label_suffix:
        label += f"<br/>{clean_label(label_suffix, 38)}"
    return (
        f"{indent}{mermaid_key(interface['endpoint_a'])} {arrow}|\"{label}\"| "
        f"{mermaid_key(interface['endpoint_b'])}"
    )


def edge_for_resource_relationship(relationship: dict[str, Any], *, indent: str = "    ") -> str:
    label = clean_label(relationship["label"])
    interface_refs = relationship.get("interface_refs", [])
    if interface_refs:
        label += "<br/>" + " / ".join(interface_refs)
    arrow = "-.->" if relationship.get("status") in {"candidate", "unresolved"} else "-->"
    return (
        f"{indent}{mermaid_key(relationship['from'])} {arrow}|\"{label}\"| "
        f"{mermaid_key(relationship['to'])}"
    )


def generated_header() -> list[str]:
    return [
        "<!-- GENERATED VIEW: DO NOT EDIT. Run python scripts/generate-mermaid-views.py -->",
        "# Architecture Atlas",
        "",
        "> **Baseline Candidate - Not Approved.** These diagrams are generated from",
        "> `model/system.yaml`, catalogs under `model/`, and `.seal/proof.yaml`. They have no",
        "> independent architecture authority. Candidate, proposed, deferred, and",
        "> unresolved labels do not imply approval or executed verification.",
        "",
        "The diagrams deliberately omit RF implementation values, build instructions,",
        "operating procedures, and recovered implementation detail. `CFG-REC` is shown",
        "only as a descriptive evidence configuration and does not inherit the proposed",
        "`CFG-REP`/`CFG-DOM` resource decomposition.",
        "This report is the ID-rich engineering drill-down. Plain-language canonical",
        "figures are generated separately under `docs/figures/`.",
        "Start with [Architecture](../architecture.md) for the subsystem explanation. These reference views retain stable IDs; full qualifiers live in the companion tables.",
        "",
        "## Configuration and context views",
        "",
    ]


def configuration_view(catalogs: dict[str, dict[str, Any]], index: dict[str, dict[str, Any]]) -> list[str]:
    body: list[str] = []
    delta_labels = {
        "CFG-REC": "evidence only - role mapping narrowed",
        "CFG-REP": "current proposed baseline",
        "CFG-DOM": "current - substitution criteria unresolved",
        "CFG-DIG": "future - adds IFC-INT-008 candidate",
        "CFG-SOS": "future outer context - OP-004 / OP-005 / OP-006",
    }
    for config in catalogs["architecture"]["configurations"]:
        extra = delta_labels[config["id"]]
        body.append("    " + node(index, config["id"], extra))
    for config in catalogs["architecture"]["configurations"]:
        for predecessor in config.get("predecessor_ids", []):
            meaning = clean_label(config["derivation_relationship"], 54)
            body.append(
                f'    {mermaid_key(predecessor)} -->|"{meaning}<br/>derivation is not approval"| '
                f"{mermaid_key(config['id'])}"
            )
    return flow_diagram(
        "1",
        "What is current, reference, and future?",
        "CFG-REC / CFG-REP / CFG-DOM / CFG-DIG / CFG-SOS",
        body,
        "Derivation denotes lineage, not exact inheritance, equivalence, or approval. Future context is outside the current implementation baseline.",
    )


def boundary_view(
    catalogs: dict[str, dict[str, Any]], index: dict[str, dict[str, Any]]
) -> list[str]:
    body = [
        '    subgraph OUTER["C2 Ecosystem outer boundary - CFG-SOS proposed context"]',
        "        " + node(index, "OP-010", "independently managed human performer"),
        "        " + node(index, "OP-001", "independently managed external system"),
        "        " + node(index, "OP-003", "independently managed external system"),
        "        " + node(index, "OP-004", "future / unresolved"),
        "        " + node(index, "OP-005", "future / unresolved"),
        "        " + node(index, "OP-006", "future / unresolved"),
        "        " + node(index, "OP-007", "external support performer"),
        "        " + node(index, "OP-008", "independent authority"),
        "        " + node(index, "OP-009", "future / unresolved"),
        '        subgraph INNER["Relay UAS inner boundary - proposed for CFG-REP/CFG-DOM/CFG-DIG"]',
        "            " + node(index, "OP-002", "system under study"),
        "        end",
        "    end",
    ]
    realization = {
        rel["from"]: rel["to"]
        for rel in catalogs["traceability"]["relationships"]
        if rel["relation"] in {"realized_by", "partially_realized_by"}
    }
    for exchange in catalogs["architecture"]["information_exchanges"]:
        if exchange["id"] not in {"IX-001", "IX-002", "IX-003", "IX-004", "IX-005", "IX-006", "IX-007", "IX-009", "IX-010"}:
            continue
        interface_id = realization.get(exchange["id"])
        suffix = f" / {interface_id}" if interface_id else " / unresolved"
        arrow = "-.->" if set(exchange.get("applicable_configurations", [])).issubset({"CFG-DIG", "CFG-SOS"}) else "-->"
        body.append(
            f'    {mermaid_key(exchange["from"])} {arrow}|"{exchange["id"]}{suffix}<br/>{clean_label(exchange["flow_class"])}"| '
            f'{mermaid_key(exchange["to"])}'
        )
    return flow_diagram(
        "2",
        "What is inside the project boundary?",
        "CFG-SOS outer context - CFG-REP / CFG-DOM / CFG-DIG inner constituent",
        body,
        "External constituents remain independently managed. Only catalogued information exchanges are drawn; unconnected future actors remain context, not implied interfaces.",
    )


def operational_connectivity_view(
    catalogs: dict[str, dict[str, Any]], index: dict[str, dict[str, Any]]
) -> list[str]:
    exchange_ids = ["IX-001", "IX-002", "IX-003", "IX-004", "IX-005"]
    realization = {
        rel["from"]: rel["to"]
        for rel in catalogs["traceability"]["relationships"]
        if rel["from"] in exchange_ids and rel["relation"] in {"realized_by", "partially_realized_by"}
    }
    body = [
        "    " + node(index, "OP-010"),
        "    " + node(index, "OP-001"),
        "    " + node(index, "OP-002"),
        "    " + node(index, "OP-003"),
    ]
    for exchange_id in exchange_ids:
        exchange = index[exchange_id]
        interface_id = realization.get(exchange_id, "UNRESOLVED")
        label = f"{exchange_id} / {interface_id}<br/>{clean_label(exchange['flow_class'], 34)}"
        body.append(
            f'    {mermaid_key(exchange["from"])} -->|"{label}"| {mermaid_key(exchange["to"])}'
        )
    return flow_diagram(
        "3",
        "How current-system traffic moves",
        "CFG-REP / CFG-DOM",
        body,
        "`IX-001` is independent Relay-UAS platform command. `IX-002` through `IX-005` are relayed mission traffic.",
    )


def resource_diagrams(catalogs: dict[str, dict[str, Any]], index: dict[str, dict[str, Any]]) -> list[str]:
    interfaces = interface_by_id(catalogs)
    resource_relationships = catalogs["architecture"].get("resource_relationships", [])
    lines: list[str] = ["## Relay-UAS resource views", ""]

    structure_ids = ["CMP-AFR-01", "CMP-AFR-02", "CMP-AFR-03", "CMP-AFR-04", "CMP-AFR-05", "CMP-MNT-01", "CMP-COM-01"]
    body = ["    " + node(index, item_id) for item_id in structure_ids]
    body.extend(
        edge_for_resource_relationship(item)
        for item in resource_relationships
        if "structure" in item.get("view_groups", [])
    )
    body.append(edge_for_interface(interfaces["IFC-INT-007"]))
    lines.extend(flow_diagram("4A", "Structure and payload mounting", "CFG-REP / CFG-DOM", body))

    power_ids = ["CMP-PWR-01", "CMP-PWR-02", "CMP-PWR-03", "CMP-PWR-04", "CMP-PRP-01", "CMP-PRP-02", "CMP-PRP-03", "CMP-AVN-01", "CMP-COM-01"]
    body = ["    " + node(index, item_id) for item_id in power_ids]
    body.extend([
        edge_for_interface(interfaces["IFC-INT-011"]),
        *[
            edge_for_resource_relationship(item)
            for item in resource_relationships
            if "power" in item.get("view_groups", [])
        ],
        edge_for_interface(interfaces["IFC-INT-001"]),
        edge_for_interface(interfaces["IFC-INT-015"]),
        edge_for_interface(interfaces["IFC-INT-002"]),
        edge_for_interface(interfaces["IFC-INT-003"], label_suffix="platform-to-payload"),
        edge_for_interface(interfaces["IFC-INT-006"]),
        edge_for_interface(interfaces["IFC-INT-013"]),
        edge_for_interface(interfaces["IFC-INT-014"]),
    ])
    lines.extend(flow_diagram("4B", "How power and propulsion connect", "CFG-REP / CFG-DOM", body))

    avionics_ids = ["OP-010", "CMP-AVN-01", "CMP-AVN-02", "CMP-AVN-03", "CMP-AVN-04", "CMP-PRP-02", "CMP-PWR-02"]
    body = ["    " + node(index, item_id) for item_id in avionics_ids]
    body.extend([
        edge_for_interface(interfaces["IFC-EXT-005"], label_suffix="separate platform command"),
        edge_for_interface(interfaces["IFC-INT-005"]),
        edge_for_interface(interfaces["IFC-INT-004"]),
        edge_for_interface(interfaces["IFC-INT-006"]),
        edge_for_interface(interfaces["IFC-INT-009"]),
        edge_for_interface(interfaces["IFC-INT-012"]),
    ])
    lines.extend(flow_diagram("4C", "How platform control works", "CFG-REP / CFG-DOM", body))

    body = [
        "    " + node(index, "OP-001"),
        "    " + node(index, "OP-003"),
        "    " + node(index, "CMP-PWR-03"),
        "    " + node(index, "CMP-MNT-01"),
        '    subgraph PAYLOAD["Relay-payload black-box envelope"]',
        "        " + node(index, "CMP-COM-01"),
        "        " + node(index, "CMP-COM-02", "physical-resource envelope"),
        edge_for_interface(interfaces["IFC-INT-010"], indent="        ", label_suffix="payload-internal - characteristics undefined"),
        "    end",
        edge_for_interface(interfaces["IFC-INT-003"], label_suffix="platform boundary crossing"),
        edge_for_interface(interfaces["IFC-INT-007"], label_suffix="platform boundary crossing"),
        edge_for_interface(interfaces["IFC-EXT-001"], label_suffix="implementation undefined"),
        edge_for_interface(interfaces["IFC-EXT-002"], label_suffix="implementation undefined"),
        edge_for_interface(interfaces["IFC-EXT-003"], label_suffix="implementation undefined"),
        edge_for_interface(interfaces["IFC-EXT-004"], label_suffix="implementation undefined"),
    ]
    lines.extend(flow_diagram(
        "4D",
        "How the relay payload is bounded",
        "CFG-REP / CFG-DOM",
        body,
        "`IFC-INT-010` stays inside the payload black-box envelope. Only `IFC-INT-003` and `IFC-INT-007` cross from platform to payload.",
    ))

    body = [
        "    " + node(index, "OP-007"),
        "    " + node(index, "OP-002"),
        edge_for_interface(interfaces["IFC-EXT-006"], label_suffix="IX-010 support/governance"),
    ]
    lines.extend(flow_diagram(
        "4E",
        "Maintenance and configuration support",
        "CFG-REP / CFG-DOM / CFG-DIG / CFG-SOS",
        body,
        "This support/governance interface is intentionally omitted from airborne mission-traffic diagrams.",
    ))

    ix_008_gap = next(
        item for item in catalogs["traceability"]["relationships"]
        if item["from"] == "IX-008" and item["relation"] == "deferred_to_gap"
    )
    body = [
        "    " + node(index, "CMP-AVN-01"),
        "    " + node(index, "CMP-COM-01", "future payload [PROPOSED]"),
        edge_for_interface(interfaces["IFC-INT-008"], label_suffix="future / proposed"),
        "    " + node(index, "IX-008", "future sensor-data exchange [UNRESOLVED]"),
        "    " + node(index, ix_008_gap["to"], "realizing interface unresolved"),
        f'    IX_008 -.->|"{clean_label(ix_008_gap["relation"].replace("_", " "))}"| '
        f'{mermaid_key(ix_008_gap["to"])}',
    ]
    lines.extend(flow_diagram(
        "4F",
        "Future digital interface delta",
        "CFG-DIG / CFG-SOS only",
        body,
        "`IFC-INT-008` is not part of the current `CFG-REP`/`CFG-DOM` two-interface payload boundary.",
    ))
    return lines


def reconciliation_views(catalogs: dict[str, dict[str, Any]]) -> list[str]:
    reconciliation = catalogs["architecture"]["configuration_reconciliation"]
    component_counts = collections.Counter(
        item["mapping_classification"]
        for item in reconciliation["candidate_components_to_recovered"]
    )
    interface_counts = collections.Counter(
        item["mapping_classification"]
        for item in reconciliation["candidate_interfaces_to_recovered"]
    )
    lines = ["## Evidence correspondence views", ""]
    body = [
        '    REC_STRUCTURE["Recovered structure and hardware"] -->|"direct / class-level support"| CAND_STRUCTURE["CMP-AFR-01 through CMP-AFR-05"]',
        '    REC_PROPULSION["Recovered propulsion resources"] -->|"direct role support"| CAND_PROPULSION["CMP-PRP-01 through CMP-PRP-03"]',
        '    REC_POWER["Recovered power resources and harness"] -->|"direct / partial / unknown"| CAND_POWER["CMP-PWR-01 through CMP-PWR-04"]',
        '    REC_AVIONICS["Recovered control and navigation resources"] -->|"direct / partial support"| CAND_AVIONICS["CMP-AVN-01 through CMP-AVN-04"]',
        '    REC_PAYLOAD["Recovered payload modules and antennas"] -->|"partial / inferred correspondence"| CAND_PAYLOAD["CMP-COM-01 / CMP-COM-02"]',
        '    REC_MOUNTING["Recovered payload retention"] -->|"partial role support"| CAND_MOUNTING["CMP-MNT-01"]',
    ]
    lines.extend(flow_diagram(
        "4G",
        "How recovered evidence informs candidate roles",
        "CFG-REC informs CFG-REP / CFG-DOM - no exact inheritance",
        body,
        "This is a grouped view of the controlled record-level mapping. Five recovered records remain unmatched and one remains unknown; no contradiction was found.",
    ))

    def count(classification: str, values: collections.Counter[str]) -> int:
        return values.get(classification, 0)

    body = [
        f'    COVERAGE["Two-way candidate coverage<br/>{len(reconciliation["candidate_components_to_recovered"])} components / {len(reconciliation["candidate_interfaces_to_recovered"])} interfaces"]',
        f'    COVERAGE --> DIRECT["Direct source support<br/>components {count("DIRECT_SOURCE_SUPPORT", component_counts)} / interfaces {count("DIRECT_SOURCE_SUPPORT", interface_counts)}"]',
        f'    COVERAGE --> INDIRECT["Indirect source support<br/>components {count("INDIRECT_SOURCE_SUPPORT", component_counts)} / interfaces {count("INDIRECT_SOURCE_SUPPORT", interface_counts)}"]',
        f'    COVERAGE --> INFERENCE["Engineering inference<br/>components {count("ENGINEERING_INFERENCE", component_counts)} / interfaces {count("ENGINEERING_INFERENCE", interface_counts)}"]',
        f'    COVERAGE --> PROPOSED["Proposed architecture only<br/>components {count("PROPOSED_ARCHITECTURE_ONLY", component_counts)} / interfaces {count("PROPOSED_ARCHITECTURE_ONLY", interface_counts)}"]',
        f'    COVERAGE --> NONE["No recovered evidence<br/>components {count("NO_RECOVERED_EVIDENCE", component_counts)} / interfaces {count("NO_RECOVERED_EVIDENCE", interface_counts)}"]',
        f'    COVERAGE --> NA["Not applicable<br/>components {count("NOT_APPLICABLE", component_counts)} / interfaces {count("NOT_APPLICABLE", interface_counts)}"]',
    ]
    lines.extend(flow_diagram(
        "4H",
        "Candidate architecture evidence coverage",
        "CFG-REP / CFG-DOM current - CFG-DIG future interface classified separately",
        body,
        "Coverage classification is evidence posture, not approval, identity, or requirement verification.",
    ))
    return lines


def mode_view(
    catalogs: dict[str, dict[str, Any]], index: dict[str, dict[str, Any]]
) -> list[str]:
    architecture = catalogs["architecture"]
    ordered_modes = ["MODE-005", "MODE-001", "MODE-002", "MODE-003", "MODE-004"]
    body = [
        f'    state "{item_id} {record_name(index[item_id])}" as {mermaid_key(item_id)}'
        for item_id in ordered_modes
    ]
    body.append(f"    [*] --> {mermaid_key(architecture['initial_mode'])}")
    for transition in architecture["mode_transitions"]:
        triggers = " / ".join(transition["trigger_refs"])
        body.append(
            f"    {mermaid_key(transition['from'])} --> {mermaid_key(transition['to'])}: "
            f"{triggers} - {clean_label(transition['label'])}"
        )
    body.extend([
        "    note right of MODE_003",
        "      Payload function degraded",
        "      Platform control may remain available",
        "      REQ-007 [PROPOSED]",
        "      Evidence [DEFERRED]",
        "    end note",
    ])
    return state_diagram(
        "5",
        "How operating modes change",
        "CFG-REP / CFG-DOM",
        body,
        "Only transitions supported by current scenarios or requirements are shown; all remain candidate unless stated otherwise.",
    )


def launch_sequence(index: dict[str, dict[str, Any]]) -> list[str]:
    body = [
        '    participant Operator as OP-010 Operator',
        '    participant Receiver as CMP-AVN-04 Control receiver',
        '    participant Flight as CMP-AVN-01 Flight-control resource',
        '    participant Nav as CMP-AVN-02 Navigation/sensor resources',
        '    participant Propulsion as CMP-PRP-02 Propulsion control',
        '    participant Relay as OP-002 Relay UAS health/status',
        "    Operator->>Receiver: IX-001 / IFC-EXT-005 platform command intent",
        "    Receiver->>Flight: IFC-INT-005 platform control input",
        "    Nav-->>Flight: IFC-INT-009 navigation/timing information",
        "    Flight->>Propulsion: IFC-INT-004 propulsion command",
        "    Relay-->>Operator: IX-009 / IFC-EXT-007 health/status [PROPOSED]",
        "    Note over Operator,Relay: SCN-002 architecture walkthrough - no procedure defined",
    ]
    return sequence_diagram("6", "Launch and positioning sequence", "CFG-REP / CFG-DOM", body)


def relay_sequence(index: dict[str, dict[str, Any]]) -> list[str]:
    body = [
        '    participant Operator as OP-010 Platform operator',
        '    participant Platform as CMP-AVN-04 Platform command receiver',
        '    participant Ground as OP-001 Ground control node',
        '    participant Payload as CMP-COM-01 Relay payload black box',
        '    participant Remote as OP-003 Remote UAS',
        "    Operator->>Platform: IX-001 / IFC-EXT-005 separate Relay-UAS platform command",
        "    rect rgb(245, 245, 245)",
        "        Ground->>Payload: IX-002 / IFC-EXT-001 outbound traffic",
        "        Payload->>Remote: IX-003 / IFC-EXT-002 outbound traffic",
        "        Remote-->>Payload: IX-004 / IFC-EXT-003 return telemetry",
        "        Payload-->>Ground: IX-005 / IFC-EXT-004 return telemetry",
        "    end",
        "    Note over Ground,Remote: SCN-003 / SCN-004 logical relay only - external paths undefined",
    ]
    return sequence_diagram("7A", "Carrier command path", "CFG-REP / CFG-DOM", body[:2] + [body[5]],
                            "Carrier command is logically separate from the relay payload; isolation and link performance are not verified.") + sequence_diagram(
        "7B", "Relayed mission traffic", "CFG-REP / CFG-DOM", body[2:5] + body[6:],
        "The conceptual service includes return telemetry. Only outbound stationary service is quantitatively screened.")


def degradation_sequence(index: dict[str, dict[str, Any]]) -> list[str]:
    body = [
        '    participant Ground as OP-001 Ground control node',
        '    participant Payload as CMP-COM-01 Relay payload black box',
        '    participant Relay as OP-002 Relay UAS platform',
        '    participant Operator as OP-010 Platform operator',
        "    Payload--xGround: SCN-007 relay function loss or degradation",
        "    Relay-->>Operator: IX-009 / IFC-EXT-007 health/status [PROPOSED]",
        "    Operator->>Relay: IX-001 / IFC-EXT-005 independent platform command",
        "    alt Payload lost and platform remains controllable",
        "        Note over Payload,Relay: MODE-003 - CTL-004 / REQ-007 [PROPOSED]",
        "        Relay-->>Operator: transition intent toward MODE-004 Return / Recovery",
        "    else Platform control also impaired",
        "        Note over Relay,Operator: HAZ-001 / GAP-HAZ-001 - no modeled consequence-management behavior",
        "        Note over Ground,Operator: GAP-VER-001 - no executed recovery evidence",
        "    end",
    ]
    return sequence_diagram(
        "8",
        "What happens on relay degradation?",
        "CFG-REP / CFG-DOM",
        body,
        "The second path terminates at explicit gaps; it does not invent a recovery behavior.",
    )


def lifecycle_view(
    catalogs: dict[str, dict[str, Any]], index: dict[str, dict[str, Any]]
) -> list[str]:
    scenario_ids = [f"SCN-{number:03d}" for number in range(1, 9)]
    body = ["    " + node(index, item_id, status_of(index, item_id)) for item_id in scenario_ids]
    for transition in catalogs["architecture"]["scenario_transitions"]:
        arrow = "-.->" if transition["transition_type"] == "future" else "-->"
        gap_note = " / " + " / ".join(transition.get("gap_refs", [])) if transition.get("gap_refs") else ""
        body.append(
            f'    {mermaid_key(transition["from"])} {arrow}|"{clean_label(transition["label"])}{gap_note}"| '
            f'{mermaid_key(transition["to"])}'
        )
    return flow_diagram(
        "9",
        "Scenario lifecycle",
        "CFG-REP / CFG-DOM current - CFG-DIG / CFG-SOS proposed branches",
        body,
        "Dashed branches are future proposals without complete activity, interface, requirement, hazard, or verification allocation.",
    )


def health_status_view(index: dict[str, dict[str, Any]]) -> list[str]:
    item_ids = [
        "SCN-007", "IX-009", "IFC-INT-006", "FUN-HLT-01", "CMP-AVN-01",
        "IFC-EXT-007", "OP-010", "REQ-008", "VER-005", "VER-008", "VER-009",
    ]
    body = ["    " + node(index, item_id, status_of(index, item_id)) for item_id in item_ids]
    body.extend([
        '    SCN_007 -->|"uses"| IX_009',
        '    IX_009 -->|"supported by"| FUN_HLT_01',
        '    IFC_INT_006 -->|"battery-state input only"| FUN_HLT_01',
        '    FUN_HLT_01 -->|"allocated to"| CMP_AVN_01',
        '    IX_009 -->|"realized by"| IFC_EXT_007',
        '    IFC_EXT_007 -->|"made available to"| OP_010',
        '    REQ_FUN_008 -->|"allocates behavior"| FUN_HLT_01',
        '    REQ_FUN_008 -->|"model review"| VER_005',
        '    REQ_FUN_008 -.->|"physical evidence"| VER_008',
        '    REQ_FUN_008 -.->|"external conformance"| VER_009',
    ])
    return flow_diagram(
        "9A",
        "Health/status logical thread",
        "CFG-REP / CFG-DOM",
        body,
        "The logical status purpose is proposed. Message content, transport, external authority, and physical evidence remain unresolved.",
    )


def design_dependency_view(
    catalogs: dict[str, dict[str, Any]], index: dict[str, dict[str, Any]]
) -> list[str]:
    item_ids = [
        "REQ-012", "TS-006", "TS-001", "REQ-011", "TS-002",
        "TS-004", "REQ-010", "TS-003", "REQ-009", "GAP-BUDGET-001",
    ]
    body = ["    " + node(index, item_id, status_of(index, item_id)) for item_id in item_ids]
    for relationship in catalogs["traceability"]["relationships"]:
        if relationship.get("view_group") != "mass_cost_power_endurance":
            continue
        arrow = "-.->" if relationship["to"].startswith("GAP-") else "-->"
        label = clean_label(relationship["relation"].replace("_", " "))
        body.append(
            f'    {mermaid_key(relationship["from"])} {arrow}|"{label}"| '
            f'{mermaid_key(relationship["to"])}'
        )
    return flow_diagram(
        "9B",
        "Why mass, power, endurance, and cost are coupled",
        "CFG-REP / CFG-DOM",
        body,
        "This is one coupled design problem. The diagram adds no values and does not resolve any trade study.",
    )


def hazard_view(catalogs: dict[str, dict[str, Any]], index: dict[str, dict[str, Any]]) -> list[str]:
    controls = catalogs["assurance"]["controls"]
    requirements = {item["id"]: item for item in catalogs["assurance"]["requirements"]}
    body: list[str] = []
    emitted: set[str] = set()

    def emit(item_id: str, extra: str = "") -> None:
        if item_id not in emitted:
            body.append("    " + node(index, item_id, extra))
            emitted.add(item_id)

    for hazard_id in ["HAZ-004", "HAZ-008"]:
        emit(hazard_id, "[PROPOSED]")
        control = next(item for item in controls if hazard_id in item.get("mitigates", []))
        emit(control["id"], "[PROPOSED]")
        body.append(f'    {mermaid_key(hazard_id)} -->|"mitigated by"| {mermaid_key(control["id"])}')
        for requirement_id in control["implemented_by"]:
            emit(requirement_id, "[PROPOSED]")
            body.append(f'    {mermaid_key(control["id"])} -->|"implemented by"| {mermaid_key(requirement_id)}')
            for verification_id in requirements[requirement_id].get("verification_ids", []):
                emit(verification_id, status_of(index, verification_id))
                body.append(f'    {mermaid_key(requirement_id)} -->|"verification allocation"| {mermaid_key(verification_id)}')
                emit("GAP-VER-001", "[OPEN PHYSICAL / EXTERNAL EVIDENCE]")
                if index[verification_id].get("execution_status") in {"executed_pass", "executed_with_open_gaps"}:
                    body.append(f'    {mermaid_key(verification_id)} -.->|"model review complete - physical evidence absent"| GAP_VER_001')
                else:
                    body.append(f'    {mermaid_key(verification_id)} -.->|"execution unavailable"| GAP_VER_001')
    return flow_diagram(
        "10",
        "Hazard-control-requirement-verification",
        "CFG-REP / CFG-DOM",
        body,
        "Executed model reviews establish trace consistency only. Deferred physical methods remain unexecuted, and no review provides approval or safety credit.",
    )


def verification_readiness_view(index: dict[str, dict[str, Any]]) -> list[str]:
    body = [
        '    ACCEPTED["PRESERVED OWNER-ACCEPTED REVIEW<br/>0.7.0 / EVD-008 through EVD-012"]',
        '    EXECUTED["LATEST RECORDED MODEL REVIEW<br/>0.8.0 / VER-001 through VER-007<br/>EVD-013 - not owner accepted"]',
        '    PASS["EXECUTED PASS<br/>VER-002 / VER-007"]',
        '    OPEN["EXECUTED WITH OPEN GAPS<br/>VER-001 / VER-003 through VER-006"]',
        '    PHYSICAL["PHYSICAL-EVIDENCE-REQUIRED<br/>REQ-006 / REQ-008<br/>GAP-VER-001"]',
        '    EXTERNAL["EXTERNAL-AUTHORITY-REQUIRED<br/>REQ-001 / REQ-004<br/>GAP-IFC-001"]',
        '    DEFERRED["INTENTIONALLY-DEFERRED<br/>DEF-001 / DEF-004"]',
        "    " + node(index, "VER-008", "future physical evidence"),
        "    " + node(index, "VER-009", "external authority required"),
        "    " + node(index, "TS-009", "formal deferral"),
        '    ACCEPTED -->|"historical acceptance boundary preserved"| EXECUTED',
        '    EXECUTED -->|"no structural failure"| PASS',
        '    EXECUTED -->|"known gaps retained"| OPEN',
        '    PHYSICAL -.->|"no execution evidence"| VER_008',
        '    EXTERNAL -.->|"authority and specification absent"| VER_009',
        '    DEFERRED -.->|"outside current scope"| TS_009',
    ]
    return flow_diagram(
        "10A",
        "What has been checked and what still needs evidence?",
        "CFG-REP / CFG-DOM with project-scope deferrals",
        body,
        "VER-001 through VER-007 have 0.8.0 model-level evidence in EVD-013 but no owner acceptance. The current 0.9.0 identifier and documentation refactor has no new evidence record. EVD-008 through EVD-012 preserve the accepted 0.7.0 work package. VER-008 remains deferred and VER-009 remains blocked; none of these records constitutes physical verification, external conformance, safety approval, or technical-baseline approval.",
    )


def trace_view(index: dict[str, dict[str, Any]]) -> list[str]:
    ids = [
        "NEED-001", "CAP-001", "SCN-003", "OA-004", "IX-002",
        "FUN-REL-01", "CMP-COM-01", "IFC-EXT-001",
        "REQ-001", "VER-001", "VER-009", "GAP-IFC-001",
    ]
    body = ["    " + node(index, item_id, status_of(index, item_id)) for item_id in ids]
    body.extend([
        '    NEED_001 -->|"motivates"| CAP_001',
        '    CAP_001 -->|"exercised by"| SCN_003',
        '    SCN_003 -->|"uses"| OA_004',
        '    OA_004 -->|"information exchange"| IX_002',
        '    IX_002 -->|"supports"| FUN_REL_01',
        '    FUN_REL_01 -->|"allocated to"| CMP_COM_01',
        '    CMP_COM_01 -->|"external interface"| IFC_EXT_001',
        '    IFC_EXT_001 -->|"allocated requirement"| REQ_001',
        '    REQ_001 -->|"model analysis"| VER_001',
        '    REQ_001 -.->|"external conformance"| VER_009',
        '    VER_009 -.->|"authority and evidence unresolved"| GAP_IFC_001',
    ])
    # Split the long trace at the payload component; preserve every relationship.
    first_ids = ids[:7]
    second_ids = ids[6:]
    edges = [line for line in body if '-->' in line or '-.->' in line]
    first = ["    " + node(index, i, status_of(index, i)) for i in first_ids] + edges[:6]
    second = ["    " + node(index, i, status_of(index, i)) for i in second_ids] + edges[6:]
    return flow_diagram("11A", "Relay trace: need to payload", "CFG-REP / CFG-DOM", first,
                        "Follow the need to its allocated payload role; continue at CMP-COM-01 in 11B.") + flow_diagram(
        "11B", "Relay trace: payload to evidence", "CFG-REP / CFG-DOM", second,
        "Continue from CMP-COM-01 in 11A. Model review and external conformance are different evidence obligations.")



def governance_view(index: dict[str, dict[str, Any]]) -> list[str]:
    body = [
        "    " + node(index, "SRC-INT-001", "registered source"),
        "    " + node(index, "EVD-002", "registered evidence record"),
        "    " + node(index, "CLM-REC-001", "source-supported claim"),
        "    " + node(index, "CFG-REC", "descriptive evidence configuration"),
        "    " + node(index, "CLM-REC-005", "controlled role mapping demonstrated"),
        "    " + node(index, "GAP-REC-001", "narrowed - exact equivalence unresolved"),
        "    " + node(index, "DEC-002", "proposed owner decision"),
        "    " + node(index, "GAP-STD-001", "unresolved standards decision"),
        '    BASELINE["Baseline Candidate - Not Approved<br/>model-valid may still be gapped"]',
        '    SRC_INT_001 -->|"registered as"| EVD_002',
        '    EVD_002 -->|"supports - does not approve"| CLM_REC_001',
        '    CLM_REC_001 -->|"applicable to evidence configuration"| CFG_REC',
        '    CLM_REC_005 -->|"records two-way role correspondence"| CFG_REC',
        '    CFG_REC -.->|"complete reconstruction unresolved"| GAP_REC_001',
        '    DEC_002 -.->|"owner review required"| GAP_STD_001',
        '    GAP_REC_001 -->|"gap remains visible"| BASELINE',
        '    GAP_STD_001 -->|"gap remains visible"| BASELINE',
    ]
    return flow_diagram(
        "12",
        "Evidence and approval governance",
        "Project governance - CFG-REC evidence semantics - all configurations remain not approved",
        body,
        "Evidence supports claims; it does not approve architecture. Proposed decisions require explicit owner action.",
    )


def interface_inventory(catalogs: dict[str, dict[str, Any]]) -> list[str]:
    evidence_by_interface = {
        item["candidate_id"]: item["mapping_classification"]
        for item in catalogs["architecture"]["configuration_reconciliation"]["candidate_interfaces_to_recovered"]
    }
    lines = [
        "## Generated interface inventory",
        "",
        "This inventory is generated directly from `model/architecture.yaml`. Model-review",
        "allocation is distinct from real-world external conformance and execution evidence.",
        "",
        "| ID | Endpoints | Direction | Flow class | Configurations | Recovered evidence | Maturity | Model review | External conformance | Unknown attributes |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for interface in catalogs["architecture"]["interfaces"]:
        verification = ", ".join(interface.get("verification_ids", [])) or "None - explicit gap"
        model_review = ", ".join(interface.get("internal_model_verification_ids", [])) or verification
        external_conformance = interface.get(
            "external_conformance_status", "not an external conformance interface"
        )
        unknowns = "; ".join(interface.get("unknown_attributes", [])) or "None recorded"
        maturity = f"{interface.get('evidence_basis')} / {interface.get('decision_status')}"
        row = [
            interface["id"],
            f"{interface['endpoint_a']} to {interface['endpoint_b']}",
            interface["direction"],
            interface["flow_class"],
            ", ".join(interface["applicable_configurations"]),
            evidence_by_interface[interface["id"]],
            maturity,
            model_review,
            external_conformance,
            unknowns,
        ]
        lines.append("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |")
    lines.extend(["", "## Validation notes", ""])
    lines.extend([
        f"- Optional syntax validation expects Mermaid CLI `mmdc` {PINNED_MERMAID_CLI} when installed locally.",
        "- Absence of Node.js or the pinned CLI does not invalidate standard-library catalog validation.",
        "- This technical report remains Mermaid-based; canonical SVG figures are generated and validated separately.",
        "",
    ])
    return lines


def select_numbered_views(lines: list[str], keep: set[str], section_title: str) -> list[str]:
    """Keep selected generated subviews without duplicating their rendering logic."""
    result = [section_title, ""]
    current_number: str | None = None
    current: list[str] = []

    def flush() -> None:
        if current_number in keep:
            result.extend(current)

    for line in lines:
        if line.startswith("### "):
            flush()
            current = [line]
            current_number = line.split()[1].rstrip(".")
        elif current_number is not None:
            current.append(line)
    flush()
    return result


def render(catalogs: dict[str, dict[str, Any]]) -> str:
    index = build_index(catalogs)
    lines = generated_header()
    lines.extend(configuration_view(catalogs, index))
    lines.extend(boundary_view(catalogs, index))
    lines.extend(operational_connectivity_view(catalogs, index))
    lines.extend(select_numbered_views(
        resource_diagrams(catalogs, index), {"4B", "4C", "4D"},
        "## Selected resource connectivity views",
    ))
    lines.extend(select_numbered_views(
        reconciliation_views(catalogs), {"4G"}, "## Evidence correspondence view",
    ))
    lines.extend(["## Behavioral views", ""])
    lines.extend(mode_view(catalogs, index))
    lines.extend(relay_sequence(index))
    lines.extend(degradation_sequence(index))
    lines.extend(design_dependency_view(catalogs, index))
    lines.extend(["## Assurance and traceability views", ""])
    lines.extend(verification_readiness_view(index))
    lines.extend(trace_view(index))
    lines.extend(interface_inventory(catalogs))
    return "\n".join(lines).rstrip() + "\n"


def extract_diagrams(markdown: str) -> list[tuple[str, str]]:
    diagrams: list[tuple[str, str]] = []
    title = "untitled"
    in_mermaid = False
    body: list[str] = []
    for line in markdown.splitlines():
        if line.startswith("### "):
            title = line[4:].strip()
        elif line == "```mermaid":
            in_mermaid = True
            body = []
        elif in_mermaid and line == "```":
            diagrams.append((title, "\n".join(body) + "\n"))
            in_mermaid = False
        elif in_mermaid:
            body.append(line)
    return diagrams


def find_mmdc() -> str | None:
    candidates = [
        ROOT / "node_modules" / ".bin" / ("mmdc.cmd" if sys.platform == "win32" else "mmdc"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return shutil.which("mmdc")


def validate_mermaid_syntax(markdown: str) -> int:
    executable = find_mmdc()
    if not executable:
        print(
            f"MERMAID-PARSER: SKIPPED - pinned mmdc {PINNED_MERMAID_CLI} "
            "is not installed locally"
        )
        return 0
    version = subprocess.run(
        [executable, "--version"], capture_output=True, text=True, check=False
    )
    reported = (version.stdout or version.stderr).strip()
    if PINNED_MERMAID_CLI not in reported:
        print(
            f"MERMAID-PARSER: SKIPPED - available mmdc version is {reported!r}, "
            f"expected pinned {PINNED_MERMAID_CLI}"
        )
        return 0
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="relay-uas-mermaid-") as temp_name:
        temp = Path(temp_name)
        for number, (title, diagram) in enumerate(extract_diagrams(markdown), start=1):
            source = temp / f"diagram-{number:02d}.mmd"
            output = temp / f"diagram-{number:02d}.svg"
            source.write_text(diagram, encoding="utf-8", newline="\n")
            result = subprocess.run(
                [executable, "-i", str(source), "-o", str(output)],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode:
                error = clean_label(result.stderr or result.stdout or "unknown parser error", 400)
                failures.append(f"{title}: {error}")
    if failures:
        print("MERMAID-PARSER: FAILED - one or more generated diagrams did not render")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(
        f"MERMAID-PARSER: PASSED - validated every generated diagram "
        f"with pinned mmdc {PINNED_MERMAID_CLI}"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail when the generated report is stale")
    parser.add_argument(
        "--validate-syntax",
        action="store_true",
        help="optionally validate each diagram with locally installed pinned Mermaid CLI",
    )
    args = parser.parse_args()

    catalogs = load_catalogs()
    expected = render(catalogs)
    result = 0
    if args.check:
        actual = OUTPUT.read_text(encoding="utf-8-sig") if OUTPUT.exists() else ""
        if actual != expected:
            print(f"GENERATED-VIEWS-STALE: run {Path(__file__).name}")
            result = 1
        else:
            print("GENERATED-VIEWS-CURRENT: docs/reference/architecture-atlas.md")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(expected, encoding="utf-8", newline="\n")
        print("GENERATED-VIEWS-WRITTEN: docs/reference/architecture-atlas.md")

    if args.validate_syntax:
        result = max(result, validate_mermaid_syntax(expected))
    return result


if __name__ == "__main__":
    sys.exit(main())
