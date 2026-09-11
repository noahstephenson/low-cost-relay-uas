# Repository readability review

This presentation pass follows commit `89b5169383aa71759dbd2f583d810026bab93f06`. It preserves the research title, frozen tag, model catalogs, source/evidence records, numerical inputs, and tabular results.

## Reading path

The overview now teaches the problem through one existing mission example. Architecture explains mission traffic, carrier control, electrical energy, and mechanical support. Feasibility follows those assumptions through visibility, link margin, analytical closure, and physical screening. Engineering status separates the numerical result from the evidence still needed for an aircraft. The reference guide explains IDs, generators, and reproduction.

The [paper-argument test](paper-argument-test.md) contains a 170-word argument and three bounded contributions. Verdict: sufficient to begin drafting a conditional architecture case study; scientific novelty remains modest and physical validation remains absent.

## Diagram coverage

| Maintained view family | Final instances | Review |
|---|---:|---|
| Plain-language architecture SVGs | 9 | All rendered and inspected; corrected overview label fit and physical-subsystem text overflow |
| Analysis SVGs | 6 | All rendered and inspected; enlarged primary map, improved contrast/labels, and widened plot margins |
| Generated reference Mermaid views | 15 | All parsed/rendered with Mermaid CLI 11.4.1 and inspected; browser rendering checked at approximately 800 px reading width |

The two mission-map filenames intentionally show the same primary result; they are not separate experiments. Historical archived diagrams were not rewritten and remain explicitly non-authoritative in the archive index.

Dense atlas labels now have companion detail tables. The long relay trace is split at the payload component; carrier command and relayed mission traffic have separate sequences. A stale `REQ_FUN_001` diagram key was corrected to the existing `REQ-001` requirement, restoring the intended trace without changing a catalog relationship. Regression tests now reject undeclared flow endpoints and verify the requirement-to-verification connections.

## Verification

- Existing 17 scientific tests plus two diagram regressions pass.
- Baseline and generated-artifact checks pass; the README reading-order guard follows the new tutorial sections.
- Local documentation links and anchors were checked across maintained Markdown.
- Regenerating views and analysis artifacts produces identical files on repeat runs.
- Model/source/evidence files and numerical CSV/JSON/YAML inputs and outputs match the pre-pass baseline after newline normalization.
- Architecture headline counts remain 18 / 6 / 6 / 60 and 6 / 2 / 2 / 80.

## Limits

Reference diagrams remain more detailed than introductory figures and should be read with their adjacent tables. Browser-specific Mermaid layout can differ; the reviewed renders use the pinned CLI with Chrome. Presentation quality and passing software checks do not establish control isolation, real propagation, full-mission performance, affordability, safety, or airworthiness. Those evidence gaps are preserved rather than hidden by the narrative.
