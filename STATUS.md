# STATUS.md — sell-your-car-calm-guide

Last updated: 2026-11-08

## What was built

A step-by-step life-admin guide to selling a car privately, published under **Asdale Dynamics, LLC**. Two formats, one source of truth, fully offline:

- **`docs/`** — 8 markdown chapters (00–07): start-here, pricing the car fairly (KBB/Edmunds/live-market method, three prices), title + bill of sale paperwork, safe test drives, payment safety (cash / cashier's-check / wire rules, scam patterns), notifying the DMV and insurer, all checklists in one place, and ready-to-use templates (bill of sale, DMV notice-of-sale letter, glovebox folder inventory).
- **`site/`** — a static, no-JavaScript website: a `index.html` cover for all five stages, `checklists.html` as a print-optimized one-stage-per-page checklist sheet, and a shared `styles.css` with a dedicated `@media print` block. No build step; open in a browser.
- **`tests/run_tests.py`** — dependency-free verification suite (structure, license line, internal links, anchors, HTML hygiene, secret-freedom, print CSS).

Topics covered per the brief: fair pricing, title & bill of sale, safe test drives, payment safety, DMV & insurer notifications. Distinct from the buying-side guide and the maintenance-log MCP server (see README "Related projects").

## How to run / use it

- **Read the guide:** `docs/00-start-here.md`, then follow chapter order.
- **Use the website:** open `site/index.html` in any browser (double-click it; no server needed).
- **Print the checklists:** open `site/checklists.html`, press Ctrl+P / ⌘P — each stage prints on its own page.
- **Run the verification tests:**

  ```sh
  python3 tests/run_tests.py
  ```

## Verification results

`python3 tests/run_tests.py` → **PASS** (all tests). The suite checks:

- All 15 required files exist
- LICENSE contains the exact line `Copyright (c) 2026 Asdale Dynamics, LLC` and is MIT; README credits Asdale Dynamics, LLC
- No secrets (private keys, API keys, tokens) and no personal contact data in any file
- Every relative markdown/HTML link and in-page anchor resolves
- HTML hygiene: doctype, UTF-8 declaration, balanced core tags, local stylesheet only (**zero external URLs** — nothing is fetched live)
- `checklists.html` has all five printable stage sections and checkbox CSS; `styles.css` has the print block
- No stray non-English (CJK) characters anywhere (a writing pass caught and fixed three earlier)

## Known gaps

- **State specifics are not enumerated.** Notarization requirements, notice-of-sale deadlines, plate-return rules vary by state; the guide teaches the lookup pattern ("[your state] DMV …") rather than listing all 50 states. A per-state appendix is a natural v2 addition.
- **Not legal/financial advice.** Liens, probate transfers, inherited vehicles, and out-of-state sales are flagged as "call the DMV / an attorney" rather than solved in detail.
- Website is intentionally plain (semantic HTML + one CSS file, no JS). Screens it will not win: aesthetics competitions. It will win: printing reliably, working offline forever.
- Chapter numbering is enforced by tests (`check_markdown_links` walks docs/), but there is no lint for markdown style beyond that.

## Project conventions

- Git initialized locally and committed at completion. Never pushed; no remotes.
- MIT license; credit to Asdale Dynamics, LLC in README and LICENSE.
- No secrets, API keys, or personal data in any file (tested).
