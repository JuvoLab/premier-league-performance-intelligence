# Review record — 8 November 2026

Status: local review candidate. Source code is published on GitHub; no application hosting deployment has been performed.

## Reproducibility

Fresh environment `.qa-venv`, Python **3.12.14**, Windows, `include-system-site-packages=false`. Installed the five pinned direct requirements into this isolated environment. `pip check` returned **No broken requirements found**. The complete 41-package snapshot is in requirements-lock-windows-py312.txt; it is a Windows/Python 3.12 lock, not a claim of Linux verification.

Fresh source retrieval into `data/clean-reproduction`, with no reuse of the original raw-file cache: **380 matches + match index**, source commit `4b73468fc5b0f1950f9f66fada70ad3a4f9327cb`. All **381 file hashes matched** the original source manifest. SQLite logical dumps matched exactly, including tables, keys and rows. All score/event reconciliation checks passed. This verifies fresh-environment reproduction on the same Windows machine, not a second operating system.

Five tests passed in **37.86 seconds** on the isolated environment, including source probability rejection, complete coverage and score totals, temporal-prefix invariance, SQL/Pandas agreement and Streamlit team/prefix filter changes. The test process finished without the prior temporary-directory cleanup exception when run with normal filesystem access. That earlier exception concerned test cleanup permissions rather than failed analytical assertions.

## Interface review

Verified rendering in the isolated environment. Team filter, season-prefix filter, trend tab and player contribution view work. Keyboard Enter activates the trend tab; ArrowRight changed the rolling window from 5 to 6. At a 390px viewport the document width remained 390px: no page-level horizontal overflow. Cards stack and the trend chart is visible. Tabs have their own horizontal scrolling on narrow screens; long tables remain scrollable. This is not certification of screen-reader behavior or touch-device compatibility.

Official logo displayed with noncommercial source credit. Player view correctly shows Jamie Vardy: **24 shot goals, 118 shots, 22.30 shot xG**. No ratings or inferred attributes are displayed. App tests also verified Arsenal's first-19-appearance points total of 39 and full-season total of 71.

## Fixes made during QA

- Shared absolute data locations, independent of current launch directory; isolated data location via PLPI_DATA_DIR.
- Reject a local source pin that differs from the verified commit.
- Player aggregation follows the exact match index, avoiding unrelated cached event files, and invalidates after a database rebuild.
- Closed read database connections explicitly; retained atomic replacement of the rebuilt database.
- Added official provider logo and provenance record.
- Added complete isolated-environment dependency snapshot.

## Limits and release gate

Public hosting requires its own smoke test. WCAG conformance and cross-browser/device certification have not been established. The historical season and single-provider restrictions remain deliberate. Attribution documentation does not imply endorsement by StatsBomb.

Before public release, the owner reviews the dashboard, case study, permitted-output approach and visuals. GitHub authorization must be verified in the publishing session. Hosting should build private runtime data from the pinned source rather than commit provider datasets. Registering interest with StatsBomb, if undertaken, requires the owner's own details and explicit instruction; no form has been submitted. Publication/deployment requires separate approval.
