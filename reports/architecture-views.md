<!-- GENERATED VIEW: DO NOT EDIT. Run python scripts/generate-mermaid-views.py -->
# Generated Architecture Views

> **Baseline Candidate - Not Approved.** These diagrams are generated from
> `system.yaml`, catalogs under `model/`, and `.seal/proof.yaml`. They have no
> independent architecture authority. Candidate, proposed, deferred, and
> unresolved labels do not imply approval or executed verification.

The diagrams deliberately omit RF implementation values, build instructions,
operating procedures, and detailed recovered-item mapping. `CFG-REC` is shown
only as a descriptive evidence configuration and does not inherit the proposed
`CFG-REP`/`CFG-DOM` resource decomposition.

## Configuration and context views

### 1. Configuration derivation

Configuration scope: `CFG-REC / CFG-REP / CFG-DOM / CFG-DIG / CFG-SOS`.

Derivation denotes an architecture relationship, not exact inheritance, equivalence, or approval.

```mermaid
flowchart LR
    %% Configuration scope: CFG-REC / CFG-REP / CFG-DOM / CFG-DIG / CFG-SOS
    CFG_REC["CFG-REC<br/>Reference evidence<br/>reference evidence - [UNVERIFIED mapping]"]
    CFG_REP["CFG-REP<br/>Replica candidate<br/>[PROPOSED]"]
    CFG_DOM["CFG-DOM<br/>Domestic candidate<br/>[PROPOSED]"]
    CFG_DIG["CFG-DIG<br/>Digital extension<br/>[PROPOSED]"]
    CFG_SOS["CFG-SOS<br/>C2 Ecosystem context<br/>outer system-of-systems context - [PROPOSED]"]
    CFG_REC -->|"proposed functional derivation, not an exact clone<br/>derivation is not approval"| CFG_REP
    CFG_REP -->|"proposed substitution architecture<br/>derivation is not approval"| CFG_DOM
    CFG_REP -->|"future concept branch<br/>derivation is not approval"| CFG_DIG
    CFG_DIG -->|"outer system-of-systems context containing the relay UAS as one constituent<br/>derivation is not approval"| CFG_SOS
```

### 2. Two-boundary context

Configuration scope: `CFG-SOS outer context - CFG-REP / CFG-DOM / CFG-DIG inner constituent`.

External constituents remain independently managed. Dashed relationships are proposed or TBD.

```mermaid
flowchart LR
    %% Configuration scope: CFG-SOS outer context - CFG-REP / CFG-DOM / CFG-DIG inner constituent
    subgraph OUTER["C2 Ecosystem outer boundary - CFG-SOS proposed context"]
        OP_010["OP-010<br/>Operator<br/>independently managed human performer"]
        OP_001["OP-001<br/>Ground Control Node<br/>independently managed external system"]
        OP_003["OP-003<br/>Remote UAS Node<br/>independently managed external system"]
        OP_004["OP-004<br/>UGV<br/>proposed / TBD"]
        OP_005["OP-005<br/>Radio User<br/>proposed / TBD"]
        OP_006["OP-006<br/>Network Service<br/>proposed / TBD"]
        OP_007["OP-007<br/>Maintenance Personnel<br/>external support performer"]
        OP_008["OP-008<br/>Spectrum-Management Authority<br/>independent authority"]
        OP_009["OP-009<br/>Supporting Infrastructure<br/>proposed / TBD"]
        subgraph INNER["Relay UAS inner boundary - proposed for CFG-REP/CFG-DOM/CFG-DIG"]
            OP_002["OP-002<br/>Relay UAS / Relay Node<br/>system under study"]
        end
    end
    OP_010 -->|"IX-001 platform command"| OP_002
    OP_001 <-->|"IX-002 through IX-005 relay thread"| OP_002
    OP_002 <-->|"mission traffic relationship"| OP_003
    OP_007 <-->|"IX-010 / IFC-EXT-006 support"| OP_002
    OP_008 -.->|"external authority - criteria unresolved"| OP_002
    OP_001 -.->|"IX-006 / IX-007 proposed / TBD"| OP_004
    OP_002 -.->|"relationship proposed / TBD"| OP_005
    OP_002 -.->|"relationship proposed / TBD"| OP_006
    OP_009 -.->|"support relationship proposed / TBD"| OP_002
```

### 3. Current three-node operational connectivity

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
    OP_010 -.->|"platform command is separate from relayed mission traffic"| OP_001
```

## Relay-UAS resource views

### 4A. Structure and payload mounting

Configuration scope: `CFG-REP / CFG-DOM`.

```mermaid
flowchart LR
    %% Configuration scope: CFG-REP / CFG-DOM
    CMP_AFR_01["CMP-AFR-01<br/>Center frame plate"]
    CMP_AFR_02["CMP-AFR-02<br/>Arm assembly"]
    CMP_AFR_03["CMP-AFR-03<br/>Landing gear"]
    CMP_AFR_04["CMP-AFR-04<br/>Payload mount interface"]
    CMP_AFR_05["CMP-AFR-05<br/>Fastener and hardware set"]
    CMP_MNT_01["CMP-MNT-01<br/>Modular payload bay"]
    CMP_COM_01["CMP-COM-01<br/>Relay payload module (black box)"]
    CMP_AFR_01 -.->|"structural decomposition"| CMP_AFR_02
    CMP_AFR_01 -.->|"structural decomposition"| CMP_AFR_03
    CMP_AFR_01 -.->|"structural decomposition"| CMP_AFR_04
    CMP_AFR_01 -.->|"hardware set"| CMP_AFR_05
    CMP_AFR_04 -.->|"mount relationship [TBD]"| CMP_MNT_01
    CMP_MNT_01 <-->|"IFC-INT-007<br/>mechanical mounting"| CMP_COM_01
```

### 4B. Power and propulsion connectivity

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
    CMP_PWR_01 -.->|"source association - IFC not allocated"| CMP_PWR_02
    CMP_PWR_04 -.->|"resource association - IFC not allocated"| CMP_PWR_02
    CMP_PWR_02 -->|"IFC-INT-001<br/>electrical power"| CMP_PRP_02
    CMP_PWR_03 -->|"IFC-INT-002<br/>electrical power"| CMP_AVN_01
    CMP_PWR_03 -->|"IFC-INT-003<br/>electrical power<br/>platform-to-payload"| CMP_COM_01
    CMP_PWR_02 -->|"IFC-INT-006<br/>health and status"| CMP_AVN_01
    CMP_PRP_02 -.->|"propulsion association"| CMP_PRP_01
    CMP_PRP_01 -.->|"propulsion association"| CMP_PRP_03
```

### 4C. Avionics and platform control connectivity

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
    CMP_AVN_03 -.->|"navigation resource - IFC unresolved"| CMP_AVN_01
```

### 4D. Payload boundary and external traffic

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

### 4E. Maintenance and configuration support

Configuration scope: `CFG-REP / CFG-DOM / CFG-DIG / CFG-SOS`.

This support/governance interface is intentionally omitted from airborne mission-traffic diagrams.

```mermaid
flowchart LR
    %% Configuration scope: CFG-REP / CFG-DOM / CFG-DIG / CFG-SOS
    OP_007["OP-007<br/>Maintenance Personnel"]
    OP_002["OP-002<br/>Relay UAS / Relay Node"]
    OP_007 <-->|"IFC-EXT-006<br/>configuration and maintenance<br/>IX-010 support/governance"| OP_002
```

### 4F. Future digital interface delta

Configuration scope: `CFG-DIG / CFG-SOS only`.

`IFC-INT-008` is not part of the current `CFG-REP`/`CFG-DOM` two-interface payload boundary.

```mermaid
flowchart LR
    %% Configuration scope: CFG-DIG / CFG-SOS only
    CMP_AVN_01["CMP-AVN-01<br/>Flight controller"]
    CMP_COM_01["CMP-COM-01<br/>Relay payload module (black box)<br/>future payload [PROPOSED]"]
    CMP_AVN_01 <-->|"IFC-INT-008<br/>payload management and health and status<br/>future / proposed"| CMP_COM_01
    IX_008["IX-008<br/>Video or sensor-data return candidate<br/>future sensor-data exchange [TBD]"]
    IX_008 -.->|"realizing interface TBD - GAP-SOS-002"| CMP_COM_01
```

## Behavioral views

### 5. Operating-mode state

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
    MODE_005 --> MODE_001: SCN-002 transition
    MODE_001 --> MODE_002: SCN-002 station established
    MODE_002 --> MODE_003: SCN-007 relay function degraded
    MODE_003 --> MODE_004: SCN-007 recovery intent
    MODE_002 --> MODE_004: SCN-008 termination or REQ-FUN-005
    MODE_004 --> MODE_005: SCN-008 recovered
    note right of MODE_003
      Payload function degraded
      Platform control may remain available
      REQ-FUN-007 [PROPOSED]
      Evidence [DEFERRED]
    end note
```

### 6. Launch and positioning sequence

Configuration scope: `CFG-REP / CFG-DOM`.

```mermaid
sequenceDiagram
    %% Configuration scope: CFG-REP / CFG-DOM
    participant Operator as OP-010 Operator
    participant Receiver as CMP-AVN-04 Control receiver
    participant Flight as CMP-AVN-01 Flight-control resource
    participant Nav as CMP-AVN-02 Navigation/sensor resources
    participant Propulsion as CMP-PRP-02 Propulsion control
    participant Relay as OP-002 Relay UAS health/status
    Operator->>Receiver: IX-001 / IFC-EXT-005 platform command intent
    Receiver->>Flight: IFC-INT-005 platform control input
    Nav-->>Flight: IFC-INT-009 navigation/timing information
    Flight->>Propulsion: IFC-INT-004 propulsion command
    Relay-->>Operator: IX-009 partial health/status - GAP-SOS-003
    Note over Operator,Relay: SCN-002 architecture walkthrough - no procedure defined
```

### 7. Bidirectional relay sequence

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

### 8. Degradation and recovery sequence

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
    Relay-->>Operator: IX-009 health/status indication (partial)
    Operator->>Relay: IX-001 / IFC-EXT-005 independent platform command
    alt Payload lost and platform remains controllable
        Note over Payload,Relay: MODE-003 - CTL-004 / REQ-FUN-007 [PROPOSED]
        Relay-->>Operator: transition intent toward MODE-004 Return / Recovery
    else Platform control also impaired
        Note over Relay,Operator: HAZ-001 / GAP-HAZ-001 - no modeled consequence-management behavior
        Note over Ground,Operator: GAP-VER-001 - no executed recovery evidence
    end
```

### 9. Scenario lifecycle

Configuration scope: `CFG-REP / CFG-DOM current - CFG-DIG / CFG-SOS proposed branches`.

Dashed branches are future proposals without complete activity, interface, requirement, hazard, or verification allocation.

```mermaid
flowchart LR
    %% Configuration scope: CFG-REP / CFG-DOM current - CFG-DIG / CFG-SOS proposed branches
    SCN_001["SCN-001<br/>System setup and initialization<br/>[PROPOSED]"]
    SCN_002["SCN-002<br/>Relay-UAS launch and positioning<br/>[PROPOSED]"]
    SCN_003["SCN-003<br/>Remote-UAS command through the relay<br/>[PROPOSED]"]
    SCN_004["SCN-004<br/>Remote-UAS telemetry return<br/>[PROPOSED]"]
    SCN_005["SCN-005<br/>UGV command and telemetry through the architecture<br/>[PROPOSED]"]
    SCN_006["SCN-006<br/>Video or sensor-data return<br/>[PROPOSED]"]
    SCN_007["SCN-007<br/>Relay degradation, loss, or recovery<br/>[PROPOSED]"]
    SCN_008["SCN-008<br/>Mission termination and data recovery<br/>[PROPOSED]"]
    SCN_001 -->|"progression"| SCN_002
    SCN_002 -->|"outbound thread"| SCN_003
    SCN_002 -->|"return thread"| SCN_004
    SCN_003 -->|"degraded"| SCN_007
    SCN_004 -->|"degraded"| SCN_007
    SCN_003 -->|"normal termination"| SCN_008
    SCN_004 -->|"normal termination"| SCN_008
    SCN_007 -->|"recovery intent"| SCN_008
    SCN_001 -.->|"future CFG-SOS / GAP-SOS-001"| SCN_005
    SCN_001 -.->|"future CFG-DIG / CFG-SOS / GAP-SOS-002"| SCN_006
```

## Assurance and traceability views

### 10. Hazard-control-requirement-verification

Configuration scope: `CFG-REP / CFG-DOM`.

Verification nodes are candidate or deferred methods. They are not executed evidence and provide no approval or safety credit.

```mermaid
flowchart LR
    %% Configuration scope: CFG-REP / CFG-DOM
    HAZ_004["HAZ-004<br/>Propeller contact injury<br/>[PROPOSED]"]
    CTL_001["CTL-001<br/>Ground-safe motor arming inhibit and visible armed-state indication<br/>[PROPOSED]"]
    HAZ_004 -->|"mitigated by"| CTL_001
    REQ_FUN_006["REQ-FUN-006<br/>Inhibit arming in Ground Safe<br/>[PROPOSED]"]
    CTL_001 -->|"implemented by"| REQ_FUN_006
    VER_004["VER-004<br/>Operational-scenario walkthrough<br/>[DEFERRED] or [UNVERIFIED]"]
    REQ_FUN_006 -->|"verification allocation"| VER_004
    GAP_VER_001["GAP-VER-001<br/>Execution evidence missing<br/>[UNVERIFIED]"]
    VER_004 -.->|"execution evidence missing"| GAP_VER_001
    VER_006["VER-006<br/>Hazard-control-requirement cross-reference<br/>[DEFERRED] or [UNVERIFIED]"]
    REQ_FUN_006 -->|"verification allocation"| VER_006
    VER_006 -.->|"execution evidence missing"| GAP_VER_001
    REQ_SAF_002["REQ-SAF-002<br/>Show armed state to operator<br/>[PROPOSED]"]
    CTL_001 -->|"implemented by"| REQ_SAF_002
    REQ_SAF_002 -->|"verification allocation"| VER_004
    VER_004 -.->|"execution evidence missing"| GAP_VER_001
    REQ_SAF_002 -->|"verification allocation"| VER_006
    VER_006 -.->|"execution evidence missing"| GAP_VER_001
    HAZ_008["HAZ-008<br/>Payload separation in flight<br/>[PROPOSED]"]
    CTL_005["CTL-005<br/>Payload retention under flight loads<br/>[PROPOSED]"]
    HAZ_008 -->|"mitigated by"| CTL_005
    REQ_IFC_004["REQ-IFC-004<br/>Retain payload under flight loads<br/>[PROPOSED]"]
    CTL_005 -->|"implemented by"| REQ_IFC_004
    VER_005["VER-005<br/>Interface-catalog inspection<br/>[DEFERRED] or [UNVERIFIED]"]
    REQ_IFC_004 -->|"verification allocation"| VER_005
    VER_005 -.->|"execution evidence missing"| GAP_VER_001
    REQ_IFC_004 -->|"verification allocation"| VER_006
    VER_006 -.->|"execution evidence missing"| GAP_VER_001
    VER_008["VER-008<br/>Deferred physical verification method<br/>[DEFERRED] or [UNVERIFIED]"]
    REQ_IFC_004 -->|"verification allocation"| VER_008
    VER_008 -.->|"execution evidence missing"| GAP_VER_001
```

### 11. End-to-end architecture trace

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
    VER_001["VER-001<br/>Requirement and architecture analysis<br/>[PROPOSED]"]
    GAP_VER_001["GAP-VER-001<br/>Execution evidence missing<br/>[UNRESOLVED]"]
    NEED_001 -->|"motivates"| CAP_001
    CAP_001 -->|"exercised by"| SCN_003
    SCN_003 -->|"uses"| OA_004
    OA_004 -->|"information exchange"| IX_002
    IX_002 -->|"supports"| FUN_REL_01
    FUN_REL_01 -->|"allocated to"| CMP_COM_01
    CMP_COM_01 -->|"external interface"| IFC_EXT_001
    IFC_EXT_001 -->|"allocated requirement"| REQ_FUN_001
    REQ_FUN_001 -->|"verification allocation"| VER_001
    VER_001 -.->|"execution evidence unresolved"| GAP_VER_001
```

### 12. Evidence and approval governance

Configuration scope: `Project governance - CFG-REC evidence semantics - all configurations remain not approved`.

Evidence supports claims; it does not approve architecture. Proposed decisions require explicit owner action.

```mermaid
flowchart LR
    %% Configuration scope: Project governance - CFG-REC evidence semantics - all configurations remain not approved
    SRC_INT_001["SRC-INT-001<br/>Recovered-article research report<br/>registered source"]
    EVD_002["EVD-002<br/>EVD-002<br/>registered evidence record"]
    CLM_REC_001["CLM-REC-001<br/>Recovered-article flight-controller identification record<br/>source-supported claim"]
    CFG_REC["CFG-REC<br/>Reference evidence<br/>descriptive evidence configuration"]
    CLM_REC_005["CLM-REC-005<br/>Recovered-to-generic model reconciliation<br/>generic mapping not demonstrated"]
    GAP_REC_001["GAP-REC-001<br/>Recovered-to-candidate mapping unresolved<br/>unresolved mapping gap"]
    DEC_002["DEC-002<br/>Select UAF terminology and version posture<br/>proposed owner decision"]
    GAP_STD_001["GAP-STD-001<br/>UAF version decision unresolved<br/>unresolved standards decision"]
    BASELINE["Baseline Candidate - Not Approved<br/>model-valid may still be gapped"]
    SRC_INT_001 -->|"registered as"| EVD_002
    EVD_002 -->|"supports - does not approve"| CLM_REC_001
    CLM_REC_001 -->|"applicable to evidence configuration"| CFG_REC
    CLM_REC_005 -->|"prevents silent proposed-resource inheritance"| CFG_REC
    CFG_REC -.->|"mapping unresolved"| GAP_REC_001
    DEC_002 -.->|"owner review required"| GAP_STD_001
    GAP_REC_001 -->|"gap remains visible"| BASELINE
    GAP_STD_001 -->|"gap remains visible"| BASELINE
```

## Generated interface inventory

This inventory is generated directly from `model/architecture.yaml`. Empty
verification cells are explicit gaps, not evidence of completion.

| ID | Endpoints | Direction | Flow class | Configurations | Maturity | Verification | Unknown attributes |
|---|---|---|---|---|---|---|---|
| IFC-INT-001 | CMP-PWR-02 to CMP-PRP-02 | a_to_b | electrical power | CFG-REP, CFG-DOM | proposed_design / proposed | VER-005, VER-008 | voltage; current; connector; protection; wiring allocation |
| IFC-INT-002 | CMP-PWR-03 to CMP-AVN-01 | a_to_b | electrical power | CFG-REP, CFG-DOM | proposed_design / proposed | VER-005, VER-008 | voltage; current; connector; power-quality envelope |
| IFC-INT-003 | CMP-PWR-03 to CMP-COM-01 | a_to_b | electrical power | CFG-REP, CFG-DOM | proposed_design / proposed | VER-005, VER-008 | voltage envelope; current envelope; connector; protection; thermal allocation |
| IFC-INT-004 | CMP-AVN-01 to CMP-PRP-02 | a_to_b | command and control | CFG-REP, CFG-DOM | proposed_design / proposed | VER-005, VER-008 | signal format; timing; connector; fault response |
| IFC-INT-005 | CMP-AVN-04 to CMP-AVN-01 | a_to_b | command and control | CFG-REP, CFG-DOM | proposed_design / proposed | VER-005, VER-008 | protocol; connector; timing; failsafe behavior |
| IFC-INT-006 | CMP-PWR-02 to CMP-AVN-01 | a_to_b | health and status | CFG-REP, CFG-DOM | proposed_design / proposed | VER-005, VER-008 | measurement set; accuracy; update rate; connector; fault indication |
| IFC-INT-007 | CMP-MNT-01 to CMP-COM-01 | bidirectional_physical | mechanical mounting | CFG-REP, CFG-DOM | proposed_design / proposed | VER-005, VER-008 | geometry; load envelope; retention margin; inspection criteria |
| IFC-EXT-001 | OP-001 to CMP-COM-01 | a_to_b | command and control | CFG-REP, CFG-DOM | proposed_design / proposed | None - explicit gap | frequency; waveform; protocol; power; data rate; message format; endpoint compatibility; verification authority |
| IFC-EXT-002 | CMP-COM-01 to OP-003 | a_to_b | command and control | CFG-REP, CFG-DOM | proposed_design / proposed | None - explicit gap | frequency; waveform; protocol; power; data rate; message format; endpoint compatibility; verification authority |
| IFC-EXT-003 | OP-003 to CMP-COM-01 | a_to_b | telemetry | CFG-REP, CFG-DOM | proposed_design / proposed | None - explicit gap | frequency; waveform; protocol; power; data rate; message format; endpoint compatibility; verification authority |
| IFC-EXT-004 | CMP-COM-01 to OP-001 | a_to_b | telemetry | CFG-REP, CFG-DOM | proposed_design / proposed | None - explicit gap | frequency; waveform; protocol; power; data rate; message format; endpoint compatibility; verification authority |
| IFC-EXT-005 | OP-010 to CMP-AVN-04 | a_to_b | command and control | CFG-REP, CFG-DOM | proposed_design / proposed | None - explicit gap | frequency; waveform; protocol; power; message format; failsafe behavior; verification authority |
| IFC-INT-008 | CMP-AVN-01 to CMP-COM-01 | bidirectional | payload management and health and status | CFG-DIG, CFG-SOS | proposed_design / proposed | VER-004, VER-005, VER-007 | adoption decision; data model; protocol; connector; timing; authority; failure response |
| IFC-INT-009 | CMP-AVN-02 to CMP-AVN-01 | a_to_b | navigation and timing | CFG-REP, CFG-DOM | engineering_inference / proposed | VER-005, VER-008 | sensor set; data format; timing; accuracy; fault detection; connector |
| IFC-INT-010 | CMP-COM-01 to CMP-COM-02 | bidirectional_physical | physical-resource coupling | CFG-REP, CFG-DOM | proposed_design / proposed | None - explicit gap | antenna count; role; placement; connector; all RF characteristics |
| IFC-EXT-006 | OP-007 to OP-002 | bidirectional | configuration and maintenance | CFG-REP, CFG-DOM, CFG-DIG, CFG-SOS | proposed_design / proposed | VER-004, VER-005, VER-007 | data set; format; transport; authorization; retention period; tool ownership |

## Validation notes

- Optional syntax validation expects Mermaid CLI `mmdc` 11.4.1 when installed locally.
- Absence of Node.js or the pinned CLI does not invalidate standard-library catalog validation.
- No generated SVG or PNG is required; GitHub-rendered Markdown is the primary artifact.
