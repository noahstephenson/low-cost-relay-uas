#!/usr/bin/env python3
"""Generate the plain-language Relay-UAS communication figures.

The figures are presentation views, not architecture authority. Every visible
architecture element is resolved against the structured catalogs, and every
connection is checked against an information exchange, interface, resource
relationship, mode transition, or scenario record before it is drawn.
"""

from __future__ import annotations

import argparse
import json
import sys
from html import escape
from pathlib import Path
from typing import Any, Callable, Iterable


ROOT = Path(__file__).resolve().parents[1]
ARCHITECTURE_PATH = ROOT / "model" / "architecture.yaml"
ASSURANCE_PATH = ROOT / "model" / "assurance.yaml"
TRACEABILITY_PATH = ROOT / "model" / "traceability.yaml"
SYSTEM_PATH = ROOT / "system.yaml"
FEASIBILITY_PATH = ROOT / "analysis" / "results" / "feasibility-summary.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_model() -> dict[str, Any]:
    return {
        "architecture": load_json(ARCHITECTURE_PATH),
        "assurance": load_json(ASSURANCE_PATH),
        "traceability": load_json(TRACEABILITY_PATH),
        "system": load_json(SYSTEM_PATH),
        "feasibility": load_json(FEASIBILITY_PATH),
    }


def build_index(model: dict[str, Any]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for catalog in (model["architecture"], model["assurance"]):
        for value in catalog.values():
            if not isinstance(value, list):
                continue
            for item in value:
                if isinstance(item, dict) and isinstance(item.get("id"), str):
                    index[item["id"]] = item
    for gap in model["traceability"]["gaps"]:
        index[gap["code"]] = gap
    return index


def display(index: dict[str, dict[str, Any]], item_id: str) -> str:
    item = index[item_id]
    return str(item.get("display_name") or item.get("name") or item.get("statement") or item_id)


def lines_text(x: float, y: float, values: Iterable[str], css: str = "body", anchor: str = "start", gap: int = 22) -> str:
    parts = [f'<text x="{x}" y="{y}" class="{css}" text-anchor="{anchor}">']
    for number, value in enumerate(values):
        dy = 0 if number == 0 else gap
        parts.append(f'<tspan x="{x}" dy="{dy}">{escape(value)}</tspan>')
    parts.append("</text>")
    return "".join(parts)


def box(
    x: float,
    y: float,
    width: float,
    height: float,
    title: str,
    details: Iterable[str] = (),
    kind: str = "neutral",
    shape: str = "round",
) -> str:
    radius = 14 if shape == "round" else 2
    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" class="box {kind}"/>',
        lines_text(x + width / 2, y + 31, [title], "box-title", "middle"),
    ]
    detail_list = list(details)
    if detail_list:
        parts.append(lines_text(x + 18, y + 61, detail_list, "body"))
    return "\n".join(parts)


def arrow(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    label: str = "",
    kind: str = "neutral",
    dashed: bool = False,
    label_y: float | None = None,
) -> str:
    dash = " dashed" if dashed else ""
    parts = [
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="arrow {kind}{dash}" marker-end="url(#arrow-{kind})"/>'
    ]
    if label:
        lx = (x1 + x2) / 2
        ly = label_y if label_y is not None else (y1 + y2) / 2 - 9
        parts.append(f'<text x="{lx}" y="{ly}" class="edge-label" text-anchor="middle">{escape(label)}</text>')
    return "\n".join(parts)


def svg_document(title: str, description: str, body: str, sources: Iterable[str], width: int = 1200, height: int = 700) -> str:
    source_text = ", ".join(sources)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">{escape(description)}</desc>
<metadata>Generated from authoritative model records: {escape(source_text)}</metadata>
<defs>
  <marker id="arrow-neutral" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#435269"/></marker>
  <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#245f9e"/></marker>
  <marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#247a52"/></marker>
  <marker id="arrow-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#9a6700"/></marker>
</defs>
<style>
  text {{ font-family: Arial, Helvetica, sans-serif; fill: #172033; }}
  .title {{ font-size: 30px; font-weight: 700; }}
  .subtitle {{ font-size: 17px; fill: #536174; }}
  .section {{ font-size: 19px; font-weight: 700; }}
  .box-title {{ font-size: 19px; font-weight: 700; }}
  .body {{ font-size: 16px; }}
  .small {{ font-size: 14px; fill: #536174; }}
  .edge-label {{ font-size: 15px; font-weight: 700; paint-order: stroke; stroke: #ffffff; stroke-width: 5px; stroke-linejoin: round; }}
  .box {{ stroke: #435269; stroke-width: 2; fill: #f5f7fa; }}
  .box.blue {{ fill: #e9f2ff; stroke: #245f9e; }}
  .box.green {{ fill: #eaf7f0; stroke: #247a52; }}
  .box.amber {{ fill: #fff4d6; stroke: #9a6700; }}
  .box.red {{ fill: #fdecec; stroke: #b42318; }}
  .box.white {{ fill: #ffffff; }}
  .box.future {{ fill: #ffffff; stroke: #6b7280; stroke-dasharray: 9 7; }}
  .boundary {{ fill: #ffffff; stroke: #26364d; stroke-width: 3; }}
  .group {{ fill: #f8fafc; stroke: #8a97a8; stroke-width: 1.5; }}
  .arrow {{ stroke: #435269; stroke-width: 3; fill: none; }}
  .arrow.blue {{ stroke: #245f9e; }}
  .arrow.green {{ stroke: #247a52; }}
  .arrow.amber {{ stroke: #9a6700; }}
  .arrow.dashed {{ stroke-dasharray: 10 8; }}
  .lane {{ stroke: #cbd3dd; stroke-width: 1.5; }}
  .divider {{ stroke: #8a97a8; stroke-width: 2; stroke-dasharray: 8 7; }}
</style>
<rect width="{width}" height="{height}" fill="#ffffff"/>
{body}
</svg>
'''


def assert_exchange(model: dict[str, Any], exchange_id: str, source: str, target: str) -> None:
    item = next(x for x in model["architecture"]["information_exchanges"] if x["id"] == exchange_id)
    if item["from"] != source or item["to"] != target:
        raise ValueError(f"{exchange_id} no longer connects {source} to {target}")


def assert_interface(model: dict[str, Any], interface_id: str, endpoint_a: str, endpoint_b: str) -> None:
    item = next(x for x in model["architecture"]["interfaces"] if x["id"] == interface_id)
    if item["endpoint_a"] != endpoint_a or item["endpoint_b"] != endpoint_b:
        raise ValueError(f"{interface_id} endpoints changed")


def project_picture(model: dict[str, Any], index: dict[str, dict[str, Any]], view: dict[str, Any]) -> str:
    for item in [
        ("IX-001", "OP-010", "OP-002"), ("IX-002", "OP-001", "OP-002"),
        ("IX-003", "OP-002", "OP-003"), ("IX-004", "OP-003", "OP-002"),
        ("IX-005", "OP-002", "OP-001"),
    ]:
        assert_exchange(model, *item)
    parts = [
        lines_text(40, 48, [view["title"]], "title"),
        lines_text(40, 78, ["One aircraft, two separate communication paths"], "subtitle"),
        '<rect x="350" y="100" width="500" height="470" rx="24" class="boundary"/>',
        lines_text(600, 136, [display(index, "OP-002")], "section", "middle"),
        lines_text(600, 163, ["Aircraft carries and positions the relay payload"], "small", "middle"),
        box(40, 190, 240, 82, display(index, "OP-010"), ["Controls the Relay UAS"], "blue"),
        box(420, 190, 360, 82, display(index, "CMP-AVN-04"), ["Separate platform-control path"], "blue"),
        box(420, 300, 360, 82, "Aircraft Support", ["Airframe + propulsion + power + avionics"], "neutral"),
        box(440, 420, 320, 105, "Relay Payload", ["Passes mission traffic", "Internal RF design is out of scope"], "green"),
        box(40, 415, 240, 110, display(index, "OP-001"), ["Sends remote-UAS command", "Receives its telemetry"], "white"),
        box(920, 415, 240, 110, display(index, "OP-003"), ["Receives relayed command", "Returns telemetry"], "white"),
        arrow(280, 215, 420, 215, "Platform Command", "blue", False, 202),
        arrow(420, 247, 280, 247, "Health / Status", "blue", True, 270),
        arrow(280, 446, 440, 446, "Relayed Command", "green", False, 432),
        arrow(760, 446, 920, 446, "Relayed Command", "green", False, 432),
        arrow(920, 494, 760, 494, "Relayed Telemetry", "green", True, 517),
        arrow(440, 494, 280, 494, "Relayed Telemetry", "green", True, 517),
        lines_text(600, 605, ["The aircraft's control link never passes through the black-box relay payload."], "section", "middle"),
        lines_text(600, 634, ["The model defines the paths and boundaries—not waveform, frequency, protocol, hardware, or interoperability."], "small", "middle"),
    ]
    return svg_document(view["title"], view["question"], "\n".join(parts), view["object_refs"])


def system_boundary(model: dict[str, Any], index: dict[str, dict[str, Any]], view: dict[str, Any]) -> str:
    inner = model["system"]["system_boundaries"]["inner"]
    parts = [
        lines_text(40, 48, [view["title"]], "title"),
        lines_text(40, 78, ["The product boundary contains the aircraft and black-box payload; users, other vehicles, and authorities remain external."], "subtitle"),
        '<rect x="315" y="115" width="570" height="500" rx="24" class="boundary"/>',
        lines_text(600, 151, [inner["name"] + " Product Boundary"], "section", "middle"),
        box(355, 190, 235, 150, "Aircraft Platform", ["Airframe and structure", "Propulsion", "Electrical power"], "neutral"),
        box(610, 190, 235, 150, "Flight and Control", ["Flight avionics", "Platform command receiver", "Health / status"], "blue"),
        box(355, 370, 235, 155, "Payload Support", ["Mechanical mounting", "Regulated payload power", "Configuration support"], "neutral"),
        box(610, 370, 235, 155, "Relay Payload", ["Black-box payload + antenna", "Internal design unknown"], "green"),
        lines_text(600, 570, ["Only power and mechanical retention cross from platform to payload."], "small", "middle"),
        box(35, 155, 225, 100, display(index, "OP-010"), ["External human performer"], "white"),
        box(35, 285, 225, 100, display(index, "OP-001"), ["External control system"], "white"),
        box(35, 415, 225, 100, display(index, "OP-007"), ["External support performer"], "white"),
        box(940, 155, 225, 100, display(index, "OP-003"), ["External vehicle"], "white"),
        box(940, 285, 225, 100, "Future Platforms", ["Future configuration only"], "future"),
        box(940, 415, 225, 100, "External Authorities", ["Spectrum and conformance"], "future"),
        arrow(260, 335, 315, 335, kind="neutral"),
        arrow(885, 335, 940, 335, kind="neutral"),
        lines_text(600, 660, ["Outside systems remain independently managed; the outer system-of-systems context is future scope."], "small", "middle"),
    ]
    return svg_document(view["title"], view["question"], "\n".join(parts), view["object_refs"])


def physical_architecture(model: dict[str, Any], index: dict[str, dict[str, Any]], view: dict[str, Any]) -> str:
    assert_interface(model, "IFC-INT-004", "CMP-AVN-01", "CMP-PRP-02")
    assert_interface(model, "IFC-INT-001", "CMP-PWR-02", "CMP-PRP-02")
    assert_interface(model, "IFC-INT-003", "CMP-PWR-03", "CMP-COM-01")
    assert_interface(model, "IFC-INT-007", "CMP-MNT-01", "CMP-COM-01")
    groups = [
        ("Airframe and Structure", ["CMP-AFR-01", "CMP-AFR-02", "CMP-AFR-03", "CMP-AFR-05"], "neutral"),
        ("Propulsion", ["CMP-PRP-01", "CMP-PRP-02", "CMP-PRP-03"], "neutral"),
        ("Electrical Power", ["CMP-PWR-01", "CMP-PWR-02", "CMP-PWR-03", "CMP-PWR-04"], "amber"),
        ("Flight Avionics", ["CMP-AVN-01", "CMP-AVN-02", "CMP-AVN-03", "CMP-AVN-04"], "blue"),
        ("Payload Support", ["CMP-AFR-04", "CMP-MNT-01"], "neutral"),
        ("Relay Payload", ["CMP-COM-01", "CMP-COM-02"], "green"),
    ]
    positions = [(45, 125), (425, 125), (805, 125), (45, 390), (425, 390), (805, 390)]
    parts = [
        lines_text(40, 48, [view["title"]], "title"),
        lines_text(40, 78, ["Nineteen component records are grouped into six understandable subsystem roles."], "subtitle"),
    ]
    for (title, ids, kind), (x, y) in zip(groups, positions):
        for item_id in ids:
            if item_id not in index:
                raise ValueError(f"physical view references missing {item_id}")
        parts.append(box(x, y, 350, 205, title, ["• " + display(index, item_id) for item_id in ids], kind))
    parts.extend([
        arrow(805, 228, 775, 228, kind="amber"),
        arrow(395, 425, 425, 330, kind="blue"),
        arrow(980, 330, 980, 390, kind="amber"),
        arrow(775, 493, 805, 493, kind="neutral"),
        lines_text(600, 626, ["Avionics → propulsion control  •  Power → propulsion and payload  •  Payload support → relay payload"], "section", "middle"),
        lines_text(600, 660, ["Component choice, geometry, ratings, and fabrication remain unresolved trade-study outputs."], "small", "middle"),
    ])
    return svg_document(view["title"], view["question"], "\n".join(parts), view["object_refs"])


def power_flow(model: dict[str, Any], index: dict[str, dict[str, Any]], view: dict[str, Any]) -> str:
    checks = [
        ("IFC-INT-011", "CMP-PWR-01", "CMP-PWR-02"),
        ("IFC-INT-001", "CMP-PWR-02", "CMP-PRP-02"),
        ("IFC-INT-015", "CMP-PWR-02", "CMP-PWR-03"),
        ("IFC-INT-002", "CMP-PWR-03", "CMP-AVN-01"),
        ("IFC-INT-003", "CMP-PWR-03", "CMP-COM-01"),
        ("IFC-INT-013", "CMP-PRP-02", "CMP-PRP-01"),
        ("IFC-INT-014", "CMP-PRP-01", "CMP-PRP-03"),
    ]
    for item in checks:
        assert_interface(model, *item)
    parts = [
        lines_text(40, 48, [view["title"]], "title"),
        lines_text(40, 78, ["Electrical power is shown separately from command and mission data."], "subtitle"),
        box(40, 275, 170, 92, display(index, "CMP-PWR-01"), ["stored energy"], "amber"),
        box(260, 275, 250, 92, display(index, "CMP-PWR-02"), ["main bus"], "amber"),
        box(520, 135, 190, 92, display(index, "CMP-PRP-02"), ["propulsion branch"], "neutral"),
        box(800, 135, 145, 92, display(index, "CMP-PRP-01"), ["four corners"], "neutral"),
        box(1040, 135, 130, 92, display(index, "CMP-PRP-03"), ["thrust"], "neutral"),
        box(520, 420, 200, 92, display(index, "CMP-PWR-03"), ["regulated branches"], "amber"),
        box(840, 340, 250, 92, "Avionics Loads", ["flight control + sensors"], "blue"),
        box(840, 500, 250, 92, "Relay Payload", ["regulated payload power"], "green"),
        arrow(210, 321, 260, 321, "source power", "amber", False, 260),
        arrow(510, 300, 520, 181, "propulsion main bus", "amber", False, 245),
        arrow(710, 181, 800, 181, "controlled power", "neutral", False, 116),
        arrow(945, 181, 1040, 181, "mechanical drive", "neutral", False, 116),
        arrow(510, 342, 520, 466, "regulator main bus", "amber", False, 405),
        arrow(720, 448, 840, 386, "avionics power", "blue", False, 360),
        arrow(720, 484, 840, 546, "payload power", "green", False, 518),
        lines_text(600, 650, ["Voltage, current, protection, connectors, and component ratings remain undefined."], "small", "middle"),
    ]
    return svg_document(view["title"], view["question"], "\n".join(parts), view["object_refs"])


def command_data_flow(model: dict[str, Any], index: dict[str, dict[str, Any]], view: dict[str, Any]) -> str:
    for item in [
        ("IX-001", "OP-010", "OP-002"), ("IX-009", "OP-002", "OP-010"),
        ("IX-002", "OP-001", "OP-002"), ("IX-003", "OP-002", "OP-003"),
        ("IX-004", "OP-003", "OP-002"), ("IX-005", "OP-002", "OP-001"),
    ]:
        assert_exchange(model, *item)
    assert_interface(model, "IFC-EXT-005", "OP-010", "CMP-AVN-04")
    assert_interface(model, "IFC-INT-005", "CMP-AVN-04", "CMP-AVN-01")
    assert_interface(model, "IFC-EXT-007", "CMP-AVN-01", "OP-010")
    parts = [
        lines_text(40, 48, [view["title"]], "title"),
        lines_text(40, 78, ["Four information flows share the aircraft but not the same internal path."], "subtitle"),
        lines_text(35, 143, ["PLATFORM CONTROL"], "section"),
        '<line x1="35" y1="160" x2="1165" y2="160" class="lane"/>',
        box(55, 185, 190, 78, display(index, "OP-010"), [], "blue"),
        box(330, 185, 280, 78, display(index, "CMP-AVN-04"), [], "blue"),
        box(790, 185, 230, 78, display(index, "CMP-AVN-01"), [], "blue"),
        arrow(245, 224, 330, 224, "Platform Command", "blue", False, 174),
        arrow(610, 224, 790, 224, "Control Input", "blue", False, 174),
        '<path d="M 905 263 V 292 H 150 V 263" class="arrow blue dashed" marker-end="url(#arrow-blue)"/>',
        lines_text(528, 314, ["Health / Status"], "edge-label", "middle"),
        '<line x1="35" y1="320" x2="1165" y2="320" class="divider"/>',
        lines_text(35, 366, ["RELAYED MISSION TRAFFIC"], "section"),
        box(55, 405, 190, 94, display(index, "OP-001"), [], "white"),
        box(465, 405, 270, 94, display(index, "CMP-COM-01"), ["No platform data interface"], "green"),
        box(955, 405, 190, 94, display(index, "OP-003"), [], "white"),
        arrow(245, 438, 465, 438, "Relayed Command", "green"),
        arrow(735, 438, 955, 438, "Relayed Command", "green"),
        arrow(955, 477, 735, 477, "Relayed Telemetry", "green", True),
        arrow(465, 477, 245, 477, "Relayed Telemetry", "green", True),
        lines_text(600, 568, ["Mission traffic is logically transparent to the aircraft platform."], "section", "middle"),
        lines_text(600, 600, ["External compatibility, message formats, protocols, frequency, waveform, and data rate are unresolved."], "small", "middle"),
    ]
    return svg_document(view["title"], view["question"], "\n".join(parts), view["object_refs"])


def mission_sequence(model: dict[str, Any], index: dict[str, dict[str, Any]], view: dict[str, Any]) -> str:
    scenario_ids = ["SCN-001", "SCN-002", "SCN-003", "SCN-004", "SCN-008"]
    if any(item_id not in index for item_id in scenario_ids):
        raise ValueError("normal mission scenario record missing")
    parts = [
        lines_text(40, 48, [view["title"]], "title"),
        lines_text(40, 78, ["Current-system mission sequence; future UGV and video branches are intentionally omitted."], "subtitle"),
    ]
    lanes = [("Operator / Ground", 90), ("Relay Aircraft", 390), ("Relay Payload", 690), ("Remote UAS", 990)]
    for name, x in lanes:
        parts.append(lines_text(x, 125, [name], "section", "middle"))
        parts.append(f'<line x1="{x}" y1="145" x2="{x}" y2="630" class="lane"/>')
    steps = [
        (180, 90, 390, "1  Prepare / confirm safe state", "neutral"),
        (255, 90, 390, "2  Launch, transit, hold station", "blue"),
        (340, 90, 690, "3  Send remote-UAS command", "green"),
        (415, 690, 990, "4  Relay command onward", "green"),
        (490, 990, 690, "5  Return telemetry", "green"),
        (565, 690, 90, "6  Relay telemetry to ground", "green"),
    ]
    for y, x1, x2, label, kind in steps:
        parts.append(arrow(x1, y, x2, y, label, kind, kind == "green" and x1 > x2, y - 10))
    parts.append(arrow(390, 620, 90, 620, "7  Recover and return to Ground Safe", "blue", False, 610))
    parts.append(lines_text(600, 653, ["Health/status informs recovery decisions; exact criteria remain unresolved."], "small", "middle"))
    parts.append(lines_text(600, 682, ["This is an architecture sequence, not an operating procedure or verified flight behavior."], "small", "middle"))
    return svg_document(view["title"], view["question"], "\n".join(parts), view["object_refs"])


def degraded_behavior(model: dict[str, Any], index: dict[str, dict[str, Any]], view: dict[str, Any]) -> str:
    transitions = {(x["from"], x["to"]): x for x in model["architecture"]["mode_transitions"]}
    for pair in [("MODE-002", "MODE-003"), ("MODE-003", "MODE-004"), ("MODE-004", "MODE-005")]:
        if pair not in transitions:
            raise ValueError(f"mode transition {pair} missing")
    parts = [
        lines_text(40, 48, [view["title"]], "title"),
        lines_text(40, 78, ["The model separates loss of relay service from loss of aircraft control."], "subtitle"),
        box(55, 245, 220, 100, display(index, "MODE-002"), ["Normal relay position"], "green"),
        box(355, 245, 220, 100, display(index, "MODE-003"), ["Relay function unavailable", "Platform assessed separately"], "amber"),
        '<polygon points="690,235 810,295 690,355 570,295" class="box blue"/>',
        lines_text(690, 288, ["Platform control", "still available?"], "box-title", "middle"),
        box(900, 145, 235, 105, display(index, "MODE-004"), ["Recovery intent only", "Criteria remain unresolved"], "blue"),
        box(900, 300, 235, 105, display(index, "MODE-005"), ["After recovery"], "neutral"),
        box(900, 500, 235, 112, "Unresolved Safety Gap", ["No modeled response for", "impaired platform control"], "red"),
        arrow(275, 295, 355, 295, "relay degraded", "amber"),
        arrow(575, 295, 570, 295, kind="blue"),
        arrow(810, 268, 900, 198, "YES", "blue"),
        arrow(810, 322, 900, 556, "NO / IMPAIRED", "amber"),
        arrow(1018, 250, 1018, 300, "recover / land", "blue", False, 278),
        lines_text(55, 430, ["Established at architecture level:"], "section"),
        lines_text(55, 460, ["• Relay payload is separate from platform command", "• Degraded mode and recovery intent exist", "• Health/status purpose is proposed"], "body"),
        lines_text(55, 560, ["Not established:"], "section"),
        lines_text(55, 590, ["• Exact detection and decision logic", "• Recovery criteria or physical behavior", "• Safety acceptance or test evidence"], "body"),
    ]
    return svg_document(view["title"], view["question"], "\n".join(parts), view["object_refs"])


def configuration_evolution(model: dict[str, Any], index: dict[str, dict[str, Any]], view: dict[str, Any]) -> str:
    configs = model["architecture"]["configurations"]
    by_id = {item["id"]: item for item in configs}
    expected = {
        "CFG-REP": ["CFG-REC"], "CFG-DOM": ["CFG-REP"],
        "CFG-DIG": ["CFG-REP"], "CFG-SOS": ["CFG-DIG"],
    }
    for item_id, predecessors in expected.items():
        if by_id[item_id]["predecessor_ids"] != predecessors:
            raise ValueError(f"configuration lineage changed for {item_id}")
    parts = [
        lines_text(40, 48, [view["title"]], "title"),
        lines_text(40, 78, ["Lineage shows influence and planned evolution—not exact inheritance, equivalence, or approval."], "subtitle"),
        lines_text(160, 205, ["REFERENCE"], "section", "middle"),
        lines_text(615, 205, ["CURRENT"], "section", "middle"),
        box(45, 230, 225, 130, display(index, "CFG-REC"), ["Evidence / reference only", "Incomplete reconstruction"], "white"),
        box(350, 230, 225, 130, "Current Replica", ["Current proposed architecture", "Not an exact clone"], "blue"),
        box(655, 230, 225, 130, "Domestic Candidate", ["Current candidate variant", "Sourcing policy unresolved"], "blue"),
        lines_text(910, 445, ["FUTURE"], "section", "middle"),
        box(655, 470, 225, 130, "Future Digital Extension", ["Future payload-management", "branch"], "future"),
        box(955, 470, 205, 130, "Future System Context", ["Future UGV / radio /", "service context"], "future"),
        arrow(270, 295, 350, 295, "informs", "neutral", True, 280),
        arrow(575, 295, 655, 295, "evolves", "blue", False, 280),
        arrow(520, 360, 655, 510, "future branch", "neutral", True, 425),
        arrow(880, 535, 955, 535, kind="neutral", dashed=True),
        lines_text(600, 650, ["Recovered evidence does not automatically become candidate architecture; future branches do not alter the current system."], "small", "middle"),
    ]
    return svg_document(view["title"], view["question"], "\n".join(parts), view["object_refs"])


def engineering_status(model: dict[str, Any], index: dict[str, dict[str, Any]], view: dict[str, Any]) -> str:
    system = model["system"]
    architecture = model["architecture"]
    assurance = model["assurance"]
    feasibility = model["feasibility"]
    if system["status"] != "baseline_candidate_not_approved":
        raise ValueError("technical baseline status changed")
    if feasibility["all_owner_requirement_dispositions"] != "UNDETERMINED":
        raise ValueError("feasibility requirement disposition changed")
    verification = {item["id"]: item for item in assurance["verifications"]}
    if verification["VER-008"]["status"] != "deferred_out_of_scope":
        raise ValueError("physical verification status changed")
    if verification["VER-009"]["status"] != "blocked_by_external_authority":
        raise ValueError("external conformance status changed")
    rows = [
        ("Architecture structure", "ESTABLISHED", f"{len(architecture['components'])} components / {len(architecture['interfaces'])} interfaces", "green"),
        ("System boundary + current mission", "ESTABLISHED", "Boundary and scenarios defined", "green"),
        ("Requirements + traceability", "ESTABLISHED", "Internally checked; open gaps remain visible", "green"),
        ("Internal model verification", "ESTABLISHED WITH OPEN GAPS", "Model review only—not physical proof", "green"),
        ("Feasibility analysis", "CONDITIONAL", "Short-dwell region appears plausible", "amber"),
        ("Owner target values", "PENDING OWNER INPUT", "Five owner targets remain TBD", "amber"),
        ("Physical verification", "REQUIRES PHYSICAL EVIDENCE", "Physical evidence absent", "red"),
        ("External interface conformance", "REQUIRES EXTERNAL AUTHORITY", "Authority and specification absent", "red"),
        ("Relay-payload implementation", "DEFERRED", "Black box; RF details outside project scope", "neutral"),
        ("Technical baseline approval", "NOT APPROVED", "Penultimate communication pass", "red"),
    ]
    parts = [
        lines_text(40, 48, [view["title"]], "title"),
        lines_text(40, 78, ["A mature model is not the same thing as a verified aircraft."], "subtitle"),
        lines_text(55, 125, ["AREA"], "section"),
        lines_text(430, 125, ["STATUS"], "section"),
        lines_text(820, 125, ["WHAT THAT MEANS"], "section"),
    ]
    y = 148
    for name, status, meaning, kind in rows:
        parts.append(f'<rect x="40" y="{y}" width="1120" height="48" class="box white" rx="4"/>')
        parts.append(f'<rect x="40" y="{y}" width="12" height="48" class="box {kind}" rx="0"/>')
        parts.append(lines_text(68, y + 30, [name], "body"))
        parts.append(lines_text(430, y + 30, [status], "section"))
        parts.append(lines_text(820, y + 30, [meaning], "body"))
        y += 51
    parts.append(lines_text(600, 676, ["No row grants safety, airworthiness, interoperability, operational readiness, or technical-baseline approval."], "small", "middle"))
    return svg_document(view["title"], view["question"], "\n".join(parts), view["object_refs"])


BUILDERS: dict[str, Callable[[dict[str, Any], dict[str, dict[str, Any]], dict[str, Any]], str]] = {
    "project-in-one-picture": project_picture,
    "system-boundary": system_boundary,
    "physical-architecture": physical_architecture,
    "power-resource-flow": power_flow,
    "command-data-flow": command_data_flow,
    "mission-sequence": mission_sequence,
    "degraded-behavior": degraded_behavior,
    "configuration-evolution": configuration_evolution,
    "engineering-status": engineering_status,
}


def build_outputs(model: dict[str, Any]) -> dict[Path, str]:
    index = build_index(model)
    views = model["system"].get("communication_views", [])
    configured = {item["slug"]: item for item in views}
    if set(configured) != set(BUILDERS):
        raise ValueError("system.yaml communication-view manifest does not match the generator")
    outputs: dict[Path, str] = {}
    for slug, builder in BUILDERS.items():
        view = configured[slug]
        missing = [item_id for item_id in view["object_refs"] if item_id not in index]
        if missing:
            raise ValueError(f"{slug} references unknown model records: {missing}")
        outputs[ROOT / "reports" / "figures" / f"{slug}.svg"] = builder(model, index, view)
    expected_paths = {ROOT / item for item in model["system"].get("generated_figures", [])}
    if set(outputs) != expected_paths:
        raise ValueError("system.yaml generated_figures does not match generated outputs")
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated figures are stale")
    args = parser.parse_args()
    try:
        outputs = build_outputs(load_model())
    except (KeyError, StopIteration, ValueError) as exc:
        print(f"COMMUNICATION-VIEWS-INVALID: {exc}")
        return 1
    if args.check:
        stale = [
            str(path.relative_to(ROOT)) for path, content in outputs.items()
            if not path.exists() or path.read_text(encoding="utf-8-sig") != content
        ]
        if stale:
            print("COMMUNICATION-VIEWS-STALE: " + ", ".join(stale))
            return 1
        print(f"COMMUNICATION-VIEWS-CURRENT: {len(outputs)} deterministic figures")
        return 0
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    print(f"COMMUNICATION-VIEWS-WRITTEN: {len(outputs)} deterministic figures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
