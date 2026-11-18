# Site redesign, 2026-11-18

The original page gave most paragraphs a bordered card and put repeated setup
and operational status ahead of the evidence. This pass changes presentation
and navigation; benchmark episodes, labels and analysis outputs are unchanged.

| Before | After | Why |
|---|---|---|
| Repeated rounded containers and warning-like status panels | A continuous page with numbered sections and rules | Gives the evidence a clear reading order |
| Three externally loaded typefaces | One locally served variable Manrope face, plus system monospace | A deliberate type hierarchy with fewer network requests |
| SVG labels shrank with the chart on phones | HTML comparison bars with visible values and counts | Keeps primary results readable at 320px |
| Eight quote blocks and open transcript cards | Two excerpts and an expandable session archive | Makes detailed evidence available without overwhelming the page |
| Session data downloaded on every visit | Fetch when the archive opens | Removes the 3 MB session file from initial loading |
| Mixed visual treatments | Warm paper, forest-green ink and a highlighted checkout line | Ties the visual language to the actual decision being studied |

Applied the host's Ask Emil routing: unslop design and foundations, then
 typography/marketing, color/accessibility, mobile/polish, and a final UI review.
No decorative motion was added. Plain CSS and the existing Python generator
remain the implementation.

Checks: desktop and 320/390px browser viewports, both color schemes, no page-wide
overflow, visible counts and intervals, archive filtering and expansion,
pagination, loading failure, and sampled text contrast. Static markup and
JavaScript syntax checks pass. All 11 offline benchmark tests pass. The local
Manrope font is distributed with its OFL license. Actual phone and assistive
screen-reader behaviour were not verified.
