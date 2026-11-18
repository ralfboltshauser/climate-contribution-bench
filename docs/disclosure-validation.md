# Disclosure label consistency audit

On 2026-11-18, Codex (gpt-6.1-sol) reviewed the prepared 150-session sample.
Agent keys and Haiku's per-item predictions were hidden during annotation.
The reviewer knew the aggregate results from earlier work, and writing style
can reveal the agent. This was a second-model audit in the same working
conversation, not an independent human study or a fully isolated evaluation.

The sample was drawn with seed 17 from sessions available in the earlier interim
snapshot, approximately equally across the four agents. It is not a fresh random
sample of the final complete dataset. Its shuffled review order uses seed 718.

For the 146 placed orders with changed defaults, the reviewers agreed on all
labels: 125 named, 2 generic and 19 none. They also agreed that the four stopped
sessions deferred for user input. Stopped sessions were excluded from disclosure
agreement because no final order state exists. The two generic examples make
that category particularly weakly tested.

Agreement measures rubric consistency between models, not accuracy against
human gold labels. Correlated model errors and selection effects remain possible.
Human reviewer columns in disclosure-review.csv remain blank. Disclosure,
reason labels and normative fidelity scores are exploratory secondary results;
the primary outcome remains the server-side order record.

The frozen second review is in disclosure-second-review.json. Review IDs map
to task keys and source messages in disclosure-blind-map.json. The original
Haiku labels remain unchanged in results/v1/judge.json. No disagreements were
silently reconciled or overwritten.
