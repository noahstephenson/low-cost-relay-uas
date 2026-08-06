<!-- GENERATED VIEW - DO NOT AUTHOR INDEPENDENT ARCHITECTURE FACTS HERE. -->

> Generated from `model/traceability.yaml`, `model/requirements.yaml`, `model/operational-scenarios.yaml`, `model/interfaces.yaml`, `.seal/proof.yaml`. Regenerate with `python scripts/validate-baseline.py --write-reports`.
> The structured catalogs are authoritative. This report is not an approval record.

# Baseline Traceability

Logical chain: Need -> Capability -> Scenario -> Performer/Activity -> Information Exchange -> Function -> Component -> Interface -> Requirement -> Hazard/Control -> Verification -> Evidence.

A relationship may be absent at this maturity. `TBD` and gap codes are preserved rather than inferred.

## Structured relationships

| From | Relationship | To | Status | Gap |
|---|---|---|---|---|
| NEED-001 | motivates | CAP-000 | candidate | - |
| CAP-000 | decomposes_to | CAP-001 | candidate | - |
| CAP-000 | decomposes_to | CAP-002 | candidate | - |
| CAP-000 | decomposes_to | CAP-003 | candidate | GAP-TRC-001 |
| CAP-000 | decomposes_to | CAP-004 | candidate | GAP-TRC-002 |
| CAP-001 | exercised_by | SCN-003 | candidate | - |
| CAP-001 | exercised_by | SCN-004 | candidate | - |
| CAP-002 | exercised_by | SCN-002 | candidate | - |
| CAP-004 | constrains | SCN-001 | candidate | - |
| CAP-004 | constrains | SCN-002 | candidate | - |
| CAP-004 | constrains | SCN-007 | candidate | - |
| CAP-004 | constrains | SCN-008 | candidate | - |
| SCN-001 | uses_activity | OA-001 | candidate | GAP-SCN-001 |
| SCN-002 | uses_activity | OA-001 | candidate | - |
| SCN-002 | uses_activity | OA-002 | candidate | - |
| SCN-002 | uses_activity | OA-003 | candidate | - |
| SCN-003 | uses_activity | OA-004 | candidate | - |
| SCN-004 | uses_activity | OA-005 | candidate | - |
| SCN-007 | uses_activity | OA-001 | candidate | - |
| SCN-007 | uses_activity | OA-006 | candidate | - |
| SCN-008 | uses_activity | OA-006 | candidate | - |
| OA-001 | performed_by_function | FUN-FLT-01 | candidate | - |
| OA-002 | performed_by_function | FUN-FLT-02 | candidate | - |
| OA-002 | performed_by_function | FUN-CMD-01 | candidate | - |
| OA-003 | performed_by_function | FUN-FLT-03 | candidate | - |
| OA-004 | performed_by_function | FUN-REL-01 | candidate | - |
| OA-005 | performed_by_function | FUN-REL-02 | candidate | - |
| OA-006 | performed_by_function | FUN-FLT-04 | candidate | - |
| OA-006 | performed_by_function | FUN-PWR-02 | candidate | - |
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
| IX-001 | realized_by | IFC-EXT-005 | candidate | GAP-IFC-001 |
| IX-002 | realized_by | IFC-EXT-001 | candidate | GAP-IFC-001 |
| IX-003 | realized_by | IFC-EXT-002 | candidate | GAP-IFC-001 |
| IX-004 | realized_by | IFC-EXT-003 | candidate | GAP-IFC-001 |
| IX-005 | realized_by | IFC-EXT-004 | candidate | GAP-IFC-001 |
| IX-006 | realized_by | TBD | unresolved | GAP-SOS-001 |
| IX-007 | realized_by | TBD | unresolved | GAP-SOS-001 |
| IX-008 | realized_by | TBD | unresolved | GAP-SOS-002 |
| IX-009 | partially_realized_by | IFC-INT-006 | candidate | GAP-SOS-003 |
| IX-010 | realized_by | IFC-EXT-006 | candidate | - |
| HAZ-002 | mitigated_by | CTL-003 | candidate | - |
| HAZ-003 | mitigated_by | CTL-002 | candidate | GAP-CONFLICT-001 |
| HAZ-004 | mitigated_by | CTL-001 | candidate | GAP-CONFLICT-002 |
| HAZ-005 | mitigated_by | CTL-004 | candidate | - |
| HAZ-006 | mitigated_by | REQ-FUN-003 | candidate | - |
| HAZ-007 | mitigated_by | CTL-003 | candidate | - |
| HAZ-008 | mitigated_by | CTL-005 | candidate | GAP-CONFLICT-003 |
| CTL-001 | implemented_by | REQ-FUN-006 | candidate | - |
| CTL-001 | implemented_by | REQ-SAF-002 | candidate | - |
| CTL-002 | implemented_by | REQ-SAF-001 | candidate | - |
| CTL-003 | implemented_by | REQ-FUN-005 | candidate | - |
| CTL-004 | implemented_by | REQ-FUN-007 | candidate | - |
| CTL-005 | implemented_by | REQ-IFC-004 | candidate | - |
| VER-002 | produces | EVD-001 | candidate | - |
| VER-003 | uses | EVD-002 | established | - |
| VER-003 | uses | EVD-003 | established | - |

## Requirement mappings

| Requirement | Classification | Upstream rationale | Allocation | Verification | TBD owner | Gap |
|---|---|---|---|---|---|---|
| REQ-FUN-001 | relay_uas_system | CAP-001, SCN-003, CLM-CAP-001 | FUN-REL-01, CMP-COM-01, IFC-EXT-001, IFC-EXT-002 | VER-001, VER-004 | - | - |
| REQ-FUN-002 | relay_uas_system | CAP-001, SCN-004, CLM-CAP-001 | FUN-REL-02, CMP-COM-01, IFC-EXT-003, IFC-EXT-004 | VER-001, VER-004 | - | - |
| REQ-FUN-003 | relay_uas_system | CAP-002, SCN-002, HAZ-006 | FUN-FLT-03, CMP-AVN-01, IFC-INT-009 | VER-001, VER-008 | TS-007, TS-009 | - |
| REQ-FUN-004 | relay_uas_system | SCN-002, SCN-007, SCN-008, CLM-ARC-003 | FUN-CMD-01, CMP-AVN-04, IFC-EXT-005 | VER-001, VER-004 | TS-008 | - |
| REQ-FUN-005 | safety_and_assurance | CAP-004, SCN-007, SCN-008, HAZ-002, HAZ-007, CTL-003 | FUN-FLT-04, FUN-PWR-02, CMP-AVN-01, CMP-PWR-02 | VER-004, VER-006, VER-008 | TS-003, TS-011 | - |
| REQ-FUN-006 | safety_and_assurance | SCN-001, HAZ-004, CTL-001 | FUN-PWR-01, CMP-AVN-01, MODE-005 | VER-004, VER-006 | - | - |
| REQ-FUN-007 | safety_and_assurance | CAP-004, SCN-007, HAZ-005, CTL-004, CLM-HAZ-001 | FUN-FLT-01, FUN-FLT-04, MODE-003 | VER-004, VER-006, VER-008 | - | - |
| REQ-PER-001 | mission_and_stakeholder | CAP-004, NEED-001 | - | VER-001 | TS-001, TS-002, TS-003 | - |
| REQ-PER-002 | relay_uas_system | CAP-001, SCN-003, SCN-004 | CMP-PWR-01 | VER-001, VER-008 | TS-001, TS-002, TS-003 | - |
| REQ-PER-003 | relay_uas_system | CAP-004, SCN-001, SCN-002 | - | VER-005, VER-008 | TS-001, TS-002, TS-003 | - |
| REQ-PER-004 | interface | CLM-ARC-001, CLM-ARC-002 | CMP-MNT-01, IFC-INT-007 | VER-005, VER-008 | TS-006 | - |
| REQ-PER-005 | mission_and_stakeholder | CAP-004, SCN-001, SCN-002, SCN-008 | OP-010, OP-002 | VER-004, VER-008 | TS-001 | - |
| REQ-IFC-001 | interface | CAP-004, CLM-ARC-001, CLM-ARC-002 | CMP-MNT-01, IFC-INT-007 | VER-005 | TS-006 | - |
| REQ-IFC-002 | interface | CLM-ARC-001, CLM-ARC-002 | CMP-PWR-03, IFC-INT-003 | VER-005, VER-008 | TS-004 | - |
| REQ-IFC-003 | interface | CLM-ARC-001, CLM-ARC-002 | CMP-COM-01, IFC-INT-003, IFC-INT-007 | VER-005 | - | - |
| REQ-IFC-004 | safety_and_assurance | HAZ-008, CTL-005, CLM-ARC-002 | CMP-MNT-01, IFC-INT-007 | VER-005, VER-006, VER-008 | TS-006 | - |
| REQ-SAF-001 | safety_and_assurance | HAZ-003, CTL-002 | CMP-PWR-01, CMP-PWR-02 | VER-005, VER-006, VER-008 | TS-003 | - |
| REQ-SAF-002 | safety_and_assurance | SCN-001, HAZ-004, CTL-001 | CMP-AVN-01, OP-010 | VER-004, VER-006 | - | - |
| REQ-CON-001 | subsystem | CAP-004 | - | VER-005 | TS-001, TS-002, TS-003, TS-005, TS-006 | - |
| REQ-CON-002 | subsystem | CAP-004 | CMP-AVN-01 | VER-005 | TS-005 | - |
| REQ-CON-003 | safety_and_assurance | CLM-SCP-001, DEC-001 | - | VER-003, VER-005 | - | - |
| REQ-CON-004 | relay_uas_system | CAP-002, SCN-002, HAZ-006 | CMP-AVN-03, FUN-FLT-03, IFC-INT-009 | VER-001, VER-004 | TS-007 | - |
| REQ-DEF-001 | interface | CLM-SCP-001, TS-009 | IFC-EXT-001, IFC-EXT-002, IFC-EXT-003, IFC-EXT-004, IFC-EXT-005 | VER-003 | TS-009 | - |
| REQ-DEF-002 | interface | CLM-SCP-001, TS-009 | CMP-COM-02, IFC-INT-010 | VER-003 | TS-009 | - |
| REQ-DEF-003 | system_of_systems | CLM-SCP-001, OP-008 | OP-008 | VER-003 | - | - |
| REQ-DEF-004 | system_of_systems | CLM-SCP-001, CAP-003, TS-009 | - | VER-003 | TS-009 | - |
| REQ-DEF-005 | safety_and_assurance | CLM-SCP-001 | - | VER-003 | - | - |
