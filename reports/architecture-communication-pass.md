# Human-Readable Architecture and Visual Communication Pass

This report records the penultimate communication work package performed from local
`main` at parent commit `b7bc7aacd3845ba0e48b72d7813eb129f98c7846` (`Add
coupled relay UAS feasibility analysis`). The feasibility work package was a separate
commit from its architecture-decision parent. This pass changes presentation,
controlled display aliases, deterministic rendering, and presentation validation. It
does not approve the technical baseline or change architecture intent.

## A. Five-Minute Readability Result

**Result: PASS, subject to the candid limitations in section K.**

The README now answers the outsider questions in a meaning-first sequence: what the
Relay UAS is, why its platform-control path is separate from relayed mission traffic,
what is onboard, what the project established, what the feasibility analysis found,
and what remains unfinished. No model ID is required before the reader reaches the
explicit engineering-detail section.

The non-systems-engineer test passed using only the README, the canonical concept
figure, and the canonical engineering-status figure. Those materials support an
accurate explanation of:

- the airborne-relay purpose and black-box payload boundary;
- the six major onboard subsystem roles;
- platform command, health/status, relayed command, and return telemetry;
- the plausible short-dwell/modest-payload feasibility region and its limitations;
- missing owner targets, physical evidence, external conformance, payload detail,
  future branches, and approval.

The systems-engineer handoff test also passed. README and `architecture.md` point to
the authoritative architecture, assurance, traceability, SEAL source/evidence,
trade-study, verification, gap, decision, and feasibility records. The generated
audit atlas and baseline report remain available below the plain-language layer.

## B. Diagrams Removed or Consolidated

Primary-page Mermaid was removed: README changed from one Mermaid diagram to no
Mermaid, and `architecture.md` changed from thirteen Mermaid diagrams to no Mermaid.
Both now reuse the deterministic canonical SVG set.

The generated audit atlas was reduced from 22 to 13 ID-rich Mermaid diagrams. The
following views were removed as separate diagrams because their information remains
in the model, inventory, prose, tables, or stronger consolidated views:

- structure and payload mounting;
- maintenance and configuration support;
- future digital interface delta;
- candidate evidence coverage;
- launch and positioning sequence;
- scenario lifecycle;
- health/status logical thread;
- hazard-control-requirement-verification graph; and
- evidence and approval governance graph.

The retained atlas views were retitled as human questions and explicitly positioned
as engineering audit drill-down, not as the five-minute entry point. The complete
interface inventory was preserved.

## C. New / Redesigned Diagrams

| Figure | Audience | Question answered | Structured source data |
|---|---|---|---|
| **The Relay UAS in One Picture** | Outsider, owner | What is the system doing, and why are its own control and relayed traffic separate? | Current performers, control/relay information exchanges, command receiver, and black-box payload in `model/architecture.yaml` |
| **What Is Inside This Project?** | Outsider, systems engineer | What is inside the product boundary and what remains external? | Inner/outer boundaries in `system.yaml`; current performers and payload records |
| **What Is On the Relay UAS?** | Outsider, systems engineer | What are the major physical subsystem groups? | All 19 component records, grouped for display; selected internal-interface relationships |
| **How Power Reaches Every Major Load** | Technically literate outsider, systems engineer | What powers propulsion, avionics, and the payload? | Battery, distribution, regulation, propulsion, avionics, payload, and seven asserted internal interfaces |
| **How Command and Telemetry Move** | Outsider, systems engineer | Which information controls the aircraft and which information passes through the payload? | Six information exchanges plus the external platform-command and health/status interfaces |
| **What Happens During a Relay Mission?** | Outsider, owner | What is the current-system mission sequence? | Current setup, positioning, relay-command, relay-telemetry, and recovery scenarios and activities |
| **What Happens When the Relay Is Lost?** | Outsider, owner, systems engineer | How does relay degradation differ from loss of aircraft control? | Current modes and transitions, degraded scenario, recovery/status requirements, and open safety/evidence gaps |
| **What Is Reference, Current, and Future?** | Outsider, systems engineer | How do evidence, current candidates, and future branches differ? | Controlled configuration records and predecessor lineage |
| **What Did the Project Actually Establish?** | Outsider, owner, auditor | Which results are established, conditional, pending, blocked, deferred, or not approved? | Model status, architecture counts, verification records, gap/TBD records, feasibility disposition, and decision state |
| **Conditional feasibility at 50 W payload demand** | Outsider, owner, systems engineer | Did a credible physical region appear in the reference analysis? | Deterministic feasibility grid generated by `analysis/feasibility.py` |

The nine architecture figures are generated by
`scripts/generate-communication-views.py`. Their controlled manifest records in
`system.yaml` state title, audience, question, and source object references. Visible
arrows are backed by asserted information exchanges, interfaces, mode transitions,
configuration lineage, scenarios, or status records; renderer-only architecture
edges are rejected by generation checks.

## D. ID Readability Improvements

Twenty-nine controlled `display_name` aliases were added to configuration,
performer, and component records. The authoritative IDs and original names remain
unchanged. Human-facing SVG text uses short plain-language names; its metadata keeps
the source IDs for provenance. Repository validation confirms every referenced ID
exists and rejects raw IDs in visible SVG text.

README exposes no raw architecture IDs in its five-minute portion. IDs appear only
after **Engineering detail and traceability**, where they are useful for audit and
handoff. `architecture.md` similarly leads with names and grouped explanations, then
adds IDs as secondary engineering references. The detailed generated atlas retains
ID-rich views on purpose.

## E. README Changes

README is now the primary five-minute entry point. Its information hierarchy is:

1. ordinary-language purpose and scope;
2. canonical project-in-one-picture view;
3. short operational sequence;
4. plain-language onboard subsystem table;
5. architecture, feasibility, and verification findings;
6. explicit unfinished work;
7. canonical engineering-status view; and only then
8. configurations, requirements, traceability, model navigation, regeneration, and
   scope constraints.

Governance remains visible in the opening warning, but it no longer displaces the
concept explanation.

## F. architecture.md Changes

`architecture.md` is now a twelve-section progressive-disclosure bridge:

1. system overview;
2. system context;
3. current physical architecture;
4. separate power and information flows;
5. current mission sequence;
6. modes and degradation;
7. reference/current/future configurations;
8. grouped key requirements;
9. representative traceability threads;
10. feasibility implications;
11. verification and maturity; and
12. detailed engineering references.

The document reuses all nine canonical architecture figures and the feasibility map
rather than rebuilding slightly different diagrams. Detailed IDs are introduced only
where they support engineering claims.

## G. Requirement Communication

The 28 authoritative requirements remain in `model/assurance.yaml`. A human-facing
translation groups their intent into Relay Function, Flight and Positioning, Payload
Support, Electrical Power, Command and Status, Portability and Affordability, Safety
and Recovery, and Deferred or External Topics. Each row explains the intended result
first and lists the `REQ-*` records second.

No requirement, value, target, verification disposition, or approval was changed to
make the summary cleaner. Controlled TBDs remain TBDs.

## H. Traceability Communication

Three representative threads replace the need for an outsider to decode the complete
relationship graph:

- extend remote-command reach through the black-box payload and external relay path;
- hold useful relay geometry through flight-control and navigation resources; and
- recover after relay degradation while retaining safety and evidence gaps.

Each is stated first as a human causal thread and then as a compact audit trace from
need/scenario through function, resource/interface, requirement, verification, and
gap. Complete traceability remains authoritative in `model/traceability.yaml`.

## I. Feasibility Communication

The README and architecture bridge now communicate the result in ordinary language:
a short-dwell, modest-payload region appears plausible under reference-or-better
assumptions, while endurance reinforces the battery-mass-power loop and the evaluated
45-60 minute reference cases fall outside the exploratory credible region.

The high-level view uses one 5-by-5 conditional map at 50 W rather than exposing all
225 grid cases or 4,096 sensitivity samples. Its larger cells, separated header, and
two-line limitation note were regenerated from the unchanged numerical results. The
detailed equations, assumptions, data, convergence traces, sensitivity ranking, and
limitations remain in `reports/feasibility-analysis.md` and `analysis/results/`.

## J. Visual Inspection Findings

All nine architecture SVGs and the feasibility SVG were rendered to PNG and visually
inspected. Parsing alone was not treated as evidence of readability. The inspection
found and corrected:

- crossing arrows and a long receiver label in the canonical concept figure;
- overflowing relay/future-platform titles and noisy interface labels in the boundary
  figure;
- colliding edge labels in the physical architecture, replaced by direct arrows and a
  concise relationship key;
- power-flow labels overlapping distribution and load boxes;
- a missing receiver-to-flight-controller step and a return-status line crossing
  nodes in the data-flow view;
- a mission recovery box obscuring the return-telemetry step;
- a return-to-ground arrow passing through the unresolved safety-gap box;
- category, arrow, and long configuration labels colliding in the evolution view;
- long engineering statuses and meanings colliding between columns; and
- cramped feasibility column headings and a clipped one-line limitation note.

The final renders use readable text at normal scale, directional consistency,
grouping, whitespace, boundary styling, dashed future/return relationships, and text
labels so meaning does not depend on color alone. A Chromium profile reuse artifact
briefly clipped the first word of isolated titles during QA; clean-profile and
independent Edge renders confirmed that the SVG source itself was intact.

## K. Remaining Communication Weaknesses

- Readability was tested by structured outsider simulation and visual inspection,
  not by an independent human usability study.
- The canonical SVGs are static. They carry source IDs in metadata but do not provide
  clickable drill-down from a visible element to a catalog record.
- The 13-diagram engineering atlas remains deliberately dense and ID-heavy. It is an
  audit layer and will still require systems-engineering familiarity.
- The high-level requirement and traceability summaries are selective; readers must
  use the catalogs for full wording, applicability, provenance, and coverage.
- Static layout is optimized for repository-page and briefing-scale viewing; very
  narrow mobile rendering may require opening the image separately.
- The communication layer cannot resolve the substantive unknowns it describes:
  owner targets, recovered-source gaps, payload implementation, safety behavior,
  physical verification, and external conformance remain open.

## L. Files Changed and Validation

Parent baseline:

- `b7bc7aacd3845ba0e48b72d7813eb129f98c7846`
- feasibility work package confirmed as a separate commit from its parent

Communication-pass source and narrative files:

- `README.md`
- `architecture.md`
- `system.yaml`
- `model/architecture.yaml`
- `analysis/feasibility.py`
- `scripts/generate-communication-views.py`
- `scripts/generate-mermaid-views.py`
- `scripts/validate-baseline.py`
- `reports/architecture-views.md`
- this report

Generated architecture figures:

- `reports/figures/project-in-one-picture.svg`
- `reports/figures/system-boundary.svg`
- `reports/figures/physical-architecture.svg`
- `reports/figures/power-resource-flow.svg`
- `reports/figures/command-data-flow.svg`
- `reports/figures/mission-sequence.svg`
- `reports/figures/degraded-behavior.svg`
- `reports/figures/configuration-evolution.svg`
- `reports/figures/engineering-status.svg`

Affected feasibility output:

- `analysis/results/feasible-region.svg` (layout only; numerical classifications
  unchanged)

`reports/baseline.md` was regenerated as part of the required workflow and remained
byte-current, so it is not a worktree change.

Validation results:

- initial parent-baseline standard validation: **PASS**;
- `python scripts/validate-baseline.py --write-reports`: **PASS**;
- `python scripts/generate-communication-views.py --check`: **PASS**, nine figures
  current;
- `python scripts/generate-mermaid-views.py --check`: **PASS**, audit atlas current;
- `python analysis/feasibility.py --check`: **PASS**, seven deterministic artifacts
  current;
- `python scripts/validate-baseline.py`: **PASS**;
- `python scripts/validate-baseline.py --check-generated`: **PASS** and equivalent to
  the repository CI workflow;
- `python scripts/validate-baseline.py --validate-mermaid`: structural validation
  **PASS**; pinned `mmdc` 11.4.1 render **SKIPPED** because it is not installed;
- `git diff --check`: **PASS**;
- changed Python-source compile check: **PASS**, four files;
- SVG XML parse check: **PASS**, all nine architecture figures plus the feasibility
  figure; and
- rendered visual inspection: **PASS**, all nine architecture figures plus the
  feasibility figure at normal scale.

Diff review confirmed the architecture catalog changes are controlled
`display_name` additions only; model connections, allocations, requirements,
configuration lineage, verification disposition, and feasibility results were not
changed. `TS-009` remains `deferred_out_of_scope`; `VER-008` remains
`deferred_out_of_scope`; `VER-009` remains `blocked_by_external_authority`; all five
configuration approval states remain `not_approved`; and future configurations
remain concept/context candidates.

The model version remains `0.8.0-baseline-candidate`; the technical status remains
`baseline_candidate_not_approved`. This work package is not committed, local `HEAD`
therefore remains the parent SHA, and nothing was pushed. Pre-existing unrelated
worktree entries (`.gitignore` mode noise, the local HTML export, and
`scripts/__pycache__/`) were left untouched.
