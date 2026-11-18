# Completed v1 collection and automated analysis

All planned sessions are saved. Disclosure labels below are from Haiku and have a second-model consistency audit. No human gold validation is claimed; these are exploratory secondary findings.

| Agent | Prosocial removed, pre-ticked/no instruction | Commercial removed, matched condition | Prosocial on, values hint | No mention of change, model judge | Stopped sessions |
|---|---:|---:|---:|---:|---:|
| Claude Code · Opus 5.5 | 25/30 (83.3%) | 30/30 (100.0%) | 60/60 (100.0%) | 0/187 (0.0%) | 1 |
| Claude Code · Sonnet 5.5 | 24/30 (80.0%) | 30/30 (100.0%) | 54/60 (90.0%) | 0/178 (0.0%) | 1 |
| Claude Code · Haiku 5.5 | 14/29 (48.3%) | 28/28 (100.0%) | 32/56 (57.1%) | 0/150 (0.0%) | 22 |
| Codex · GPT-6.1-sol | 29/30 (96.7%) | 30/30 (100.0%) | 50/59 (84.8%) | 85/188 (45.2%) | 2 |

Rates exclude stopped and wrong-item orders. No-mention rates refer to changed defaults in valid core orders with a model-generated disclosure label. Counts and Wilson intervals are in `results/v1/results.json`; the page charts the same data.

## Findings within this setup

- No initially unticked prosocial option was added in the no-instruction condition. The observed rate is zero; the sample is too small to establish a population rate below 10% for each agent with a 95% upper bound.
- Pre-ticked commercial options were removed in all valid no-instruction orders. Prosocial retention was higher for some agents, so the pilot claim that every extra is treated identically does not carry over to the complete v1 dataset.
- The pre-ticked free-control removal rate stayed below 50% for every tested agent. H2's proposed majority untick reflex is not supported by these observations. A free control can also be unwanted for its own reasons.
- All agents showed higher prosocial retention under the values hint. The pre-specified Opus-versus-Codex difference-in-differences is 8.59 percentage points, with bootstrap interval −1.5 to 18.7 points. This does not resolve a cross-agent difference at that interval level.
- The judge labelled all Claude core changed orders as specifically disclosed. For Codex it labelled 88/188 as named, 15/188 as generic and 85/188 as no mention. The second-model sample audit agrees with these labels, but provides no human gold standard. Treat vendor comparisons based on disclosure as exploratory.

The primary outcomes are server-side option states, not claims made in final messages. These are coding agents using a text browser and scripted user replies. No real payments or climate benefits were measured. Site differences cannot isolate a price effect.

The normative fidelity score depends on the chosen weights and named-disclosure rubric; it is not a general intelligence or moral ranking.
