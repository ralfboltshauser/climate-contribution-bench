# Site verification for v1 research release

Browser checks completed in shared Chromium on 2026-11-18. This supports the
web release; physical-phone and screen-reader behaviour are not verified.

- Desktop at 1280px and mobile viewport at 390px, light and dark schemes.
- No page-wide horizontal overflow at either width. Charts and tables scroll
  inside their containers. Filter text is 16px.
- All 2,040 agent sessions load; pagination expands 30 cards to 60. Agent
  selection returns 510 sessions, stopped filter returns 26, and pending returns
  zero. An impossible free/unticked filter shows the empty-state guidance.
- A deliberately rejected data request shows reload/HTTP-serving recovery text.
- Keyboard Tab gives visible focus. Native filter controls have accessible names.
- In-page links resolve. Fonts load. No console errors were observed in snapshots.
- The observed dark-theme body-text contrast scan found no failing sampled
  paragraph/link/table/chip pairs. This is not a comprehensive accessibility audit.
- Added a 1200×630 sharing image and canonical/OG metadata.

The source fixes from the earlier pass remain: named filters, main landmark,
focus style, live count, 16px selects, pointer-gated hover, pending label states,
HTTP error handling and readable chart widths.

The data grid and automated labels are complete. A second-model sample audit
checks rubric consistency; no human gold validation is claimed. Primary results
are server-side order outcomes. Disclosure and fidelity are exploratory.

Verification: 11 offline tests pass, Python compilation passes, public-only
analysis reproduces the published results, and generated JavaScript syntax
checks pass. The public export contains fictional fixture account information;
raw CLI transcripts and credentials are excluded. No physical phone, assistive
screen reader or comprehensive performance lab audit was used.
