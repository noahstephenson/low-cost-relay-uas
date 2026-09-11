<!-- GENERATED VIEW: DO NOT EDIT. Run python scripts/generate-mermaid-views.py -->
# Architecture Atlas

> **Baseline Candidate - Not Approved.** These diagrams are generated from
> `model/system.yaml`, catalogs under `model/`, and `.seal/proof.yaml`. They have no
> independent architecture authority. Candidate, proposed, deferred, and
> unresolved labels do not imply approval or executed verification.

The diagrams deliberately omit RF implementation values, build instructions,
operating procedures, and recovered implementation detail. `CFG-REC` is shown
only as a descriptive evidence configuration and does not inherit the proposed
`CFG-REP`/`CFG-DOM` resource decomposition.
This report is the ID-rich engineering drill-down. Plain-language canonical
figures are generated separately under `docs/figures/`.
Start with [Architecture](../architecture.md) for the subsystem explanation. These reference views retain stable IDs; full qualifiers live in the companion tables.

## Configuration and context views

### 1. What is current, reference, and future?

Configuration scope: `CFG-REC / CFG-REP / CFG-DOM / CFG-DIG / CFG-SOS`.

Derivation denotes lineage, not exact inheritance, equivalence, or approval. Future context is outside the current implementation baseline.

<details>
<summary>Open what is current, reference, and future? diagram and detail table</summary>

```mermaid
%%{init: {"theme": "neutral", "htmlLabels": false, "themeVariables": {"fontSize": "18px"}, "flowchart": {"htmlLabels": false, "nodeSpacing": 35, "rankSpacing": 45}}}%%
flowchart LR
    %% Configuration scope: CFG-REC / CFG-REP / CFG-DOM / CFG-DIG / CFG-SOS
    CFG_REC["CFG-REC<br/>Reference evidence"]
    CFG_REP["CFG-REP<br/>Replica candidate"]
    CFG_DOM["CFG-DOM<br/>Domestic candidate"]
    CFG_DIG["CFG-DIG<br/>Digital extension"]
    CFG_SOS["CFG-SOS<br/>C2 Ecosystem context"]
    CFG_REC -->|"R1"| CFG_REP
    CFG_REP -->|"R2"| CFG_DOM
    CFG_REP -->|"R3"| CFG_DIG
    CFG_DIG -->|"R4"| CFG_SOS
```

The picture shows connections. Full names, status qualifiers, and numbered relationship labels are below.

| Diagram key | Full description |
|---|---|
| `CFG_REC` | CFG-REC; Reference evidence; evidence only - role mapping narrowed |
| `CFG_REP` | CFG-REP; Replica candidate; current proposed baseline |
| `CFG_DOM` | CFG-DOM; Domestic candidate; current - substitution criteria unresolved |
| `CFG_DIG` | CFG-DIG; Digital extension; future - adds IFC-INT-008 candidate |
| `CFG_SOS` | CFG-SOS; C2 Ecosystem context; future outer context - OP-004 / OP-005 / OP-006 |
| `R1` | proposed functional derivation, not an exact clone; derivation is not approval |
| `R2` | proposed substitution architecture; derivation is not approval |
| `R3` | future concept branch; derivation is not approval |
| `R4` | outer system-of-systems context containing the relay UAS as one constituent; derivation is not approval |

</details>

### 2. What is inside the project boundary?

Configuration scope: `CFG-SOS outer context - CFG-REP / CFG-DOM / CFG-DIG inner constituent`.

External constituents remain independently managed. Only catalogued information exchanges are drawn; unconnected future actors remain context, not implied interfaces.

<details>
<summary>Open what is inside the project boundary? diagram and detail table</summary>

```mermaid
%%{init: {"theme": "neutral", "htmlLabels": false, "themeVariables": {"fontSize": "18px"}, "flowchart": {"htmlLabels": false, "nodeSpacing": 35, "rankSpacing": 45}}}%%
flowchart TB
    %% Configuration scope: CFG-SOS outer context - CFG-REP / CFG-DOM / CFG-DIG inner constituent
    subgraph OUTER["External context"]
        OP_010["OP-010<br/>Operator"]
        OP_001["OP-001<br/>Ground Control"]
        OP_003["OP-003<br/>Remote UAS"]
        OP_004["OP-004<br/>UGV"]
        OP_005["OP-005<br/>Radio User"]
        OP_006["OP-006<br/>Network Service"]
        OP_007["OP-007<br/>Maintenance"]
        OP_008["OP-008<br/>Spectrum-Management<br/>Authority"]
        OP_009["OP-009<br/>Supporting Infrastructure"]
        subgraph INNER["Relay UAS"]
            OP_002["OP-002<br/>Relay UAS"]
        end
    end
    OP_010 -->|"R1"| OP_002
    OP_001 -->|"R2"| OP_002
    OP_002 -->|"R3"| OP_003
    OP_003 -->|"R4"| OP_002
    OP_002 -->|"R5"| OP_001
    OP_001 -.->|"R6"| OP_004
    OP_004 -.->|"R7"| OP_001
    OP_002 -->|"R8"| OP_010
    OP_007 -->|"R9"| OP_002
```

The picture shows connections. Full names, status qualifiers, and numbered relationship labels are below.

| Diagram key | Full description |
|---|---|
| `OUTER` | C2 Ecosystem outer boundary - CFG-SOS proposed context |
| `OP_010` | OP-010; Operator; independently managed human performer |
| `OP_001` | OP-001; Ground Control; independently managed external system |
| `OP_003` | OP-003; Remote UAS; independently managed external system |
| `OP_004` | OP-004; UGV; future / unresolved |
| `OP_005` | OP-005; Radio User; future / unresolved |
| `OP_006` | OP-006; Network Service; future / unresolved |
| `OP_007` | OP-007; Maintenance; external support performer |
| `OP_008` | OP-008; Spectrum-Management Authority; independent authority |
| `OP_009` | OP-009; Supporting Infrastructure; future / unresolved |
| `INNER` | Relay UAS inner boundary - proposed for CFG-REP/CFG-DOM/CFG-DIG |
| `OP_002` | OP-002; Relay UAS; system under study |
| `R1` | IX-001 / IFC-EXT-005; command and control |
| `R2` | IX-002 / IFC-EXT-001; command and control |
| `R3` | IX-003 / IFC-EXT-002; command and control |
| `R4` | IX-004 / IFC-EXT-003; telemetry |
| `R5` | IX-005 / IFC-EXT-004; telemetry |
| `R6` | IX-006 / unresolved; command and control |
| `R7` | IX-007 / unresolved; telemetry |
| `R8` | IX-009 / IFC-EXT-007; health and status |
| `R9` | IX-010 / IFC-EXT-006; configuration and maintenance |

</details>

### 3. How current-system traffic moves

Configuration scope: `CFG-REP / CFG-DOM`.

`IX-001` is independent Relay-UAS platform command. `IX-002` through `IX-005` are relayed mission traffic.

<details>
<summary>Open how current-system traffic moves diagram and detail table</summary>

```mermaid
%%{init: {"theme": "neutral", "htmlLabels": false, "themeVariables": {"fontSize": "18px"}, "flowchart": {"htmlLabels": false, "nodeSpacing": 35, "rankSpacing": 45}}}%%
flowchart LR
    %% Configuration scope: CFG-REP / CFG-DOM
    OP_010["OP-010<br/>Operator"]
    OP_001["OP-001<br/>Ground Control"]
    OP_002["OP-002<br/>Relay UAS"]
    OP_003["OP-003<br/>Remote UAS"]
    OP_010 -->|"R1"| OP_002
    OP_001 -->|"R2"| OP_002
    OP_002 -->|"R3"| OP_003
    OP_003 -->|"R4"| OP_002
    OP_002 -->|"R5"| OP_001
```

The picture shows connections. Full names, status qualifiers, and numbered relationship labels are below.

| Diagram key | Full description |
|---|---|
| `OP_010` | OP-010; Operator |
| `OP_001` | OP-001; Ground Control |
| `OP_002` | OP-002; Relay UAS |
| `OP_003` | OP-003; Remote UAS |
| `R1` | IX-001 / IFC-EXT-005; command and control |
| `R2` | IX-002 / IFC-EXT-001; command and control |
| `R3` | IX-003 / IFC-EXT-002; command and control |
| `R4` | IX-004 / IFC-EXT-003; telemetry |
| `R5` | IX-005 / IFC-EXT-004; telemetry |

</details>

## Selected resource connectivity views

### 4B. How power and propulsion connect

Configuration scope: `CFG-REP / CFG-DOM`.

<details>
<summary>Open how power and propulsion connect diagram and detail table</summary>

```mermaid
%%{init: {"theme": "neutral", "htmlLabels": false, "themeVariables": {"fontSize": "18px"}, "flowchart": {"htmlLabels": false, "nodeSpacing": 35, "rankSpacing": 45}}}%%
flowchart TB
    %% Configuration scope: CFG-REP / CFG-DOM
    CMP_PWR_01["CMP-PWR-01<br/>Battery"]
    CMP_PWR_02["CMP-PWR-02<br/>Main Power Distribution"]
    CMP_PWR_03["CMP-PWR-03<br/>Power Regulators"]
    CMP_PWR_04["CMP-PWR-04<br/>Battery Connection"]
    CMP_PRP_01["CMP-PRP-01<br/>Motors"]
    CMP_PRP_02["CMP-PRP-02<br/>Motor Controllers"]
    CMP_PRP_03["CMP-PRP-03<br/>Propellers"]
    CMP_AVN_01["CMP-AVN-01<br/>Flight Controller"]
    CMP_COM_01["CMP-COM-01<br/>Relay Payload (Black Box)"]
    CMP_PWR_01 -->|"R1"| CMP_PWR_02
    CMP_PWR_04 -.->|"R2"| CMP_PWR_02
    CMP_PWR_02 -->|"R3"| CMP_PRP_02
    CMP_PWR_02 -->|"R4"| CMP_PWR_03
    CMP_PWR_03 -->|"R5"| CMP_AVN_01
    CMP_PWR_03 -->|"R6"| CMP_COM_01
    CMP_PWR_02 -->|"R7"| CMP_AVN_01
    CMP_PRP_02 -->|"R8"| CMP_PRP_01
    CMP_PRP_01 -->|"R9"| CMP_PRP_03
```

The picture shows connections. Full names, status qualifiers, and numbered relationship labels are below.

| Diagram key | Full description |
|---|---|
| `CMP_PWR_01` | CMP-PWR-01; Battery |
| `CMP_PWR_02` | CMP-PWR-02; Main Power Distribution |
| `CMP_PWR_03` | CMP-PWR-03; Power Regulators |
| `CMP_PWR_04` | CMP-PWR-04; Battery Connection |
| `CMP_PRP_01` | CMP-PRP-01; Motors |
| `CMP_PRP_02` | CMP-PRP-02; Motor Controllers |
| `CMP_PRP_03` | CMP-PRP-03; Propellers |
| `CMP_AVN_01` | CMP-AVN-01; Flight Controller |
| `CMP_COM_01` | CMP-COM-01; Relay Payload (Black Box) |
| `R1` | IFC-INT-011; electrical power |
| `R2` | physical connection resource; IFC-INT-011 |
| `R3` | IFC-INT-001; electrical power |
| `R4` | IFC-INT-015; electrical power |
| `R5` | IFC-INT-002; electrical power |
| `R6` | IFC-INT-003; electrical power; platform-to-payload |
| `R7` | IFC-INT-006; health and status |
| `R8` | IFC-INT-013; controlled electrical propulsion power |
| `R9` | IFC-INT-014; mechanical propulsion drive |

</details>

### 4C. How platform control works

Configuration scope: `CFG-REP / CFG-DOM`.

<details>
<summary>Open how platform control works diagram and detail table</summary>

```mermaid
%%{init: {"theme": "neutral", "htmlLabels": false, "themeVariables": {"fontSize": "18px"}, "flowchart": {"htmlLabels": false, "nodeSpacing": 35, "rankSpacing": 45}}}%%
flowchart LR
    %% Configuration scope: CFG-REP / CFG-DOM
    OP_010["OP-010<br/>Operator"]
    CMP_AVN_01["CMP-AVN-01<br/>Flight Controller"]
    CMP_AVN_02["CMP-AVN-02<br/>Flight Sensors"]
    CMP_AVN_03["CMP-AVN-03<br/>Navigation Sensor"]
    CMP_AVN_04["CMP-AVN-04<br/>Platform Command Receiver"]
    CMP_PRP_02["CMP-PRP-02<br/>Motor Controllers"]
    CMP_PWR_02["CMP-PWR-02<br/>Main Power Distribution"]
    OP_010 -->|"R1"| CMP_AVN_04
    CMP_AVN_04 -->|"R2"| CMP_AVN_01
    CMP_AVN_01 -->|"R3"| CMP_PRP_02
    CMP_PWR_02 -->|"R4"| CMP_AVN_01
    CMP_AVN_02 -->|"R5"| CMP_AVN_01
    CMP_AVN_03 -->|"R6"| CMP_AVN_01
```

The picture shows connections. Full names, status qualifiers, and numbered relationship labels are below.

| Diagram key | Full description |
|---|---|
| `OP_010` | OP-010; Operator |
| `CMP_AVN_01` | CMP-AVN-01; Flight Controller |
| `CMP_AVN_02` | CMP-AVN-02; Flight Sensors |
| `CMP_AVN_03` | CMP-AVN-03; Navigation Sensor |
| `CMP_AVN_04` | CMP-AVN-04; Platform Command Receiver |
| `CMP_PRP_02` | CMP-PRP-02; Motor Controllers |
| `CMP_PWR_02` | CMP-PWR-02; Main Power Distribution |
| `R1` | IFC-EXT-005; command and control; separate platform command |
| `R2` | IFC-INT-005; command and control |
| `R3` | IFC-INT-004; command and control |
| `R4` | IFC-INT-006; health and status |
| `R5` | IFC-INT-009; navigation and timing |
| `R6` | IFC-INT-012; navigation and timing |

</details>

### 4D. How the relay payload is bounded

Configuration scope: `CFG-REP / CFG-DOM`.

`IFC-INT-010` stays inside the payload black-box envelope. Only `IFC-INT-003` and `IFC-INT-007` cross from platform to payload.

<details>
<summary>Open how the relay payload is bounded diagram and detail table</summary>

```mermaid
%%{init: {"theme": "neutral", "htmlLabels": false, "themeVariables": {"fontSize": "18px"}, "flowchart": {"htmlLabels": false, "nodeSpacing": 35, "rankSpacing": 45}}}%%
flowchart LR
    %% Configuration scope: CFG-REP / CFG-DOM
    OP_001["OP-001<br/>Ground Control"]
    OP_003["OP-003<br/>Remote UAS"]
    CMP_PWR_03["CMP-PWR-03<br/>Power Regulators"]
    CMP_MNT_01["CMP-MNT-01<br/>Modular Payload Bay"]
    subgraph PAYLOAD["Payload boundary"]
        CMP_COM_01["CMP-COM-01<br/>Relay Payload (Black Box)"]
        CMP_COM_02["CMP-COM-02<br/>Payload Antenna Envelope"]
        CMP_COM_01 <-->|"R1"| CMP_COM_02
    end
    CMP_PWR_03 -->|"R2"| CMP_COM_01
    CMP_MNT_01 <-->|"R3"| CMP_COM_01
    OP_001 -->|"R4"| CMP_COM_01
    CMP_COM_01 -->|"R5"| OP_003
    OP_003 -->|"R6"| CMP_COM_01
    CMP_COM_01 -->|"R7"| OP_001
```

The picture shows connections. Full names, status qualifiers, and numbered relationship labels are below.

| Diagram key | Full description |
|---|---|
| `OP_001` | OP-001; Ground Control |
| `OP_003` | OP-003; Remote UAS |
| `CMP_PWR_03` | CMP-PWR-03; Power Regulators |
| `CMP_MNT_01` | CMP-MNT-01; Modular Payload Bay |
| `PAYLOAD` | Relay-payload black-box envelope |
| `CMP_COM_01` | CMP-COM-01; Relay Payload (Black Box) |
| `CMP_COM_02` | CMP-COM-02; Payload Antenna Envelope; physical-resource envelope |
| `R1` | IFC-INT-010; physical-resource coupling; payload-internal - characteristics undefined |
| `R2` | IFC-INT-003; electrical power; platform boundary crossing |
| `R3` | IFC-INT-007; mechanical mounting; platform boundary crossing |
| `R4` | IFC-EXT-001; command and control; implementation undefined |
| `R5` | IFC-EXT-002; command and control; implementation undefined |
| `R6` | IFC-EXT-003; telemetry; implementation undefined |
| `R7` | IFC-EXT-004; telemetry; implementation undefined |

</details>

## Evidence correspondence view

### 4G. How recovered evidence informs candidate roles

Configuration scope: `CFG-REC informs CFG-REP / CFG-DOM - no exact inheritance`.

This is a grouped view of the controlled record-level mapping. Five recovered records remain unmatched and one remains unknown; no contradiction was found.

<details>
<summary>Open how recovered evidence informs candidate roles diagram and detail table</summary>

```mermaid
%%{init: {"theme": "neutral", "htmlLabels": false, "themeVariables": {"fontSize": "18px"}, "flowchart": {"htmlLabels": false, "nodeSpacing": 35, "rankSpacing": 45}}}%%
flowchart LR
    %% Configuration scope: CFG-REC informs CFG-REP / CFG-DOM - no exact inheritance
    REC_STRUCTURE["Recovered structure and<br/>hardware"] -->|"direct / class-level support"| CAND_STRUCTURE["CMP-AFR-01 through CMP-<br/>AFR-05"]
    REC_PROPULSION["Recovered propulsion<br/>resources"] -->|"direct role support"| CAND_PROPULSION["CMP-PRP-01 through CMP-<br/>PRP-03"]
    REC_POWER["Recovered power resources<br/>and harness"] -->|"R1"| CAND_POWER["CMP-PWR-01 through CMP-<br/>PWR-04"]
    REC_AVIONICS["Recovered control and<br/>navigation resources"] -->|"direct / partial support"| CAND_AVIONICS["CMP-AVN-01 through CMP-<br/>AVN-04"]
    REC_PAYLOAD["Recovered payload modules<br/>and antennas"] -->|"partial / inferred correspondence"| CAND_PAYLOAD["CMP-COM-01 / CMP-COM-02"]
    REC_MOUNTING["Recovered payload<br/>retention"] -->|"partial role support"| CAND_MOUNTING["CMP-MNT-01"]
```

The picture shows connections. Full names, status qualifiers, and numbered relationship labels are below.

| Diagram key | Full description |
|---|---|
| `REC_STRUCTURE` | Recovered structure and hardware |
| `CAND_STRUCTURE` | CMP-AFR-01 through CMP-AFR-05 |
| `REC_PROPULSION` | Recovered propulsion resources |
| `CAND_PROPULSION` | CMP-PRP-01 through CMP-PRP-03 |
| `REC_POWER` | Recovered power resources and harness |
| `CAND_POWER` | CMP-PWR-01 through CMP-PWR-04 |
| `R1` | direct / partial / unknown |
| `REC_AVIONICS` | Recovered control and navigation resources |
| `CAND_AVIONICS` | CMP-AVN-01 through CMP-AVN-04 |
| `REC_PAYLOAD` | Recovered payload modules and antennas |
| `CAND_PAYLOAD` | CMP-COM-01 / CMP-COM-02 |
| `REC_MOUNTING` | Recovered payload retention |
| `CAND_MOUNTING` | CMP-MNT-01 |

</details>

## Behavioral views

### 5. How operating modes change

Configuration scope: `CFG-REP / CFG-DOM`.

Only transitions supported by current scenarios or requirements are shown; all remain candidate unless stated otherwise.

<details>
<summary>Open how operating modes change diagram</summary>

```mermaid
%%{init: {"htmlLabels": false, "theme": "neutral"}}%%
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
    MODE_003 --> MODE_004: SCN-007 / REQ-007 - recovery intent
    MODE_002 --> MODE_004: SCN-008 / REQ-005 - normal termination or low-battery recovery
    MODE_004 --> MODE_005: SCN-008 - platform recovered and made ground safe
    note right of MODE_003
      Payload function degraded
      Platform control may remain available
      REQ-007 [PROPOSED]
      Evidence [DEFERRED]
    end note
```

</details>

### 7A. Carrier command path

Configuration scope: `CFG-REP / CFG-DOM`.

Carrier command is logically separate from the relay payload; isolation and link performance are not verified.

<details>
<summary>Open carrier command path diagram</summary>

```mermaid
%%{init: {"theme": "neutral"}}%%
sequenceDiagram
    %% Configuration scope: CFG-REP / CFG-DOM
    participant Operator as OP-010 Platform<br/>operator
    participant Platform as CMP-AVN-04 Platform<br/>command receiver
    Operator->>Platform: IX-001 / IFC-EXT-005 separate Relay-UAS<br/>platform command
```

</details>

### 7B. Relayed mission traffic

Configuration scope: `CFG-REP / CFG-DOM`.

The conceptual service includes return telemetry. Only outbound stationary service is quantitatively screened.

<details>
<summary>Open relayed mission traffic diagram</summary>

```mermaid
%%{init: {"theme": "neutral"}}%%
sequenceDiagram
    %% Configuration scope: CFG-REP / CFG-DOM
    participant Ground as OP-001 Ground<br/>control node
    participant Payload as CMP-COM-01 Relay<br/>payload black box
    participant Remote as OP-003 Remote UAS
    rect rgb(245, 245, 245)
        Ground->>Payload: IX-002 / IFC-EXT-001 outbound traffic
        Payload->>Remote: IX-003 / IFC-EXT-002 outbound traffic
        Remote-->>Payload: IX-004 / IFC-EXT-003 return telemetry
        Payload-->>Ground: IX-005 / IFC-EXT-004 return telemetry
    end
    Note over Ground,Remote: SCN-003 / SCN-004 logical relay only -<br/>external paths undefined
```

</details>

### 8. What happens on relay degradation?

Configuration scope: `CFG-REP / CFG-DOM`.

The second path terminates at explicit gaps; it does not invent a recovery behavior.

<details>
<summary>Open what happens on relay degradation? diagram</summary>

```mermaid
%%{init: {"theme": "neutral"}}%%
sequenceDiagram
    %% Configuration scope: CFG-REP / CFG-DOM
    participant Ground as OP-001 Ground<br/>control node
    participant Payload as CMP-COM-01 Relay<br/>payload black box
    participant Relay as OP-002 Relay UAS<br/>platform
    participant Operator as OP-010 Platform<br/>operator
    Payload--xGround: SCN-007 relay function loss or degradation
    Relay-->>Operator: IX-009 / IFC-EXT-007 health/status<br/>[PROPOSED]
    Operator->>Relay: IX-001 / IFC-EXT-005 independent platform<br/>command
    alt Payload lost and platform remains controllable
        Note over Payload,Relay: MODE-003 - CTL-004 / REQ-007 [PROPOSED]
        Relay-->>Operator: transition intent toward MODE-004 Return /<br/>Recovery
    else Platform control also impaired
        Note over Relay,Operator: HAZ-001 / GAP-HAZ-001 - no modeled<br/>consequence-management behavior
        Note over Ground,Operator: GAP-VER-001 - no executed recovery<br/>evidence
    end
```

</details>

### 9B. Why mass, power, endurance, and cost are coupled

Configuration scope: `CFG-REP / CFG-DOM`.

This is one coupled design problem. The diagram adds no values and does not resolve any trade study.

<details>
<summary>Open why mass, power, endurance, and cost are coupled diagram and detail table</summary>

```mermaid
%%{init: {"theme": "neutral", "htmlLabels": false, "themeVariables": {"fontSize": "18px"}, "flowchart": {"htmlLabels": false, "nodeSpacing": 35, "rankSpacing": 45}}}%%
flowchart TB
    %% Configuration scope: CFG-REP / CFG-DOM
    REQ_012["REQ-012<br/>Accommodate payload<br/>envelope"]
    TS_006["TS-006<br/>Payload mount interface<br/>standard"]
    TS_001["TS-001<br/>Airframe material and<br/>construction method"]
    REQ_011["REQ-011<br/>Limit system gross mass"]
    TS_002["TS-002<br/>Propulsion sizing"]
    TS_004["TS-004<br/>Payload power allocation"]
    REQ_010["REQ-010<br/>Provide on-station<br/>endurance"]
    TS_003["TS-003<br/>Battery architecture"]
    REQ_009["REQ-009<br/>Limit system unit cost"]
    GAP_BUDGET_001["GAP-BUDGET-001<br/>Coupled targets and<br/>evidence unresolved"]
    REQ_012 -->|"contributes to"| REQ_011
    TS_002 -->|"coupled to"| TS_003
    TS_004 -->|"constrains"| TS_003
    TS_006 -->|"defines envelope for"| REQ_012
    TS_001 -->|"contributes mass to"| REQ_011
    REQ_011 -->|"drives"| TS_002
    REQ_010 -->|"sets energy demand for"| TS_003
    TS_003 -->|"contributes mass to"| REQ_011
    TS_003 -->|"contributes cost to"| REQ_009
    REQ_009 -.->|"remains blocked by"| GAP_BUDGET_001
```

The picture shows connections. Full names, status qualifiers, and numbered relationship labels are below.

| Diagram key | Full description |
|---|---|
| `REQ_012` | REQ-012; Accommodate payload envelope; [PROPOSED] |
| `TS_006` | TS-006; Payload mount interface standard; [PROPOSED] |
| `TS_001` | TS-001; Airframe material and construction method; [PROPOSED] |
| `REQ_011` | REQ-011; Limit system gross mass; [PROPOSED] |
| `TS_002` | TS-002; Propulsion sizing; [PROPOSED] |
| `TS_004` | TS-004; Payload power allocation; [PROPOSED] |
| `REQ_010` | REQ-010; Provide on-station endurance; [PROPOSED] |
| `TS_003` | TS-003; Battery architecture; [PROPOSED] |
| `REQ_009` | REQ-009; Limit system unit cost; [PROPOSED] |
| `GAP_BUDGET_001` | GAP-BUDGET-001; Coupled targets and evidence unresolved; [UNRESOLVED] |

</details>

## Assurance and traceability views

### 10A. What has been checked and what still needs evidence?

Configuration scope: `CFG-REP / CFG-DOM with project-scope deferrals`.

VER-001 through VER-007 have 0.8.0 model-level evidence in EVD-013 but no owner acceptance. The current 0.9.0 identifier and documentation refactor has no new evidence record. EVD-008 through EVD-012 preserve the accepted 0.7.0 work package. VER-008 remains deferred and VER-009 remains blocked; none of these records constitutes physical verification, external conformance, safety approval, or technical-baseline approval.

<details>
<summary>Open what has been checked and what still needs evidence? diagram and detail table</summary>

```mermaid
%%{init: {"theme": "neutral", "htmlLabels": false, "themeVariables": {"fontSize": "18px"}, "flowchart": {"htmlLabels": false, "nodeSpacing": 35, "rankSpacing": 45}}}%%
flowchart LR
    %% Configuration scope: CFG-REP / CFG-DOM with project-scope deferrals
    ACCEPTED["Accepted review<br/>0.7.0 / EVD-008 through<br/>EVD-012"]
    EXECUTED["Latest model review<br/>0.8.0 / VER-001 through<br/>VER-007"]
    PASS["Review pass<br/>VER-002 / VER-007"]
    OPEN["Review with gaps<br/>VER-001 / VER-003 through<br/>VER-006"]
    PHYSICAL["Physical evidence needed<br/>REQ-006 / REQ-008"]
    EXTERNAL["External authority needed<br/>REQ-001 / REQ-004"]
    DEFERRED["Deferred scope<br/>DEF-001 / DEF-004"]
    VER_008["VER-008<br/>Deferred physical<br/>verification method"]
    VER_009["VER-009<br/>External conformance<br/>verification"]
    TS_009["TS-009<br/>Relay payload<br/>characterization"]
    ACCEPTED -->|"historical acceptance boundary preserved"| EXECUTED
    EXECUTED -->|"no structural failure"| PASS
    EXECUTED -->|"known gaps retained"| OPEN
    PHYSICAL -.->|"no execution evidence"| VER_008
    EXTERNAL -.->|"authority and specification absent"| VER_009
    DEFERRED -.->|"outside current scope"| TS_009
```

The picture shows connections. Full names, status qualifiers, and numbered relationship labels are below.

| Diagram key | Full description |
|---|---|
| `ACCEPTED` | PRESERVED OWNER-ACCEPTED REVIEW; 0.7.0 / EVD-008 through EVD-012 |
| `EXECUTED` | LATEST RECORDED MODEL REVIEW; 0.8.0 / VER-001 through VER-007; EVD-013 - not owner accepted |
| `PASS` | EXECUTED PASS; VER-002 / VER-007 |
| `OPEN` | EXECUTED WITH OPEN GAPS; VER-001 / VER-003 through VER-006 |
| `PHYSICAL` | PHYSICAL-EVIDENCE-REQUIRED; REQ-006 / REQ-008; GAP-VER-001 |
| `EXTERNAL` | EXTERNAL-AUTHORITY-REQUIRED; REQ-001 / REQ-004; GAP-IFC-001 |
| `DEFERRED` | INTENTIONALLY-DEFERRED; DEF-001 / DEF-004 |
| `VER_008` | VER-008; Deferred physical verification method; future physical evidence |
| `VER_009` | VER-009; External conformance verification; external authority required |
| `TS_009` | TS-009; Relay payload characterization; formal deferral |

</details>

### 11A. Relay trace: need to payload

Configuration scope: `CFG-REP / CFG-DOM`.

Follow the need to its allocated payload role; continue at CMP-COM-01 in 11B.

<details>
<summary>Open relay trace: need to payload diagram and detail table</summary>

```mermaid
%%{init: {"theme": "neutral", "htmlLabels": false, "themeVariables": {"fontSize": "18px"}, "flowchart": {"htmlLabels": false, "nodeSpacing": 35, "rankSpacing": 45}}}%%
flowchart TB
    %% Configuration scope: CFG-REP / CFG-DOM
    NEED_001["NEED-001<br/>Extend mission reach"]
    CAP_001["CAP-001<br/>Beyond-Line-of-Sight<br/>Control"]
    SCN_003["SCN-003<br/>Remote-UAS command<br/>through the relay"]
    OA_004["OA-004<br/>Relay outbound traffic"]
    IX_002["IX-002<br/>Remote-UAS command toward<br/>relay"]
    FUN_REL_01["FUN-REL-01<br/>Relay outbound traffic"]
    CMP_COM_01["CMP-COM-01<br/>Relay Payload (Black Box)"]
    NEED_001 -->|"motivates"| CAP_001
    CAP_001 -->|"exercised by"| SCN_003
    SCN_003 -->|"uses"| OA_004
    OA_004 -->|"information exchange"| IX_002
    IX_002 -->|"supports"| FUN_REL_01
    FUN_REL_01 -->|"allocated to"| CMP_COM_01
```

The picture shows connections. Full names, status qualifiers, and numbered relationship labels are below.

| Diagram key | Full description |
|---|---|
| `NEED_001` | NEED-001; Extend mission reach; [PROPOSED] |
| `CAP_001` | CAP-001; Beyond-Line-of-Sight Control; [PROPOSED] |
| `SCN_003` | SCN-003; Remote-UAS command through the relay; [PROPOSED] |
| `OA_004` | OA-004; Relay outbound traffic; [PROPOSED] |
| `IX_002` | IX-002; Remote-UAS command toward relay; [PROPOSED] |
| `FUN_REL_01` | FUN-REL-01; Relay outbound traffic; [PROPOSED] |
| `CMP_COM_01` | CMP-COM-01; Relay Payload (Black Box); [PROPOSED] |

</details>

### 11B. Relay trace: payload to evidence

Configuration scope: `CFG-REP / CFG-DOM`.

Continue from CMP-COM-01 in 11A. Model review and external conformance are different evidence obligations.

<details>
<summary>Open relay trace: payload to evidence diagram and detail table</summary>

```mermaid
%%{init: {"theme": "neutral", "htmlLabels": false, "themeVariables": {"fontSize": "18px"}, "flowchart": {"htmlLabels": false, "nodeSpacing": 35, "rankSpacing": 45}}}%%
flowchart TB
    %% Configuration scope: CFG-REP / CFG-DOM
    CMP_COM_01["CMP-COM-01<br/>Relay Payload (Black Box)"]
    IFC_EXT_001["IFC-EXT-001<br/>Ground-control outbound<br/>traffic to relay payload"]
    REQ_001["REQ-001<br/>Relay outbound traffic"]
    VER_001["VER-001<br/>Requirement and<br/>architecture analysis"]
    VER_009["VER-009<br/>External conformance<br/>verification"]
    GAP_IFC_001["GAP-IFC-001<br/>External conformance<br/>authority missing"]
    CMP_COM_01 -->|"external interface"| IFC_EXT_001
    IFC_EXT_001 -->|"allocated requirement"| REQ_001
    REQ_001 -->|"model analysis"| VER_001
    REQ_001 -.->|"external conformance"| VER_009
    VER_009 -.->|"authority and evidence unresolved"| GAP_IFC_001
```

The picture shows connections. Full names, status qualifiers, and numbered relationship labels are below.

| Diagram key | Full description |
|---|---|
| `CMP_COM_01` | CMP-COM-01; Relay Payload (Black Box); [PROPOSED] |
| `IFC_EXT_001` | IFC-EXT-001; Ground-control outbound traffic to relay payload; [PROPOSED] |
| `REQ_001` | REQ-001; Relay outbound traffic; [PROPOSED] |
| `VER_001` | VER-001; Requirement and architecture analysis; [EXECUTED WITH OPEN GAPS] |
| `VER_009` | VER-009; External conformance verification; [BLOCKED] |
| `GAP_IFC_001` | GAP-IFC-001; External conformance authority missing; [UNRESOLVED] |

</details>

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
