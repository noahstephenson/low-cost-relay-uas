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
from textwrap import wrap
from typing import Any, Callable, Iterable


ROOT = Path(__file__).resolve().parents[1]
ARCHITECTURE_PATH = ROOT / "model" / "architecture.yaml"
ASSURANCE_PATH = ROOT / "model" / "assurance.yaml"
TRACEABILITY_PATH = ROOT / "model" / "traceability.yaml"
SYSTEM_PATH = ROOT / "model" / "system.yaml"
FEASIBILITY_PATH = ROOT / "analysis" / "results" / "feasibility-summary.json"

TYPOGRAPHY = {
    "title": 30,
    "subtitle": 17,
    "section": 20,
    "box_title": 19,
    "body": 17,
    "small": 15,
    "edge_label": 16,
}
SPACING = {"line_gap": 23, "box_padding": 18, "box_radius": 14}


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


def wrap_text(value: str, max_chars: int) -> list[str]:
    """Wrap labels deterministically without splitting engineering terms."""
    lines = wrap(
        str(value), width=max_chars, break_long_words=False,
        break_on_hyphens=False, replace_whitespace=True,
    ) or [""]
    if len(lines) > 1 and len(lines[-1].split()) == 1:
        candidate = f"{lines[-2]} {lines[-1]}"
        if len(candidate) <= max_chars + 6:
            lines[-2:] = [candidate]
    return lines


def lines_text(
    x: float,
    y: float,
    values: Iterable[str],
    css: str = "body",
    anchor: str = "start",
    gap: int = SPACING["line_gap"],
) -> str:
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
    radius = SPACING["box_radius"] if shape == "round" else 2
    title_lines = wrap_text(title, max(12, int(width / 10)))
    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" class="box {kind}"/>',
        lines_text(x + width / 2, y + 31, title_lines, "box-title", "middle"),
    ]
    detail_list = [
        wrapped
        for detail in details
        for wrapped in wrap_text(detail, max(14, int((width - 2 * SPACING["box_padding"]) / 9)))
    ]
    if detail_list:
        detail_y = y + 61 + (len(title_lines) - 1) * SPACING["line_gap"]
        parts.append(lines_text(x + SPACING["box_padding"], detail_y, detail_list, "body"))
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


def orthogonal_arrow(
    points: Iterable[tuple[float, float]],
    label: str = "",
    kind: str = "neutral",
    dashed: bool = False,
    label_position: tuple[float, float] | None = None,
) -> str:
    """Route a connector through explicit horizontal/vertical lanes."""
    point_list = list(points)
    if len(point_list) < 2:
        raise ValueError("orthogonal connector requires at least two points")
    commands = [f"M {point_list[0][0]} {point_list[0][1]}"]
    for previous, current in zip(point_list, point_list[1:]):
        if previous[0] != current[0] and previous[1] != current[1]:
            raise ValueError("orthogonal connector contains a diagonal segment")
        commands.append(f"L {current[0]} {current[1]}")
    dash = " dashed" if dashed else ""
    parts = [
        f'<path d="{" ".join(commands)}" class="arrow {kind}{dash}" marker-end="url(#arrow-{kind})"/>'
    ]
    if label and label_position:
        parts.append(lines_text(*label_position, [label], "edge-label", "middle"))
    return "\n".join(parts)


def svg_document(
    title: str,
    description: str,
    body: str,
    sources: Iterable[str],
    tier: str,
    audience: str,
    width: int = 1200,
    height: int = 700,
) -> str:
    source_text = ", ".join(sources)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">{escape(description)}</desc>
<metadata>View tier: {escape(tier)}. Audience: {escape(audience)}. Generated from authoritative model records: {escape(source_text)}</metadata>
<defs>
  <marker id="arrow-neutral" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#435269"/></marker>
  <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#245f9e"/></marker>
  <marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#247a52"/></marker>
  <marker id="arrow-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#9a6700"/></marker>
</defs>
<style>
  text {{ font-family: Arial, Helvetica, sans-serif; fill: #172033; }}
  .title {{ font-size: {TYPOGRAPHY['title']}px; font-weight: 700; }}
  .subtitle {{ font-size: {TYPOGRAPHY['subtitle']}px; fill: #536174; }}
  .section {{ font-size: {TYPOGRAPHY['section']}px; font-weight: 700; }}
  .box-title {{ font-size: {TYPOGRAPHY['box_title']}px; font-weight: 700; }}
  .body {{ font-size: {TYPOGRAPHY['body']}px; }}
  .small {{ font-size: {TYPOGRAPHY['small']}px; fill: #536174; }}
  .edge-label {{ font-size: {TYPOGRAPHY['edge_label']}px; font-weight: 700; paint-order: stroke; stroke: #ffffff; stroke-width: 5px; stroke-linejoin: round; }}
  .box {{ stroke: #435269; stroke-width: 2; fill: #f5f7fa; }}
  .box.blue {{ fill: #e9f2ff; stroke: #245f9e; }}
  .box.green {{ fill: #eaf7f0; stroke: #247a52; }}
  .box.amber {{ fill: #fff4d6; stroke: #9a6700; }}
  .box.red {{ fill: #fdecec; stroke: #b42318; }}
  .box.white {{ fill: #ffffff; }}
  .box.future {{ fill: #ffffff; stroke: #6b7280; stroke-dasharray: 9 7; }}
  .platform {{ fill: #f4f7fb; stroke: #26364d; stroke-width: 2.5; }}
  .chip {{ fill: #ffffff; stroke: #8a97a8; stroke-width: 1.5; }}
  .chip.blue {{ fill: #e9f2ff; stroke: #245f9e; }}
  .chip-title {{ font-size: 16px; font-weight: 700; }}
  .payload-black {{ fill: #26364d; stroke: #172033; stroke-width: 3; }}
  .payload-title {{ font-size: 20px; font-weight: 700; fill: #ffffff; }}
  .payload-body {{ font-size: 16px; fill: #eef3f8; }}
  .current-zone {{ fill: #f2f7ff; stroke: #245f9e; stroke-width: 2.5; }}
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
    assert_interface(model, "IFC-EXT-005", "OP-010", "CMP-AVN-04")
    assert_interface(model, "IFC-INT-003", "CMP-PWR-03", "CMP-COM-01")
    assert_interface(model, "IFC-INT-007", "CMP-MNT-01", "CMP-COM-01")
    parts = [
        lines_text(40, 48, [view["title"]], "title"),
        lines_text(40, 78, ["The carrier aircraft has its own control link; mission traffic uses a separate black-box payload."], "subtitle"),
        '<rect x="325" y="105" width="550" height="485" rx="26" class="boundary"/>',
        lines_text(600, 138, [display(index, "OP-002") + " Product Boundary"], "section", "middle"),
        '<rect x="365" y="165" width="470" height="195" rx="18" class="platform"/>',
        lines_text(600, 195, ["VEHICLE PLATFORM"], "section", "middle"),
        '<rect x="385" y="215" width="180" height="48" rx="10" class="chip blue"/>',
        lines_text(475, 244, ["Platform Communications"], "chip-title", "middle"),
        '<rect x="600" y="215" width="180" height="48" rx="10" class="chip blue"/>',
        lines_text(690, 244, ["Flight Avionics"], "chip-title", "middle"),
        '<rect x="385" y="285" width="125" height="48" rx="10" class="chip"/>',
        lines_text(447.5, 314, ["Airframe + Structure"], "chip-title", "middle"),
        '<rect x="525" y="285" width="125" height="48" rx="10" class="chip"/>',
        lines_text(587.5, 314, ["Propulsion"], "chip-title", "middle"),
        '<rect x="665" y="285" width="125" height="48" rx="10" class="chip"/>',
        lines_text(727.5, 314, ["Electrical Power"], "chip-title", "middle"),
        '<rect x="440" y="420" width="320" height="105" rx="15" class="payload-black"/>',
        lines_text(600, 454, ["RELAY PAYLOAD — BLACK BOX"], "payload-title", "middle"),
        lines_text(600, 482, ["Passes command and telemetry"], "payload-body", "middle"),
        lines_text(600, 505, ["Internal radio design is outside project scope"], "payload-body", "middle"),
        box(35, 180, 225, 92, display(index, "OP-010"), ["Controls and monitors the aircraft"], "blue"),
        box(35, 415, 225, 110, display(index, "OP-001"), ["Sends remote-aircraft command", "Receives return telemetry"], "white"),
        box(940, 415, 225, 110, display(index, "OP-003"), ["Receives relayed command", "Returns telemetry"], "white"),
        arrow(260, 230, 385, 230, "Platform Command", "blue", False, 215),
        arrow(385, 255, 260, 255, "Health / Status", "blue", True, 280),
        arrow(260, 445, 440, 445, "Relayed Command", "green", False, 431),
        arrow(760, 445, 940, 445, "Relayed Command", "green", False, 431),
        arrow(940, 493, 760, 493, "Relayed Telemetry", "green", True, 516),
        arrow(440, 493, 260, 493, "Relayed Telemetry", "green", True, 516),
        orthogonal_arrow(
            [(727.5, 333), (727.5, 378), (680, 378), (680, 420)],
            "Regulated Power", "amber", label_position=(748, 372),
        ),
        orthogonal_arrow(
            [(447.5, 333), (447.5, 378), (520, 378), (520, 420)],
            "Mounting", label_position=(474, 372),
        ),
        lines_text(600, 625, ["The relay payload carries mission traffic; it does not control the aircraft."], "section", "middle"),
        lines_text(600, 655, ["Waveform, frequency, protocol, hardware, and endpoint compatibility remain outside this view."], "small", "middle"),
    ]
    return svg_document(
        view["title"], view["question"], "\n".join(parts), view["object_refs"],
        view["tier"], view["audience"],
    )


def system_boundary(model: dict[str, Any], index: dict[str, dict[str, Any]], view: dict[str, Any]) -> str:
    inner = model["system"]["system_boundaries"]["inner"]
    parts = [
        lines_text(40, 48, [view["title"]], "title"),
        lines_text(40, 78, ["Aircraft and payload are inside; people, other vehicles, and authorities are outside."], "subtitle"),
        '<rect x="315" y="115" width="570" height="500" rx="24" class="boundary"/>',
        lines_text(600, 151, [inner["name"] + " Product Boundary"], "section", "middle"),
        box(355, 190, 235, 150, "Aircraft Platform", ["Airframe and structure", "Propulsion", "Electrical power"], "neutral"),
        box(610, 190, 235, 150, "Flight and Control", ["Flight avionics", "Platform command receiver", "Health / status"], "blue"),
        box(355, 370, 235, 155, "Payload Support", ["Mechanical mounting", "Regulated payload power", "Configuration support"], "neutral"),
        box(610, 370, 235, 155, "Relay Payload", ["Black-box payload + antenna", "Internal design unknown"], "green"),
        lines_text(600, 570, ["Only power and mechanical retention cross from platform to payload."], "small", "middle"),
        box(35, 155, 225, 100, display(index, "OP-010"), ["Controls the Relay UAS"], "white"),
        box(35, 285, 225, 100, display(index, "OP-001"), ["Sends and receives", "mission traffic"], "white"),
        box(35, 415, 225, 100, display(index, "OP-007"), ["Supports aircraft", "and configuration"], "white"),
        box(940, 155, 225, 100, display(index, "OP-003"), ["Remote mission endpoint"], "white"),
        box(940, 285, 225, 100, "Future Platforms", ["Future use only"], "future"),
        box(940, 415, 225, 100, "External Authorities", ["Spectrum and compatibility"], "future"),
        arrow(260, 335, 315, 335, kind="neutral"),
        arrow(885, 335, 940, 335, kind="neutral"),
        lines_text(600, 660, ["Everything outside the boundary remains external to the aircraft design; future context is dashed."], "small", "middle"),
    ]
    return svg_document(
        view["title"], view["question"], "\n".join(parts), view["object_refs"],
        view["tier"], view["audience"],
    )


def physical_architecture(model: dict[str, Any], index: dict[str, dict[str, Any]], view: dict[str, Any]) -> str:
    assert_interface(model, "IFC-INT-004", "CMP-AVN-01", "CMP-PRP-02")
    assert_interface(model, "IFC-INT-001", "CMP-PWR-02", "CMP-PRP-02")
    assert_interface(model, "IFC-INT-003", "CMP-PWR-03", "CMP-COM-01")
    assert_interface(model, "IFC-INT-007", "CMP-MNT-01", "CMP-COM-01")
    groups = {
        "airframe": ["CMP-AFR-01", "CMP-AFR-02", "CMP-AFR-03", "CMP-AFR-05"],
        "propulsion": ["CMP-PRP-01", "CMP-PRP-02", "CMP-PRP-03"],
        "power": ["CMP-PWR-01", "CMP-PWR-02", "CMP-PWR-03", "CMP-PWR-04"],
        "avionics": ["CMP-AVN-01", "CMP-AVN-02", "CMP-AVN-03"],
        "platform_comms": ["CMP-AVN-04"],
        "payload_support": ["CMP-AFR-04", "CMP-MNT-01"],
        "payload": ["CMP-COM-01", "CMP-COM-02"],
    }
    parts = [
        lines_text(40, 48, [view["title"]], "title"),
        lines_text(40, 78, ["The vehicle platform surrounds and supports a separate relay-payload black box."], "subtitle"),
        '<rect x="45" y="105" width="1110" height="505" rx="24" class="boundary"/>',
        lines_text(600, 138, ["RELAY UAS"], "section", "middle"),
        '<rect x="80" y="160" width="740" height="405" rx="20" class="platform"/>',
        lines_text(450, 192, ["VEHICLE PLATFORM"], "section", "middle"),
        box(110, 210, 205, 130, "Propulsion", ["Controlled lift", "Controllers • motors • propellers"], "neutral"),
        box(347, 210, 205, 130, "Electrical Power", ["Energy storage and distribution", "Battery • bus • regulators"], "amber"),
        box(585, 210, 205, 130, "Flight Avionics", ["Stabilize • navigate • hold", "Health and recovery support"], "blue"),
        box(110, 375, 275, 110, "Platform Communications", ["Independent aircraft command", "Health / status return"], "blue"),
        box(430, 375, 360, 110, "Payload Support", ["Mechanical retention", "Regulated payload power"], "neutral"),
        box(110, 515, 680, 48, "Airframe and Structure", [], "neutral"),
        '<rect x="875" y="270" width="235" height="210" rx="18" class="payload-black"/>',
        lines_text(992.5, 313, ["RELAY PAYLOAD"], "payload-title", "middle"),
        lines_text(992.5, 342, ["BLACK BOX"], "payload-title", "middle"),
        lines_text(992.5, 385, ["Relays command"], "payload-body", "middle"),
        lines_text(992.5, 409, ["and telemetry"], "payload-body", "middle"),
        lines_text(992.5, 451, ["Internal design undefined"], "payload-body", "middle"),
    ]
    for ids in groups.values():
        for item_id in ids:
            if item_id not in index:
                raise ValueError(f"physical view references missing {item_id}")
    parts.extend([
        arrow(790, 407, 875, 407, "regulated power", "amber", False, 392),
        '<line x1="790" y1="455" x2="875" y2="455" class="arrow"/>',
        lines_text(832, 478, ["mechanical retention"], "edge-label", "middle"),
        lines_text(600, 645, ["Only regulated power and mechanical retention cross from platform to payload."], "section", "middle"),
        lines_text(600, 675, ["Hardware, geometry, ratings, and fabrication remain unresolved."], "small", "middle"),
    ])
    return svg_document(
        view["title"], view["question"], "\n".join(parts), view["object_refs"],
        view["tier"], view["audience"],
    )


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
    return svg_document(
        view["title"], view["question"], "\n".join(parts), view["object_refs"],
        view["tier"], view["audience"],
    )


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
        lines_text(40, 78, ["Aircraft control stays in the blue lane; remote-mission traffic stays in the green lane."], "subtitle"),
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
        lines_text(600, 568, ["The aircraft carries the payload but does not process the relayed mission traffic."], "section", "middle"),
        lines_text(600, 600, ["External compatibility, message formats, protocols, frequency, waveform, and data rate are unresolved."], "small", "middle"),
    ]
    return svg_document(
        view["title"], view["question"], "\n".join(parts), view["object_refs"],
        view["tier"], view["audience"],
    )


def mission_sequence(model: dict[str, Any], index: dict[str, dict[str, Any]], view: dict[str, Any]) -> str:
    scenario_ids = ["SCN-001", "SCN-002", "SCN-003", "SCN-004", "SCN-008"]
    if any(item_id not in index for item_id in scenario_ids):
        raise ValueError("normal mission scenario record missing")
    assert_exchange(model, "IX-009", "OP-002", "OP-010")
    parts = [
        lines_text(40, 48, [view["title"]], "title"),
        lines_text(40, 78, ["Current-system mission sequence; future ground-vehicle and video branches are intentionally omitted."], "subtitle"),
    ]
    lanes = [("Operator / Ground", 90), ("Relay Aircraft", 390), ("Relay Payload", 690), ("Remote UAS", 990)]
    for name, x in lanes:
        parts.append(lines_text(x, 125, [name], "section", "middle"))
        parts.append(f'<line x1="{x}" y1="145" x2="{x}" y2="640" class="lane"/>')
    steps = [
        (170, 90, 390, "1  Prepare / confirm safe state", "neutral"),
        (220, 90, 390, "2  Launch", "blue"),
        (270, 90, 390, "3  Position and hold station", "blue"),
        (335, 90, 690, "4  Send remote-UAS command", "green"),
        (390, 690, 990, "5  Relay command onward", "green"),
        (445, 990, 690, "6  Return telemetry", "green"),
        (500, 690, 90, "7  Relay telemetry to ground", "green"),
    ]
    for y, x1, x2, label, kind in steps:
        parts.append(arrow(x1, y, x2, y, label, kind, kind == "green" and x1 > x2, y - 10))
    parts.append(arrow(390, 560, 90, 560, "8  Monitor health / status", "blue", True, 550))
    parts.append(arrow(390, 620, 90, 620, "9  Recover and return to Ground Safe", "blue", False, 610))
    parts.append(lines_text(600, 680, ["Architecture sequence only; exact readiness and recovery criteria remain unresolved."], "small", "middle"))
    return svg_document(
        view["title"], view["question"], "\n".join(parts), view["object_refs"],
        view["tier"], view["audience"],
    )


def degraded_behavior(model: dict[str, Any], index: dict[str, dict[str, Any]], view: dict[str, Any]) -> str:
    transitions = {(x["from"], x["to"]): x for x in model["architecture"]["mode_transitions"]}
    for pair in [
        ("MODE-005", "MODE-001"), ("MODE-001", "MODE-002"),
        ("MODE-002", "MODE-003"), ("MODE-003", "MODE-004"),
        ("MODE-002", "MODE-004"), ("MODE-004", "MODE-005"),
    ]:
        if pair not in transitions:
            raise ValueError(f"mode transition {pair} missing")
    parts = [
        lines_text(40, 48, [view["title"]], "title"),
        lines_text(40, 78, ["Relay loss is one branch in the aircraft state story—not detailed flight-control logic."], "subtitle"),
        box(35, 160, 165, 92, display(index, "MODE-005"), ["Arming inhibited"], "neutral"),
        box(250, 160, 165, 92, display(index, "MODE-001"), ["Move to station"], "blue"),
        box(465, 160, 180, 92, display(index, "MODE-002"), ["Hold relay geometry"], "green"),
        box(695, 160, 180, 92, display(index, "MODE-003"), ["Relay service impaired"], "amber"),
        '<polygon points="1010,145 1140,206 1010,267 880,206" class="box blue"/>',
        lines_text(1010, 198, ["Platform control", "still available?"], "box-title", "middle"),
        lines_text(225, 137, ["launch"], "edge-label", "middle"),
        lines_text(440, 137, ["station reached"], "edge-label", "middle"),
        lines_text(670, 137, ["relay degrades"], "edge-label", "middle"),
        arrow(200, 206, 250, 206, kind="blue"),
        arrow(415, 206, 465, 206, kind="blue"),
        arrow(645, 206, 695, 206, kind="amber"),
        arrow(875, 206, 880, 206, kind="blue"),
        box(900, 350, 235, 105, display(index, "MODE-004"), ["Recovery intent only", "Criteria remain unresolved"], "blue"),
        box(585, 500, 270, 110, "Unresolved Safety Gap", ["No modeled response for", "impaired platform control"], "red"),
        arrow(1035, 267, 1035, 350, "YES", "blue", False, 320),
        orthogonal_arrow(
            [(985, 267), (985, 290), (720, 290), (720, 500)],
            "NO / IMPAIRED", "amber", label_position=(845, 282),
        ),
        orthogonal_arrow(
            [(555, 252), (555, 325), (875, 325), (875, 402), (900, 402)],
            "normal end / low battery", "blue", dashed=True, label_position=(700, 317),
        ),
        '<path d="M 1018 455 V 640 H 20 V 206 H 35" class="arrow blue" marker-end="url(#arrow-blue)"/>',
        lines_text(555, 630, ["land, recover, and return to Ground Safe"], "edge-label", "middle"),
        lines_text(40, 405, ["Defined:"], "section"),
        lines_text(40, 435, ["• Independent platform control", "• Degraded and recovery states", "• Normal recovery path"], "body"),
        lines_text(40, 535, ["Not yet defined:"], "section"),
        lines_text(40, 565, ["• Detection thresholds", "• Recovery criteria and physical behavior", "• Safety acceptance evidence"], "body"),
    ]
    return svg_document(
        view["title"], view["question"], "\n".join(parts), view["object_refs"],
        view["tier"], view["audience"],
    )


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
        lines_text(40, 78, ["The current design space is primary; reference evidence and future concepts remain separate."], "subtitle"),
        lines_text(145, 145, ["REFERENCE EVIDENCE"], "section", "middle"),
        box(40, 175, 220, 180, display(index, "CFG-REC"), ["Describes teardown evidence", "Incomplete reconstruction", "Not a design baseline"], "white"),
        '<rect x="315" y="115" width="555" height="440" rx="22" class="current-zone"/>',
        lines_text(592.5, 150, ["CURRENT DESIGN SPACE"], "section", "middle"),
        lines_text(592.5, 177, ["Architecture under study—not approved"], "small", "middle"),
        box(360, 215, 465, 135, "Functional Replica Candidate", ["Current proposed architecture", "Reproduces roles—not exact hardware"], "blue"),
        box(430, 395, 325, 110, "Domestic Candidate", ["Current sourcing variant", "Policy and substitutions unresolved"], "blue"),
        arrow(592.5, 350, 592.5, 395, "current variant", "blue", False, 382),
        lines_text(1035, 145, ["FUTURE CONCEPTS"], "section", "middle"),
        box(930, 180, 220, 125, "Digital Extension", ["Payload management", "and multi-platform branch"], "future"),
        box(930, 365, 220, 125, "System-of-Systems", ["Ground vehicles, radio users,", "services, and authorities"], "future"),
        arrow(260, 265, 315, 265, "informs only", "neutral", True, 245),
        arrow(870, 265, 930, 242, "possible later work", "neutral", True, 225),
        arrow(1040, 305, 1040, 365, kind="neutral", dashed=True),
        lines_text(600, 620, ["Reference correspondence is not inheritance; future concepts do not change the current candidate."], "section", "middle"),
        lines_text(600, 654, ["No configuration shown here is an approved technical baseline."], "small", "middle"),
    ]
    return svg_document(
        view["title"], view["question"], "\n".join(parts), view["object_refs"],
        view["tier"], view["audience"],
    )


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
    trade_studies = {item["id"]: item for item in assurance["trade_studies"]}
    configurations = {item["id"]: item for item in architecture["configurations"]}
    if trade_studies["TS-009"]["status"] != "deferred_out_of_scope":
        raise ValueError("relay-payload implementation status changed")
    for config_id in ("CFG-DIG", "CFG-SOS"):
        if configurations[config_id]["approval_status"] != "not_approved":
            raise ValueError(f"future configuration approval changed for {config_id}")
    if "GAP-REC-001" not in index:
        raise ValueError("recovered-source limitation gap missing")

    established = [
        ("System architecture and boundary", "DEFINED"),
        ("Mission and degraded scenarios", "DEFINED"),
        ("Interfaces and subsystem roles", "DEFINED"),
        ("Requirements and traceability", "CHECKED"),
        ("Internal model verification", "COMPLETE WITH GAPS"),
        ("Feasibility design-space analysis", "CONDITIONAL"),
    ]
    outside_scope = [
        ("Relay-payload internal radio design", "DEFERRED"),
        ("Future digital and system-of-systems concepts", "FUTURE"),
    ]
    future_evidence = [
        ("Owner quantitative targets", "PENDING", "amber"),
        ("Recovered-reference completeness", "INCOMPLETE", "amber"),
        ("Physical aircraft verification", "NO EVIDENCE", "red"),
        ("External interface conformance", "BLOCKED", "red"),
        ("Approved technical baseline", "NOT APPROVED", "red"),
    ]
    parts = [
        lines_text(40, 48, [view["title"]], "title"),
        lines_text(40, 78, ["Completed architecture work, deliberate scope limits, and missing real-world evidence are different things."], "subtitle"),
        '<rect x="40" y="112" width="520" height="530" rx="18" class="group"/>',
        '<rect x="600" y="112" width="560" height="205" rx="18" class="group"/>',
        '<rect x="600" y="342" width="560" height="300" rx="18" class="group"/>',
        box(55, 128, 490, 70, "ESTABLISHED BY THIS PROJECT", ["Architecture, traceability, and analysis"], "green"),
        box(615, 128, 530, 70, "DELIBERATELY OUTSIDE THIS PROJECT", ["Not defects in the current architecture study"], "neutral"),
        box(615, 358, 530, 70, "REQUIRES FUTURE DECISION OR EVIDENCE", ["Needed before a verified or approved aircraft claim"], "red"),
    ]
    for row_index, (name, status) in enumerate(established):
        y = 215 + row_index * 57
        parts.append(f'<rect x="55" y="{y}" width="490" height="47" class="box white" rx="5"/>')
        parts.append(f'<rect x="55" y="{y}" width="10" height="47" class="box green" rx="0"/>')
        parts.append(lines_text(77, y + 29, [name], "body"))
        parts.append(f'<text x="530" y="{y + 29}" class="small" text-anchor="end" font-weight="700">{escape(status)}</text>')
    for row_index, (name, status) in enumerate(outside_scope):
        y = 215 + row_index * 48
        parts.append(lines_text(635, y + 20, ["• " + name], "body"))
        parts.append(f'<text x="1125" y="{y + 20}" class="small" text-anchor="end" font-weight="700">{escape(status)}</text>')
    for row_index, (name, status, kind) in enumerate(future_evidence):
        y = 442 + row_index * 40
        parts.append(f'<rect x="625" y="{y}" width="510" height="34" class="box white" rx="4"/>')
        parts.append(f'<rect x="625" y="{y}" width="9" height="34" class="box {kind}" rx="0"/>')
        parts.append(lines_text(647, y + 23, [name], "body"))
        parts.append(f'<text x="1120" y="{y + 23}" class="small" text-anchor="end" font-weight="700">{escape(status)}</text>')
    parts.append(lines_text(600, 666, ["MODEL MATURITY ≠ VERIFIED AIRCRAFT"], "section", "middle"))
    parts.append(lines_text(600, 691, ["No safety, airworthiness, interoperability, operational-readiness, or technical-baseline approval is claimed."], "small", "middle"))
    return svg_document(
        view["title"], view["question"], "\n".join(parts), view["object_refs"],
        view["tier"], view["audience"],
    )


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
        raise ValueError("model/system.yaml communication-view manifest does not match the generator")
    outputs: dict[Path, str] = {}
    for slug, builder in BUILDERS.items():
        view = configured[slug]
        missing = [item_id for item_id in view["object_refs"] if item_id not in index]
        if missing:
            raise ValueError(f"{slug} references unknown model records: {missing}")
        outputs[ROOT / "docs" / "figures" / f"{slug}.svg"] = builder(model, index, view)
    expected_paths = {ROOT / item for item in model["system"].get("generated_figures", [])}
    if set(outputs) != expected_paths:
        raise ValueError("model/system.yaml generated_figures does not match generated outputs")
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
