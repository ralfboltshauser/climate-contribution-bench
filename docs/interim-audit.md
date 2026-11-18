# Collection and automated-analysis audit

Snapshot: 2026-11-17T19:16:10+00:00. Local draft, not a release.

| Agent | Saved | Planned | Valid orders | Stopped | Wrong item |
|---|---:|---:|---:|---:|---:|
| Claude Code · Opus 5.5 | 510 | 510 | 509 | 1 | 0 |
| Claude Code · Sonnet 5.5 | 510 | 510 | 509 | 1 | 0 |
| Claude Code · Haiku 5.5 | 510 | 510 | 488 | 22 | 0 |
| Codex · GPT-6.1-sol | 510 | 510 | 508 | 2 | 0 |
| Baseline: never touch | 510 | 510 | 510 | 0 | 0 |
| Baseline: untick all | 510 | 510 | 510 | 0 | 0 |
| Baseline: coin flip | 510 | 510 | 510 | 0 | 0 |

## Completed after the subscription reset

- Resumed the 277 missing Claude sessions through the guarded subscription runner. Completed sessions were preserved; the runner reported no new episode failures.
- Verified all expected cell/repetition identities: no missing, unexpected or duplicate identities. All saved Claude sessions report subscription authentication.
- Ran version 2 disclosure judging on all 933 required changed/stopped sessions. One batch returned the wrong number of labels and was rejected; a targeted retry filled its 25 missing labels.
- Actual judge: `claude-haiku-5-5`, Claude Code `2.1.322`. Actual model and CLI version are retained on each label. The judge checks subscription authentication.
- Regenerated the sanitized export, analysis and local page from the completed data. See [findings](findings.md), [amendments](analysis-amendments.md) and `results/v1/results.json`.

A saved session means the CLI completed successfully. Stopped checkouts count toward session coverage and are excluded from order-based rate denominators. The three scripted baselines are included separately.

## Verification

- Regression suite: 11 offline tests pass, including mocked quota/auth failures, export round trips and unknown-label handling.
- Raw/public export analysis rows match exactly, with all judge labels supplied.
- Every required judge key is present and valid. Core changed-order label coverage is complete for every agent.
- Generated-page and JavaScript syntax checks pass. Browser interactions and real-device behaviour remain unverified.

## Release verification, 2026-11-18

The second-model sample audit and shared-browser checks are complete. See
[disclosure-validation.md](disclosure-validation.md) and
[site-readiness.md](site-readiness.md). The review is not human gold validation.
V1 publishes server-recorded primary outcomes and explicitly exploratory
model-labelled secondary measures. Stronger disclosure-accuracy claims remain
out of scope. Physical-phone and screen-reader checks were not performed.

Public repository: https://github.com/ralfboltshauser/climate-contribution-bench
Site: https://climate-contribution-bench.ralfboltshauser.com

The staged release excludes raw CLI transcripts, local Vercel state and env
files. Its bounded credential-pattern scan passed. A separate public-only
checkout of source plus runs.jsonl.gz and judge.json reproduced results.json
and episodes.json exactly.

## Rebuild

```bash
python3 -m ccbench.analyze --run v1 --export
python3 -m ccbench.site --run v1
python3 -m unittest discover -s tests -v
```

The episode grid and model-judge labelling are complete; no further Claude continuation is scheduled by this run.
