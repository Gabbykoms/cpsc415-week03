# Evaluation results

Run date: October 5, 2026. Both runs used OpenRouter, the same five cases, the same prompt, a 2,048-token output limit, and a 60-second timeout. No retries, schema enforcement, or case adjustments. Each run exited 1 because one case failed.

| Model | Passed | Failed case and interpretation | Input tokens | Output tokens |
|---|---|---|---|---|
| `minimax/minimax-m3` | 4/5 | Billing: returned `high` instead of `medium`; urgency judgment call | 1,452 | 553 |
| `xiaomi/mimo-v2.6-flash` | 4/5 | Sales: strict JSON parsing failed; real output-contract failure | 673 | 328 |

MiniMax treated the duplicate charge as urgent, while Xiaomi matched the expected medium urgency. Xiaomi failed strict JSON parsing on the sales case, while MiniMax passed it; both accepted the unrelated case, and their different ambiguous-case categories were both allowed.

## Evidence and limits

- [MiniMax run](results/minimax.txt)
- [Xiaomi run](results/xiaomi.txt)
- All ten API calls returned token usage, including Xiaomi's invalid classification reply. Total: 2,125 input tokens and 881 output tokens.
- The sales failure means Xiaomi's reply could not be parsed as strict JSON. The runner did not retain that raw reply, so the precise formatting defect is not established.
- Both models returned allowed but different categories on the ambiguous case: MiniMax technical, Xiaomi billing. Neither is a failure.
- The nine parsed responses had relevant one-sentence reasons on manual inspection.
- This is one run per model on five cases, not evidence of general model superiority. Actual dollar charges were not checked on OpenRouter Activity.
- No local-model run was performed.

## Local verification

Standard-library checks passed for valid JSON, malformed replies, fenced JSON, surrounding prose, missing fields, invalid category/urgency types, blank reasons, duplicate keys, and CLI argument errors. A mocked API response verified that invalid billed replies retain usage. A mocked five-case run verified that the runner continues after an invalid reply and includes its usage in totals. `git diff --check` passed.

## Outstanding lab requirements

- Gabriel approved the spec unchanged; no student correction was made. This requirement remains unmet and is not represented as complete.
- Team-wide conventions have not been supplied; `CLAUDE.md` documents the conventions used for this lab.
- Gabriel should personally review and be able to explain the code line described in the README.
