<!-- GENERATED VIEW - DO NOT AUTHOR INDEPENDENT ARCHITECTURE FACTS HERE. -->

> Generated from `model/traceability.yaml`, `model/requirements.yaml`, `model/interfaces.yaml`, `model/operational-scenarios.yaml`, `model/elements.yaml`, `.seal/sources.yaml`. Regenerate with `python scripts/validate-baseline.py --write-reports`.
> The structured catalogs are authoritative. This report is not an approval record.

# Baseline Gaps

> These gaps remain visible by design. Their presence does not make the structured baseline invalid.

| Code | Category | Gap | Affected IDs | Disposition | Severity |
|---|---|---|---|---|---|
| GAP-REC-001 | configuration mapping | The current generic relay-UAS decomposition is not demonstrated to be an as-built model of CFG-REC. | CFG-REC, CFG-REP, CFG-DOM, CLM-REC-005 | unresolved | major |
| GAP-SRC-001 | missing evidence | Original standalone teardown photographs, measurements, and inspection records are not present in the repository. | CFG-REC, SRC-GAP-001 | unresolved | major |
| GAP-CFG-001 | unknown configuration applicability | The untracked Cameo/MagicDraw HTML export has not been reconciled to a configuration or authority level. | SRC-REPO-009 | unresolved | major |
| GAP-CFG-002 | unknown configuration applicability | HAZ-009 and the external hazards do not yet have defensible configuration applicability. | HAZ-009, HAZ-EXT-001, HAZ-EXT-002, HAZ-EXT-003 | unresolved | moderate |
| GAP-TRC-001 | unallocated capability | CAP-003 has no allocated operational activity, function, component, or supported requirement mechanism. | CAP-003, REQ-DEF-004, TS-009 | true_coverage_gap | major |
| GAP-TRC-002 | legacy traceability gap | CAP-004 has no operational-activity allocation in the legacy traceability matrix; the new scenarios constrain it but do not fabricate a mission activity. | CAP-004, SRC-REPO-008 | expected_at_current_maturity | moderate |
| GAP-TRC-003 | legacy traceability gap | The legacy requirement matrix omits multiple existing requirements and cannot substantiate its intended all-ID coverage. | SRC-REPO-004, SRC-REPO-008 | contradictory | major |
| GAP-CONFLICT-001 | conflicting statements | hazard-analysis.md and traceability.md describe HAZ-003 mitigation as TODO or unmitigated, while requirements.md defines REQ-SAF-001 as a mitigation. | HAZ-003, REQ-SAF-001, CTL-002, SRC-REPO-006, SRC-REPO-008 | contradictory | major |
| GAP-CONFLICT-002 | conflicting statements | hazard-analysis.md names a MODE-005 arming inhibit for HAZ-004 but leaves the trace as TODO despite REQ-FUN-006 and REQ-SAF-002. | HAZ-004, REQ-FUN-006, REQ-SAF-002, CTL-001, SRC-REPO-006 | contradictory | moderate |
| GAP-CONFLICT-003 | conflicting statements | HAZ-008 is linked to REQ-IFC-001 in legacy views, while REQ-IFC-004 is the more direct load-retention requirement. | HAZ-008, REQ-IFC-001, REQ-IFC-004, CTL-005, SRC-REPO-006, SRC-REPO-008 | contradictory | moderate |
| GAP-HAZ-001 | unmitigated hazard | HAZ-001 has no defined control or mitigating requirement. | HAZ-001 | true_coverage_gap | major |
| GAP-HAZ-002 | unmitigated hazard | HAZ-009 remains an undefined placeholder and cannot be analyzed. | HAZ-009 | unresolved | moderate |
| GAP-IFC-001 | interface verification | IFC-EXT-001 through IFC-EXT-005 have no verification allocation or interface authority. | IFC-EXT-001, IFC-EXT-002, IFC-EXT-003, IFC-EXT-004, IFC-EXT-005 | unresolved | major |
| GAP-IFC-002 | interface definition | External communications interfaces intentionally retain unknown protocol, frequency, waveform, power, data-rate, and message-format attributes. | IFC-EXT-001, IFC-EXT-002, IFC-EXT-003, IFC-EXT-004, IFC-EXT-005, TS-009 | intentionally_out_of_scope | expected |
| GAP-SCN-001 | scenario activity mapping | SCN-001 uses OA-001 as the nearest existing activity, but setup and initialization lacks a dedicated approved operational activity. | SCN-001, OA-001 | expected_at_current_maturity | moderate |
| GAP-SOS-001 | proposed system-of-systems thread | UGV command and telemetry exchanges have no allocated activity, system function, interface, requirement, hazard set, or verification authority. | CFG-SOS, SCN-005, OP-004, IX-006, IX-007 | true_coverage_gap | major |
| GAP-SOS-002 | proposed system-of-systems thread | Video or sensor-data return has no allocated current interface, function, requirement, hazard set, or verification authority. | CFG-DIG, CFG-SOS, SCN-006, IX-008 | true_coverage_gap | major |
| GAP-SOS-003 | health and status coverage | IX-009 is only partially represented by battery-state telemetry and lacks complete Relay-UAS health and status allocation. | IX-009, IFC-INT-006 | true_coverage_gap | moderate |
| GAP-BUDGET-001 | mass-cost-endurance coupling | Mass, cost, power, endurance, and payload envelopes remain unresolved and mutually coupled. | REQ-PER-001, REQ-PER-002, REQ-PER-003, REQ-PER-004, TS-001, TS-002, TS-003, TS-004, TS-006 | unresolved | major |
| GAP-VER-001 | verification evidence | Most requirements have candidate or deferred verification methods but no execution evidence. | VER-001, VER-004, VER-005, VER-006, VER-007, VER-008 | expected_at_current_maturity | major |

## Derived gap indexes

- Unknown configuration applicability: SRC-REPO-009, SRC-EXT-001, SRC-EXT-002, HAZ-009, HAZ-EXT-001, HAZ-EXT-002, HAZ-EXT-003
- Interfaces without verification allocation: IFC-EXT-001, IFC-EXT-002, IFC-EXT-003, IFC-EXT-004, IFC-EXT-005, IFC-INT-010
- Scenarios without an information exchange: -
- Requirements with an explicit provenance gap: -
- Proposed scenarios touching CFG-SOS: SCN-001, SCN-005, SCN-006, SCN-008

## Interpretation

External communications interfaces remain intentionally undefined at implementation level. UGV, radio-user, network-service, and broader sensor-data threads are proposals, not current three-node architecture capabilities. Mass, cost, power, endurance, capability allocation, hazard control, and verification evidence gaps remain open.
