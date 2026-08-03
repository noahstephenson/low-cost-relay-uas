#!/usr/bin/env python3
"""check-ids.py — consistency checks over the ID scheme described in system.yaml
and traceability.md's "Consistency Checks" section.

Implements, over plain markdown table parsing (stdlib only, no pip install
needed in CI):

  1. Every REQ- in requirements.md appears in traceability.md Matrix 3.
  2. Every CMP-/FUN-/IFC- referenced anywhere exists in architecture.md.
  3. Every CAP- has at least one allocated OA- or an explicit documented
     exception.
  4. Every HAZ- has a mitigating REQ- or is explicitly marked unmitigated.
  5. No duplicate IDs within a prefix.
  6. No ID referenced anywhere that is not defined somewhere.

Exit code is non-zero if any check fails.

Parsing approach
-----------------
No markdown library is used. Tables are recognized by line-based scanning:
a line starting with '|' begins a table row, the following '|---|---|...'
line is the header separator, and rows continue until a non-'|' line. The ID
that a table *defines* is taken from the first column of the row, for the
specific "definer" files/tables called out in traceability.md and
system.yaml's id_scheme.

Range/list notation
--------------------
This repo's prose uses shorthand like "CMP-PRP-01..03", "IFC-INT-001..007",
and "MODE-001..004" to mean "every ID from N to M", not a literal ID. A full
range-expansion grammar is overkill for a handful of fixed-width numeric
ranges, so this script implements *only* the "<prefix>-<N>..<M>" case (same
prefix stem, numeric start/end, zero-padded to the width of the start). Any
other shorthand (e.g. comma lists, "C1-C4" propeller corner labels, which are
not IDs at all) is left alone — comma-separated IDs are already handled
because each one matches the ID regex independently, and non-ID shorthand
never matches the regex to begin with.

Prefix scope
------------
The dangling-reference check only tracks prefixes this repo actually defines
and traces: CAP, OA, OP, CMP, FUN, IFC, REQ, HAZ, TS, MODE. TS and MODE are
included (beyond the six required checks) purely to avoid false-positive
"dangling reference" noise from the many legitimate TS-/MODE- mentions in
prose — they are not otherwise subject to the six required checks.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Prefixes tracked for definition/reference bookkeeping, and the file(s) in
# which each prefix is authoritatively *defined* (per traceability.md's
# "Source of truth" note and system.yaml's id_scheme).
DEFINER_FILES = {
    "CAP": ["uaf-views.md"],
    "OA": ["uaf-views.md"],
    "OP": ["uaf-views.md"],
    "CMP": ["architecture.md"],
    "FUN": ["architecture.md"],
    "IFC": ["architecture.md"],
    "REQ": ["requirements.md"],
    "HAZ": ["hazard-analysis.md"],
    "TS": ["trade-studies.md"],
    "MODE": ["README.md"],
}

PREFIXES = list(DEFINER_FILES.keys())
# Longest-prefix-first so e.g. "MODE" doesn't get shadowed by a shorter match.
_PREFIX_ALT = "|".join(sorted(PREFIXES, key=len, reverse=True))

ID_TOKEN_RE = re.compile(
    rf"\b(?:{_PREFIX_ALT})-[A-Z0-9]+(?:-[A-Z0-9]+)*(?:\.\.[A-Z0-9]+)?\b"
)

RANGE_RE = re.compile(r"^(?P<base>[A-Z]+(?:-[A-Z0-9]+)*-)(?P<start>\d+)\.\.(?P<end>\d+)$")


def expand_token(token):
    """Expand '<prefix>-...-<N>..<M>' shorthand into individual IDs.
    Non-range tokens are returned as a single-element list unchanged."""
    m = RANGE_RE.match(token)
    if not m:
        return [token]
    base, start, end = m.group("base"), m.group("start"), m.group("end")
    width = len(start)
    try:
        lo, hi = int(start), int(end)
    except ValueError:
        return [token]
    if lo > hi or hi - lo > 500:  # sanity guard against runaway expansion
        return [token]
    return [f"{base}{str(n).zfill(width)}" for n in range(lo, hi + 1)]


def prefix_of(token_id):
    for p in sorted(PREFIXES, key=len, reverse=True):
        if token_id.startswith(p + "-"):
            return p
    return None


FENCE_RE = re.compile(r"```.*?```", re.DOTALL)


def find_all_references(text):
    """Return every ID token found in text, ranges expanded.

    Two kinds of non-ID noise are filtered out before returning:

    - Fenced code blocks (```...```) are stripped first. The only ID-shaped
      token that lives exclusively inside a fence in this repo is the
      "TS-XXX" placeholder in trade-studies.md's copy-paste template, which
      is not a real ID. Mermaid diagrams also live in fences and repeat IDs
      that are already referenced in surrounding prose/tables, so dropping
      fenced content does not hide any otherwise-undetected reference.
    - Prefix "stems" used as wildcard/family shorthand, e.g. `CMP-AFR-*` or
      the truncated `IFC-INT-` in "interfaces (`IFC-INT-`) are internal" —
      these mean "the whole family", not a literal ID. Detected by checking
      whether the character immediately following the regex match is '-' or
      '*' (i.e. the match was cut short by a non-alnum continuation rather
      than ending cleanly at a word boundary).
    """
    text = FENCE_RE.sub("", text)
    out = []
    for m in ID_TOKEN_RE.finditer(text):
        end = m.end()
        if end < len(text) and text[end] in ("-", "*"):
            continue  # wildcard/family stem, not a concrete ID
        out.extend(expand_token(m.group(0)))
    return out


def clean_cell(cell):
    cell = cell.strip()
    cell = cell.replace("**", "").replace("`", "")
    return cell.strip()


def iter_table_rows(lines):
    """Yield lists of raw cell strings for each data row of every markdown
    table found in `lines` (header separator rows like |---|---| are
    skipped, header rows are skipped)."""
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if line.lstrip().startswith("|") and i + 1 < n:
            sep = lines[i + 1]
            if re.match(r"^\s*\|[\s:|-]+\|\s*$", sep):
                # header row is lines[i], separator is lines[i+1]
                j = i + 2
                while j < n and lines[j].lstrip().startswith("|"):
                    cells = [c for c in lines[j].split("|")]
                    # split on '|' of a line like "| a | b |" gives
                    # ['', ' a ', ' b ', ''] — drop the empty ends
                    if cells and cells[0].strip() == "":
                        cells = cells[1:]
                    if cells and cells[-1].strip() == "":
                        cells = cells[:-1]
                    yield [clean_cell(c) for c in cells]
                    j += 1
                i = j
                continue
        i += 1


def read(relpath):
    p = ROOT / relpath
    return p.read_text(encoding="utf-8")


def section(text, heading_pattern):
    """Return the text of a '## ...' section whose heading matches
    heading_pattern (regex), up to the next '## ' heading or EOF."""
    lines = text.splitlines()
    start = None
    for idx, line in enumerate(lines):
        if line.startswith("## ") and re.search(heading_pattern, line):
            start = idx
            break
    if start is None:
        return ""
    end = len(lines)
    for idx in range(start + 1, len(lines)):
        if lines[idx].startswith("## "):
            end = idx
            break
    return "\n".join(lines[start:end])


def first_col_ids(table_text, prefix):
    """Definitions: first-column cell of each row, if it matches `prefix-...`
    exactly (a defining cell is a single ID, not a reference list)."""
    ids = []
    for row in iter_table_rows(table_text.splitlines()):
        if not row:
            continue
        cell = row[0]
        if re.match(rf"^{prefix}-[A-Z0-9]+(?:-[A-Z0-9]+)*$", cell):
            ids.append(cell)
    return ids


def main():
    all_md = sorted(ROOT.glob("*.md"))
    file_text = {p.name: p.read_text(encoding="utf-8") for p in all_md}

    failures = []  # list of (check_name, [detail lines])

    # ---- Build defined-ID sets (with duplicate tracking) per prefix ----
    defined_lists = {p: [] for p in PREFIXES}  # includes duplicates
    for prefix, files in DEFINER_FILES.items():
        for fname in files:
            text = file_text.get(fname, "")
            defined_lists[prefix].extend(first_col_ids(text, prefix))

    defined_sets = {p: set(ids) for p, ids in defined_lists.items()}

    # ---- Check 5: no duplicate IDs within a prefix ----
    dup_report = {}
    for prefix, ids in defined_lists.items():
        seen = {}
        for i in ids:
            seen[i] = seen.get(i, 0) + 1
        dups = sorted(k for k, v in seen.items() if v > 1)
        if dups:
            dup_report[prefix] = dups
    if dup_report:
        details = []
        for prefix, dups in dup_report.items():
            details.append(f"  {prefix}: {', '.join(dups)}")
        failures.append(("No duplicate IDs within a prefix", details))

    # ---- Check 6 (and 2): every referenced ID is defined somewhere ----
    # Scan every .md file in the repo root for ID-shaped tokens and check
    # each against the defining set for its prefix.
    dangling = {}  # prefix -> {id: [files referencing it]}
    for fname, text in file_text.items():
        for tok in find_all_references(text):
            p = prefix_of(tok)
            if p is None:
                continue
            if tok not in defined_sets.get(p, set()):
                dangling.setdefault(p, {}).setdefault(tok, set()).add(fname)

    if dangling:
        details = []
        for prefix in sorted(dangling):
            details.append(f"  {prefix}:")
            for tok in sorted(dangling[prefix]):
                files = ", ".join(sorted(dangling[prefix][tok]))
                details.append(f"    {tok}  (referenced in: {files})")
        failures.append(
            ("No ID referenced that is not defined somewhere "
             "(covers CMP-/FUN-/IFC- vs architecture.md)", details)
        )

    # ---- Check 1: every REQ- in requirements.md appears in Matrix 3 ----
    matrix3_text = section(file_text.get("traceability.md", ""), r"Matrix 3")
    matrix3_ids = set(first_col_ids(matrix3_text, "REQ"))
    all_req_ids = defined_sets["REQ"]
    missing_from_matrix3 = sorted(all_req_ids - matrix3_ids)
    if missing_from_matrix3:
        details = [f"  {rid}" for rid in missing_from_matrix3]
        failures.append(
            ("Every REQ- in requirements.md appears in traceability.md Matrix 3",
             details)
        )

    # ---- Check 3: every CAP- has an allocated OA- or documented exception ----
    matrix1_text = section(file_text.get("traceability.md", ""), r"Matrix 1")
    cap_gaps = []
    for row in iter_table_rows(matrix1_text.splitlines()):
        if not row or not re.match(r"^CAP-", row[0]):
            continue
        cap_id = row[0]
        activities_cell = row[2] if len(row) > 2 else ""
        has_oa = bool(re.search(r"\bOA-\d", activities_cell))
        if has_oa:
            continue
        # No allocated OA-. Look for a documented exception: does the CAP
        # id appear again in this section (e.g. a blockquote note) beyond
        # its own table row? That's the model's convention for "explicit
        # note explaining why not" (see the CAP-003 note in Matrix 1).
        occurrences = len(re.findall(re.escape(cap_id), matrix1_text))
        if occurrences <= 1:
            cap_gaps.append(cap_id)
    if cap_gaps:
        details = [f"  {c}: no allocated OA- and no documented exception note" for c in cap_gaps]
        failures.append(
            ("Every CAP- has at least one allocated OA- or a documented exception",
             details)
        )

    # ---- Check 4: every HAZ- has a mitigating REQ- or is marked unmitigated ----
    haz_log_text = section(file_text.get("hazard-analysis.md", ""), r"Hazard Log")
    haz_gaps = []
    for row in iter_table_rows(haz_log_text.splitlines()):
        if not row or not re.match(r"^HAZ-", row[0]):
            continue
        haz_id = row[0]
        # Hazard Log columns: HAZ ID | Hazard | Mode(s) | Cause | Effect |
        #                      Sev | Like | Mitigation | Traces To
        mitigation_cell = row[7] if len(row) > 7 else ""
        has_req = bool(re.search(r"\bREQ-[A-Z0-9-]+\b", mitigation_cell))
        marked_unmitigated = "unmitigated" in mitigation_cell.lower()
        if not has_req and not marked_unmitigated:
            haz_gaps.append((haz_id, mitigation_cell or "(empty)"))
    if haz_gaps:
        details = [f"  {h}: mitigation = \"{m}\" — no REQ- and not marked unmitigated"
                   for h, m in haz_gaps]
        failures.append(
            ("Every HAZ- has a mitigating REQ- or is explicitly marked unmitigated",
             details)
        )

    # ---- Report ----
    print("=" * 72)
    print("ID consistency check — low-cost-relay-uas")
    print("=" * 72)

    if not failures:
        print("\nAll checks passed.\n")
        return 0

    print(f"\n{len(failures)} check(s) failed:\n")
    for name, details in failures:
        print(f"[FAIL] {name}")
        for line in details:
            print(line)
        print()

    print("=" * 72)
    print(f"RESULT: {len(failures)} check(s) failed.")
    print("=" * 72)
    return 1


if __name__ == "__main__":
    sys.exit(main())
