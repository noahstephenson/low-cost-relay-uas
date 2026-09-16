# Writer-ready manuscript outline

> **Superseded.** This outline predates the carrier calibration (commit `4f9e2cd`, branch `codex/carrier-calibration-v1`) and the finished manuscript. The submitted paper — its title, numbers, and wording — is the sole authority; it is drafted in a local `submission/` directory that is intentionally not tracked in this repository (see `.gitignore`). Treat everything below as historical drafting context, not current claims or numbers.

**Fixed title:** System Architecture and Conditional Service Envelope of a Multirotor Communications Relay

**Purpose:** A detailed drafting specification, not the manuscript itself. Follow the paragraph order, claim wording, equations, populated tables, and exhibit instructions. Do not strengthen claims by removing qualifications.

**Audience and article form:** Aerospace systems engineers; a reproducible analytical architecture case study. Define communication margin and mathematical closure for readers outside those specialties. Keep the project venue-neutral. The ten-page budget is an editorial target, not a venue rule. The quality benchmark is discussed only in the [evidence audit](reference/manuscript-evidence-audit.md#7-submission-benchmark-editorial-only).

**Evidence:** Audited on 2026-09-11 against baseline `71ed88815fd5c5ebe9846bac140cc0628336825e` and the working tree. All 19 existing tests pass; all 1,890 existing case records were independently checked. Read the [claim register, checked literature, discrepancies, and verification record](reference/manuscript-evidence-audit.md) before drafting. C01-C30 are authoring claim IDs, not printed manuscript text. Reference keys R1-R8 are defined in the audit; final citation order is R1=[1], R2=[2], R3=[3], R4=[4], R5=[5], R8=[6], R6=[7], R7=[8].

**Thesis:** A relay that clears an obstruction and passes a link budget can still be excluded by its carrier resource demand. Explicit connectivity, analytical closure, and physical-envelope gates distinguish these limitations and identify which assumptions require reconsideration.

**Contribution sentence:** “This study presents a reproducible architecture case study that separates connectivity failure, finite sizing outside an exploratory envelope, and mathematical nonclosure under explicitly declared assumptions.”

The contribution is not the first combination of communications and propulsion energy, the discovery of battery-mass feedback, or a new sizing law. The checked literature already contains those ideas. No result is a validated aircraft prediction.

## A. Fixed structure and space budget

| Printed section | Pages including exhibits | Objective |
|---|---:|---|
| Title, abstract, keywords | 0.40 | Bounded contribution and main result |
| 1. Introduction and related work | 1.15 | Decision problem and prior work |
| 2. Architecture and assessment boundary | 0.75 | What carries, powers, controls, and relays |
| 3. Methods | 3.00 | Reproducible assumptions, equations, branches, and gates |
| 4. Results | 2.25 | Worked example, grid, and scenario comparisons |
| 5. Discussion | 1.20 | Decision value and limitations |
| 6. Conclusion | 0.25 | Answer without new claims |
| References and required end matter | 1.00 | Checked references and factual author-supplied information |
| **Total** | **10.00** | Editorial target, subject to actual outlet format |

Use four figures and five numbered tables; Tables 3 and 5 have labeled panels. Put the full parameter-to-code mapping, expanded branch algebra, case files, checker, and standalone carrier sensitivity in the supplement. The material below specifies both main-text and supplement content.

Draft Section 3 → 4 → 5 → 2 → 1 → 6 → abstract. Keep architecture catalog IDs, recovered-article history, and cost sweeps outside the main narrative. Do not invent author affiliations, funding, acknowledgments, release permissions, or a dataset DOI. Authors supply these factual end-matter fields.

## B. Title, abstract, and keywords

### B.1 Title and framing

Use the fixed title. “Low-cost” is an unestablished project aspiration and does not belong in the manuscript findings (C24). Define “service envelope” as the sampled cases satisfying the screens, not an approved operating envelope.

### B.2 Abstract blueprint

**Purpose:** Problem, method, result, and boundary in one approximately 200-230-word paragraph. Use this sentence sequence:

1. **Problem:** “An airborne communications relay must provide useful connectivity while carrying and powering its payload for the required time on station.” C01/C03.
2. **Contribution:** Use the fixed contribution sentence, shortened to fit. C01/C21.
3. **Method:** Fixed-payload geometry and received-level screening, branch-consistent hover mass closure, and exploratory physical limits. C03/C09/C12.
4. **Experiment:** Ninety separation-dwell-altitude combinations, idealized opaque screen, stationary Ground → Relay → Remote assessment. C05/C14/C30.
5. **Main result:** Eighteen physical-boundary passes, six finite exclusions, six nonclosures, and sixty connectivity failures; these are deterministic case counts. C14.
6. **Example:** Contrast 30-minute mass 8.62 kg, 45-minute finite excluded mass 106.25 kg, and 60-minute nonclosure. Call the large mass an extrapolation. C11.
7. **Sensitivity:** Six passes under an additional 12 dB loss scenario. C16.
8. **Implication/limit:** Different mechanisms require different assumption changes; full mission energy and physical performance remain unvalidated. C21/C24/C30.

Do not add improved throughput, availability, affordability, optimized placement, success probability, or measured endurance. No citations in the abstract unless the eventual outlet requires them. Transition to the introduction by unpacking why a link opportunity does not settle an aircraft decision.

**Keywords:** multirotor; airborne communications relay; conceptual sizing; architecture assessment; service envelope.

## 1. Introduction and related work

### 1.1 Why a relay is also an aircraft resource problem

**Purpose:** Establish the question without a universal communications or operational claim.

- **Paragraph 1 topic:** “A relay can change communication geometry, but the aircraft must sustain that geometry while supporting the radio.” Describe one obstructed ground-to-remote path. Cite R1/[1] for mobile-relay research context; use Figure 1 for this study's scenario. C01/C28.
- **Paragraph 2 topic:** “A communications opportunity and a carrier resource solution answer different engineering questions.” Define link margin and battery-mass feedback in one sentence each. Introduce finite sizing outside a physical envelope. C03/C08/C09.
- **Interpretation:** Explain why all gates matter before giving equations.
- **Limit:** No reconstructed aircraft or surveyed terrain claim.
- **Transition:** “Existing communication and aircraft-sizing research provides the constituent models; the present question concerns their explicit use in an architecture screening decision.”

### 1.2 Closest work and bounded contribution

**Purpose:** Locate the study honestly among related and stronger methods.

- **Paragraph 1 topic:** “Trajectory, communication energy, and battery choice have already been studied together in UAV systems.” Cite R2/[2], R3/[3], and R4/[4] with Table 1. Do not quote performance gains or imply they use these equations. C25/C28.
- **Paragraph 2 topic:** “Aircraft sizing feedback and failure to close also precede this study.” Cite R5/[5]; distinguish its data-informed models from this constant-parameter representation. C26/C27.
- **Paragraph 3 topic:** “The contribution is an auditable case study with explicit failure states rather than a new optimization method.” Use the fixed contribution sentence. Explain the traceable worked example, grid partition, and decision implications. No claim of an unprecedented taxonomy. C01/C03/C21.
- **Research question:** “Under the declared service and carrier assumptions, which separation, dwell, and altitude cases pass the combined screens, and which limiting mechanism governs the cases that do not?”
- **Scope:** “The quantitative assessment covers stationary outbound dwell; it does not establish delivered throughput, full mission energy, or physical aircraft performance.” C30/C24.
- **Transition:** “The system boundary and resource allocations define the quantities passed to the assessment.”

**Table 1 — Selected conceptual precedents.** Complete references and access limitations are in the audit.

| Reference | Established emphasis | Relationship to this study |
|---|---|---|
| [1] Zeng et al., 2016 | Mobile relay power and trajectory optimization | Geometry/resource design is prior work |
| [2] Zeng et al., 2019 | Propulsion and communication energy with service constraints | Combined energy reasoning is prior work |
| [3] Yan et al., 2021 | Battery weight and available communication energy | Battery-mass tradeoffs are prior work |
| [4] Rodrigues et al., arXiv revision 2022 | Propulsion-aware relay positioning | Relay endurance and network service are prior work |
| [5] Russell et al., 2018 | Data-informed quadcopter sizing | Sizing feedback and failure to close are prior work |
| Present study | Explicit connectivity/closure/physical partition | Reproducible conditional case and decision interpretation |

**Caption:** “Selected conceptual precedents, not an exhaustive literature taxonomy. This study does not claim methodological superiority or transfer validation from these sources.”

## 2. Architecture and assessment boundary

### 2.1 Mission and system boundary

**Purpose:** Separate conceptual responsibilities from calculated scope.

- **Paragraph 1 topic:** “The relay aircraft supports a communications payload while maintaining its assigned station.” Describe endpoints, carrier, and black-box payload using Figure 1. C01.
- **Paragraph 2 topic:** “Only stationary outbound dwell is assessed quantitatively.” List prepare → launch → transit → establish station → relay → monitor → recover once. Mark the stationary outbound interval as assessed; the reserve fraction does not supply a transit/recovery calculation. C05/C30.
- **Evidence:** [Architecture](architecture.md), MC `build`, Figure 1, Table 2.
- **Limit:** No autonomous station-keeping verification, bidirectional protocol, reconstruction, or operating procedure.
- **Transition:** “Within that boundary, payload and carrier exchange resources while serving distinct information responsibilities.”

### 2.2 Resource and information allocation

**Purpose:** Explain the aircraft around the radio and the implemented coupling.

- **Paragraph 1 topic:** “Payload mass and DC demand become carrier burdens, while fixed RF assumptions enter the connectivity screen.” Explain mounting, regulated power, propulsion, and avionics with Table 2. C03/C04.
- **Paragraph 2 topic:** “Logical command separation is an allocation, not evidence of physical isolation.” Explain distinct information paths, shared physical dependencies, and Figure 2. No optimization feedback runs from link margin to payload sizing. C02/C03.
- **Interpretation:** Architecture defines what is screened; its documentation does not validate the region.
- **Limit:** No fault tolerance, recovery, thermal compatibility, retention strength, or selected hardware claim.
- **Transition:** “The assessment begins with declared inputs and applies explicit gates to the calculation branches.”

**Table 2 — Responsibilities and evidence boundary.**

| Responsibility | Representation | Boundary |
|---|---|---|
| Relay traffic | Two outbound visibility/margin tests | No packet, scheduling, duplex, or throughput model |
| Carrier command/navigation | Avionics mass, auxiliary power, logical allocation | No control-link or station-keeping performance |
| Payload power | DC demand divided by regulator efficiency | No component, transient, thermal, or fault test |
| Retention/structure | Mount and structural mass allowances | No stress, vibration, or packaging verification |
| Hover propulsion | Constant-loading power and mass model | No matched aircraft/rotor calibration |
| Energy storage | Energy/power sizing and reserve | No measured pack, degradation, or full recovery energy |

**Caption:** “Descriptive architecture allocations and quantitative resource allowances do not establish demonstrated physical behavior.”

## 3. Methods

### 3.1 Scenario and input provenance

**Purpose:** Supply all reproduction inputs without overstating their sources.

- **Paragraph 1 topic:** “The grid samples declared geometries and durations rather than observed operations.” Define coordinates relative to the ground datum; introduce Table 3A/3C and Figure 1. C05.
- **Paragraph 2 topic:** “Manufacturer values anchor only part of the payload representation.” Explain 102 g device plus 98 g assumed integration and continuous 14 W allowance; cite R8/[6]. No measured operating point is implied. C04.
- **Paragraph 3 topic:** “Carrier nominal values are model assumptions rather than a calibrated dataset.” Table 3B separates their status; R5 provides context but not the 170 Wh/kg and 83% nominals. Input-file evidence labels do not imply validation. C27.
- **Limit:** No approved mission requirements or quantified “low-rate” service guarantee.
- **Transition:** “These inputs first determine segment visibility and received-level margin.”

**Table 3A — Service, payload, and geometry inputs.**

| Quantity / symbol | Value | Provenance / interpretation |
|---|---|---|
| Endpoint separation `D/1000` | 5, 10, 20, 30, 40, 60 km | Declared grid |
| Dwell `t` | 10, 20, 30, 45, 60 min | Stationary duration |
| Ground/remote heights `z_G,z_U` | 0/100 m | Common datum |
| Relay fraction `r`; heights `h` | 0.5; 60, 120, 240 m | Fixed midpoint, not optimized |
| Baseline screen fraction `s`; height `H` | 0.40; 80 m | Ideal opaque screen |
| Frequency `f`; bandwidth | 2400 MHz; 5 MHz | Assumed context; bandwidth unused by margin equation |
| Ground conducted power `T_G` | 30 dBm | Assumption |
| Endpoint/relay gains `G_e,G_r` | 6/2 dBi | Installed-gain allowances |
| Miscellaneous loss `L_0`; threshold `S` | 6 dB; -90 dBm | Assumptions, not product sensitivity |
| Excess loss `L_x` | 0 baseline; 12 dB stress | Deterministic scenario |
| Payload mass `m_L`; DC demand `P_L` | 0.20 kg; 14 W | Device anchors plus integration/loading assumptions |
| Relay RF output | 1.6 W = 32.0412 dBm | Maximum used as scenario input; no measured RF/DC pair |

**Table 3B — Complete carrier symbol-to-input mapping.** Print rows through physical bounds in main text; component-allocation rows go to Supplement S1. Dimensionless values have no units unless the ratio is stated.

| Symbol | Input key | Value / unit | Status |
|---|---|---|---|
| `g` | gravity_m_s2 | 9.80665 m/s² | Reference constant |
| `rho` | air_density_kg_m3 | 1.225 kg/m³ | Fixed atmosphere, not weather |
| `n` | rotor_count | 4 | Architecture assumption |
| `DL` | disk_loading_n_m2 | 60 N/m² | Design-family assumption; R5 contextual anchor |
| `FM` | rotor_figure_of_merit | 0.62 | Assumed rotor performance |
| `eta_d` | motor_controller_efficiency | 0.83 | Nominal, not R5's value |
| `k_env` | environment_power_margin | 1.15 | Hover multiplier, not wind model |
| `e_b` | battery_specific_energy_wh_kg | 170 Wh/kg | Assumed installed nominal energy |
| `p_b` | battery_specific_power_w_kg | 900 W/kg | Assumed continuous pack-class power |
| `d_b` | battery_depth_of_discharge | 0.90 | Usable-capacity assumption |
| `r_b` | reserve_fraction | 0.20 | Withheld after depth-of-discharge allowance |
| `mu_b` | battery_power_margin_ratio | 1.15 | Power-sizing margin |
| `tau` | thrust_margin_ratio | 1.75 | Installed thrust / weight assumption |
| `m_max`; `d_max`; `s_max` | analysis_max_gross_mass_kg; analysis_max_rotor_diameter_m; analysis_max_vehicle_span_m | 15 kg; 0.75 m; 1.5 m | Exploratory physical limits |
| `p_p` | propulsion_specific_power_w_kg | 2300 W/kg | Parametric motor/controller group |
| `sigma_r` | rotor_mass_per_disk_area_kg_m2 | 0.14 kg/m² | Rotor allowance |
| `m_s0` | structure_base_mass_kg | 0.95 kg | Structure allowance |
| `f_s` | structure_load_fraction | 0.18 | Structural / supported mass |
| `sigma_s` | structure_area_penalty_kg_m2 | 0.22 kg/m² | Area burden |
| `m_av` | avionics_mass_kg | 0.40 kg | Aggregate allowance |
| `m_pe` | power_electronics_mass_kg | 0.28 kg | Allowance |
| `m_m0`; `f_m` | mount_base_mass_kg; mount_payload_fraction | 0.20 kg; 0.18 | Mount base plus fraction of payload |
| `P_aux` | auxiliary_power_w | 25 W | Nonpayload electrical load |
| `eta_r` | payload_regulator_efficiency | 0.92 | Assumed conversion efficiency |

**Table 3C — Scenario definitions.** Typeset as notes under Table 3A, not a separate numbered table.

| Scenario key | Screen `H,s` | `L_x` |
|---|---|---:|
| clear_reference | None | 0 dB |
| obstructed_reference | 80 m, 0.40 | 0 dB |
| obstructed_adverse | 80 m, 0.40 | 12 dB |
| obstruction_sensitivity_h60_x40 | 60 m, 0.40 | 0 dB |
| obstruction_sensitivity_h100_x40 | 100 m, 0.40 | 0 dB |
| obstruction_sensitivity_h80_x30 | 80 m, 0.30 | 0 dB |
| obstruction_sensitivity_h80_x45 | 80 m, 0.45 | 0 dB |

**Caption:** “Declared primary inputs and scenario changes. Device values do not validate integration allowances or a common RF/DC operating point. Physical limits are exploratory; bandwidth is descriptive service context.”

### 3.2 Geometry and connectivity

**Purpose:** Define exactly what constitutes a direct or relayed link pass.

- **Paragraph 1 topic:** “Visibility is a strict geometric test on a segment crossing the screen.” Give E1-E2 and explain why the second relay hop does not cross this screen family. C06.
- **Paragraph 2 topic:** “Clear segments are screened by received-level margin using a common receiver threshold.” Give E3-E4, cite R6/[7], and explain the constant convention. C07/C29.
- **Paragraph 3 topic:** “A relay link pass requires both outbound hops to pass.” Give E5, clarify hypothetical blocked-path margins and the absent packet/scheduling calculations. C30.
- **Evidence:** MC `visible`, `distance_km`, `fspl_db`, `watts_to_dbm`, `link_margin_db`, `link_case`; Table 3A.
- **Transition:** “The carrier calculation determines whether the assumed payload can be supported for the requested dwell.”

**E1 — Coordinates and distance.** Use metres internally, kilometres in path loss. `D` is endpoint separation in metres; `x,z` are horizontal/vertical coordinates; `r` is relay fraction; `h` relay height; `ell_AB` segment length:

```text
G = (0,z_G); R = (rD,h); U = (D,z_U)
ell_AB = sqrt((x_B-x_A)^2 + (z_B-z_A)^2)/1000       [km]
```

**E2 — Screen visibility.** For `x_s=sD` strictly between segment endpoints:

```text
z_AB(x_s) = z_A + (x_s-x_A)(z_B-z_A)/(x_B-x_A)
V_AB = [z_AB(x_s) > H]
h_threshold = z_G + (H-z_G)r/s                    [m]
```

A segment not strictly crossing the screen is clear in this implementation. Equality at screen height is blocked. The threshold formula applies to a screen between G and R, as in all existing screen scenarios; do not generalize to a screen beyond R. No Fresnel clearance, diffraction, curvature, or terrain interpolation is modeled.

**E3 — Free-space loss.** Frequency `f` in MHz, `ell_AB` in km, loss in dB:

```text
L_fs = 32.44 + 20 log10(f) + 20 log10(ell_AB)
```

R6 Eq. (6) prints 32.4; retain 32.44 to reproduce the implementation. State this convention rather than claim exact numerical identity with the rounded standard.

**E4 — Margin.** `T_A` is conducted transmit level in dBm; `G_A,G_B` antenna gains in dBi; losses and margin in dB; `S` receiver threshold in dBm:

```text
M_AB = T_A + G_A + G_B - L_fs - L_0 - L_x - S
T_relay = 10 log10(1000 P_RF[W])
```

Use `T_G=30` for direct/first hop and `T_relay` for second hop. G/U use endpoint gains; R uses relay gain. Product-specific threshold fields in PI are not solver inputs.

**E5 — Connectivity predicates.** Square brackets are Boolean conditions:

```text
D_ok = V_GU AND [M_GU >= 0]
R_ok = V_GR AND V_RU AND [M_GR >= 0] AND [M_RU >= 0]
```

### 3.3 Carrier mass, power, and battery sizing

**Purpose:** Supply a dimensionally complete mass balance, not a selected-vehicle prediction.

- **Paragraph 1 topic:** “Constant disk loading makes rotor area and hover power proportional to gross mass.” Give E6; cite R7/[8] for classical hover definitions; explain the resized-family assumption. C08.
- **Paragraph 2 topic:** “Battery mass is governed by the larger energy and peak-power allowance.” Give E7, conversion from minutes to hours, and usable fraction `u=0.72`. C04/C10.
- **Paragraph 3 topic:** “Propulsion, mounting, and structural allowances complete gross mass.” Give E8; call its coefficients parametric assumptions. C09/C27.
- **Limit:** No rotor interference calibration, stress design, pack discharge curve, thermal model, or installed envelope verification. Peak-power scaling is not tested thrust performance.
- **Transition:** “The mass map is piecewise affine, allowing closure assessment independently of numerical iteration.”

**E6 — Area and hover propulsion.** `m` gross mass kg, `W` weight N, `A` total rotor disk area m², powers W:

```text
W = mg; A = W/DL
P_i = W^(3/2)/sqrt(2 rho A)
P_prop = k_env P_i/(FM eta_d) = cm
q = g/DL; c = g sqrt(DL/(2 rho)) k_env/(FM eta_d)
```

`q` is area/mass in m²/kg; `c` power/mass in W/kg. `P_i` is ideal induced hover power. Total area sums all four rotors. Figure of merit is aerodynamic; drive efficiency is separate. All input symbols are in Table 3B.

**E7 — Electrical and battery sizing.** `t` minutes; energies Wh; battery masses kg:

```text
P_0 = P_aux + P_L/eta_r
P_hover = cm + P_0
P_peak_prop = tau^(3/2) cm
P_peak_batt = P_peak_prop + P_0
u = d_b(1-r_b)
E_req = P_hover(t/60)/u
m_E = E_req/e_b
m_P = mu_b P_peak_batt/p_b
m_b = max(m_E,m_P); E_inst = e_b m_b
```

`P_0` fixed bus demand, `m_E,m_P` energy/power-sized battery candidates, `E_req` required nominal battery energy, `E_inst` installed nominal energy. Do not apply thrust scaling to auxiliary/payload power. Do not treat 14 W DC as RF power. Required and installed energy differ on the power-sized branch.

**E8 — Component balance.** Masses kg; area m²:

```text
m_mount = m_m0 + f_m m_L
m_prop = P_peak_prop/p_p + sigma_r A
F = m_L + m_av + m_pe + m_mount
m_structure = m_s0 + f_s(F + m_b + m_prop) + sigma_s A
m_new = F + m_b + m_prop + m_structure
```

`F` is fixed carried mass; `m_new` the mass implied by the trial gross mass. The supported mass inside the structural fraction includes avionics, power electronics, and mount, matching code; do not reduce it to payload+battery alone.

### 3.4 Branch-consistent analytical closure

**Purpose:** Separate physical-state reporting from iterative-solver behavior.

- **Paragraph 1 topic:** “Each battery branch gives a candidate mass, but only a self-consistent branch is admissible.” Show E11 in main text; E9-E10 in Supplement S2. Explain positivity and branch tests. C09.
- **Paragraph 2 topic:** “Finite sizing outside the envelope and mathematical nonclosure are different outcomes.” Explain the shrinking denominator and the 45-minute extrapolation. C11.
- **Paragraph 3 topic:** “Numerical iteration is a diagnostic rather than the physical result.” State E12/settings; timeout or guard does not replace a valid analytical state. C23.
- **Transition:** “Finite solutions are then compared with explicit physical screening bounds.”

**E9 — Branch coefficients (Supplement S2).** Slopes dimensionless, intercepts kg:

```text
alpha_E = c(t/60)/(u e_b);      beta_E = P_0(t/60)/(u e_b)
alpha_P = mu_b tau^(3/2)c/p_b;  beta_P = mu_b P_0/p_b
k_prop = tau^(3/2)c/p_p + sigma_r q
```

`alpha_j,beta_j` define battery candidate mass `alpha_j m + beta_j`; `k_prop` is propulsion-group mass/gross mass.

**E10 — Gross-mass branch coefficients (Supplement S2).** `j` is E or P:

```text
a_j = (1+f_s)(alpha_j+k_prop) + sigma_s q
b_j = (1+f_s)(F+beta_j) + m_s0
m_new,j = a_j m + b_j
```

`a_j` dimensionless, `b_j` kg. Positive intercepts hold for all audited inputs. This is an algebraic rearrangement of E6-E8, not a new constitutive law.

**E11 — Closure and branch consistency.**

```text
m*_j = b_j/(1-a_j)
Admissible: a_j < 1, m*_j > 0, and
  E branch: alpha_E m*_j + beta_E >= alpha_P m*_j + beta_P
  P branch: alpha_P m*_j + beta_P >= alpha_E m*_j + beta_E
```

No admissible candidate means mathematical nonclosure and no physical mass/area/power/energy/cost result. For an exact branch tie, the implementation selects E first; both branches give the same mass. A finite inconsistent candidate is not a solution. A power-branch slope below one cannot rescue a case whose energy demand dominates incompatibly.

**E12 — Iteration diagnostic.**

```text
m_(k+1) = 0.55 m_new(m_k) + 0.45 m_k
relative change = abs(m_(k+1)-m_k)/max(m_(k+1),1e-9)
```

`k` is iteration index, initial mass 5 kg, tolerance `1e-7`, limit 200 iterations, mass guard 50 kg. The guard is diagnostic; it neither imposes the physical 15 kg ceiling nor defines nonclosure. Analytical state controls reported physical quantities. No flying-aircraft stability claim follows.

### 3.5 Physical bounds and decision order

**Purpose:** Define each result label precisely.

- **Paragraph 1 topic:** “Finite mass is screened against exploratory dimensions and mass.” Give E13; explain redundant rotor/footprint limits and effective ceiling. C12/C13.
- **Paragraph 2 topic:** “The first applicable gate determines a mutually exclusive label.” Give E14; explain why separate carrier flags preserve simultaneous failures. C14/C15/C19.
- **Limit:** This differs from standalone cost/battery-fraction classification. No portability approval, affordability, or selected aircraft follows.
- **Transition:** “The prescribed grid and comparisons expose where each gate governs.”

**E13 — Physical screen.** `d_rotor` equivalent per-rotor diameter m, `span_proxy` m:

```text
d_rotor = sqrt(4A/(n pi)); span_proxy = 2 d_rotor
V_ok = finite closure AND [m <= 15] AND [d_rotor <= 0.75] AND [span_proxy <= 1.5]
m_rotor_limit = n pi DL (0.75)^2/(4g) = 10.81192375 kg
```

Diameter is per equivalent rotor, not one disk containing the area of four rotors. Limits accept equality. Span is a proxy, not a measured bounding box.

**E14 — Ordered classifier.**

```text
if D_ok:          DIRECT
elif not R_ok:    LINK FAIL
elif no closure:  NO CLOSE
elif not V_ok:    EXCLUDED
else:             PASS
```

Machine labels for Supplement S3: DIRECT=`DIRECT_SUFFICIENT`; LINK FAIL=`RELAY_CONNECTIVITY_INFEASIBLE`; NO CLOSE=`RELAY_FUNCTIONAL_VEHICLE_RESOURCE_FAILURE`; EXCLUDED=`MASS_CLOSED_PRACTICAL_CONSTRAINT_FAILURE`; PASS=`RELAY_BENEFICIAL_AND_FEASIBLE`. PASS is relay benefit plus exploratory physical screening only.

### 3.6 Experiment and verification

**Purpose:** Define selections, denominators, and checks.

- **Paragraph 1 topic:** “There are 90 unique primary combinations per scenario.” Primary is `payload_id=PAY-MESH-OEM`; use Table 3A's Cartesian product and 3C's scenarios. Total 1,890 rows = 3 payloads × 7 scenarios × 90, not independent missions. C14.
- **Paragraph 2 topic:** “Verification checks the calculation and reporting, not aircraft accuracy.” State existing tests plus independent mass-residual bisection and link reconstruction over saved cases. Give the revision in the supplement. C23.
- **Paragraph 3 topic:** “Secondary payloads are contextual comparisons, not isolated SWaP experiments.” Mass, DC, and RF fields change together; do not combine counts with primary cases. C18.
- **Evidence:** [Read-only checker](reference/check-manuscript-evidence.py), audit section 5, FI/MI/PI/DATA.
- **Transition:** “The worked case isolates dwell while keeping link geometry unchanged.”

## 4. Results

### 4.1 One geometry, different resource outcomes

**Purpose:** Make the decision distinction understandable before the full grid.

- **Paragraph 1 topic:** “The worked geometry clears the relay path while blocking the direct path.” At 10 km separation and 120 m relay height, screen=(4 km,80 m); direct line height=40 m, first-hop height=96 m. State hop margins 7.974/10.018 dB; positive hypothetical direct margin 5.955 dB does not override blockage. C06/C07.
- **Paragraph 2 topic:** “Changing dwell leaves link margins unchanged but changes the required carrier.” Use Table 4, focusing on 30/45/60 min and battery branches. C10/C11.
- **Paragraph 3 topic:** “Long-dwell outcomes have different meanings.” Forty-five minutes has an excluded finite mass; sixty minutes has no physical output. Explain E11, not numerical instability. C09/C11/C21.
- **Transition:** “The full grid shows how these resource outcomes intersect geometry and margin gates.”

**Table 4 — Worked cases.** Select `PAY-MESH-OEM`, `obstructed_reference`, `separation_km=10`, `relay_altitude_m=120`; sort by dwell. Print 30/45/60 rows in main text. Put 10/20 rows and slope column in Supplement S2.

| Dwell (min) | Gross mass (kg) | Rotor diameter (m) | Battery branch | Energy-branch slope | Label |
|---:|---:|---:|---|---:|---|
| 10 | 5.4170 | 0.5309 | Power | 0.366027 | PASS |
| 20 | 5.4170 | 0.5309 | Power | 0.540284 | PASS |
| 30 | 8.6203 | 0.6697 | Energy | 0.714541 | PASS |
| 45 | 106.2456 | 2.3511 | Energy | 0.975927 | EXCLUDED |
| 60 | No finite solution | Not defined | None admissible | 1.237313 | NO CLOSE |

Power-branch slope is 0.570330 throughout. Hop margins remain 7.974/10.018 dB. At 45 min all three physical bounds fail; at 60 min never print a last-iterate or inconsistent-candidate mass as physical. Four-decimal output is for reproduction, not measurement precision; prose uses 8.62 and 106.25 kg.

**Caption:** “Calculated dwell cases for one geometry. PASS denotes the physical screen, not validated service. The 45-minute mass is extrapolation outside the exploratory envelope; nonclosure has no reported physical size.”

### 4.2 Baseline envelope and partial assessments

**Purpose:** Quantify the information added by intersection without a false performance claim.

- **Paragraph 1 topic:** “The baseline partitions into four limiting states.” State 18/6/6/60. In Figure 3, 60 m stays blocked; at 120/240 m, 5/10/20 km pass links, with 10-30 min physical passes, 45 min exclusions, 60 min nonclosures. At 30/40/60 km margins fail. C14.
- **Paragraph 2 topic:** “Neither individual screen equals the combined pass set.” Table 5B: 30 relay-link passes, 54 carrier passes, 18 intersection passes. Thirty link passes comprise 18 passes, 6 finite exclusions, 6 nonclosures. C15/C20.
- **Paragraph 3 topic:** “Direct sufficiency changes relay benefit in the clear comparator.” Raw intersection 27 differs from 9 benefit passes because 18 intersection cases are already direct-sufficient. Total direct-sufficient count is 30, including cases not passing carrier resources. C19.
- **Limit:** Counts describe an enumerated grid, not sampling probabilities or algorithmic superiority.
- **Transition:** “The remaining comparisons test which boundaries move with screen geometry or excess loss.”

**Table 5A — Primary partitions.** Filter primary payload, group by Table 3C scenario, count E14 labels. Include zeros; every row sums to 90.

| Scenario | DIRECT | PASS | EXCLUDED | NO CLOSE | LINK FAIL |
|---|---:|---:|---:|---:|---:|
| Clear reference | 30 | 9 | 3 | 3 | 45 |
| Baseline screen | 0 | 18 | 6 | 6 | 60 |
| Baseline +12 dB | 0 | 6 | 2 | 2 | 80 |
| 60 m screen at 0.40D | 0 | 18 | 6 | 6 | 60 |
| 100 m screen at 0.40D | 0 | 9 | 3 | 3 | 75 |
| 80 m screen at 0.30D | 0 | 9 | 3 | 3 | 75 |
| 80 m screen at 0.45D | 0 | 18 | 6 | 6 | 60 |

**Table 5B — Partial screens for the same 90 cases.** Existing flag re-tabulation, not new simulations or an independent benchmark. Print the first three rows in main text; full panel in Supplement S3.

| Scenario | Direct `D_ok` | Relay `R_ok` | Carrier `V_ok` | `R_ok AND V_ok` | `NOT D_ok AND R_ok AND V_ok` |
|---|---:|---:|---:|---:|---:|
| Clear reference | 30 | 45 | 54 | 27 | 9 |
| Baseline screen | 0 | 30 | 54 | 18 | 18 |
| Baseline +12 dB | 0 | 10 | 54 | 6 | 6 |
| 60 m screen at 0.40D | 0 | 30 | 54 | 18 | 18 |
| 100 m screen at 0.40D | 0 | 15 | 54 | 9 | 9 |
| 80 m screen at 0.30D | 0 | 15 | 54 | 9 | 9 |
| 80 m screen at 0.45D | 0 | 30 | 54 | 18 | 18 |

Each scenario's carrier-only outcomes are 54 passes, 18 finite exclusions, 18 nonclosures.

**Caption:** “Panel A is mutually exclusive and sums to 90 per row. Panel B contains overlapping sets and must not be summed. A raw link/carrier intersection is not relay benefit when the direct path already passes.”

### 4.3 Scenario sensitivity and null findings

**Purpose:** Describe sampled changes without statistical robustness claims.

- **Paragraph 1 topic:** “The loss stress reduces the link-functional grid.” State 6/2/2/80; carrier counts stay 54/18/18 because carrier inputs do not change. C16.
- **Paragraph 2 topic:** “Screen height and position move the strict clearance threshold.” Figure 4 uses values below. Thresholds above 120 m remove that layer, leaving nine passes at 240 m. C17.
- **Paragraph 3 topic:** “Unchanged states are informative only at the tested resolution.” Two lower-threshold variants keep 60 m blocked and 120/240 m clear. No continuous insensitivity follows. C17.
- **Paragraph 4 topic:** “Secondary payload cases preserve the coarse baseline boundaries under common service assumptions.” One sentence only; full data in S4. No hardware equivalence. C18.
- **Transition:** “The results support a decision interpretation narrower than operational feasibility.”

Figure 4 data in order: `(80 m,0.40D):100.000 m`; `(60 m,0.40D):75.000 m`; `(100 m,0.40D):125.000 m`; `(80 m,0.30D):133.333 m`; `(80 m,0.45D):88.889 m`. Relay height must be strictly above threshold. Add no altitude samples.

## 5. Discussion

### 5.1 What decision the assessment supports

**Purpose:** Explain engineering reasoning without asserting proven remedies.

- **Paragraph 1 topic:** “Different mechanisms identify different assumptions to reconsider.” Failed links require reconsidering geometry or link assumptions; greater dwell capacity with unchanged RF assumptions cannot repair them. Finite exclusion calls for changes to demand, carrier assumptions, or physical bounds. Nonclosure requires changing the resource relationship; a raised mass ceiling cannot create a solution. C21.
- **Paragraph 2 topic:** “The contribution is transparency of the case and its accounting.” Use the 30/54/18 comparison to explain what each screen leaves undecided. No competing optimization method was implemented or outperformed. C20/C25.
- **Limit:** No selected remedy, radio, achievable larger aircraft, or universal best altitude.
- **Transition:** “That usefulness must be assessed alongside the fidelity and provenance of the assumptions.”

### 5.2 Technical limitations and alternative interpretations

**Purpose:** Address the strongest credible objections directly.

- **Paragraph 1 topic:** “The combined envelope depends on largely separable assumptions.” Altitude changes links, not density; fixed payload attributes connect the calculations. This is not full communications/aircraft co-design. C03.
- **Paragraph 2 topic:** “A physical-boundary pass is conditional on parametric carrier assumptions.” Explain fixed disk loading, efficiencies, structure allowances, and uncalibrated 170 Wh/kg and 0.83 nominals. Near-singularity outputs are unsuitable as point designs. C08/C11/C27.
- **Paragraph 3 topic:** “A received-level opportunity is not demonstrated communications service.” State absent interference, duplex/scheduling, channel variation, throughput, reverse-link and command-link evaluation; the screen excludes diffraction/Fresnel/terrain mechanisms. C05/C30.
- **Paragraph 4 topic:** “Neither grid counts nor software checks provide a physical uncertainty interval.” Deterministic cases and public-aircraft scale context supply no matched prediction residuals. No reliability probability, physical accuracy, or affordability claim follows. C14/C23/C24.
- **Transition:** “The conclusions therefore concern architecture screening under declared conditions.”

### 5.3 Prior work and evidence needed for broader claims

**Purpose:** Close the novelty argument without promising future results.

- **Paragraph 1 topic:** “The results complement existing energy and sizing analysis through an explicit case-level decision record.” Refer to Table 1 without repeating source summaries. Originality, if judged sufficient, is the case and assessment, not new theory. C25/C26/C28.
- **Paragraph 2 topic:** “Broader performance claims require independent evidence.” Identify matched measured hover power/mass, supported installed-payload demand, and mission/communications measurements as absent evidence types. This is not a hardware test plan or completed validation. C24/C27/C30.
- **Limit:** Do not append proposed optimization, new terrain scenarios, or speculative numerical improvements.
- **Transition:** “Within those limits, the assessment answers the declared screening question.”

## 6. Conclusion

**Purpose:** Approximately 150 words answering the question, with no new findings. Use five sentences:

1. “The proposed multirotor relay architecture was assessed through explicit connectivity, analytical closure, and exploratory physical-envelope gates.” C01/C03.
2. “Under the baseline assumptions, 18 of 90 sampled cases passed all required screens, while the remaining cases were classified as connectivity failures, finite physical exclusions, or mathematical nonclosures.” C14; these are cases, not a success rate.
3. “The worked dwell comparison shows why finite sizing and physical-boundary compliance cannot be treated as the same outcome.” C11.
4. “The excess-loss and obstruction comparisons show that the sampled envelope changes with the declared scenario assumptions.” C16/C17.
5. “The decision value is explicit identification of the limiting mechanism; full-mission service and physical aircraft performance remain unvalidated.” C21/C24/C30.

No readiness, selected-design, guaranteed acceptance, or promise that future measurements will confirm the model.

## C. Figure production specifications

These are instructions for future manuscript artwork. Existing SVGs are source exhibits; new composites/charts remain pending. Do not reproduce copyrighted literature figures.

### Figure 1 — Architecture and scenario boundary

**Status:** New two-panel composite specified. Reuse concepts from [project schematic](figures/project-in-one-picture.svg) and [system boundary](figures/system-boundary.svg).

**Panel A:** G → relay payload on carrier → U mission arrows. Carrier command is a separate logical path; do not depict independent fault protection. Label mounting and power supply.

**Panel B:** Worked geometry with x-axis “Distance from ground endpoint (km)” and z-axis “Height above common datum (m)”; G=(0,0), R=(5,120), U=(10,100), screen=(4,80). Annotate direct height at screen=40 m and first-hop height=96 m. Mark vertical exaggeration. Dashed direct and solid relay paths must be legible in monochrome.

**Caption:** “Proposed relay architecture and worked geometry. Quantitative assessment covers stationary Ground → Relay → Remote dwell. The ideal screen blocks the direct path and clears the relay path; it is not measured terrain. Command separation is logical, not demonstrated physical fault isolation.” C01/C02/C06.

### Figure 2 — Implemented dependencies

**Status:** Existing [architecture-causal-chain.svg](../analysis/results/architecture-causal-chain.svg); re-typeset labels if necessary without changing arrows.

**Message:** Geometry/RF assumptions feed connectivity; payload mass/DC/dwell and carrier assumptions feed closure/physical screens; outputs enter ordered classification. No link-margin arrow back to payload sizing. No axes.

**Caption:** “Implemented dependencies of shared-payload screening. Fixed payload attributes enter two largely separable calculations classified together. Altitude affects connectivity but not the constant-density hover calculation.” C03.

### Figure 3 — Primary baseline service map

**Status:** Existing [architecture-tradespace.svg](../analysis/results/architecture-tradespace.svg).

**Data:** Primary payload and `obstructed_reference`; 90 unique cases. Columns separation 5/10/20/30/40/60 km; rows dwell 10/20/30/45/60 min; altitude panels 60/120/240 m. Keep text codes PASS, EXCLUDED, NO CLOSE, LINK FAIL as well as color. DIRECT is absent in baseline.

**Caption:** “Calculated baseline classifications for 90 primary cases. PASS denotes relay benefit plus exploratory physical screening; EXCLUDED is finite closure outside the envelope; NO CLOSE has no finite carrier state; LINK FAIL is the earlier connectivity gate. These are deterministic outcomes, not probabilities.” C14/C15.

### Figure 4 — Screen clearance thresholds

**Status:** New chart specified from existing [obstruction-sensitivity.csv](../analysis/results/obstruction-sensitivity.csv), without new model evaluations.

**Layout:** Horizontal dot plot; x-axis “Required relay altitude threshold (m)” from 0-250 m; y-axis five scenarios in Section 4.3 order. Plot thresholds, annotate one decimal, add labeled dashed vertical lines at sampled 60/120/240 m. Label direction “clear only above threshold.” No fitted curve or confidence bars.

**Caption:** “First-hop strict clearance thresholds for the five screen scenarios. Thresholds above 120 m remove that altitude layer; changes remaining between 60 and 120 m do not alter sampled visibility. This is geometric scenario comparison, not a terrain or uncertainty model.” C17.

**Artwork acceptance:** Inspect all final figures at column width for legibility, units, non-color distinctions, and honest captions. Check final manuscript PDF for clipping, tiny legends, numbering, and overflow. No final manuscript PDF or new artwork was produced in this outline task.

## D. Supplement and exact data handoff

- **S1 — Complete assumptions:** Full Table 3 with FI/MI/PI keys and source/assumption distinctions. An input label such as `B_exogenous_evidence` is not a validation stamp. Separate device references and integration allowances.
- **S2 — Algebra and worked cases:** E9-E10 derivation and full Table 4; energy/power tie rule and diagnostic guard. Slopes six decimals, masses/diameters four, margins three for reproducibility, not measurement precision.
- **S3 — Case accounting:** Full Table 5, exact Section 4 filters, unchanged CSV/JSON, classifier mapping once. Denominators 90 per primary scenario; repeated scenario/payload rows are not independent observations.
- **S4 — Secondary cases:** `PAY-HELIX-NANO`: 0.15 kg, 4 W DC, 1.3 W RF; `PAY-MESH-OEM`: 0.20 kg, 14 W DC, 1.6 W RF; `PAY-SC4200-PLUS`: 0.36 kg, 24 W DC, 10 W RF. Each has identical case-by-case baseline labels and counts 18/6/6/60. Treat as existing assumed cases; detailed secondary manufacturer claims were not revalidated here. Secondary peak-power metadata is not an extra solver demand.
- **S5 — Standalone carrier context:** Retain only in supplementary material: 225 carrier grid cases and 4,096 sensitivity candidates are separate from mission cases. Any ranking must state 2,605 finite closures, 1,491 excluded nonclosures, and RMS aggregation of three Spearman correlations. Keep cost and ranking out of abstract/main results/conclusion. Reuse existing outputs; no new plots required.
- **S6 — Reproduction:** Supply [read-only checker](reference/check-manuscript-evidence.py), [evidence audit](reference/manuscript-evidence-audit.md), and commands below. Record actual submission revision and scientific-file hashes emitted by the checker. Do not label this working-tree snapshot a released dataset.

```text
python -B -m unittest discover -s tests -v
python -B scripts/validate-baseline.py --check-generated
python -B docs/reference/check-manuscript-evidence.py
git diff --check
```

## E. Writer acceptance checklist and reviewer objections

| Check / likely objection | Required response |
|---|---|
| “Is this two familiar models?” | Bounded case-study contribution, Table 5B, and explicit decisions; no novelty inflation |
| “Why trust the numbers?” | E1-E14, complete inputs, filters, tests, and independent audit; mathematical reproduction differs from physical evidence |
| “Are inputs measured?” | Table 3 distinguishes source values/assumptions; 170 Wh/kg and 0.83 remain uncalibrated nominals |
| “Does benefit mean traffic is delivered?” | Geometry/received-level screening only; no demonstrated protocol or throughput |
| “Is the 106 kg aircraft meaningful?” | Finite extrapolation excluded at point of use; never proposed as an aircraft |
| “How robust is the envelope?” | Tested deterministic scenarios only; no probabilities, continuous optimum, or uncertainty intervals |
| “What is new?” | Checked Table 1 and precise contribution; no first-of-kind or new-physics claims |
| Claim support | Every substantive assertion maps to C01-C30 or a checked source; omit new unsupported assertions |
| Tables/units | Table 5A rows sum to 90; Panel B is not summed; no nonclosure mass; minutes-to-hours for Wh |
| Equations | One notation set; distinguish RF/DC, total/per-rotor area, required/installed energy, branch validity/convergence |
| References | Use the audit's verified records and fixed citation mapping; no invented DOI/journal details |
| Artwork/end matter | Produce specified pending Figure 1/4, inspect final PDF, obtain factual authorship/funding/release information; these are future production steps |

**Ready-to-write boundary:** Argument, equations, inputs, tables, literature positioning, qualifications, and exhibit instructions are specified. The handoff does not certify acceptance. Stronger novelty or physical validation, if required by an outlet, remains an evidence gap that prose cannot remove.
