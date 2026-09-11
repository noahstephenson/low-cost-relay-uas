# Does the architecture argument hold together?

This is a review note, not a manuscript. Working title: **System Architecture and Mission Feasibility of a Multirotor Communications Relay**.

## Argument in brief

A small relay UAS must do more than place a radio above an obstruction. Its architecture must carry and power the payload, maintain the intended station, and provide a carrier-control path distinct from the mission traffic being relayed. This study describes those responsibilities and evaluates the limited question of whether declared outbound communications demands and hover-resource demands can be jointly accommodated. A stylized visibility and link-margin screen establishes when the relay offers a connectivity benefit. An analytical carrier model then determines finite mass closure and checks exploratory physical boundaries. The worked example distinguishes a thirty-minute case that passes these screens, a forty-five-minute case with finite but excessive mass, and a sixty-minute case with mathematical nonclosure. Those outcomes imply different architecture decisions: more energy cannot repair a failed link, and relaxing a mass ceiling cannot create a missing mathematical solution. The contribution is an auditable architecture assessment using established models. It is not a validated aircraft design, a reconstruction of the examined vehicle, or a general prediction of operational mission success.

## Three bounded contributions

| Contribution | Existing evidence | Boundary on the claim |
|---|---|---|
| Explicit allocation of relay-aircraft responsibilities | [Architecture and evidence table](../architecture.md#architecture-to-evidence-assessment) | Description, not demonstrated fault isolation or novel subsystem theory |
| Conditional service envelope for the proposed architecture | [Primary results](../feasibility.md#primary-relay-uas-result) and [case records](../../analysis/results/integrated-tradespace.csv) | Declared stationary outbound assumptions; no probability, optimality, or full-mission claim |
| Different decisions for different failure mechanisms | [Closure explanation](../feasibility.md#why-endurance-is-coupled) and existing dwell cases | A consequence of the implemented model, not a universal vehicle limit |

## Strongest reviewer objection

“Is this more than a familiar link budget placed beside a familiar hover-sizing model?”

The repository answers partly: it defines an aircraft architecture, gives a reproducible interface between its assumed service and carrier burdens, and explains why different failures require different changes. It does not establish a novel coupled optimization, experimentally validated prediction, or comparative advantage over alternative architectures. Fixed payload assumptions connect largely separable calculations. The paper must acknowledge that modest novelty rather than describing a stronger coupling than was implemented.

## Verdict

**Convincing enough to begin drafting as a bounded architecture case study; acceptance remains uncertain.** The tutorial reading path makes the decision argument assessable. Architecture allocations are descriptions; the envelope and closure states are calculated findings; station keeping, control isolation, reverse-link service, recovery, affordability, and physical performance remain unvalidated.

No further research is required to state this narrow argument honestly. Demonstrating those broader capabilities would require additional evidence outside this pass. The README and feasibility guide therefore lead with the aircraft, explain the gates through one example, and qualify “pass” at the point it appears.
