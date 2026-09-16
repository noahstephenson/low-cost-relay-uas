# Manuscript evidence audit

> **Superseded.** This audit predates the carrier calibration (commit `4f9e2cd`, branch `codex/carrier-calibration-v1`) and the finished manuscript. The submitted paper in `submission/relay_uas_aeroconf.tex` (local, intentionally untracked; see `.gitignore`) is the sole authority for claims and numbers. Treat everything below as historical drafting context.

Audit date: 2026-09-11. Scientific baseline: `71ed88815fd5c5ebe9846bac140cc0628336825e` plus the current working tree. Documentation changes from the earlier venue-removal task were already present. No scientific input, model, experiment, or generated scientific output was changed for this audit.

Read with the [writer-ready outline](../manuscript-outline.md). This record controls manuscript claims if older narrative documentation differs. It verifies a conditional calculation, not an aircraft. The defensible contribution is a reproducible architecture case study with explicit decision gates; novelty and acceptance remain uncertain.

## 1. Evidence hierarchy and use

1. For what was calculated, use executable equations, declared inputs, and independently checked case records.
2. For what is physically supported, use original technical sources and measured evidence. Correct code cannot validate an assumption.
3. For literature claims, use the checked primary sources below. Do not infer an absence from an abstract or from this focused search.
4. Treat earlier narrative summaries as interpretations. Correct their wording in the manuscript rather than inheriting claims of physical credibility.

Dispositions: **supported** means supported at the explicitly stated scope; **assumption** means deliberately declared rather than demonstrated; **needs qualification** permits only the bounded wording listed; **unsupported** means omit the claim. Claim IDs below are authoring aids, not text to print in the final paper.

Local evidence keys:

- **MC:** [mission_connectivity.py](../../analysis/mission_connectivity.py), functions `visible`, `link_margin_db`, `link_case`, `classify`, and `build`.
- **FC:** [feasibility.py](../../analysis/feasibility.py), functions `analytical_closure` and `solve_point`.
- **MI:** [mission inputs](../../analysis/mission-connectivity-inputs.yaml).
- **FI:** [carrier inputs](../../analysis/feasibility-inputs.yaml).
- **PI:** [payload inputs](../../analysis/relay-payloads.yaml).
- **DATA:** [case records](../../analysis/results/integrated-tradespace.csv), [summary](../../analysis/results/integrated-tradespace-summary.json), and [screen comparison](../../analysis/results/obstruction-sensitivity.csv).
- **ARCH:** [architecture-to-evidence assessment](../architecture.md#architecture-to-evidence-assessment).

## 2. Claim register

| ID | Disposition | Exact permitted wording | Evidence and verification | Qualification / author action |
|---|---|---|---|---|
| C01 | supported | The study documents a proposed multirotor relay architecture and screens a declared stationary outbound service. | ARCH; MC `build`; input-to-result inspection | Architecture allocation is descriptive, not novel theory or demonstrated behavior. |
| C02 | needs qualification | Mission traffic and carrier command are logically distinct architectural responsibilities. | ARCH and [command/data flow](../figures/command-data-flow.svg) | No tested electrical, physical, or fault isolation; shared failures remain possible. |
| C03 | supported | Connectivity and carrier resources are intersected using fixed payload assumptions. | MC `link_case` and `solve_point` arguments | Not radio/vehicle co-optimization; RF margin never changes payload demand; altitude does not change carrier density. |
| C04 | assumption | The primary payload is represented by 0.20 kg and a continuous 14 W sizing allowance. | PI; R8 verifies 102 g device, 5 W receive and 14 W peak; integration addition is 98 g | Neither installed mass nor average power is measured. RF/DC operating-point compatibility is unverified. |
| C05 | assumption | The screen, service threshold, gains, losses, and mission grid are declared analysis scenarios. | MI; outline Table 3A | No actual terrain, waveform, throughput, or authorization claim. Bandwidth is metadata, not a rate calculation. |
| C06 | supported | The baseline direct path is blocked; midpoint relay altitudes above 100 m clear the first hop in the declared geometry. | MC `visible`; independent line interpolation: 40 m direct height and 96 m first-hop height at a 4 km screen in the worked example | Clearance is strict `>`; equality is blocked. Screen is before the relay; second hop does not cross it. No Fresnel/diffraction treatment. |
| C07 | supported | At 10 km separation and 120 m relay altitude, the first and second hop margins are 7.974 and 10.018 dB. | MC; DATA; independent path-distance and dB calculation | Direct margin 5.955 dB is hypothetical clear-path margin; the actual modeled direct path is blocked. |
| C08 | supported | At fixed disk loading, the implemented propulsion power and disk area scale linearly with gross mass. | FC; substitute area into momentum expression; coefficients 108.4529369 W/kg and 0.1634442 m²/kg | A family of resized rotors, not a fixed-airframe endurance prediction. |
| C09 | supported | A finite carrier result must satisfy a positive, branch-consistent mass closure. | FC `analytical_closure`; independent bisection of original mass balance | Positive intercepts and nonnegative coefficients hold for these inputs. Do not generalize the criterion to arbitrary signed models. |
| C10 | supported | The sampled 10- and 20-minute cases are power-sized; the 30- and 45-minute cases are energy-sized. | Independent battery-branch comparison at closed mass, primary payload | The sampled branch change is between 20 and 30 min; no precise continuous transition is claimed. |
| C11 | supported | The worked 30-minute case closes at 8.6203 kg and passes exploratory physical boundaries; 45 minutes closes at 106.2456 kg and fails them; 60 minutes has no finite closure. | DATA and independent mass-balance roots | 45-minute mass is an extrapolation, not a proposed aircraft. 60-minute mass and rotor diameter must remain absent. |
| C12 | assumption | Physical screening uses ceilings of 15 kg, 0.75 m rotor diameter, and a 1.5 m footprint proxy. | FI `analysis_practical_boundaries` | Not owner requirements, safety limits, or demonstrated packaging. |
| C13 | supported | The rotor and footprint tests are redundant; the rotor ceiling implies a 10.8119 kg mass ceiling at the reference disk loading. | `span=2d`; independent `n*pi*d²*DL/(4g)` | Applies only to the stated four-rotor, 60 N/m² model. |
| C14 | supported | The baseline partitions 90 unique primary cases into 18 passes, 6 finite exclusions, 6 nonclosures, and 60 connectivity failures. | DATA; independent grouping and classifier | Ordered, mutually exclusive labels, not probabilities or independent failure frequencies. |
| C15 | supported | Before connectivity gating, the same primary cases contain 54 carrier passes, 18 finite exclusions, and 18 nonclosures. | DATA flags; independent counts | A different view of the same 90 cases. Connectivity can mask simultaneous resource failure. |
| C16 | supported | Adding 12 dB excess loss to the baseline screen produces 6 passes, 2 finite exclusions, 2 nonclosures, and 80 connectivity failures. | DATA; independent margins/classification | Deterministic stress case; no measured loss distribution or confidence level. |
| C17 | supported | The screen-family thresholds are 100, 75, 125, 133.333, and 88.889 m; the two thresholds above 120 m halve the baseline pass count to 9. | MI, DATA; independent interpolation | Coarse-grid outcome, not an optimal altitude or continuous robustness result. |
| C18 | needs qualification | All three payload cases share the same baseline classification boundaries on this grid. | DATA grouped by payload/scenario | RF output also varies; call this a secondary payload-case comparison, not a pure SWaP experiment. Hardware equivalence is unsupported. |
| C19 | supported | The clear-reference scenario labels 30 cases direct-sufficient and 9 cases relay-beneficial physical passes. | DATA; independent direct-first classification | Its raw relay-plus-carrier intersection is 27; 18 of these are already direct-sufficient. This difference is accounting, not a contradiction. |
| C20 | supported | Baseline relay-link screening passes 30 cases, carrier-only screening passes 54, and their intersection passes 18. | DATA; independent Boolean intersections | Illustrates decision information; no claim of better prediction accuracy or benchmark-algorithm superiority. |
| C21 | supported | Distinct failures imply different assumptions to reconsider. | C03, C09, C12 and first-applicable gate logic | Increasing battery capacity alone does not repair an unchanged failed link; relaxing a mass limit cannot repair nonclosure. These are model implications, not tested remedies. |
| C22 | needs qualification | The finite-subset carrier sensitivity ranking excludes nonclosing cases. | [sensitivity data](../../analysis/results/sensitivity-ranking.csv), [carrier summary](../../analysis/results/feasibility-summary.json), FC aggregation | 2,605 of 4,096 finite; conditional RMS of three Spearman correlations. Keep out of main paper; do not rank causes of nonclosure. |
| C23 | supported | Nineteen repository tests passed and all checked generated artifacts were current on the audit date. | Commands and results in section 5 | Code and artifact verification only, not independent physical validation. |
| C24 | unsupported | Omit: The aircraft is validated, airworthy, operationally ready, affordable, or guaranteed to meet its mission. | No matched physical dataset, full-mission calculation, or selected implementation | No substitute claim beyond conditional screening. |
| C25 | unsupported | Omit: This is the first work to combine communication and propulsion energy or to identify a battery-mass penalty. | R2, R3, R4 contradict that broad novelty claim | Use the precise case-study contribution in the outline. |
| C26 | unsupported | Omit: Sizing nonclosure is a newly discovered phenomenon. | R5 discusses sizing failure as mission time increases | Repository branch analysis is transparent model accounting, not a new physical law; do not equate NASA numerical sizing failure with this exact affine criterion. |
| C27 | needs qualification | The nominal battery and efficiency values are assumptions informed by broad engineering context. | FI; R5 reports approximately 135 Wh/kg stated capacity, approximately 110 Wh/kg after its usable-capacity rule, and 75% drive efficiency | R5 does not directly establish this study's 170 Wh/kg or 83%. Do not call these NASA-validated inputs. |
| C28 | supported | Established research addresses relay trajectories, communication/propulsion energy, and battery-weight choices. | R1-R4 checked primary sources | No exhaustive state-of-the-art or absence-of-prior-work claim. |
| C29 | supported | The free-space attenuation form is established; the implementation retains a 32.44 dB unit-conversion constant. | MC; R6 Eq. (6) uses rounded 32.4 | Preserve the implemented constant for reproduction; do not claim numerical identity to the rounded standard. |
| C30 | needs qualification | These results assess an assumed outbound service opportunity, not delivered packet performance. | MC only tests geometry and received-level margins | No interference/scheduling, duplex protocol, relay throughput, reverse traffic, or carrier command performance model. |

## 3. Checked bibliography and closest-work comparison

Reference keys are stable; manuscript first-use order is R1=[1], R2=[2], R3=[3], R4=[4], R5=[5], R8=[6], R6=[7], R7=[8]. Checked 2026-09-11. This was a focused primary-source search for the closest conceptual precedents, not a systematic review or proof of novelty. Search terms included mobile relay throughput, rotary-wing communication energy, relay endurance, battery weight, and small-UAS conceptual sizing. Source summaries below are deliberately narrow.

### Bibliographic records

- **R1 / [1]** Y. Zeng, R. Zhang, and T. J. Lim, “Throughput Maximization for UAV-Enabled Mobile Relaying Systems,” *IEEE Transactions on Communications*, vol. 64, no. 12, pp. 4983-4996, 2016, DOI: [10.1109/TCOMM.2016.2611512](https://doi.org/10.1109/TCOMM.2016.2611512). Publisher abstract/metadata checked; author manuscript [arXiv:1604.02517](https://arxiv.org/abs/1604.02517). Use only for joint source/relay power and trajectory optimization with mobility/information-causality constraints. Do not claim absence of particular mechanisms based on abstract access.
- **R2 / [2]** Y. Zeng, J. Xu, and R. Zhang, “Energy Minimization for Wireless Communication With Rotary-Wing UAV,” *IEEE Transactions on Wireless Communications*, vol. 18, no. 4, pp. 2329-2345, 2019. Publication details checked against the [author's institutional bibliography](https://www.ece.nus.edu.sg/stfpage/elezhang/publication_UAV.html); methods checked in [author manuscript, arXiv:1804.02238v1](https://arxiv.org/html/1804.02238v1), Sec. II-B/C, Appendix A. Publisher DOI access failed; cite the verified journal details and accessible manuscript without relying on unchecked publisher text.
- **R3 / [3]** H. Yan, S.-H. Yang, Y. Chen, and S. A. Fahmy, “Optimum Battery Weight for Maximizing Available Energy in UAV-Enabled Wireless Communications,” *IEEE Wireless Communications Letters*, vol. 10, no. 7, pp. 1410-1413, 2021, DOI: [10.1109/LWC.2021.3069078](https://doi.org/10.1109/LWC.2021.3069078). Metadata: [Warwick accepted-manuscript record](https://wrap.warwick.ac.uk/id/eprint/150537/). Methods: [author-hosted accepted manuscript](https://sfahmy.github.io/publications/2021-wcl-yan.pdf), Sec. II-III, pp. 1-3. Do not treat manuscript header placeholders as journal metadata.
- **R4 / [4]** H. Rodrigues, A. Coelho, M. Ricardo, and R. Campos, “Energy-aware Relay Positioning in Flying Networks,” [arXiv:2007.12284v4](https://arxiv.org/abs/2007.12284), Jan. 25, 2022 revision; first posted 2020. [Author manuscript](https://arxiv.org/pdf/2007.12284). Cite explicitly as an arXiv manuscript; no journal metadata was established in this audit. Abstract and methods describe propulsion-aware relay trajectory/speed selection and simulation evaluation.
- **R5 / [5]** C. R. Russell, C. R. Theodore, and M. K. Sekula, “Incorporating Test Data for Small UAS at the Conceptual Design Level,” AHS International Technical Meeting on Aeromechanics Design for Transformative Vertical Flight, 2018, NASA record 20180008701, report ARC-E-DAA-TN51087. [NASA-hosted paper](https://rotorcraft.arc.nasa.gov/Publications/files/Russell_2018_TechMx.pdf). Check component models pp. 4-5, Table 1 p. 10, and sizing discussion pp. 10-11 (PDF one-based pages). The NTRS landing page failed to open, but the NASA paper and indexed NTRS metadata were available. Use the meeting year, not the search engine's crawl/publication-age label.
- **R6 / [7]** ITU-R, *Calculation of free-space attenuation*, Recommendation P.525-5, Nov. 2024, Sec. 2, Eq. (6). [Official recommendation and status](https://www.itu.int/rec/R-REC-P.525-5-202411-I/en); [official PDF](https://www.itu.int/dms_pubrec/itu-r/rec/p/R-REC-P.525-5-202411-I%21%21PDF-E.pdf). Supports the free-space formula, not the chosen losses, gains, threshold, or screen model.
- **R7 / [8]** W. Johnson, *NDARC: NASA Design and Analysis of Rotorcraft, Theory*, NASA/TP-2009-215402, Appendix 3, Release 1.7, Dec. 2012. [NASA PDF](https://rotorcraft.arc.nasa.gov/Publications/files/NASA%20TP-2009-215402-app3.pdf), nomenclature and Sec. 7-10. The report number contains 2009; the accessed appendix is dated 2012. Supports rotorcraft sizing/hover definitions, not validation of this reduced model or its coefficients.
- **R8 / [6]** Doodle Labs, “OEM,” product page, accessed Sep. 11, 2026. [Manufacturer source](https://doodlelabs.com/product/oem/), Hardware and RF Specs. Supplies device-level reference values only. Do not import advertised range, data rate, security, or latency into the manuscript claims.

### Comparison to closest work

| Source | Problem and direction | Energy/payload treatment | Constraints / validation visible in checked evidence | Consequence for this manuscript |
|---|---|---|---|---|
| R1 | Source-relay-destination mobile relaying | Source/relay transmit power and trajectory | Mobility and information causality; numerical evaluation | Relay placement/power integration is established. No claim to outperform it; its protocol is not implemented here. |
| R2 | UAV sends/collects data with ground nodes | Propulsion plus communication energy; trajectory/time allocation | Throughput constraints; analytical model and numerical study | Combined energy/communications is prior art. Here the output is a fixed-payload screening partition, not optimized service. |
| R3 | Fly to sensors, communicate, return | Battery mass affects energy available after propulsion; nonbattery mass specified | Vertical/horizontal mission legs; analytical and numerical solutions | Battery-mass tradeoffs predate this work. This repository omits the transit/return legs included there. |
| R4 | Flying communications relay | Propulsion-aware trajectory and speed | Network service objectives; simulations | Relay endurance and network performance have already been considered together. No efficiency advantage is established here. |
| R5 | Small quadcopter design and hover mission sizing | Component sizing, battery specific energy, payload and mission duration | Wind-tunnel/hover data and component measurements inform models | Neither sizing feedback nor failure to close is new. Its validation does not transfer to this repository. |
| This study | Fixed midpoint Ground → Relay → Remote dwell | Fixed payload mass/DC/RF assumptions; resized carrier closure | Stylized screen, link margin, exploratory geometry/mass limits; software verification | Contribution is the transparent, reproducible case and its separated decision gates. No demonstrated methodological superiority. |

**Novelty decision:** Do not write that a missing integrated framework has been discovered. Write: “This study presents a reproducible architecture case study that separates connectivity failure, finite sizing outside an exploratory envelope, and mathematical nonclosure under explicitly declared assumptions.” A claim that this taxonomy itself is unprecedented remains **unsupported** and is omitted. The focused review suffices to reject broad novelty claims, not to certify originality across all literature.

## 4. Discrepancies and evidence gaps

| Issue | Finding | Required manuscript treatment |
|---|---|---|
| Older physical-credibility prose | [Detailed feasibility report](feasibility-analysis.md) begins with a “credible” physical region; current evidence is low-order and unvalidated | Use “conditional physical-boundary pass.” Do not inherit a physical credibility assertion. |
| Weak numerical provenance | R5 gives approximately 135 Wh/kg stated battery capacity (approximately 110 after its usable-capacity rule) and 75% drive efficiency, not FI's 170 and 83% | Table 3B calls these declared nominal assumptions. Do not apply usable-energy derating twice or claim the cited NASA study measured these nominal values. |
| Secondary “SWaP” wording | PI changes maximum RF output as well as mass/DC demand; service threshold stays common | Call it a payload-case comparison. Do not isolate mass/power effects experimentally from that comparison. |
| Apparent singularity novelty | R5 already reports mission-time sizing nonclosure | Explain this model's branch criterion; do not equate two different solvers or claim discovery of a universal limit. |
| Direct sufficiency precedence | Clear-reference raw intersection has 27 cases but only 9 relay-beneficial passes | Report the 18 already-direct-sufficient overlap, and retain direct-first counting. |
| Receiver thresholds in PI | Per-product threshold fields are not used by MC | Use MI's common -90 dBm throughout; no mixed manufacturer sensitivity comparison. |
| Bandwidth field | 5 MHz is service context only | No bit rate, capacity, latency, packet delivery, interference, scheduling, duplex, or reverse-link claim. |
| “Upper-load” assumption | Device peak value is used continuously, but installed integration demand and operating-point compatibility are not verified | Do not call the whole aircraft calculation conservative or a guaranteed upper bound. |
| Classical power approximation | Figure of merit and drive efficiency are constant; structural/propulsion scaling is parametric | Do not extrapolate near-singularity results as hardware designs; do not suggest a fixed-size rotor grows physically. |
| Physical and archival gaps | Existing validator reports 10 active architecture gaps, including unavailable physical evidence and recovered-source checksum mismatch | Exclude recovered-article reconstruction, conformance, or safety claims. Motivation can be omitted entirely without changing results. |
| PDF display access | Browser screenshot retrieval failed for two primary PDFs; text and source metadata were inspectable | No claim of complete graphical verification of those external papers. Only text-supported comparisons are used. |

No arithmetic/classification defect was found in the audited existing case grid. Input plausibility and physical validity remain unresolved; this audit does not silently replace or recalibrate them.

## 5. Verification record

Commands run from repository root:

```text
python -B -m unittest discover -s tests -v
python -B scripts/validate-baseline.py --check-generated
python -B docs/reference/check-manuscript-evidence.py
git diff --check
```

- Existing suite: **19 tests passed**, including independent hand-hover case, branch behavior, iteration-budget independence, classification precedence, primary loading, unique counts, and nonclosure output treatment.
- Baseline check: catalogs valid; architecture and communication views current; 7 carrier artifacts current; mission outputs current with 90 primary cases and 1,890 rows. Active architecture gaps remain reported, not resolved.
- Independent manuscript check: reconstructs links from coordinates and declared inputs, solves the original piecewise mass residual by bisection rather than importing either production solver, compares all 1,890 existing records, checks per-scenario summary counts and no physical mass for nonclosure. Mass/diameter tolerances are half a reported fourth decimal plus rounding allowance; margin tolerance is half a reported third decimal plus rounding allowance.
- The checker evaluates only existing grid records; it adds no scenarios, fits, models, or scientific outputs. It prints evidence to stdout and writes no files. It is intentionally a separate audit, not independent physical evidence.
- Reference values independently recovered: area/mass 0.1634441667 m²/kg; hover propulsion/mass 108.4529368711 W/kg; effective ceiling 10.8119237516 kg. At 30/45/60 min the energy-branch slopes are 0.7145410866 / 0.9759268413 / 1.2373125961; the power-branch slope is 0.5703304535 throughout.
- Every scenario has 90 unique primary records; all seven scenario partitions sum to 90. Primary per-scenario carrier counts remain 54/18/18.
- Documentation QA: all worked-case mass/diameter/branch/slope entries and both scenario-table panels were checked against the independent audit and saved flags. All 30 claim IDs, 14 equation groups, local links/anchors, fenced blocks, and trailing whitespace checks passed. A Git comparison confirmed that analysis, model, scripts, tests, and source-register files were unchanged.

## 6. Reviewer-style assessment

These are editorial assessment criteria, not an official conference scoring rubric.

| Criterion | Assessment | Response already required in the outline |
|---|---|---|
| Significance | Useful for explaining why a link pass does not establish an aircraft resource pass; application breadth is narrow | Lead with a concrete three-dwell decision example and quantify partial-versus-combined screening. |
| Originality | Main risk: established link, energy, and sizing ideas; close prior art exists | Explicit case-study contribution; no “first,” new physics, or optimization claim. |
| Technical correctness | Existing arithmetic, branches, and classifications reproduce; physical assumptions remain coarse | Complete equations, units, branch logic, source/assumption split, and bounded claims. |
| Reproducibility | Strong local evidence trail; independent numerical audit available | Cite exact submission revision and inputs; supply checker and case records. Current revision is an audit baseline, not a future submission revision. |
| Presentation | Writer can follow the fixed paragraph and exhibit sequence | Keep machine labels in one legend; explain each result as an engineering decision. |
| Limitations | No physical validation; no actual two-way service or full mission; sparse grid | Put scope in abstract, methods, captions, discussion, and conclusion without implying these gaps are solved. |

**Handoff verdict:** Ready to draft the narrow case study using the specified claims. Not certified as submission-ready or likely to be accepted. If stronger novelty or validated-performance evidence is required by an outlet, the current study cannot supply it through wording changes.

## 7. Submission benchmark (editorial only)

The project remains venue-neutral. As a quality benchmark, the [official IEEE Aerospace submission guidance](https://aeroconf.org/paper-submission) requires a complete, properly formatted paper and directs authors to the applicable template; incomplete drafts are not reviewed. This is a procedural requirement, not an endorsement of this study. The ten-page budget in the outline is an editorial choice, not a verified conference page limit. Before actual submission, the author must use the chosen outlet's current template and rules; no submission or target selection occurs here.
