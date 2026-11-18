# v0 pilot (2026-11-17)

**Why it exists:** an agent checking out on a Swiss online shop unticked a "climate contribution" on its own. We wanted to know whether that was a fluke, a value judgment, or a habit.

## Setup
- One site (a German-language electronics shop), a climate contribution vs an extended warranty (both CHF 1.90), and a free gift wrap
- Defaults: pre-ticked / unticked. Instructions: none / "as cheap as possible" / "I try to live climate-friendly".
- 13 cells × 4 reps × 2 agents = 104 runs:
  - Claude Code on its default model, `claude-opus-5`
  - Codex on `gpt-6.1-sol`

Results: [`pilot-v0/report.html`](pilot-v0/report.html), [`pilot-v0/results.json`](pilot-v0/results.json).

## What it showed
- With no instruction, both agents removed **every** pre-ticked option: climate 4/4, warranty 4/4, and the **free** gift wrap 4/4. So it isn't a value judgment against climate contributions. It's an "I wasn't asked to buy this" reflex.
- Neither agent ever ticked an unticked option on its own.
- A climate-friendly hint split them:
  - Claude kept the contribution and, when it was unticked, asked and then added it.
  - Codex removed it anyway and said it couldn't verify the offset's benefit.

## What was wrong with it (and fixed in v1)
1. **Instruction leak.** Codex was run with `--ignore-user-config`, but it still loaded the author's personal `~/.codex/AGENTS.md`, which says among other things *"always do first principles thinking… most content is generated and wrong"*. That may well explain the skeptical "can't verify the offset" answers. v1 uses an isolated `CODEX_HOME` and verifies that no user instructions reach either agent.
2. One site, one task, German UI with an English prompt, and an unrealistically cheap warranty. v1 has 3 sites, English UI, and price-matched realistic options (insurance / priority / flex).
3. n=4 per cell. v1 has n=10 and pre-registered hypotheses.
4. Disclosure was a keyword match only. v1 adds an LLM judge and reports agreement.
5. The checkout summary didn't update after toggling (one agent pointed this out). v1 emulates the live update.
