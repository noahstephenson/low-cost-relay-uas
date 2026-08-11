# Relay-UAS Architecture

> **Baseline Candidate - Not Approved.** This is the primary human-readable view of
> the structured model. Follow IDs into `model/architecture.yaml`,
> `model/assurance.yaml`, `.seal/proof.yaml`, and `model/traceability.yaml` for
> authoritative records and complete metadata.

## 1. Architecture Purpose

The concept places a bidirectional communications-relay payload on a conventional
small UAS so a ground-control node and remote UAS can exchange mission traffic when
their direct path is too long or obstructed. The platform is valuable because of
where it can hold station, not because the airframe is novel.

Three principles organize the model:

- Reference evidence, current candidate designs, and future extensions are separate configurations.
- The relay payload remains a black box behind a narrow platform boundary.
- Platform command is separate from the traffic relayed for another vehicle.

No diagram is approval evidence. `[PROPOSED]`, `[TBD]`, `[DEFERRED]`, and
`[UNVERIFIED]` state maturity explicitly.

## Current architecture at a glance

The current system under study is the **Relay UAS** (`OP-002`) in `CFG-REP` and
`CFG-DOM`. It contains the aircraft structure, propulsion, stored and regulated
power, flight-control and navigation resources, an independent platform-command
receiver, a modular payload bay, and a communications payload treated as a black
box. The human operator, Ground Control Node, Remote UAS, maintenance personnel,
and external authorities remain outside the product boundary.

| Question | Current architecture answer |
|---|---|
| What does it do? | Positions and holds a communications payload so outbound and return mission traffic can pass between ground control and a Remote UAS. |
| How is the aircraft controlled? | The operator uses a separate platform-command path (`IX-001`, `IFC-EXT-005`) that does not pass through the relay payload. |
| What crosses the payload boundary? | Regulated payload power (`IFC-INT-003`) and mechanical retention (`IFC-INT-007`) only. |
| What are the major aircraft subsystems? | Structure and mounting (`CMP-AFR-*`, `CMP-MNT-01`), propulsion (`CMP-PRP-*`), power (`CMP-PWR-*`), avionics (`CMP-AVN-*`), and black-box communications payload (`CMP-COM-*`). |
| What traffic is relayed? | Outbound traffic uses `IX-002` / `IX-003`; return traffic uses `IX-004` / `IX-005`. External implementation attributes remain undefined. |
| What modes matter now? | Ground Safe, Transit, Station Keeping, Relay Degraded, and Return / Recovery (`MODE-005`, then `MODE-001` through `MODE-004`). |
| What is future? | The digital payload-management interface in `CFG-DIG` and the broader UGV, radio-user, service, and infrastructure context in `CFG-SOS`. |

The current structured model is internally reviewable and has undergone a fresh
0.8.0 model-level check (`EVD-013`), but it is neither a physically verified system
nor an approved technical baseline. Read the next sections to inspect configuration
and behavior, then use the assurance and traceability sections to audit maturity.

## 2. Configuration Baselines

The current/reference axis is `CFG-REC -> CFG-REP -> CFG-DOM`. The future-extension
axis is `CFG-REP -> CFG-DIG -> CFG-SOS`.

```mermaid
flowchart LR
    %% Configuration scope: CFG-REC / CFG-REP / CFG-DOM / CFG-DIG / CFG-SOS
    CFG_REC["CFG-REC<br/>Reference evidence only<br/>role mapping complete - not exact"] -->|"informs - not exact inheritance"| CFG_REP["CFG-REP<br/>Current proposed baseline"]
    CFG_REP --> CFG_DOM["CFG-DOM<br/>Current candidate<br/>substitution criteria unresolved"]
    CFG_REP --> CFG_DIG["CFG-DIG<br/>Future extension<br/>adds IFC-INT-008 candidate"]
    CFG_DIG --> CFG_SOS["CFG-SOS<br/>Future outer context<br/>not current implementation"]
```

**Reference evidence — `CFG-REC`.** This boundary describes what the registered
sources say about the recovered article. It does not inherit candidate components,
interfaces, requirements, modes, controls, or verification claims.

**Current candidate architecture — `CFG-REP` / `CFG-DOM`.** These configurations
carry the present Relay-UAS decomposition and the two-interface payload boundary.
`CFG-DOM` currently changes supply-chain intent only; no component substitution or
domestic-content criterion has been selected.

**Future extensions — `CFG-DIG` / `CFG-SOS`.** These add a proposed digital payload
management path and broader independently managed performers. They do not silently
modify the current candidate.

## Recovered Reference vs Candidate Architecture

The controlled reconciliation contains 24 recovered-item records and 10 recovered-
connection records, plus reverse coverage for all 19 current candidate components
and all 22 interfaces. It records role correspondence, limitations, confidence, and
configuration scope. It does not claim identical hardware, exact recovered
connectivity, candidate approval, or inheritance from `CFG-REC`.

The registered PDF and workbook passed checksum verification and were reviewed in
full for architecture-relevant content. The current local DOCX does not match its
registered checksum; it was inspected only for change awareness and was not used to
strengthen technical claims. In this model, `physically_observed` means documented as
an observation in an integrity-accepted registered record, not direct inspection by
the model author or automation.

```mermaid
flowchart LR
    %% Configuration scope: CFG-REC informs CFG-REP / CFG-DOM - no exact inheritance
    REC_STRUCTURE["Recovered structure and retention"] -->|"direct / class-level / partial"| CAND_STRUCTURE["CMP-AFR-01 through CMP-AFR-05<br/>CMP-MNT-01"]
    REC_PROPULSION["Recovered propulsion resources"] -->|"direct role support"| CAND_PROPULSION["CMP-PRP-01 through CMP-PRP-03"]
    REC_POWER["Recovered power resources and harness"] -->|"direct / partial / unknown"| CAND_POWER["CMP-PWR-01 through CMP-PWR-04"]
    REC_AVIONICS["Recovered control and navigation resources"] -->|"direct / partial"| CAND_AVIONICS["CMP-AVN-01 through CMP-AVN-04"]
    REC_PAYLOAD["Recovered payload modules and antennas"] -->|"partial / inferred"| CAND_PAYLOAD["CMP-COM-01 / CMP-COM-02"]
    REC_PAYLOAD -.->|"unmatched and incomplete evidence remain"| GAPS["GAP-REC-001 / GAP-SRC-001"]
```

The recovered package supports a physically distinct payload, a power relationship,
retention, and payload-internal antenna coupling, but it does not prove that the
candidate's two modeled platform-to-payload crossings are the only recovered
crossings. It indirectly supports a separate carrier-command resource, while the
complete command path remains ambiguous. It does not establish the proposed end-to-
end health/status return or maintenance/configuration interface.

The model-completion audit disposition is explicit:

- `REC-CHG-001`: the explicit implementation-neutral source-power interface `IFC-INT-011` was added as a model-local completeness correction under `SRC-DEC-006`; it remains proposed and every electrical implementation attribute remains unknown.
- `REC-CHG-002`: keep the candidate unchanged unless the operator concept establishes a need for a separate carrier-view feedback resource and path.

## 3. System Boundaries

The inner product boundary is the Relay UAS. The outer context is the C2 Ecosystem.

```mermaid
flowchart LR
    %% Configuration scope: CFG-SOS context - CFG-REP / CFG-DOM / CFG-DIG inner constituent
    subgraph OUTER["C2 Ecosystem outer boundary [PROPOSED]"]
        OP_010["OP-010<br/>Operator"]
        OP_001["OP-001<br/>Ground control"]
        OP_003["OP-003<br/>Remote UAS"]
        OP_004["OP-004<br/>UGV [FUTURE]"]
        OP_005["OP-005<br/>Radio user [FUTURE]"]
        OP_006["OP-006<br/>Network service [FUTURE]"]
        OP_007["OP-007<br/>Maintenance"]
        OP_008["OP-008<br/>Spectrum authority"]
        OP_009["OP-009<br/>Support infrastructure [FUTURE]"]
        subgraph INNER["Relay UAS inner boundary"]
            OP_002["OP-002<br/>Relay UAS [PROPOSED]"]
        end
    end
    OP_010 -->|"IX-001 platform command"| OP_002
    OP_002 -->|"IX-009 health/status"| OP_010
    OP_001 -->|"IX-002 outbound"| OP_002
    OP_002 -->|"IX-003 outbound"| OP_003
    OP_003 -->|"IX-004 return"| OP_002
    OP_002 -->|"IX-005 return"| OP_001
    OP_007 <-->|"IX-010 maintenance"| OP_002
    OP_001 -.->|"IX-006 future command"| OP_004
    OP_004 -.->|"IX-007 future telemetry"| OP_001
```

External performers remain independently managed. The context does not imply
interoperability, authority, security, or implementation responsibility.

## 4. Capability and Operational Context

`CAP-001` addresses distance; `CAP-002` addresses obstructed geometry. They remain
separate because one can bind without the other. The concept hypothesis is the
intersection of those two capabilities with `CAP-004` low-cost attritability.

```mermaid
flowchart LR
    %% Configuration scope: CFG-REP / CFG-DOM current - CFG-SOS future scenarios
    NEED_001["NEED-001<br/>Extend mission reach"] --> CAP_000["CAP-000<br/>Extended-range employment"]
    CAP_000 --> CAP_001["CAP-001<br/>Beyond-line-of-sight control"]
    CAP_000 --> CAP_002["CAP-002<br/>Terrain-masked operation"]
    CAP_000 --> CAP_003["CAP-003<br/>Contested-spectrum resilience"]
    CAP_000 --> CAP_004["CAP-004<br/>Low-cost attritable fielding"]
    CAP_001 --> SCN_003["SCN-003 / SCN-004<br/>Bidirectional relay"]
    CAP_002 --> SCN_002["SCN-002<br/>Launch and positioning"]
    CAP_004 --> COST_MASS["REQ-PER-001 / REQ-PER-003<br/>cost and mass constraints"]
    CAP_004 --> COUPLED["TS-001 / TS-002 / TS-003<br/>coupled design trades"]
    CAP_003 -.-> GAP_TRC_001["GAP-TRC-001<br/>No allocated mechanism"]
```

`CAP-003` remains deliberately unallocated because every potential mechanism is
inside deferred payload work (`TS-009`). `CAP-004` is explicitly cross-cutting: it
constrains requirements, trade studies, configurations, and resource choices rather
than creating a meaningless operational activity (`DEC-005`).

The current mission thread keeps Relay-UAS platform command separate from relayed
traffic:

```mermaid
flowchart LR
    %% Configuration scope: CFG-REP / CFG-DOM
    OP_010["OP-010<br/>Platform operator"] -->|"IX-001 / IFC-EXT-005<br/>platform command"| OP_002["OP-002<br/>Relay UAS"]
    OP_001["OP-001<br/>Ground control"] -->|"IX-002 / IFC-EXT-001<br/>outbound"| OP_002
    OP_002 -->|"IX-003 / IFC-EXT-002<br/>outbound"| OP_003["OP-003<br/>Remote UAS"]
    OP_003 -->|"IX-004 / IFC-EXT-003<br/>return"| OP_002
    OP_002 -->|"IX-005 / IFC-EXT-004<br/>return"| OP_001
```

The relay is bidirectional, positional, and logically transparent at this level. No
frequency, protocol, data-rate, or waveform behavior is asserted.

## 5. Relay-UAS Logical/Physical Architecture

The physical architecture is a conventional multicopter decomposition. Representative
resources show subsystem ownership without reproducing the complete component catalog.

```mermaid
flowchart TB
    %% Configuration scope: CFG-REP / CFG-DOM
    OP_002["OP-002<br/>Relay UAS [PROPOSED]"] --> CMP_AFR_01["CMP-AFR-01<br/>Primary structure"]
    OP_002 --> CMP_PRP_01["CMP-PRP-01<br/>Propulsion"]
    OP_002 --> CMP_PWR_01["CMP-PWR-01<br/>Power source"]
    OP_002 --> CMP_AVN_01["CMP-AVN-01<br/>Flight control"]
    OP_002 --> CMP_MNT_01["CMP-MNT-01<br/>Payload mount"]
    OP_002 --> CMP_COM_01["CMP-COM-01<br/>Relay payload black box"]
    CMP_COM_01 --> CMP_COM_02["CMP-COM-02<br/>Antenna resource envelope"]
```

Four-corner propulsion sets are symmetric in the candidate design. Platform novelty
is avoided because added complexity competes directly with `CAP-004`. Component
selection remains open in the `TS-*` register.

Two decisions dominate the decomposition:

1. `CMP-COM-01` couples to the platform only through power and retention.
2. `CMP-AVN-04` controls the Relay UAS; it does not perform `FUN-REL-01` or `FUN-REL-02`.

## 6. Interfaces

The current interface architecture makes the payload boundary explicit while keeping
external paths implementation-neutral.

```mermaid
flowchart LR
    %% Configuration scope: CFG-REP / CFG-DOM
    CMP_PWR_03["CMP-PWR-03<br/>Payload power"] -->|"IFC-INT-003<br/>platform-to-payload"| CMP_COM_01["CMP-COM-01<br/>Relay payload"]
    CMP_MNT_01["CMP-MNT-01<br/>Payload mount"] <-->|"IFC-INT-007<br/>platform-to-payload"| CMP_COM_01
    subgraph PAYLOAD["Relay-payload black-box envelope"]
        CMP_COM_01 <-->|"IFC-INT-010<br/>payload-internal"| CMP_COM_02["CMP-COM-02<br/>Physical-resource envelope"]
    end
    OP_001["OP-001<br/>Ground control"] <-->|"IFC-EXT-001 / IFC-EXT-004"| CMP_COM_01
    CMP_COM_01 <-->|"IFC-EXT-002 / IFC-EXT-003"| OP_003["OP-003<br/>Remote UAS"]
    OP_010["OP-010<br/>Operator"] -->|"IFC-EXT-005<br/>separate platform command"| CMP_AVN_04["CMP-AVN-04<br/>Control receiver"]
    CMP_AVN_01["CMP-AVN-01<br/>Flight control"] -->|"IFC-EXT-007<br/>health/status return"| OP_010
```

Only `IFC-INT-003` and `IFC-INT-007` cross the current platform-to-payload boundary.
`IFC-INT-010` records physical coupling inside the payload envelope; it does not
define another platform interface or any antenna characteristic. `IFC-INT-008` is a
future `CFG-DIG`/`CFG-SOS` payload-management candidate and is absent from the current
architecture.

The complete 22-interface inventory, including internal power, control, health,
navigation, external traffic, and maintenance groups, is generated in the diagram
atlas. Every external interface now has model-review allocation, but real conformance
still requires external authority, specifications, and evidence (`VER-009` /
`GAP-IFC-001`). Implementation attributes remain intentionally out of scope
(`GAP-IFC-002`). Internal battery-state telemetry (`IFC-INT-006`) is an input to the
health function, not a substitute for the external `IFC-EXT-007` status return.

The completeness audit added five implementation-neutral internal interfaces that
were previously absent or represented only as diagram associations: battery source
to distribution (`IFC-INT-011`), GNSS/heading data (`IFC-INT-012`), propulsion-
controller output to motor (`IFC-INT-013`), motor drive to propeller
(`IFC-INT-014`), and distribution power to regulators (`IFC-INT-015`). These records
define architecture connectivity and failure meaning while leaving voltage, current,
connector, timing, load, sizing, and other implementation attributes unknown.

## 7. Operational Behavior

```mermaid
stateDiagram-v2
    %% Configuration scope: CFG-REP / CFG-DOM
    state "MODE-005 Ground Safe" as MODE_005
    state "MODE-001 Transit" as MODE_001
    state "MODE-002 Station Keeping" as MODE_002
    state "MODE-003 Relay Degraded" as MODE_003
    state "MODE-004 Return / Recovery" as MODE_004
    [*] --> MODE_005
    MODE_005 --> MODE_001: SCN-002
    MODE_001 --> MODE_002: SCN-002 station established
    MODE_002 --> MODE_003: SCN-007 payload degraded
    MODE_003 --> MODE_004: SCN-007 recovery intent
    MODE_002 --> MODE_004: SCN-008 or REQ-FUN-005
    MODE_004 --> MODE_005: SCN-008 recovered
```

```mermaid
sequenceDiagram
    %% Configuration scope: CFG-REP / CFG-DOM
    participant Operator as OP-010 Platform operator
    participant Platform as CMP-AVN-04 Platform command
    participant Ground as OP-001 Ground control
    participant Payload as CMP-COM-01 Relay payload
    participant Remote as OP-003 Remote UAS
    Operator->>Platform: IX-001 / IFC-EXT-005 platform command
    Ground->>Payload: IX-002 / IFC-EXT-001 outbound traffic
    Payload->>Remote: IX-003 / IFC-EXT-002 outbound traffic
    Remote-->>Payload: IX-004 / IFC-EXT-003 return traffic
    Payload-->>Ground: IX-005 / IFC-EXT-004 return traffic
```

```mermaid
sequenceDiagram
    %% Configuration scope: CFG-REP / CFG-DOM
    participant Ground as OP-001 Ground control
    participant Payload as CMP-COM-01 Relay payload
    participant Relay as OP-002 Relay UAS
    participant Operator as OP-010 Platform operator
    Payload--xGround: SCN-007 relay degradation
    Relay-->>Operator: IX-009 / IFC-EXT-007 health/status [PROPOSED]
    Operator->>Relay: IX-001 independent platform command
    alt Platform remains controllable
        Note over Payload,Relay: MODE-003 - REQ-FUN-007 / REQ-FUN-008 [PROPOSED]
        Relay-->>Operator: transition toward MODE-004
    else Platform control also impaired
        Note over Relay,Operator: HAZ-001 / GAP-HAZ-001
    end
```

`SCN-001` now maps to `OA-007` Prepare Relay UAS for operation, supported by
`FUN-CFG-01` and `FUN-HLT-01`, while the system remains in `MODE-005`. This is an
architecture thread, not a startup checklist. The degraded branch still ends at
explicit safety and evidence gaps rather than inventing a recovery behavior. UGV and
sensor/video threads remain future extensions.

## 8. Requirements and Constraints Summary

The 28 `REQ-*` records are authoritative in `model/assurance.yaml`. They cover relay
function, station keeping and recovery, unresolved performance envelopes, payload
interfaces, basic safety controls, project constraints, and explicitly deferred
items.

Bracketed `[TBD]` values are load-bearing unknowns with trade-study ownership. They
must not be replaced with borrowed figures. In particular:

- `REQ-IFC-003`: the platform-to-payload interface is limited to `IFC-INT-003` power and `IFC-INT-007` mechanical retention.
- `REQ-FUN-008`: proposed mode and health/status visibility supports setup and recovery decisions without defining implementation.
- `REQ-CON-003`: the project excludes weapons and munitions; it is not a recovered-article observation.
- `REQ-DEF-001..005`: deferred or externally owned topics, not requirements claimed satisfied here.

Mass, unit cost, power, endurance, and payload envelopes form one coupled open problem
(`GAP-BUDGET-001`), not five independent blanks. The worked TS-002/TS-003 analysis is
preserved in `trade-studies.md`.

```mermaid
flowchart LR
    %% Configuration scope: CFG-REP / CFG-DOM
    TS_006["TS-006<br/>Payload mount"] --> REQ_PER_004["REQ-PER-004<br/>Payload envelope"]
    REQ_PER_004 --> REQ_PER_003["REQ-PER-003<br/>Gross mass"]
    TS_001["TS-001<br/>Structure"] --> REQ_PER_003
    REQ_PER_003 --> TS_002["TS-002<br/>Propulsion demand"]
    TS_002 --> TS_003["TS-003<br/>Battery requirement"]
    TS_004["TS-004<br/>Payload power"] --> TS_003
    REQ_PER_002["REQ-PER-002<br/>Endurance target"] --> TS_003
    TS_003 -->|"battery mass feedback"| REQ_PER_003
    TS_003 --> REQ_PER_001["REQ-PER-001<br/>Unit cost"]
    REQ_PER_001 -.-> GAP_BUDGET_001["GAP-BUDGET-001<br/>targets and evidence unresolved"]
```

## 9. Hazards and Controls Summary

The hazard catalog is preliminary architecture reasoning, not a safety assessment.
No authoritative severity/probability scheme or risk-acceptance authority exists.

```mermaid
flowchart LR
    %% Configuration scope: CFG-REP / CFG-DOM
    HAZ_001["HAZ-001<br/>Uncommanded descent"] -.-> GAP_HAZ_001["GAP-HAZ-001<br/>DEC-003 owner decision"]
    HAZ_004["HAZ-004<br/>Propeller contact"] --> CTL_001["CTL-001<br/>Ground-safe arming control"]
    CTL_001 --> REQ_FUN_006["REQ-FUN-006<br/>Arming inhibit"]
    CTL_001 --> REQ_SAF_002["REQ-SAF-002<br/>Visible armed state"]
    REQ_FUN_006 --> VER_006["VER-006<br/>Cross-reference review<br/>EXECUTED WITH OPEN GAPS"]
    REQ_SAF_002 --> VER_006
    VER_006 -.-> GAP_VER_001["GAP-VER-001<br/>Physical / external evidence missing"]
    HAZ_008["HAZ-008<br/>Payload separation"] --> CTL_005["CTL-005<br/>Payload retention"]
    CTL_005 --> REQ_IFC_004["REQ-IFC-004<br/>Retain payload"]
    REQ_IFC_004 --> VER_008["VER-008<br/>Physical verification [DEFERRED]"]
    VER_008 -.-> GAP_VER_001
```

`HAZ-005` is only partially addressed: `REQ-FUN-007` preserves platform control but
does not restore relay service. `HAZ-009` is a reserved inactive identifier, not an
active deficiency. External hazards stay deferred pending employment context.

The current austere/non-populated employment narrative is an assumption, not an
enforceable requirement. No flight-termination or geofence function is modeled, so
`HAZ-001` remains openly unmitigated.

## 10. Verification Approach

The project owner accepted the internal architecture verification work package for
`0.7.0-baseline-candidate` as the current working verification baseline
(`SRC-DEC-005`, `EVD-012`). This disposition accepts the work and its evidence only;
it does not approve the technical baseline, physical verification, safety,
external-interface conformance, or `DEC-002` through `DEC-005`.

`VER-*` entries distinguish method readiness from execution. The accepted 0.7.0
execution trail remains in `EVD-008` through `EVD-012`. `VER-001` through `VER-007`
were re-executed against `0.8.0-baseline-candidate` in `EVD-013` after the
model-completeness corrections. That fresh review is not owner acceptance. Both
cycles establish model consistency only; neither demonstrates physical performance,
safety, external compatibility, or technical approval.

`VER-008` remains unexecuted and dependent on future physical evidence. `VER-009`
remains blocked by absent external authority, specifications, and conformance
evidence. A passing repository validator cannot substitute for either activity.

```mermaid
flowchart LR
    %% Configuration scope: CFG-REP / CFG-DOM with project-scope deferrals
    EXECUTED["CURRENT MODEL REVIEW<br/>VER-001 through VER-007<br/>EVD-013 - not owner accepted"] --> PASS["EXECUTED PASS<br/>VER-002 / VER-007"]
    ACCEPTED["PRESERVED ACCEPTED WORK PACKAGE<br/>0.7.0 / EVD-008 through EVD-012"] --> EXECUTED
    EXECUTED --> OPEN["EXECUTED WITH OPEN GAPS<br/>VER-001 / VER-003 through VER-006"]
    PHYSICAL["PHYSICAL-EVIDENCE-REQUIRED<br/>REQ-FUN-006 / REQ-FUN-008"] -.-> VER_008["VER-008<br/>Deferred physical method"]
    EXTERNAL["EXTERNAL-AUTHORITY-REQUIRED<br/>REQ-FUN-001 / REQ-FUN-004"] -.-> VER_009["VER-009<br/>External conformance"]
    DEFERRED["INTENTIONALLY-DEFERRED<br/>REQ-DEF-001 / REQ-DEF-004"] -.-> TS_009["TS-009<br/>Formal deferral"]
```

## 11. Key Traceability Threads

- Mission relay: `NEED-001 -> CAP-001 -> SCN-003 -> OA-004 -> IX-002 / IX-003 -> FUN-REL-01 -> CMP-COM-01 -> IFC-EXT-001 / IFC-EXT-002 -> REQ-FUN-001 -> VER-001 / VER-009`.
- Return telemetry: `SCN-004 -> OA-005 -> IX-004 / IX-005 -> FUN-REL-02 -> CMP-COM-01 -> IFC-EXT-003 / IFC-EXT-004 -> REQ-FUN-002 -> VER-001 / VER-009`.
- Station keeping: `CAP-002 -> SCN-002 -> OA-003 -> FUN-FLT-03 -> CMP-AVN-01 / CMP-AVN-02 / CMP-AVN-03 -> REQ-FUN-003 / REQ-CON-004 -> VER-001 / VER-008`.
- Ground safety: `HAZ-004 -> CTL-001 -> REQ-FUN-006 / REQ-SAF-002 -> VER-004 / VER-006 -> GAP-VER-001`.
- Payload retention: `HAZ-008 -> CTL-005 -> REQ-IFC-004 -> VER-005 / VER-008 -> GAP-VER-001`.
- Relay loss and recovery: `SCN-007 -> MODE-003 -> HAZ-005 -> CTL-004 -> REQ-FUN-007 -> FUN-FLT-01 / FUN-FLT-04 -> VER-006 / VER-008 -> GAP-VER-001`.
- Health/status: `SCN-007 -> IX-009 -> FUN-HLT-01 -> CMP-AVN-01 -> IFC-EXT-007 -> REQ-FUN-008 -> VER-005 / VER-008 / VER-009`.

The full relationship set belongs only in `model/traceability.yaml`; the generated
baseline report presents gap-oriented summaries rather than another matrix copy.

## 12. Open Architecture Gaps

The principal retained gaps are exact recovered-to-candidate equivalence and missing
or integrity-mismatched source evidence; unsupported `CAP-003`; unmitigated `HAZ-001`; external-interface
conformance authority; future UGV and sensor/video integration; unresolved
mass/cost/power/endurance targets; physical evidence; and the UAF-version decision.

This pass closes the SCN-001 activity mismatch and the health/status architecture
coverage gap. It reclassifies the former CAP-004 activity warning as a false-positive
model-health gap. External conformance, physical evidence, and owner decisions remain
open rather than being hidden behind those model improvements.

Cameo reconciliation is deferred future work outside this package and is not a
principal active deficiency. No Cameo content was used to close any gap.

## 13. Project-owner decisions required

`REC-CHG-001` is no longer an owner-decision blocker: `SRC-DEC-006` explicitly
authorized model-local completeness correction, so `IFC-INT-011` now records the
already intended battery-to-distribution energy path without selecting any technical
values or approving it. `REC-CHG-002` remains an owner-review question because adding
a carrier-view feedback resource would introduce new architecture intent. It is not
an approved `DEC-*` record.

### DEC-003 - HAZ-001 safety objective

- **Decision question:** Should `HAZ-001` receive a generic recovery or containment control and requirement?
- **Why it matters:** The current candidate has no architecture-level response when platform command/control is lost and recovery may still be possible.
- **Affected IDs:** `HAZ-001`, `GAP-HAZ-001`, `SCN-002`, `SCN-008`.
- **Option A:** Add a generic proposed `CTL-*` and `REQ-*` path without prescribing implementation.
- **Option B:** Retain `HAZ-001` as explicitly unmitigated.
- **Option C:** Defer the safety objective until a designated safety authority supplies criteria.
- **Codex recommendation:** Option A, with exact wording reviewed before new control and requirement records are created.
- **What changes if accepted:** A proposed hazard-control-requirement-verification path is added.
- **What remains open either way:** Physical behavior, acceptance criteria, execution evidence, and safety authority.

### DEC-004 - Explicit health/status return

- **Decision question:** Should `FUN-HLT-01`, `IFC-EXT-007`, and `REQ-FUN-008` remain in the current candidate architecture?
- **Why it matters:** Setup, mode awareness, and recovery decisions already depend on more than internal battery-state telemetry.
- **Affected IDs:** `IX-009`, `IFC-INT-006`, `FUN-HLT-01`, `IFC-EXT-007`, `REQ-FUN-008`.
- **Option A:** Accept the proposed architecture-level health/status thread.
- **Option B:** Return `IX-009` to an unresolved exchange with no current-system realization.
- **Option C:** Limit the current model to battery state and remove broader status claims.
- **Codex recommendation:** Option A because it makes the existing scenario logic explicit without selecting implementation.
- **What changes if accepted:** The proposed logical thread remains the candidate basis for later design and verification.
- **What remains open either way:** Minimum status content, transport, external authority, physical behavior, and conformance evidence.

### DEC-005 - CAP-004 semantics

- **Decision question:** Should `CAP-004` remain a cross-cutting affordability and attritability constraint rather than receive a dedicated operational activity?
- **Why it matters:** A forced mission activity would misrepresent cost and logistics as operational behavior.
- **Affected IDs:** `CAP-004`, `REQ-PER-001`, `REQ-PER-003`, `REQ-PER-004`, `REQ-PER-005`, `REQ-CON-001`, `REQ-CON-002`, `TS-001`, `TS-002`, `TS-003`, `TS-004`, `TS-006`.
- **Option A:** Confirm the cross-cutting treatment.
- **Option B:** Add a lifecycle activity later only if affordability management is deliberately modeled as behavior.
- **Option C:** Restore the prior coverage warning.
- **Codex recommendation:** Option A; do not create a synthetic activity merely for checker coverage.
- **What changes if accepted:** `GAP-TRC-002` remains reclassified and closed.
- **What remains open either way:** All numeric targets, component choices, and physical/economic evidence.

## 14. Standards Posture

The repository uses a small UAF vocabulary subset:

- Strategic concepts for needs and capabilities.
- Operational concepts for performers, activities, scenarios, and exchanges.
- Resource concepts for functions, components, and interfaces.

This keeps capability, operational context, and resource allocation connected in one
model—something plain SysML would otherwise leave partly in prose—without adopting a
full acquisition-framework apparatus. UAF draws on UML/SysML and earlier architecture
framework concepts; this repository does not claim full UAF or DoDAF conformance.

UAF 1.2 terminology remains in use. UAF 1.3 is the current OMG formal version, but
`DEC-002` / `GAP-STD-001` leaves retention, version-neutral wording, or later migration
for owner decision. This refactor is not a UAF migration.
