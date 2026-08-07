# Trade Studies

Open decisions this model does not resolve. The `TS-*` register metadata is
authoritative in `model/assurance.yaml`; this document preserves the substantive
engineering reasoning that should not be reduced to catalog fields.

The point of this file is to make the model's ignorance explicit. A `TS-*` reference
is a known gap with a defined question, not permission to fill an unknown with a
plausible value.

## Status Legend

**Open** — not started · **Scoped** — criteria defined, not evaluated · **Resolved** — decision made and recorded · **Deferred** — out of scope for this project

## Register

| TS ID | Decision | Drives | Criteria | Status |
|---|---|---|---|---|
| TS-001 | Airframe material and construction method | CMP-AFR-01, CMP-AFR-02 | Cost, mass, manufacturability, damage tolerance | Open |
| TS-002 | Propulsion sizing (motor class, prop diameter/pitch, ESC rating) | CMP-PRP-01..03 | Thrust margin, efficiency at loiter, cost | Open — iterated, not converged (see below) |
| TS-003 | Battery chemistry, cell count, capacity | CMP-PWR-01 | Endurance vs. mass vs. cost; REQ-PER-002 | Open — iterated, not converged (see below) |
| TS-004 | Payload power rail voltage and current allocation | CMP-PWR-03 | Payload-agnostic support without overprovisioning | Open |
| TS-005 | Flight controller selection | CMP-AVN-01 | Open-source firmware support, cost, I/O | Open |
| TS-006 | Payload mount interface standard | CMP-MNT-01, CMP-AFR-04 | Modularity, mass, retention under vibration | Open |
| TS-007 | Station-keeping approach and GNSS dependence | CMP-AVN-03, FUN-FLT-03 | Position hold accuracy without assuming GNSS availability | Open |
| TS-008 | Platform command link approach | CMP-AVN-04, IFC-EXT-005 | Range, cost — **platform control only, not the relay payload** | Open |
| TS-009 | Relay payload characterization | CMP-COM-01, CMP-COM-02, all `IFC-EXT-001..004` | — | **Deferred — out of scope** |
| TS-010 | Environmental envelope | All | Temperature, wind, precipitation limits | Open |
| TS-011 | Recovery approach (recoverable vs. genuinely attritable) | CMP-AFR-03, FUN-FLT-04 | Cost of recovery features vs. unit replacement cost | Open |

## TS-009 — Formal Deferral

Every other entry in the Register above is an open trade study: a decision this
project intends to make, currently sitting at Open, Scoped, or Resolved while it
waits its turn. TS-009 is categorically different, and its `Status` reflects that:
**Deferred**, not Open. This is not "not yet decided." It is **not this project's
decision to make.** RF frequency plan, waveform, protocol, modulation, transmit
power, antenna type and gain, and link budget are listed under `system.yaml`'s
`out_of_scope` from the start, alongside antenna design, gain patterns, transmit
power, and electronic-warfare/counter-EW technique. There is no state this project
reaches where TS-009 becomes a study to work; it is a boundary of the study itself.

**What would actually have to happen for someone to pick this up.** Consistent with
the scope constraints summarized in `README.md`:
moving toward a real payload would require RF engineering expertise as a separate
effort, spectrum authorization from the relevant national authority before any
radiating hardware exists, and — in a defense-affiliated context — export control
review. None of that is addressed here, and none of it is this repository's
competence to address. See `REQ-DEF-001` through `REQ-DEF-005` for the specific
items recorded as out of scope rather than silently dropped.

**Why the rest of the model doesn't have to wait on it.** This is the payoff of one
of the two choices `architecture.md` calls out as shaping everything downstream: the
payload is isolated behind exactly two interfaces. `CMP-COM-01` touches the rest of
the system through `IFC-INT-003` (regulated power) and `IFC-INT-007` (mechanical
retention), and nothing else — no data path, no control signal, no shared structure.
`REQ-IFC-003` exists specifically to hold that boundary in place: *"The
platform-to-payload interface shall be limited to power (`IFC-INT-003`) and
mechanical retention (`IFC-INT-007`)."* Its rationale is that another platform
crossing would break the isolation the architecture depends on. As long as that
requirement holds,
TS-009 can be picked up — by this project, by someone else entirely, on whatever
timeline RF engineering, spectrum authorization, and export control allow — without
the platform architecture around it needing to change. A payload decision is a
mount-and-rail question, not a redesign.

## Worked Trade Studies

TS-002 and TS-003 are worked together below, per `architecture.md`'s own note that
they "must be worked together rather than in sequence." Neither resolves to a point
design. What follows is the iteration itself — starting assumption, forward
calculation, feedback, at least one more pass — shown explicitly rather than
collapsed into a single converged answer, per this study's own convention that a
`[TBD]` is a load-bearing statement of what is not yet known, not a placeholder for
a number borrowed from a comparable system.

### TS-002 — Propulsion sizing (motor class, prop diameter/pitch, ESC rating)

**Question.** What motor class, propeller diameter/pitch, and ESC current rating
should the four corner sets (`CMP-PRP-01..03`) use, given that the thrust
requirement they're sized against is itself a function of an all-up mass (AUW) that
this same loop has not yet closed?

**Options.**

- **Smaller-diameter, higher-KV motors and proportionally smaller props.** Cheaper
  per unit, shorter arms (`CMP-AFR-02`) — lighter, cheaper structure, better fit with
  single-operator portability (`REQ-PER-005`). Costs hover efficiency: smaller disk
  area at a given thrust means higher disk loading, which (by actuator disk /
  momentum theory) means more power per unit of thrust. That power penalty is paid
  on every gram the battery carries, which feeds directly into TS-003.
- **Larger-diameter, lower-KV motors and proportionally larger props.** Lower disk
  loading, better power-per-unit-thrust — the one lever available to reduce the
  loop's gain without fighting the airframe-cost trade directly (TS-001). Costs arm
  length: `CMP-AFR-02` length sets the propeller clearance / diameter limit, and
  longer arms mean more structure, more mass, and more cost — working against
  `CAP-004` on a different axis than the one it's trying to help.
- **ESC current rating.** Follows from whichever motor is chosen and the final AUW's
  peak thrust demand (including whatever wind-tolerance margin TS-010 eventually
  sets). Cannot be pinned before either of those closes; carried as a dependent
  quantity, not decided here.

**Evaluation criteria.** Thrust margin (including the not-yet-set wind-tolerance
requirement from TS-010), hover power-per-unit-thrust (disk loading), unit cost,
arm-length impact on structure and portability, and — the criterion that actually
governs this trade — how strongly the choice feeds back into TS-003's required
battery mass.

**Analysis.** Propulsion sizing cannot be evaluated in isolation from battery
sizing: the thrust requirement depends on AUW, AUW depends on battery mass, and
battery mass depends on the hover power this trade sets. The full pass-by-pass
iteration is walked through under TS-003's Analysis below, since that is where the
loop's mass/endurance output actually lands. What belongs here is what TS-002
specifically controls *within* that loop: disk loading, and the arm-length/cost
ceiling on how much disk-area growth is available to blunt the loop's gain before it
runs into TS-001's structural-cost trade.

**Decision.** Not resolved to a point design. Directional lean toward the
lower-disk-loading end of the option space (larger prop for a given thrust,
within whatever arm-length/cost ceiling TS-001 sets), because it is the only lever
here that reduces the loop's gain without directly trading against airframe cost.
How far that lean can go — and whether the resulting arm length still fits
`REQ-PER-005`'s single-operator, no-support-equipment constraint — cannot be pinned
without TS-001 (structure) and TS-003 (battery) closing at the same time. Status:
**Open**, not Resolved — this is a genuinely coupled decision, not an
under-analyzed one.

**Consequences / affected IDs.** `CMP-PRP-01..03`, `CMP-AFR-02` (arm length),
`REQ-PER-002` (endurance, still `[TBD]`), `REQ-PER-003` (gross mass, still `[TBD]`),
`REQ-PER-001` (unit cost, still `[TBD]`), `CAP-004`. Directly coupled to TS-003
(below) and TS-001 (airframe structural efficiency). See the shared finding at the
end of TS-003 for where this leaves the model.

### TS-003 — Battery chemistry, cell count, capacity

**Question.** What chemistry, cell count, and capacity should `CMP-PWR-01` use,
given that required capacity depends on hover power (set by TS-002), and hover
power depends on AUW, which depends on the battery's own mass?

**Options.**

- **Li-Poly (LiPo).** Higher continuous discharge capability (specific power),
  which matches hover's steady, non-trivial current draw well, and is the more
  COTS-commodity, field-reusable option consistent with `REQ-CON-001`. Trades some
  specific energy (capacity per unit mass) for that discharge headroom — meaning
  more mass is needed for a given required watt-hours than a chemistry optimized the
  other way.
- **Li-ion (cylindrical or pouch).** Better specific energy — less battery mass for
  the same required watt-hours, which directly reduces the loop's gain (see
  Analysis). Trades continuous discharge capability, which may require more
  parallel cell strings to meet peak hover current, adding pack complexity, BMS
  overhead, and some of the mass savings back.
- **Cell count / series-parallel topology.** Bounded by `CMP-PWR-03`'s regulator
  design (TS-004, itself open) and `CMP-PWR-02`'s bus voltage. Not resolved here —
  it is downstream of both the chemistry choice above and TS-004.

**Evaluation criteria.** Specific energy vs. specific power against hover's
continuous current draw, COTS availability and field reusability (`REQ-CON-001`,
and the field-replaceable framing already built into `CMP-PWR-04`), unit cost
contribution — `architecture.md` already flags this component as "likely the
highest-value single reusable component" and "expected to dominate reusable cost" —
and, centrally, how battery mass feeds back into TS-002's required thrust.

**Analysis.** This is the loop `architecture.md` names explicitly. Walked forward
as an iteration rather than collapsed into a single pass:

- **Pass 0 — the one piece with the fewest circular dependencies.** Start from
  *dry mass*: airframe (`CMP-AFR-*`), propulsion hardware minus battery
  (`CMP-PRP-*`), avionics (`CMP-AVN-*`), payload mount (`CMP-MNT-01`), and the
  payload mass/volume *envelope* reserved for `CMP-COM-01`/`CMP-COM-02` (an
  envelope, not a value — see `architecture.md`). This is still not a number: TS-001
  (structure), TS-006 (mount), and the envelope width itself (TS-004/TS-006) are all
  open. But it is boundable in *kind* without circularity — `REQ-PER-005` (single
  operator, hand-launched, no support equipment) implies a platform light enough for
  one person to carry and launch alongside their own equipment, which bounds dry
  mass to "small platform" order, not "heavy lift" order. That is an inference from
  an existing requirement, not an invented figure, and it is the only foothold this
  iteration starts from.
- **Pass 1 — size propulsion (TS-002) against dry mass alone, battery mass not yet
  included.** This produces a first-guess thrust requirement and, from it, a
  first-guess hover power `P1`, using whatever disk loading TS-002 leans toward.
  `P1` is necessarily an underestimate, because it ignores the battery that hasn't
  been sized yet.
- **Pass 2 — size the battery (this trade) against `P1` and a candidate endurance.**
  `REQ-PER-002` is `[TBD]`, so this pass has to be run against a *range* of
  candidate endurance targets rather than a single value, to show how sensitive the
  result is to a decision that hasn't been made: a short-dwell candidate (enough to
  reposition or demonstrate the relay function briefly) versus a
  mission-useful-dwell candidate (long enough that `OP-002` actually delivers
  persistent link geometry rather than a brief window). Required energy scales with
  `P1 × endurance`; required battery mass scales with that energy divided by the
  chemistry's specific energy (TS-003's own open question above). The short-dwell
  candidate produces a modest `M_batt`; the mission-useful candidate produces a
  substantially larger one — this is not a numeric claim, it is the shape of a
  linear-in-endurance relationship applied to an unresolved input.
- **Pass 3 — feed `M_batt` back into AUW, re-run TS-002.** New AUW = dry mass +
  `M_batt` (pass 2) is heavier than the pass-0/pass-1 assumption. At a fixed disk
  area (arm length not yet re-opened), higher weight means higher disk loading,
  and — by the same momentum-theory relationship TS-002 relies on — power per unit
  thrust gets *worse*, not just proportionally more. Hover power rises to `P2 > P1`,
  and it rises faster than the mass that caused it, because of that disk-loading
  effect. This is the feedback closing, and it is the step a single-pass sizing
  exercise skips.
- **Pass 4 — re-size the battery for `P2` at the same endurance candidate.**
  Required energy is now `P2 × endurance` (larger than pass 2's), so `M_batt2 >
  M_batt1`. Whether this converges to a stable, modest correction or keeps growing
  pass over pass depends on three things, none of which this model currently pins:
  (a) how much disk-area growth TS-002 can still apply within TS-001's arm-length/
  cost ceiling to blunt the disk-loading penalty; (b) which chemistry TS-003 lands
  on (higher specific energy directly reduces the loop's gain); and (c) how large
  the candidate endurance is, because the loop's gain scales with it — a short-dwell
  target reaches a small correction quickly, a mission-useful-dwell target pushes
  the iteration further into the region where these second-order effects dominate.

  For context on why this matters and isn't merely a rounding effect: it is a
  widely observed pattern in small electric multirotor design *in general* — not a
  number derived for or assigned to this platform — that battery mass ends up
  representing a large minority to a majority of all-up mass once flight times move
  from token (a few minutes) to operationally meaningful (tens of minutes),
  precisely because hover offers no forward-flight lift assist to offset the
  induced-power cost of carrying more weight. That pattern is cited here only to
  explain *why* the iteration above has real gain, not to fill any `[TBD]` in this
  repository with a borrowed figure.

**Decision.** Not resolved to a chemistry, cell count, or capacity. Directional
lean toward LiPo, given the fit between its discharge characteristics and hover's
continuous current draw and its better fit with `REQ-CON-001`'s COTS preference —
but this is secondary and provisional. The real blocker is sequencing, not
chemistry: capacity cannot be sized until `REQ-PER-002` is set, and — per the
finding below — `REQ-PER-002` should not be set without first knowing what this
loop does to mass and cost at the value being considered. Setting the endurance
requirement first and discovering the loop's consequences afterward is exactly the
sequencing error `architecture.md` flagged TS-002 and TS-003 to avoid by being
worked together. Status: **Open**, not Resolved.

**Consequences / affected IDs.** `CMP-PWR-01`, `CMP-PWR-03` (rail sizing, TS-004),
`REQ-PER-002` (endurance), `REQ-PER-003` (gross mass), `REQ-PER-001` (unit cost).
Coupled to TS-002 (above) and TS-001 (structural efficiency).

### TS-002 / TS-003 — Shared Finding: Does the Endurance-vs-Cost Loop Close?

The capability analysis in `architecture.md` names the falsification condition this finding
addresses directly: *"if the endurance-versus-cost loop in TS-003 closes
unfavourably, a platform cheap enough to be attritable may not hold station long
enough to be useful, and the intersection is empty for physical reasons rather than
institutional ones."* The iteration above is a direct evaluation of that condition,
and the honest answer is: **not resolved, and not confidently favorable.**

Three things push toward the unfavorable side, and none of them are addressed by
making the rest of the platform cheaper:

1. **Rotary-wing hover is structurally power-hungry.** Unlike a fixed-wing vehicle,
   there is no forward-flight lift assist to offset the induced-power cost of extra
   weight. Every gram of added battery mass increases disk loading (at fixed prop
   size) and therefore increases power-per-unit-thrust, not just total thrust — the
   loop in Pass 3/4 above has real, physically grounded gain, not merely a rounding
   correction.
2. **The dominant cost driver is the one component cost-cutting elsewhere doesn't
   touch.** `architecture.md` already identifies `CMP-PWR-01` as "likely the
   highest-value single reusable component" and expected to "dominate reusable
   cost." Battery cost per watt-hour is set by chemistry and market, not by how
   aggressively the airframe, propulsion, or avionics are cost-optimized
   (`REQ-CON-001`/`REQ-CON-002`). A design strategy of "cheap by COTS everything"
   does not reduce the one budget line the endurance target grows fastest.
3. **The lever that could reduce the loop's gain is the one the cost strategy
   already spends.** Structural efficiency — bigger, more efficient rotors within a
   lighter, more capable structure — is the main way to blunt the disk-loading
   feedback (Pass 3 above). README's own Key Technical Challenge 1 already states
   this plainly: "structural efficiency is what buys margin in that loop, and
   structural efficiency is exactly what an inexpensive airframe gives up."

None of this means the intersection is *definitely* empty — a short-dwell endurance
target plausibly converges to a small, genuinely cheap, genuinely attritable
platform through this same iteration. But a short dwell time is also in tension with
the reason `OP-002` exists in the first place: the operational concept in `architecture.md`
describes the relay's value as *positional* and dependent on *sustained* geometry
(`OA-003`, `FUN-FLT-03`), not a brief window. A relay that must be relaunched every
few minutes to maintain a link does not obviously deliver `CAP-001`/`CAP-002` in any
operationally useful sense, even if it is cheap.

**This is recorded as a finding, not engineered around.** No value has been chosen
for `REQ-PER-002` here, and none should be, until the sensitivity this iteration
describes is actually evaluated against a real target rather than the two
illustrative candidates used above. What this trade study does establish is that
`REQ-PER-002`, `REQ-PER-003`, and `REQ-PER-001` are not three independent `[TBD]`s
that can be filled in one at a time — they are three views of the same unresolved
coupling, and setting any one of them first constrains the other two in ways the
model does not yet make explicit. See the requirements and open-gap summaries in
`architecture.md` and `reports/baseline.md` for how this is carried forward.

## Template

<!-- Copy this block when working a trade study. -->

```
### TS-XXX — <decision>

**Question.**
**Options.**
**Evaluation criteria.**
**Analysis.**
**Decision.**
**Consequences / affected IDs.**
```
