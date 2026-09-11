<!-- GENERATED VIEW - DO NOT EDIT. -->

# Traceability

[Overview](../../README.md) · [Architecture](../architecture.md) · [Feasibility](../feasibility.md) · [Engineering Status](../engineering-status.md) · [Reference index](README.md)

Representative traces explain engineering cause and effect first. The complete relationship register follows for audit.

Generated from `model/architecture.yaml`, `model/assurance.yaml`, `model/traceability.yaml`. The structured catalogs remain authoritative.

## Representative traces

**Extend remote command reach**

Need → airborne-relay capability → outbound-relay scenario → relay behavior → black-box payload → external relay path → **Relay outbound traffic (REQ-001)** → architecture review now; external conformance later.

**Return remote-aircraft telemetry**

Relay scenario → return-traffic behavior → black-box payload → return external path → **Relay return traffic (REQ-002)** → architecture review now; external conformance later.

**Hold a useful relay position**

Station-keeping capability → position-and-hold scenario → flight behavior → avionics and navigation → **Maintain commanded station position (REQ-003)** → analysis after owner tolerance; physical evidence later.

**Recover after payload loss**

Degraded scenario → separate carrier-control intent → recovery mode → **Recover after payload loss (REQ-007)** → model review recorded; physical recovery evidence absent.

## Complete relationship register

The model contains 177 explicit relationships.

<details>
<summary>Open complete relationship table</summary>

| From | Relationship | To | Status | Gap |
|---|---|---|---|---|
| NEED-001 | motivates | CAP-000 | candidate | - |
| CAP-000 | decomposes_to | CAP-001 | candidate | - |
| CAP-000 | decomposes_to | CAP-002 | candidate | - |
| CAP-000 | decomposes_to | CAP-003 | candidate | GAP-TRC-001 |
| CAP-000 | decomposes_to | CAP-004 | candidate | - |
| CAP-001 | exercised_by | SCN-003 | candidate | - |
| CAP-001 | exercised_by | SCN-004 | candidate | - |
| CAP-002 | exercised_by | SCN-002 | candidate | - |
| CAP-004 | constrains | SCN-001 | candidate | - |
| CAP-004 | constrains | SCN-002 | candidate | - |
| CAP-004 | constrains | SCN-007 | candidate | - |
| CAP-004 | constrains | SCN-008 | candidate | - |
| CAP-004 | constrains | REQ-009 | candidate | - |
| CAP-004 | constrains | REQ-011 | candidate | - |
| CAP-004 | constrains | REQ-012 | candidate | - |
| CAP-004 | constrains | REQ-013 | candidate | - |
| CAP-004 | constrains | REQ-020 | candidate | - |
| CAP-004 | constrains | REQ-021 | candidate | - |
| CAP-004 | governed_by | TS-001 | candidate | GAP-BUDGET-001 |
| CAP-004 | governed_by | TS-002 | candidate | GAP-BUDGET-001 |
| CAP-004 | governed_by | TS-003 | candidate | GAP-BUDGET-001 |
| CAP-004 | governed_by | TS-004 | candidate | GAP-BUDGET-001 |
| CAP-004 | governed_by | TS-006 | candidate | GAP-BUDGET-001 |
| SCN-001 | uses_activity | OA-007 | candidate | - |
| SCN-002 | uses_activity | OA-001 | candidate | - |
| SCN-002 | uses_activity | OA-002 | candidate | - |
| SCN-002 | uses_activity | OA-003 | candidate | - |
| SCN-003 | uses_activity | OA-004 | candidate | - |
| SCN-004 | uses_activity | OA-005 | candidate | - |
| SCN-007 | uses_activity | OA-001 | candidate | - |
| SCN-007 | uses_activity | OA-006 | candidate | - |
| SCN-008 | uses_activity | OA-006 | candidate | - |
| SCN-001 | uses_exchange | IX-001 | candidate | - |
| SCN-001 | uses_exchange | IX-009 | candidate | - |
| SCN-001 | uses_exchange | IX-010 | candidate | - |
| SCN-002 | uses_exchange | IX-001 | candidate | - |
| SCN-002 | uses_exchange | IX-009 | candidate | - |
| SCN-003 | uses_exchange | IX-002 | candidate | - |
| SCN-003 | uses_exchange | IX-003 | candidate | - |
| SCN-004 | uses_exchange | IX-004 | candidate | - |
| SCN-004 | uses_exchange | IX-005 | candidate | - |
| SCN-007 | uses_exchange | IX-001 | candidate | - |
| SCN-007 | uses_exchange | IX-009 | candidate | - |
| SCN-008 | uses_exchange | IX-001 | candidate | - |
| SCN-008 | uses_exchange | IX-009 | candidate | - |
| SCN-008 | uses_exchange | IX-010 | candidate | - |
| OA-001 | performed_by_function | FUN-FLT-01 | candidate | - |
| OA-002 | performed_by_function | FUN-FLT-02 | candidate | - |
| OA-002 | performed_by_function | FUN-CMD-01 | candidate | - |
| OA-003 | performed_by_function | FUN-FLT-03 | candidate | - |
| OA-004 | performed_by_function | FUN-REL-01 | candidate | - |
| OA-005 | performed_by_function | FUN-REL-02 | candidate | - |
| OA-006 | performed_by_function | FUN-FLT-04 | candidate | - |
| OA-006 | performed_by_function | FUN-PWR-02 | candidate | - |
| OA-007 | performed_by_function | FUN-CFG-01 | candidate | - |
| OA-007 | performed_by_function | FUN-HLT-01 | candidate | - |
| FUN-FLT-01 | allocated_to | CMP-AVN-01 | candidate | - |
| FUN-FLT-01 | allocated_to | CMP-AVN-02 | candidate | - |
| FUN-FLT-01 | allocated_to | CMP-PRP-01 | candidate | - |
| FUN-FLT-01 | allocated_to | CMP-PRP-02 | candidate | - |
| FUN-FLT-01 | allocated_to | CMP-PRP-03 | candidate | - |
| FUN-FLT-02 | allocated_to | CMP-AVN-01 | candidate | - |
| FUN-FLT-02 | allocated_to | CMP-AVN-03 | candidate | - |
| FUN-FLT-03 | allocated_to | CMP-AVN-01 | candidate | - |
| FUN-FLT-03 | allocated_to | CMP-AVN-02 | candidate | - |
| FUN-FLT-03 | allocated_to | CMP-AVN-03 | candidate | - |
| FUN-FLT-04 | allocated_to | CMP-AVN-01 | candidate | - |
| FUN-REL-01 | allocated_to | CMP-COM-01 | candidate | - |
| FUN-REL-02 | allocated_to | CMP-COM-01 | candidate | - |
| FUN-PWR-01 | allocated_to | CMP-PWR-02 | candidate | - |
| FUN-PWR-01 | allocated_to | CMP-PWR-03 | candidate | - |
| FUN-PWR-02 | allocated_to | CMP-PWR-02 | candidate | - |
| FUN-PWR-02 | allocated_to | CMP-AVN-01 | candidate | - |
| FUN-CMD-01 | allocated_to | CMP-AVN-04 | candidate | - |
| FUN-CFG-01 | allocated_to | CMP-AVN-01 | candidate | - |
| FUN-HLT-01 | allocated_to | CMP-AVN-01 | candidate | - |
| FUN-HLT-01 | allocated_to | CMP-PWR-02 | candidate | - |
| IX-001 | realized_by | IFC-EXT-005 | candidate | - |
| IX-002 | realized_by | IFC-EXT-001 | candidate | - |
| IX-003 | realized_by | IFC-EXT-002 | candidate | - |
| IX-004 | realized_by | IFC-EXT-003 | candidate | - |
| IX-005 | realized_by | IFC-EXT-004 | candidate | - |
| IX-006 | deferred_to_gap | GAP-SOS-001 | unresolved | GAP-SOS-001 |
| IX-007 | deferred_to_gap | GAP-SOS-001 | unresolved | GAP-SOS-001 |
| IX-008 | deferred_to_gap | GAP-SOS-002 | unresolved | GAP-SOS-002 |
| IX-009 | realized_by | IFC-EXT-007 | candidate | - |
| IFC-INT-006 | provides_input_to | FUN-HLT-01 | candidate | - |
| IX-001 | supported_by_function | FUN-CMD-01 | candidate | - |
| IX-002 | supported_by_function | FUN-REL-01 | candidate | - |
| IX-003 | supported_by_function | FUN-REL-01 | candidate | - |
| IX-004 | supported_by_function | FUN-REL-02 | candidate | - |
| IX-005 | supported_by_function | FUN-REL-02 | candidate | - |
| IX-009 | supported_by_function | FUN-HLT-01 | candidate | - |
| IX-010 | realized_by | IFC-EXT-006 | candidate | - |
| CMP-COM-01 | contains_payload_internal_coupling | IFC-INT-010 | candidate | - |
| IFC-INT-010 | couples_inside_payload_envelope_to | CMP-COM-02 | candidate | - |
| HAZ-002 | mitigated_by | CTL-003 | candidate | - |
| HAZ-003 | mitigated_by | CTL-002 | candidate | - |
| HAZ-004 | mitigated_by | CTL-001 | candidate | - |
| HAZ-005 | mitigated_by | CTL-004 | candidate | - |
| HAZ-006 | mitigated_by | REQ-003 | candidate | - |
| HAZ-007 | mitigated_by | CTL-003 | candidate | - |
| HAZ-008 | mitigated_by | CTL-005 | candidate | - |
| CTL-001 | implemented_by | REQ-006 | candidate | - |
| CTL-001 | implemented_by | REQ-019 | candidate | - |
| CTL-002 | implemented_by | REQ-018 | candidate | - |
| CTL-003 | implemented_by | REQ-005 | candidate | - |
| CTL-004 | implemented_by | REQ-007 | candidate | - |
| CTL-005 | implemented_by | REQ-017 | candidate | - |
| VER-002 | produces | EVD-001 | candidate | - |
| VER-003 | uses | EVD-002 | established | - |
| VER-003 | uses | EVD-003 | established | - |
| DEC-002 | governs_standard_version_for | CFG-REP | unresolved | GAP-STD-001 |
| DEC-002 | governs_standard_version_for | CFG-DOM | unresolved | GAP-STD-001 |
| DEC-002 | governs_standard_version_for | CFG-DIG | unresolved | GAP-STD-001 |
| DEC-002 | governs_standard_version_for | CFG-SOS | unresolved | GAP-STD-001 |
| HAZ-001 | governed_by | DEC-003 | unresolved | GAP-HAZ-001 |
| DEC-004 | governs_candidate | FUN-HLT-01 | candidate | - |
| DEC-004 | governs_candidate | IFC-EXT-007 | candidate | - |
| DEC-004 | governs_candidate | REQ-008 | candidate | - |
| DEC-005 | governs_candidate | CAP-004 | candidate | - |
| REQ-012 | contributes_to | REQ-011 | candidate | GAP-BUDGET-001 |
| REQ-011 | coupled_to | REQ-010 | candidate | GAP-BUDGET-001 |
| REQ-010 | coupled_to | REQ-009 | candidate | GAP-BUDGET-001 |
| TS-002 | coupled_to | TS-003 | candidate | GAP-BUDGET-001 |
| TS-001 | constrains | TS-002 | candidate | GAP-BUDGET-001 |
| TS-004 | constrains | TS-003 | candidate | GAP-BUDGET-001 |
| IFC-EXT-001 | model_reviewed_by | VER-005 | candidate | - |
| IFC-EXT-001 | conformance_verified_by | VER-009 | unresolved | GAP-IFC-001 |
| IFC-EXT-002 | model_reviewed_by | VER-005 | candidate | - |
| IFC-EXT-002 | conformance_verified_by | VER-009 | unresolved | GAP-IFC-001 |
| IFC-EXT-003 | model_reviewed_by | VER-005 | candidate | - |
| IFC-EXT-003 | conformance_verified_by | VER-009 | unresolved | GAP-IFC-001 |
| IFC-EXT-004 | model_reviewed_by | VER-005 | candidate | - |
| IFC-EXT-004 | conformance_verified_by | VER-009 | unresolved | GAP-IFC-001 |
| IFC-EXT-005 | model_reviewed_by | VER-005 | candidate | - |
| IFC-EXT-005 | conformance_verified_by | VER-009 | unresolved | GAP-IFC-001 |
| IFC-EXT-006 | model_reviewed_by | VER-005 | candidate | - |
| IFC-EXT-006 | conformance_verified_by | VER-009 | unresolved | GAP-IFC-001 |
| IFC-EXT-007 | model_reviewed_by | VER-005 | candidate | - |
| IFC-EXT-007 | conformance_verified_by | VER-009 | unresolved | GAP-IFC-001 |
| CFG-REC | informs_at_role_level | CFG-REP | established | GAP-REC-001 |
| EVD-006 | supports | CLM-REC-005 | established | GAP-REC-001 |
| EVD-007 | supports | CLM-REC-005 | established | GAP-REC-001 |
| EVD-008 | records_execution_of | VER-002 | established | - |
| EVD-009 | records_execution_of | VER-001 | established | GAP-VER-001 |
| EVD-009 | records_execution_of | VER-004 | established | GAP-VER-001 |
| EVD-010 | records_execution_of | VER-005 | established | GAP-IFC-001 |
| EVD-010 | records_execution_of | VER-007 | established | - |
| EVD-011 | records_execution_of | VER-003 | established | GAP-SRC-001 |
| EVD-011 | records_execution_of | VER-006 | established | GAP-HAZ-001 |
| EVD-012 | supports | CLM-SCP-001 | established | - |
| IFC-INT-011 | supports | FUN-PWR-01 | candidate | - |
| REQ-018 | allocated_to | IFC-INT-011 | candidate | GAP-VER-001 |
| IFC-INT-012 | supports | FUN-FLT-02 | candidate | - |
| IFC-INT-012 | supports | FUN-FLT-03 | candidate | - |
| REQ-003 | allocated_to | IFC-INT-012 | candidate | GAP-VER-001 |
| IFC-INT-013 | supports | FUN-FLT-01 | candidate | - |
| IFC-INT-014 | supports | FUN-FLT-01 | candidate | - |
| REQ-007 | allocated_to | IFC-INT-013 | candidate | GAP-VER-001 |
| REQ-007 | allocated_to | IFC-INT-014 | candidate | GAP-VER-001 |
| IFC-INT-015 | supports | FUN-PWR-01 | candidate | - |
| REQ-015 | allocated_to | IFC-INT-015 | candidate | GAP-VER-001 |
| TS-006 | defines_envelope_for | REQ-012 | candidate | GAP-BUDGET-001 |
| TS-001 | contributes_mass_to | REQ-011 | candidate | GAP-BUDGET-001 |
| REQ-011 | drives | TS-002 | candidate | GAP-BUDGET-001 |
| REQ-010 | sets_energy_demand_for | TS-003 | candidate | GAP-BUDGET-001 |
| TS-003 | contributes_mass_to | REQ-011 | candidate | GAP-BUDGET-001 |
| TS-003 | contributes_cost_to | REQ-009 | candidate | GAP-BUDGET-001 |
| REQ-009 | remains_blocked_by | GAP-BUDGET-001 | unresolved | GAP-BUDGET-001 |
| EVD-013 | records_execution_of | VER-001 | established | GAP-VER-001 |
| EVD-013 | records_execution_of | VER-002 | established | - |
| EVD-013 | records_execution_of | VER-003 | established | GAP-SRC-001 |
| EVD-013 | records_execution_of | VER-004 | established | GAP-VER-001 |
| EVD-013 | records_execution_of | VER-005 | established | GAP-IFC-001 |
| EVD-013 | records_execution_of | VER-006 | established | GAP-HAZ-001 |
| EVD-013 | records_execution_of | VER-007 | established | - |

</details>

See [Decisions & gaps](decisions-and-gaps.md) for the human interpretation of unresolved relationships.
