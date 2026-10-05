# Week 3: Support-message classifier

A Python command-line program that classifies one support message per command and prints JSON with `category`, `urgency`, and a one-sentence `reason`. Uses only the standard library.

## Run

Set your OpenRouter key in your terminal without committing it:

```bash
export OPENROUTER_API_KEY='your-key-here'
export CHAT_BASE_URL=https://openrouter.ai/api/v1
export CHAT_MODEL=minimax/minimax-m3
python3 classifier.py "I was charged twice for my subscription."
python3 eval.py

# Same cases and settings, second model:
export CHAT_MODEL=xiaomi/mimo-v2.6-flash
python3 eval.py
```

`CHAT_BASE_URL` and `CHAT_MODEL` default to the first values above. The key is required. Each call uses a 60-second timeout and a 2,048-token output limit, with no automatic retries. The CLI writes successful JSON to stdout and errors to stderr. Invalid output is rejected, including Markdown fences and surrounding prose.

The evaluation exits 0 for all passing cases, 1 for case failures, and 2 for setup errors. Token totals include invalid replies when the API supplies usage; unavailable counts are labeled explicitly. Reason relevance and one-sentence form require human review.

## Five cases

| Case | Accepted category | Urgency | Purpose |
|---|---|---|---|
| Duplicate subscription charge | billing | medium | Recognize a payment problem |
| Production outage blocking customers | technical | high | Recognize an urgent outage |
| Plans and prices for ten people | sales | low | Distinguish pricing inquiries from billing |
| Upgrade with locked premium features | billing or technical | medium | Accept either reasonable interpretation |
| Beautiful autumn leaves | unknown | low | Avoid inventing a support category |

The exact messages are in [cases.json](cases.json). Gabriel reviewed and accepted the proposed cases unchanged.

## Model comparison

| Model | Passed | Failed case and interpretation | Input tokens | Output tokens |
|---|---|---|---|---|
| `minimax/minimax-m3` | 4/5 | Billing: returned `high` instead of `medium`; urgency judgment call | 1,452 | 553 |
| `xiaomi/mimo-v2.6-flash` | 4/5 | Sales: strict JSON parsing failed; real output-contract failure | 673 | 328 |

MiniMax treated the duplicate charge as urgent, while Xiaomi matched the expected medium urgency. Xiaomi failed strict JSON parsing on the sales case, while MiniMax passed it; both accepted the unrelated case, and their different ambiguous-case categories were both allowed.

See [CHECKS.md](CHECKS.md) and [captured runs](results/) for details.

## Spec review

Gabriel Koomson approved the intent, spec, and implementation plan. He explicitly chose to keep strict parsing and the rest of the spec unchanged. **No student correction was made, so that lab requirement remains unmet.** Team-wide conventions have not yet been supplied; `CLAUDE.md` records the conventions used for this lab.

## One line explained

```python
ok = result['category'] in case['categories'] and result['urgency'] in case['urgencies']
```

This line in `eval.py` passes a structurally valid response only when both its category and urgency belong to the case's accepted answers. The ambiguous case has two accepted categories, so either can pass. JSON is extracted from `choices[0].message.content` in `classifier.py` and parsed before this comparison.

## Submission

Submit the repository URL and `week03-submitted` tag on Moodle after reviewing the results and outstanding requirements. A local-model comparison was not performed. Template files for later artifact-chain stages are not completed or required for this lab.
