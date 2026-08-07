#!/usr/bin/env python3
"""Generate deterministic GitHub-renderable Mermaid architecture views.

The authoritative catalogs are JSON-compatible YAML 1.2, so this script uses only
the Python standard library. It does not infer implementation detail or approve any
candidate relationship.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports" / "architecture-views.md"
PINNED_MERMAID_CLI = "11.4.1"

CATALOG_PATHS = {
    "system": ROOT / "system.yaml",
    "sources": ROOT / ".seal" / "sources.yaml",
    "proof": ROOT / ".seal" / "proof.yaml",
    "architecture": ROOT / "model" / "architecture.yaml",
    "assurance": ROOT / "model" / "assurance.yaml",
    "traceability": ROOT / "model" / "traceability.yaml",
}

SHORT_LABELS = {
    "SRC-INT-001": "Recovered-article research report",
    "GAP-STD-001": "UAF version decision unresolved",
    "GAP-REC-001": "Recovered-to-candidate mapping unresolved",
    "GAP-HAZ-001": "HAZ-001 has no defined control",
    "GAP-VER-001": "Execution evidence missing",
    "REQ-FUN-001": "Relay outbound traffic",
    "REQ-FUN-006": "Inhibit arming in Ground Safe",
    "REQ-FUN-007": "Remain controllable after payload loss",
    "REQ-IFC-004": "Retain payload under flight loads",
    "REQ-SAF-001": "Protect and retain battery",
    "REQ-SAF-002": "Show armed state to operator",
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
        record.get("name")
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
        return "[DEFERRED]" if record.get("disposition") == "deferred" else "[UNRESOLVED]"
    status = record.get("decision_status") or record.get("status") or "unverified"
    labels = {
        "proposed": "[PROPOSED]",
        "deferred": "[DEFERRED]",
        "unknown": "[TBD]",
        "candidate": "[PROPOSED]",
        "unverified": "[UNVERIFIED]",
    }
    return labels.get(str(status), clean_label(status))


def flow_diagram(number: str, title: str, scope: str, body: Iterable[str], note: str = "") -> list[str]:
    lines = [f"### {number}. {title}", "", f"Configuration scope: `{scope}`."]
    if note:
        lines.extend(["", note])
    lines.extend(["", "```mermaid", "flowchart LR", f"    %% Configuration scope: {scope}"])
    lines.extend(body)
    lines.extend(["```", ""])
    return lines


def sequence_diagram(number: str, title: str, scope: str, body: Iterable[str], note: str = "") -> list[str]:
    lines = [f"### {number}. {title}", "", f"Configuration scope: `{scope}`."]
    if note:
        lines.extend(["", note])
    lines.extend(["", "```mermaid", "sequenceDiagram", f"    %% Configuration scope: {scope}"])
    lines.extend(body)
    lines.extend(["```", ""])
    return lines


def state_diagram(number: str, title: str, scope: str, body: Iterable[str], note: str = "") -> list[str]:
    lines = [f"### {number}. {title}", "", f"Configuration scope: `{scope}`."]
    if note:
        lines.extend(["", note])
    lines.extend(["", "```mermaid", "stateDiagram-v2", f"    %% Configuration scope: {scope}"])
    lines.extend(body)
    lines.extend(["```", ""])
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


def generated_header() -> list[str]:
    return [
        "<!-- GENERATED VIEW: DO NOT EDIT. Run python scripts/generate-mermaid-views.py -->",
        "# Generated Architecture Views",
        "",
        "> **Baseline Candidate - Not Approved.** These diagrams are generated from",
        "> `system.yaml`, catalogs under `model/`, and `.seal/proof.yaml`. They have no",
        "> independent architecture authority. Candidate, proposed, deferred, and",
        "> unresolved labels do not imply approval or executed verification.",
        "",
        "The diagrams deliberately omit RF implementation values, build instructions,",
        "operating procedures, and detailed recovered-item mapping. `CFG-REC` is shown",
        "only as a descriptive evidence configuration and does not inherit the proposed",
        "`CFG-REP`/`CFG-DOM` resource decomposition.",
        "",
        "## Configuration and context views",
        "",
    ]


def configuration_view(catalogs: dict[str, dict[str, Any]], index: dict[str, dict[str, Any]]) -> list[str]:
    body: list[str] = []
    for config in catalogs["architecture"]["configurations"]:
        extra = "reference evidence; [UNVERIFIED mapping]" if config["id"] == "CFG-REC" else "[PROPOSED]"
        if config["id"] == "CFG-SOS":
            extra = "outer system-of-systems context; [PROPOSED]"
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
        "Configuration derivation",
        "CFG-REC / CFG-REP / CFG-DOM / CFG-DIG / CFG-SOS",
        body,
        "Derivation denotes an architecture relationship, not exact inheritance, equivalence, or approval.",
    )


def boundary_view(index: dict[str, dict[str, Any]]) -> list[str]:
    body = [
        '    subgraph OUTER["C2 Ecosystem outer boundary - CFG-SOS proposed context"]',
        "        " + node(index, "OP-010", "independently managed human performer"),
        "        " + node(index, "OP-001", "independently managed external system"),
        "        " + node(index, "OP-003", "independently managed external system"),
        "        " + node(index, "OP-004", "proposed / TBD"),
        "        " + node(index, "OP-005", "proposed / TBD"),
        "        " + node(index, "OP-006", "proposed / TBD"),
        "        " + node(index, "OP-007", "external support performer"),
        "        " + node(index, "OP-008", "independent authority"),
        "        " + node(index, "OP-009", "proposed / TBD"),
        '        subgraph INNER["Relay UAS inner boundary - proposed for CFG-REP/CFG-DOM/CFG-DIG"]',
        "            " + node(index, "OP-002", "system under study"),
        "        end",
        "    end",
        '    OP_010 -->|"IX-001 platform command"| OP_002',
        '    OP_001 <-->|"IX-002 through IX-005 relay thread"| OP_002',
        '    OP_002 <-->|"mission traffic relationship"| OP_003',
        '    OP_007 <-->|"IX-010 / IFC-EXT-006 support"| OP_002',
        '    OP_008 -.->|"external authority; criteria unresolved"| OP_002',
        '    OP_001 -.->|"IX-006 / IX-007 proposed / TBD"| OP_004',
        '    OP_002 -.->|"relationship proposed / TBD"| OP_005',
        '    OP_002 -.->|"relationship proposed / TBD"| OP_006',
        '    OP_009 -.->|"support relationship proposed / TBD"| OP_002',
    ]
    return flow_diagram(
        "2",
        "Two-boundary context",
        "CFG-SOS outer context; CFG-REP / CFG-DOM / CFG-DIG inner constituent",
        body,
        "External constituents remain independently managed. Dashed relationships are proposed or TBD.",
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
        interface_id = realization.get(exchange_id, "TBD")
        label = f"{exchange_id} / {interface_id}<br/>{clean_label(exchange['flow_class'], 34)}"
        body.append(
            f'    {mermaid_key(exchange["from"])} -->|"{label}"| {mermaid_key(exchange["to"])}'
        )
    body.extend([
        '    OP_010 -.->|"platform command is separate from relayed mission traffic"| OP_001',
    ])
    return flow_diagram(
        "3",
        "Current three-node operational connectivity",
        "CFG-REP / CFG-DOM",
        body,
        "`IX-001` is independent Relay-UAS platform command. `IX-002` through `IX-005` are relayed mission traffic.",
    )


def resource_diagrams(catalogs: dict[str, dict[str, Any]], index: dict[str, dict[str, Any]]) -> list[str]:
    interfaces = interface_by_id(catalogs)
    lines: list[str] = ["## Relay-UAS resource views", ""]

    structure_ids = ["CMP-AFR-01", "CMP-AFR-02", "CMP-AFR-03", "CMP-AFR-04", "CMP-AFR-05", "CMP-MNT-01", "CMP-COM-01"]
    body = ["    " + node(index, item_id) for item_id in structure_ids]
    body.extend([
        '    CMP_AFR_01 -.->|"structural decomposition"| CMP_AFR_02',
        '    CMP_AFR_01 -.->|"structural decomposition"| CMP_AFR_03',
        '    CMP_AFR_01 -.->|"structural decomposition"| CMP_AFR_04',
        '    CMP_AFR_01 -.->|"hardware set"| CMP_AFR_05',
        '    CMP_AFR_04 -.->|"mount relationship [TBD]"| CMP_MNT_01',
        edge_for_interface(interfaces["IFC-INT-007"]),
    ])
    lines.extend(flow_diagram("4A", "Structure and payload mounting", "CFG-REP / CFG-DOM", body))

    power_ids = ["CMP-PWR-01", "CMP-PWR-02", "CMP-PWR-03", "CMP-PWR-04", "CMP-PRP-01", "CMP-PRP-02", "CMP-PRP-03", "CMP-AVN-01", "CMP-COM-01"]
    body = ["    " + node(index, item_id) for item_id in power_ids]
    body.extend([
        '    CMP_PWR_01 -.->|"source association; IFC not allocated"| CMP_PWR_02',
        '    CMP_PWR_04 -.->|"resource association; IFC not allocated"| CMP_PWR_02',
        edge_for_interface(interfaces["IFC-INT-001"]),
        edge_for_interface(interfaces["IFC-INT-002"]),
        edge_for_interface(interfaces["IFC-INT-003"], label_suffix="platform-to-payload"),
        edge_for_interface(interfaces["IFC-INT-006"]),
        '    CMP_PRP_02 -.->|"propulsion association"| CMP_PRP_01',
        '    CMP_PRP_01 -.->|"propulsion association"| CMP_PRP_03',
    ])
    lines.extend(flow_diagram("4B", "Power and propulsion connectivity", "CFG-REP / CFG-DOM", body))

    avionics_ids = ["OP-010", "CMP-AVN-01", "CMP-AVN-02", "CMP-AVN-03", "CMP-AVN-04", "CMP-PRP-02", "CMP-PWR-02"]
    body = ["    " + node(index, item_id) for item_id in avionics_ids]
    body.extend([
        edge_for_interface(interfaces["IFC-EXT-005"], label_suffix="separate platform command"),
        edge_for_interface(interfaces["IFC-INT-005"]),
        edge_for_interface(interfaces["IFC-INT-004"]),
        edge_for_interface(interfaces["IFC-INT-006"]),
        edge_for_interface(interfaces["IFC-INT-009"]),
        '    CMP_AVN_03 -.->|"navigation resource; IFC unresolved"| CMP_AVN_01',
    ])
    lines.extend(flow_diagram("4C", "Avionics and platform control connectivity", "CFG-REP / CFG-DOM", body))

    body = [
        "    " + node(index, "OP-001"),
        "    " + node(index, "OP-003"),
        "    " + node(index, "CMP-PWR-03"),
        "    " + node(index, "CMP-MNT-01"),
        '    subgraph PAYLOAD["Relay-payload black-box envelope"]',
        "        " + node(index, "CMP-COM-01"),
        "        " + node(index, "CMP-COM-02", "physical-resource envelope"),
        edge_for_interface(interfaces["IFC-INT-010"], indent="        ", label_suffix="payload-internal; no RF characteristics"),
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
        "Payload boundary and external traffic",
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

    body = [
        "    " + node(index, "CMP-AVN-01"),
        "    " + node(index, "CMP-COM-01", "future payload [PROPOSED]"),
        edge_for_interface(interfaces["IFC-INT-008"], label_suffix="future / proposed"),
        "    " + node(index, "IX-008", "future sensor-data exchange [TBD]"),
        '    IX_008 -.->|"realizing interface TBD - GAP-SOS-002"| CMP_COM_01',
    ]
    lines.extend(flow_diagram(
        "4F",
        "Future digital interface delta",
        "CFG-DIG / CFG-SOS only",
        body,
        "`IFC-INT-008` is not part of the current `CFG-REP`/`CFG-DOM` two-interface payload boundary.",
    ))
    return lines


def mode_view(index: dict[str, dict[str, Any]]) -> list[str]:
    body = [
        '    state "MODE-005 Ground Safe" as MODE_005',
        '    state "MODE-001 Transit" as MODE_001',
        '    state "MODE-002 Station Keeping" as MODE_002',
        '    state "MODE-003 Relay Degraded" as MODE_003',
        '    state "MODE-004 Return / Recovery" as MODE_004',
        "    [*] --> MODE_005",
        "    MODE_005 --> MODE_001: SCN-002 transition",
        "    MODE_001 --> MODE_002: SCN-002 station established",
        "    MODE_002 --> MODE_003: SCN-007 relay function degraded",
        "    MODE_003 --> MODE_004: SCN-007 recovery intent",
        "    MODE_002 --> MODE_004: SCN-008 termination or REQ-FUN-005",
        "    MODE_004 --> MODE_005: SCN-008 recovered",
        "    note right of MODE_003",
        "      Payload function degraded",
        "      Platform control may remain available",
        "      REQ-FUN-007 [PROPOSED]; evidence [DEFERRED]",
        "    end note",
    ]
    return state_diagram(
        "5",
        "Operating-mode state",
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
        "    Relay-->>Operator: IX-009 health/status (partial realization; GAP-SOS-003)",
        "    Note over Operator,Relay: SCN-002 architecture walkthrough; no procedure defined",
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
        "    Note over Ground,Remote: SCN-003 / SCN-004 logical relay only; external paths intentionally undefined",
    ]
    return sequence_diagram("7", "Bidirectional relay sequence", "CFG-REP / CFG-DOM", body)


def degradation_sequence(index: dict[str, dict[str, Any]]) -> list[str]:
    body = [
        '    participant Ground as OP-001 Ground control node',
        '    participant Payload as CMP-COM-01 Relay payload black box',
        '    participant Relay as OP-002 Relay UAS platform',
        '    participant Operator as OP-010 Platform operator',
        "    Payload--xGround: SCN-007 relay function loss or degradation",
        "    Relay-->>Operator: IX-009 health/status indication (partial)",
        "    Operator->>Relay: IX-001 / IFC-EXT-005 independent platform command",
        "    alt Payload lost; platform remains controllable",
        "        Note over Payload,Relay: MODE-003; CTL-004 / REQ-FUN-007 [PROPOSED]",
        "        Relay-->>Operator: transition intent toward MODE-004 Return / Recovery",
        "    else Platform control also impaired",
        "        Note over Relay,Operator: HAZ-001 / GAP-HAZ-001 - no modeled consequence-management behavior",
        "        Note over Ground,Operator: GAP-VER-001 - no executed recovery evidence",
        "    end",
    ]
    return sequence_diagram(
        "8",
        "Degradation and recovery sequence",
        "CFG-REP / CFG-DOM",
        body,
        "The second path terminates at explicit gaps; it does not invent a recovery behavior.",
    )


def lifecycle_view(index: dict[str, dict[str, Any]]) -> list[str]:
    scenario_ids = [f"SCN-{number:03d}" for number in range(1, 9)]
    body = ["    " + node(index, item_id, status_of(index, item_id)) for item_id in scenario_ids]
    body.extend([
        '    SCN_001 -->|"progression"| SCN_002',
        '    SCN_002 -->|"outbound thread"| SCN_003',
        '    SCN_002 -->|"return thread"| SCN_004',
        '    SCN_003 -->|"degraded"| SCN_007',
        '    SCN_004 -->|"degraded"| SCN_007',
        '    SCN_003 -->|"normal termination"| SCN_008',
        '    SCN_004 -->|"normal termination"| SCN_008',
        '    SCN_007 -->|"recovery intent"| SCN_008',
        '    SCN_001 -.->|"future CFG-SOS / GAP-SOS-001"| SCN_005',
        '    SCN_001 -.->|"future CFG-DIG / CFG-SOS / GAP-SOS-002"| SCN_006',
    ])
    return flow_diagram(
        "9",
        "Scenario lifecycle",
        "CFG-REP / CFG-DOM current; CFG-DIG / CFG-SOS proposed branches",
        body,
        "Dashed branches are future proposals without complete activity, interface, requirement, hazard, or verification allocation.",
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
                emit(verification_id, "[DEFERRED] or [UNVERIFIED]")
                body.append(f'    {mermaid_key(requirement_id)} -->|"verification allocation"| {mermaid_key(verification_id)}')
                emit("GAP-VER-001", "[UNVERIFIED]")
                body.append(f'    {mermaid_key(verification_id)} -.->|"execution evidence missing"| GAP_VER_001')
    return flow_diagram(
        "10",
        "Hazard-control-requirement-verification",
        "CFG-REP / CFG-DOM",
        body,
        "Verification nodes are candidate or deferred methods. They are not executed evidence and provide no approval or safety credit.",
    )


def trace_view(index: dict[str, dict[str, Any]]) -> list[str]:
    ids = [
        "NEED-001", "CAP-001", "SCN-003", "OA-004", "IX-002",
        "FUN-REL-01", "CMP-COM-01", "IFC-EXT-001",
        "REQ-FUN-001", "VER-001", "GAP-VER-001",
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
        '    IFC_EXT_001 -->|"allocated requirement"| REQ_FUN_001',
        '    REQ_FUN_001 -->|"verification allocation"| VER_001',
        '    VER_001 -.->|"execution evidence unresolved"| GAP_VER_001',
    ])
    return flow_diagram(
        "11",
        "End-to-end architecture trace",
        "CFG-REP / CFG-DOM",
        body,
        "The thread is readable end to end, but candidate relationships and evidence gaps remain visible.",
    )


def governance_view(index: dict[str, dict[str, Any]]) -> list[str]:
    body = [
        "    " + node(index, "SRC-INT-001", "registered source"),
        "    " + node(index, "EVD-002", "registered evidence record"),
        "    " + node(index, "CLM-REC-001", "source-supported claim"),
        "    " + node(index, "CFG-REC", "descriptive evidence configuration"),
        "    " + node(index, "CLM-REC-005", "generic mapping not demonstrated"),
        "    " + node(index, "GAP-REC-001", "unresolved mapping gap"),
        "    " + node(index, "DEC-002", "proposed owner decision"),
        "    " + node(index, "GAP-STD-001", "unresolved standards decision"),
        '    BASELINE["Baseline Candidate - Not Approved<br/>model-valid may still be gapped"]',
        '    SRC_INT_001 -->|"registered as"| EVD_002',
        '    EVD_002 -->|"supports; does not approve"| CLM_REC_001',
        '    CLM_REC_001 -->|"applicable to evidence configuration"| CFG_REC',
        '    CLM_REC_005 -->|"prevents silent proposed-resource inheritance"| CFG_REC',
        '    CFG_REC -.->|"mapping unresolved"| GAP_REC_001',
        '    DEC_002 -.->|"owner review required"| GAP_STD_001',
        '    GAP_REC_001 -->|"gap remains visible"| BASELINE',
        '    GAP_STD_001 -->|"gap remains visible"| BASELINE',
    ]
    return flow_diagram(
        "12",
        "Evidence and approval governance",
        "Project governance; CFG-REC evidence semantics; all configurations remain not approved",
        body,
        "Evidence supports claims; it does not approve architecture. Proposed decisions require explicit owner action.",
    )


def interface_inventory(catalogs: dict[str, dict[str, Any]]) -> list[str]:
    lines = [
        "## Generated interface inventory",
        "",
        "This inventory is generated directly from `model/architecture.yaml`. Empty",
        "verification cells are explicit gaps, not evidence of completion.",
        "",
        "| ID | Endpoints | Direction | Flow class | Configurations | Maturity | Verification | Unknown attributes |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for interface in catalogs["architecture"]["interfaces"]:
        verification = ", ".join(interface.get("verification_ids", [])) or "None - explicit gap"
        unknowns = "; ".join(interface.get("unknown_attributes", [])) or "None recorded"
        maturity = f"{interface.get('evidence_basis')} / {interface.get('decision_status')}"
        row = [
            interface["id"],
            f"{interface['endpoint_a']} to {interface['endpoint_b']}",
            interface["direction"],
            interface["flow_class"],
            ", ".join(interface["applicable_configurations"]),
            maturity,
            verification,
            unknowns,
        ]
        lines.append("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |")
    lines.extend(["", "## Validation notes", ""])
    lines.extend([
        f"- Optional syntax validation expects Mermaid CLI `mmdc` {PINNED_MERMAID_CLI} when installed locally.",
        "- Absence of Node.js or the pinned CLI does not invalidate standard-library catalog validation.",
        "- No generated SVG or PNG is required; GitHub-rendered Markdown is the primary artifact.",
        "",
    ])
    return lines


def render(catalogs: dict[str, dict[str, Any]]) -> str:
    index = build_index(catalogs)
    lines = generated_header()
    lines.extend(configuration_view(catalogs, index))
    lines.extend(boundary_view(index))
    lines.extend(operational_connectivity_view(catalogs, index))
    lines.extend(resource_diagrams(catalogs, index))
    lines.extend(["## Behavioral views", ""])
    lines.extend(mode_view(index))
    lines.extend(launch_sequence(index))
    lines.extend(relay_sequence(index))
    lines.extend(degradation_sequence(index))
    lines.extend(lifecycle_view(index))
    lines.extend(["## Assurance and traceability views", ""])
    lines.extend(hazard_view(catalogs, index))
    lines.extend(trace_view(index))
    lines.extend(governance_view(index))
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
            f"MERMAID-PARSER: skipped because unavailable "
            f"(pinned mmdc {PINNED_MERMAID_CLI} is not installed locally)"
        )
        return 0
    version = subprocess.run(
        [executable, "--version"], capture_output=True, text=True, check=False
    )
    reported = (version.stdout or version.stderr).strip()
    if PINNED_MERMAID_CLI not in reported:
        print(
            f"MERMAID-PARSER: skipped because available mmdc version is {reported!r}; "
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
        print("MERMAID-PARSER: failed")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"MERMAID-PARSER: passed with pinned mmdc {PINNED_MERMAID_CLI}")
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
            print("GENERATED-VIEWS-CURRENT: reports/architecture-views.md")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(expected, encoding="utf-8", newline="\n")
        print("GENERATED-VIEWS-WRITTEN: reports/architecture-views.md")

    if args.validate_syntax:
        result = max(result, validate_mermaid_syntax(expected))
    return result


if __name__ == "__main__":
    sys.exit(main())
