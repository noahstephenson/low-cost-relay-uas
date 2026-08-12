<!-- GENERATED VIEW: DO NOT EDIT. Run python scripts/generate-mermaid-views.py -->
# Generated Architecture Views

> **Baseline Candidate - Not Approved.** These diagrams are generated from
> `system.yaml`, catalogs under `model/`, and `.seal/proof.yaml`. They have no
> independent architecture authority. Candidate, proposed, deferred, and
> unresolved labels do not imply approval or executed verification.

The diagrams deliberately omit RF implementation values, build instructions,
operating procedures, and recovered implementation detail. `CFG-REC` is shown
only as a descriptive evidence configuration and does not inherit the proposed
`CFG-REP`/`CFG-DOM` resource decomposition.
This report is the ID-rich engineering drill-down. Plain-language canonical
figures are generated separately under `reports/figures/`.

## Configuration and context views

### 1. What is current, reference, and future?

Configuration scope: `CFG-REC / CFG-REP / CFG-DOM / CFG-DIG / CFG-SOS`.

Derivation denotes lineage, not exact inheritance, equivalence, or approval. Future context is outside the current implementation baseline.

```mermaid
flowchart LR
    %% Configuration scope: CFG-REC / CFG-REP / CFG-DOM / CFG-DIG / CFG-SOS
    CFG_REC["CFG-REC<br/>Reference evidence<br/>evidence only - role mapping narrowed"]
    CFG_REP["CFG-REP<br/>Replica candidate<br/>current proposed baseline"]
    CFG_DOM["CFG-DOM<br/>Domestic candidate<br/>current - substitution criteria unresolved"]
    CFG_DIG["CFG-DIG<br/>Digital extension<br/>future - adds IFC-INT-008 candidate"]
    CFG_SOS["CFG-SOS<br/>C2 Ecosystem context<br/>future outer context - OP-004 / OP-005 / OP-006"]
    CFG_REC -->|"proposed functional derivation, not an exact clone<br/>derivation is not approval"| CFG_REP
    CFG_REP -->|"proposed substitution architecture<br/>derivation is not approval"| CFG_DOM
    CFG_REP -->|"future concept branch<br/>derivation is not approval"| CFG_DIG
    CFG_DIG -->|"outer system-of-systems context containing the relay UAS as one constituent<br/>derivation is not approval"| CFG_SOS
```

### 2. What is inside the project boundary?

Configuration scope: `CFG-SOS outer context - CFG-REP / CFG-DOM / CFG-DIG inner constituent`.

External constituents remain independently managed. Only catalogued information exchanges are drawn; unconnected future actors remain context, not implied interfaces.

```mermaid
flowchart LR
    %% Configuration scope: CFG-SOS outer context - CFG-REP / CFG-DOM / CFG-DIG inner constituent
    subgraph OUTER["C2 Ecosystem outer boundary - CFG-SOS proposed context"]
        OP_010["OP-010<br/>Operator<br/>independently managed human performer"]
        OP_001["OP-001<br/>Ground Control Node<br/>independently managed external system"]
        OP_003["OP-003<br/>Remote UAS Node<br/>independently managed external system"]
        OP_004["OP-004<br/>UGV<br/>future / unresolved"]
        OP_005["OP-005<br/>Radio User<br/>future / unresolved"]
        OP_006["OP-006<br/>Network Service<br/>future / unresolved"]
        OP_007["OP-007<br/>Maintenance Personnel<br/>external support performer"]
        OP_008["OP-008<br/>Spectrum-Management Authority<br/>independent authority"]
        OP_009["OP-009<br/>Supporting Infrastructure<br/>future / unresolved"]
        subgraph INNER["Relay UAS inner boundary - proposed for CFG-REP/CFG-DOM/CFG-DIG"]
            OP_002["OP-002<br/>Relay UAS / Relay Node<br/>system under study"]
        end
    end
    OP_010 -->|"IX-001 / IFC-EXT-005<br/>command and control"| OP_002
    OP_001 -->|"IX-002 / IFC-EXT-001<br/>command and control"| OP_002
    OP_002 -->|"IX-003 / IFC-EXT-002<br/>command and control"| OP_003
    OP_003 -->|"IX-004 / IFC-EXT-003<br/>telemetry"| OP_002
    OP_002 -->|"IX-005 / IFC-EXT-004<br/>telemetry"| OP_001
    OP_001 -.->|"IX-006 / unresolved<br/>command and control"| OP_004
    OP_004 -.->|"IX-007 / unresolved<br/>telemetry"| OP_001
    OP_002 -->|"IX-009 / IFC-EXT-007<br/>health and status"| OP_010
    OP_007 -->|"IX-010 / IFC-EXT-006<br/>configuration and maintenance"| OP_002
```

### 3. How current-system traffic moves

Configuration scope: `CFG-REP / CFG-DOM`.

`IX-001` is independent Relay-UAS platform command. `IX-002` through `IX-005` are relayed mission traffic.

```mermaid
flowchart LR
    %% Configuration scope: CFG-REP / CFG-DOM
    OP_010["OP-010<br/>Operator"]
    OP_001["OP-001<br/>Ground Control Node"]
    OP_002["OP-002<br/>Relay UAS / Relay Node"]
    OP_003["OP-003<br/>Remote UAS Node"]
    OP_010 -->|"IX-001 / IFC-EXT-005<br/>command and control"| OP_002
    OP_001 -->|"IX-002 / IFC-EXT-001<br/>command and control"| OP_002
    OP_002 -->|"IX-003 / IFC-EXT-002<br/>command and control"| OP_003
    OP_003 -->|"IX-004 / IFC-EXT-003<br/>telemetry"| OP_002
    OP_002 -->|"IX-005 / IFC-EXT-004<br/>telemetry"| OP_001
```

## Selected resource connectivity views

### 4B. How power and propulsion connect

Configuration scope: `CFG-REP / CFG-DOM`.

```mermaid
flowchart LR
    %% Configuration scope: CFG-REP / CFG-DOM
    CMP_PWR_01["CMP-PWR-01<br/>Battery pack"]
    CMP_PWR_02["CMP-PWR-02<br/>Power distribution board"]
    CMP_PWR_03["CMP-PWR-03<br/>Step-down regulator(s)"]
    CMP_PWR_04["CMP-PWR-04<br/>Battery connector"]
    CMP_PRP_01["CMP-PRP-01<br/>Brushless motor"]
    CMP_PRP_02["CMP-PRP-02<br/>Electronic speed controller"]
    CMP_PRP_03["CMP-PRP-03<br/>Propeller"]
    CMP_AVN_01["CMP-AVN-01<br/>Flight controller"]
    CMP_COM_01["CMP-COM-01<br/>Relay payload module (black box)"]
    CMP_PWR_01 -->|"IFC-INT-011<br/>electrical power"| CMP_PWR_02
    CMP_PWR_04 -.->|"physical connection resource<br/>IFC-INT-011"| CMP_PWR_02
    CMP_PWR_02 -->|"IFC-INT-001<br/>electrical power"| CMP_PRP_02
    CMP_PWR_02 -->|"IFC-INT-015<br/>electrical power"| CMP_PWR_03
    CMP_PWR_03 -->|"IFC-INT-002<br/>electrical power"| CMP_AVN_01
    CMP_PWR_03 -->|"IFC-INT-003<br/>electrical power<br/>platform-to-payload"| CMP_COM_01
    CMP_PWR_02 -->|"IFC-INT-006<br/>health and status"| CMP_AVN_01
    CMP_PRP_02 -->|"IFC-INT-013<br/>controlled electrical propulsion power"| CMP_PRP_01
    CMP_PRP_01 -->|"IFC-INT-014<br/>mechanical propulsion drive"| CMP_PRP_03
```

### 4C. How platform control works

Configuration scope: `CFG-REP / CFG-DOM`.

```mermaid
flowchart LR
    %% Configuration scope: CFG-REP / CFG-DOM
    OP_010["OP-010<br/>Operator"]
    CMP_AVN_01["CMP-AVN-01<br/>Flight controller"]
    CMP_AVN_02["CMP-AVN-02<br/>IMU / sensor suite"]
    CMP_AVN_03["CMP-AVN-03<br/>GNSS / compass module"]
    CMP_AVN_04["CMP-AVN-04<br/>Control link receiver"]
    CMP_PRP_02["CMP-PRP-02<br/>Electronic speed controller"]
    CMP_PWR_02["CMP-PWR-02<br/>Power distribution board"]
    OP_010 -->|"IFC-EXT-005<br/>command and control<br/>separate platform command"| CMP_AVN_04
    CMP_AVN_04 -->|"IFC-INT-005<br/>command and control"| CMP_AVN_01
    CMP_AVN_01 -->|"IFC-INT-004<br/>command and control"| CMP_PRP_02
    CMP_PWR_02 -->|"IFC-INT-006<br/>health and status"| CMP_AVN_01
    CMP_AVN_02 -->|"IFC-INT-009<br/>navigation and timing"| CMP_AVN_01
    CMP_AVN_03 -->|"IFC-INT-012<br/>navigation and timing"| CMP_AVN_01
```

### 4D. How the relay payload is isolated

Configuration scope: `CFG-REP / CFG-DOM`.

`IFC-INT-010` stays inside the payload black-box envelope. Only `IFC-INT-003` and `IFC-INT-007` cross from platform to payload.

```mermaid
flowchart LR
    %% Configuration scope: CFG-REP / CFG-DOM
    OP_001["OP-001<br/>Ground Control Node"]
    OP_003["OP-003<br/>Remote UAS Node"]
    CMP_PWR_03["CMP-PWR-03<br/>Step-down regulator(s)"]
    CMP_MNT_01["CMP-MNT-01<br/>Modular payload bay"]
    subgraph PAYLOAD["Relay-payload black-box envelope"]
        CMP_COM_01["CMP-COM-01<br/>Relay payload module (black box)"]
        CMP_COM_02["CMP-COM-02<br/>Antenna physical-resource envelope<br/>physical-resource envelope"]
        CMP_COM_01 <-->|"IFC-INT-010<br/>physical-resource coupling<br/>payload-internal - characteristics undefined"| CMP_COM_02
    end
    CMP_PWR_03 -->|"IFC-INT-003<br/>electrical power<br/>platform boundary crossing"| CMP_COM_01
    CMP_MNT_01 <-->|"IFC-INT-007<br/>mechanical mounting<br/>platform boundary crossing"| CMP_COM_01
    OP_001 -->|"IFC-EXT-001<br/>command and control<br/>implementation undefined"| CMP_COM_01
    CMP_COM_01 -->|"IFC-EXT-002<br/>command and control<br/>implementation undefined"| OP_003
    OP_003 -->|"IFC-EXT-003<br/>telemetry<br/>implementation undefined"| CMP_COM_01
    CMP_COM_01 -->|"IFC-EXT-004<br/>telemetry<br/>implementation undefined"| OP_001
```

## Evidence correspondence view

### 4G. How recovered evidence informs candidate roles

Configuration scope: `CFG-REC informs CFG-REP / CFG-DOM - no exact inheritance`.

This is a grouped view of the controlled record-level mapping. Five recovered records remain unmatched and one remains unknown; no contradiction was found.

```mermaid
flowchart LR
    %% Configuration scope: CFG-REC informs CFG-REP / CFG-DOM - no exact inheritance
    REC_STRUCTURE["Recovered structure and hardware"] -->|"direct / class-level support"| CAND_STRUCTURE["CMP-AFR-01 through CMP-AFR-05"]
    REC_PROPULSION["Recovered propulsion resources"] -->|"direct role support"| CAND_PROPULSION["CMP-PRP-01 through CMP-PRP-03"]
    REC_POWER["Recovered power resources and harness"] -->|"direct / partial / unknown"| CAND_POWER["CMP-PWR-01 through CMP-PWR-04"]
    REC_AVIONICS["Recovered control and navigation resources"] -->|"direct / partial support"| CAND_AVIONICS["CMP-AVN-01 through CMP-AVN-04"]
    REC_PAYLOAD["Recovered payload modules and antennas"] -->|"partial / inferred correspondence"| CAND_PAYLOAD["CMP-COM-01 / CMP-COM-02"]
    REC_MOUNTING["Recovered payload retention"] -->|"partial role support"| CAND_MOUNTING["CMP-MNT-01"]
```

## Behavioral views

### 5. How operating modes change

Configuration scope: `CFG-REP / CFG-DOM`.

Only transitions supported by current scenarios or requirements are shown; all remain candidate unless stated otherwise.

```mermaid
stateDiagram-v2
    %% Configuration scope: CFG-REP / CFG-DOM
    state "MODE-005 Ground Safe" as MODE_005
    state "MODE-001 Transit" as MODE_001
    state "MODE-002 Station Keeping" as MODE_002
    state "MODE-003 Relay Degraded" as MODE_003
    state "MODE-004 Return / Recovery" as MODE_004
    [*] --> MODE_005
    MODE_005 --> MODE_001: SCN-002 - launch and transit
    MODE_001 --> MODE_002: SCN-002 - relay station established
    MODE_002 --> MODE_003: SCN-007 - relay function degraded
    MODE_003 --> MODE_004: SCN-007 / REQ-FUN-007 - recovery intent
    MODE_002 --> MODE_004: SCN-008 / REQ-FUN-005 - normal termination or low-battery recovery
    MODE_004 --> MODE_005: SCN-008 - platform recovered and made ground safe
    note right of MODE_003
      Payload function degraded
      Platform control may remain available
      REQ-FUN-007 [PROPOSED]
      Evidence [DEFERRED]
    end note
```

### 7. How command and telemetry flow

Configuration scope: `CFG-REP / CFG-DOM`.

```mermaid
sequenceDiagram
    %% Configuration scope: CFG-REP / CFG-DOM
    participant Operator as OP-010 Platform operator
    participant Platform as CMP-AVN-04 Platform command receiver
    participant Ground as OP-001 Ground control node
    participant Payload as CMP-COM-01 Relay payload black box
    participant Remote as OP-003 Remote UAS
    Operator->>Platform: IX-001 / IFC-EXT-005 separate Relay-UAS platform command
    rect rgb(245, 245, 245)
        Ground->>Payload: IX-002 / IFC-EXT-001 outbound traffic
        Payload->>Remote: IX-003 / IFC-EXT-002 outbound traffic
        Remote-->>Payload: IX-004 / IFC-EXT-003 return telemetry
        Payload-->>Ground: IX-005 / IFC-EXT-004 return telemetry
    end
    Note over Ground,Remote: SCN-003 / SCN-004 logical relay only - external paths undefined
```

### 8. What happens on relay degradation?

Configuration scope: `CFG-REP / CFG-DOM`.

The second path terminates at explicit gaps; it does not invent a recovery behavior.

```mermaid
sequenceDiagram
    %% Configuration scope: CFG-REP / CFG-DOM
    participant Ground as OP-001 Ground control node
    participant Payload as CMP-COM-01 Relay payload black box
    participant Relay as OP-002 Relay UAS platform
    participant Operator as OP-010 Platform operator
    Payload--xGround: SCN-007 relay function loss or degradation
    Relay-->>Operator: IX-009 / IFC-EXT-007 health/status [PROPOSED]
    Operator->>Relay: IX-001 / IFC-EXT-005 independent platform command
    alt Payload lost and platform remains controllable
        Note over Payload,Relay: MODE-003 - CTL-004 / REQ-FUN-007 [PROPOSED]
        Relay-->>Operator: transition intent toward MODE-004 Return / Recovery
    else Platform control also impaired
        Note over Relay,Operator: HAZ-001 / GAP-HAZ-001 - no modeled consequence-management behavior
        Note over Ground,Operator: GAP-VER-001 - no executed recovery evidence
    end
```

### 9B. Why mass, power, endurance, and cost are coupled

Configuration scope: `CFG-REP / CFG-DOM`.

This is one coupled design problem. The diagram adds no values and does not resolve any trade study.

```mermaid
flowchart LR
    %% Configuration scope: CFG-REP / CFG-DOM
    REQ_PER_004["REQ-PER-004<br/>The payload bay shall accommodate a payload of up to [TBD] mass within a [TBD] volume envelope.<br/>[PROPOSED]"]
    TS_006["TS-006<br/>Payload mount interface standard<br/>[PROPOSED]"]
    TS_001["TS-001<br/>Airframe material and construction method<br/>[PROPOSED]"]
    REQ_PER_003["REQ-PER-003<br/>System gross mass shall not exceed [TBD].<br/>[PROPOSED]"]
    TS_002["TS-002<br/>Propulsion sizing<br/>[PROPOSED]"]
    TS_004["TS-004<br/>Payload power allocation<br/>[PROPOSED]"]
    REQ_PER_002["REQ-PER-002<br/>The system shall provide at least [TBD] minutes of on-station endurance.<br/>[PROPOSED]"]
    TS_003["TS-003<br/>Battery architecture<br/>[PROPOSED]"]
    REQ_PER_001["REQ-PER-001<br/>System unit cost shall not exceed [TBD].<br/>[PROPOSED]"]
    GAP_BUDGET_001["GAP-BUDGET-001<br/>Coupled targets and evidence unresolved<br/>[UNRESOLVED]"]
    REQ_PER_004 -->|"contributes to"| REQ_PER_003
    TS_002 -->|"coupled to"| TS_003
    TS_004 -->|"constrains"| TS_003
    TS_006 -->|"defines envelope for"| REQ_PER_004
    TS_001 -->|"contributes mass to"| REQ_PER_003
    REQ_PER_003 -->|"drives"| TS_002
    REQ_PER_002 -->|"sets energy demand for"| TS_003
    TS_003 -->|"contributes mass to"| REQ_PER_003
    TS_003 -->|"contributes cost to"| REQ_PER_001
    REQ_PER_001 -.->|"remains blocked by"| GAP_BUDGET_001
```

## Assurance and traceability views

### 10A. What has been checked and what still needs evidence?

Configuration scope: `CFG-REP / CFG-DOM with project-scope deferrals`.

VER-001 through VER-007 have current 0.8.0 model-level evidence in EVD-013 but no new owner acceptance. EVD-008 through EVD-012 preserve the accepted 0.7.0 work package. VER-008 remains deferred and VER-009 remains blocked; neither review constitutes physical verification, external conformance, safety approval, or technical-baseline approval.

```mermaid
flowchart LR
    %% Configuration scope: CFG-REP / CFG-DOM with project-scope deferrals
    ACCEPTED["PRESERVED OWNER-ACCEPTED REVIEW<br/>0.7.0 / EVD-008 through EVD-012"]
    EXECUTED["CURRENT MODEL REVIEW<br/>0.8.0 / VER-001 through VER-007<br/>EVD-013 - not owner accepted"]
    PASS["EXECUTED PASS<br/>VER-002 / VER-007"]
    OPEN["EXECUTED WITH OPEN GAPS<br/>VER-001 / VER-003 through VER-006"]
    PHYSICAL["PHYSICAL-EVIDENCE-REQUIRED<br/>REQ-FUN-006 / REQ-FUN-008<br/>GAP-VER-001"]
    EXTERNAL["EXTERNAL-AUTHORITY-REQUIRED<br/>REQ-FUN-001 / REQ-FUN-004<br/>GAP-IFC-001"]
    DEFERRED["INTENTIONALLY-DEFERRED<br/>REQ-DEF-001 / REQ-DEF-004"]
    VER_008["VER-008<br/>Deferred physical verification method<br/>future physical evidence"]
    VER_009["VER-009<br/>External conformance verification<br/>external authority required"]
    TS_009["TS-009<br/>Relay payload characterization<br/>formal deferral"]
    ACCEPTED -->|"historical acceptance boundary preserved"| EXECUTED
    EXECUTED -->|"no structural failure"| PASS
    EXECUTED -->|"known gaps retained"| OPEN
    PHYSICAL -.->|"no execution evidence"| VER_008
    EXTERNAL -.->|"authority and specification absent"| VER_009
    DEFERRED -.->|"outside current scope"| TS_009
```

### 11. Example end-to-end relay trace

Configuration scope: `CFG-REP / CFG-DOM`.

The thread is readable end to end, but candidate relationships and evidence gaps remain visible.

```mermaid
flowchart LR
    %% Configuration scope: CFG-REP / CFG-DOM
    NEED_001["NEED-001<br/>Extend mission reach<br/>[PROPOSED]"]
    CAP_001["CAP-001<br/>Beyond-Line-of-Sight Control<br/>[PROPOSED]"]
    SCN_003["SCN-003<br/>Remote-UAS command through the relay<br/>[PROPOSED]"]
    OA_004["OA-004<br/>Relay outbound traffic<br/>[PROPOSED]"]
    IX_002["IX-002<br/>Remote-UAS command toward relay<br/>[PROPOSED]"]
    FUN_REL_01["FUN-REL-01<br/>Relay outbound traffic<br/>[PROPOSED]"]
    CMP_COM_01["CMP-COM-01<br/>Relay payload module (black box)<br/>[PROPOSED]"]
    IFC_EXT_001["IFC-EXT-001<br/>Ground-control outbound traffic to relay payload<br/>[PROPOSED]"]
    REQ_FUN_001["REQ-FUN-001<br/>Relay outbound traffic<br/>[PROPOSED]"]
    VER_001["VER-001<br/>Requirement and architecture analysis<br/>[EXECUTED WITH OPEN GAPS]"]
    VER_009["VER-009<br/>External conformance verification<br/>[BLOCKED]"]
    GAP_IFC_001["GAP-IFC-001<br/>External conformance authority missing<br/>[UNRESOLVED]"]
    NEED_001 -->|"motivates"| CAP_001
    CAP_001 -->|"exercised by"| SCN_003
    SCN_003 -->|"uses"| OA_004
    OA_004 -->|"information exchange"| IX_002
    IX_002 -->|"supports"| FUN_REL_01
    FUN_REL_01 -->|"allocated to"| CMP_COM_01
    CMP_COM_01 -->|"external interface"| IFC_EXT_001
    IFC_EXT_001 -->|"allocated requirement"| REQ_FUN_001
    REQ_FUN_001 -->|"model analysis"| VER_001
    REQ_FUN_001 -.->|"external conformance"| VER_009
    VER_009 -.->|"authority and evidence unresolved"| GAP_IFC_001
```

## Generated interface inventory

This inventory is generated directly from `model/architecture.yaml`. Model-review
allocation is distinct from real-world external conformance and execution evidence.

| ID | Endpoints | Direction | Flow class | Configurations | Recovered evidence | Maturity | Model review | External conformance | Unknown attributes |
|---|---|---|---|---|---|---|---|---|---|
| IFC-INT-001 | CMP-PWR-02 to CMP-PRP-02 | a_to_b | electrical power | CFG-REP, CFG-DOM | DIRECT_SOURCE_SUPPORT | proposed_design / proposed | VER-005, VER-008 | not an external conformance interface | voltage; current; connector; protection; wiring allocation |
| IFC-INT-002 | CMP-PWR-03 to CMP-AVN-01 | a_to_b | electrical power | CFG-REP, CFG-DOM | INDIRECT_SOURCE_SUPPORT | proposed_design / proposed | VER-005, VER-008 | not an external conformance interface | voltage; current; connector; power-quality envelope |
| IFC-INT-003 | CMP-PWR-03 to CMP-COM-01 | a_to_b | electrical power | CFG-REP, CFG-DOM | INDIRECT_SOURCE_SUPPORT | proposed_design / proposed | VER-005, VER-008 | not an external conformance interface | voltage envelope; current envelope; connector; protection; thermal allocation |
| IFC-INT-004 | CMP-AVN-01 to CMP-PRP-02 | a_to_b | command and control | CFG-REP, CFG-DOM | ENGINEERING_INFERENCE | proposed_design / proposed | VER-005, VER-008 | not an external conformance interface | signal format; timing; connector; fault response |
| IFC-INT-005 | CMP-AVN-04 to CMP-AVN-01 | a_to_b | command and control | CFG-REP, CFG-DOM | INDIRECT_SOURCE_SUPPORT | proposed_design / proposed | VER-005, VER-008 | not an external conformance interface | protocol; connector; timing; failsafe behavior |
| IFC-INT-006 | CMP-PWR-02 to CMP-AVN-01 | a_to_b | health and status | CFG-REP, CFG-DOM | ENGINEERING_INFERENCE | proposed_design / proposed | VER-005, VER-008 | not an external conformance interface | measurement set; accuracy; update rate; connector; fault indication |
| IFC-INT-007 | CMP-MNT-01 to CMP-COM-01 | bidirectional_physical | mechanical mounting | CFG-REP, CFG-DOM | DIRECT_SOURCE_SUPPORT | proposed_design / proposed | VER-005, VER-008 | not an external conformance interface | geometry; load envelope; retention margin; inspection criteria |
| IFC-EXT-001 | OP-001 to CMP-COM-01 | a_to_b | command and control | CFG-REP, CFG-DOM | PROPOSED_ARCHITECTURE_ONLY | proposed_design / proposed | VER-005, VER-007 | external_authority_and_execution_evidence_required | frequency; waveform; protocol; power; data rate; message format; endpoint compatibility; verification authority |
| IFC-EXT-002 | CMP-COM-01 to OP-003 | a_to_b | command and control | CFG-REP, CFG-DOM | PROPOSED_ARCHITECTURE_ONLY | proposed_design / proposed | VER-005, VER-007 | external_authority_and_execution_evidence_required | frequency; waveform; protocol; power; data rate; message format; endpoint compatibility; verification authority |
| IFC-EXT-003 | OP-003 to CMP-COM-01 | a_to_b | telemetry | CFG-REP, CFG-DOM | ENGINEERING_INFERENCE | proposed_design / proposed | VER-005, VER-007 | external_authority_and_execution_evidence_required | frequency; waveform; protocol; power; data rate; message format; endpoint compatibility; verification authority |
| IFC-EXT-004 | CMP-COM-01 to OP-001 | a_to_b | telemetry | CFG-REP, CFG-DOM | ENGINEERING_INFERENCE | proposed_design / proposed | VER-005, VER-007 | external_authority_and_execution_evidence_required | frequency; waveform; protocol; power; data rate; message format; endpoint compatibility; verification authority |
| IFC-EXT-005 | OP-010 to CMP-AVN-04 | a_to_b | command and control | CFG-REP, CFG-DOM | INDIRECT_SOURCE_SUPPORT | proposed_design / proposed | VER-005, VER-007 | external_authority_and_execution_evidence_required | frequency; waveform; protocol; power; message format; failsafe behavior; verification authority |
| IFC-INT-008 | CMP-AVN-01 to CMP-COM-01 | bidirectional | payload management and health and status | CFG-DIG, CFG-SOS | NOT_APPLICABLE | proposed_design / proposed | VER-004, VER-005, VER-007 | not an external conformance interface | adoption decision; data model; protocol; connector; timing; authority; failure response |
| IFC-INT-009 | CMP-AVN-02 to CMP-AVN-01 | a_to_b | navigation and timing | CFG-REP, CFG-DOM | NO_RECOVERED_EVIDENCE | engineering_inference / proposed | VER-005, VER-008 | not an external conformance interface | sensor set; data format; timing; accuracy; fault detection; connector |
| IFC-INT-010 | CMP-COM-01 to CMP-COM-02 | bidirectional_physical | physical-resource coupling | CFG-REP, CFG-DOM | DIRECT_SOURCE_SUPPORT | proposed_design / proposed | VER-005 | not an external conformance interface | antenna count; role; placement; connector; all RF characteristics |
| IFC-EXT-006 | OP-007 to OP-002 | bidirectional | configuration and maintenance | CFG-REP, CFG-DOM, CFG-DIG, CFG-SOS | PROPOSED_ARCHITECTURE_ONLY | proposed_design / proposed | VER-005, VER-007 | external_authority_and_execution_evidence_required | data set; format; transport; authorization; retention period; tool ownership |
| IFC-EXT-007 | CMP-AVN-01 to OP-010 | a_to_b | health and status | CFG-REP, CFG-DOM | PROPOSED_ARCHITECTURE_ONLY | proposed_design / proposed | VER-004, VER-005, VER-007 | external_authority_and_execution_evidence_required | minimum status set; format; transport; update behavior; endpoint compatibility; conformance authority |
| IFC-INT-011 | CMP-PWR-01 to CMP-PWR-02 | a_to_b | electrical power | CFG-REP, CFG-DOM | INDIRECT_SOURCE_SUPPORT | proposed_design / proposed | VER-005, VER-008 | not an external conformance interface | voltage; current; polarity; protection; connector implementation; physical routing |
| IFC-INT-012 | CMP-AVN-03 to CMP-AVN-01 | a_to_b | navigation and timing | CFG-REP, CFG-DOM | NO_RECOVERED_EVIDENCE | engineering_inference / proposed | VER-005, VER-008 | not an external conformance interface | data format; timing; accuracy; fault detection; connector |
| IFC-INT-013 | CMP-PRP-02 to CMP-PRP-01 | a_to_b | controlled electrical propulsion power | CFG-REP, CFG-DOM | INDIRECT_SOURCE_SUPPORT | proposed_design / proposed | VER-005, VER-008 | not an external conformance interface | electrical characteristics; connector; wiring; fault response |
| IFC-INT-014 | CMP-PRP-01 to CMP-PRP-03 | a_to_b | mechanical propulsion drive | CFG-REP, CFG-DOM | INDIRECT_SOURCE_SUPPORT | proposed_design / proposed | VER-005, VER-008 | not an external conformance interface | attachment method; rotation direction; torque envelope; retention criteria |
| IFC-INT-015 | CMP-PWR-02 to CMP-PWR-03 | a_to_b | electrical power | CFG-REP, CFG-DOM | INDIRECT_SOURCE_SUPPORT | proposed_design / proposed | VER-005, VER-008 | not an external conformance interface | voltage; current; connector; protection; branch allocation |

## Validation notes

- Optional syntax validation expects Mermaid CLI `mmdc` 11.4.1 when installed locally.
- Absence of Node.js or the pinned CLI does not invalidate standard-library catalog validation.
- This technical report remains Mermaid-based; canonical SVG figures are generated and validated separately.
