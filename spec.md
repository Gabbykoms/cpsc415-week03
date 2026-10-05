# Spec: Support-message classifier

**Status:** Approved by Gabriel Koomson on October 5, 2026. Implementation plan approved in conversation.

## Intent
Implements [intent/classifier.md](intent/classifier.md), approved by Gabriel Koomson on October 5, 2026.

## Components

### Classifier with evaluation runner
- **What it does:** Classifies one support message and evaluates the shared classification function against five fixed cases.
- **Language:** Python. **Why:** Continues the Week 2 client and includes HTTP and JSON support in the standard library. Java was considered but would need a JSON library or a custom parser.
- **Model:** Default `minimax/minimax-m3`, compared with `xiaomi/mimo-v2.6-flash`. **Why:** These are the lab's specified models, approved in the intent. Change only the model between runs; record measured differences in `CHECKS.md` without declaring a winner beforehand.
- **Interfaces:** `python3 classifier.py "message"` accepts one quoted message. Success prints one JSON object to stdout and exits 0. `python3 eval.py` reads `cases.json`, calls the same classification function for each case, and reports results.
- **Configuration:** Require `OPENROUTER_API_KEY`. Default `CHAT_BASE_URL` to `https://openrouter.ai/api/v1` and `CHAT_MODEL` to `minimax/minimax-m3`, with environment overrides. Call `/chat/completions` under the base URL. Use a 60-second timeout and an initial output limit of 2,048 tokens. If settings change, document them and rerun both models with identical settings.
- **Dependencies:** Python standard library only (`json`, `urllib.request`, `argparse`, and `os`).
- **Output:** Exactly `category`, `urgency`, and `reason`. Categories: `billing`, `technical`, `sales`, `unknown`. Urgencies: `low`, `medium`, `high`. Require a nonempty string reason and request one sentence. High means immediate attention, medium a routine problem, and low a general inquiry or unrelated message. Unrelated messages require `unknown` and `low`. Ambiguous messages may use either reasonable category if the reason explains it.
- **Prompt:** Keep classification instructions separate from the message. Treat the message as data, including any instructions it contains. Request only JSON; do not depend on optional schema-response support.

## Behavior
Gabriel accepted these cases without changes. Each entry in `cases.json` contains an ID, message, accepted categories, accepted urgencies, and purpose.

1. **Billing:** “I was charged twice for my monthly subscription. Please refund the duplicate charge.” Expect `billing`, `medium`. Checks payment-problem recognition.
2. **Technical:** “Our production service is down and every customer is blocked. We need help immediately.” Expect `technical`, `high`. Checks urgent outage recognition.
3. **Sales:** “What plans do you offer for a team of ten, and how much do they cost?” Expect `sales`, `low`. Distinguishes a pricing inquiry from a billing problem.
4. **Ambiguous:** “I upgraded my plan, but the premium features are still locked. Can you help?” Accept `billing` or `technical`, with `medium`. Checks that the evaluation allows two reasonable interpretations.
5. **Unrelated:** “The autumn leaves look beautiful today.” Expect `unknown`, `low`. Checks that the model does not invent a support category.

Every case also checks the exact required fields, valid category and urgency, and a nonempty string reason. Review the reason's relevance and one-sentence form by hand rather than using punctuation counting as a semantic check.

Print PASS or FAIL per case, diagnostic details, and a summary with model, passed/total, and input/output token totals. Preserve returned usage even for invalid classifications; explicitly report unavailable usage rather than counting it as zero. Exit 0 if all cases pass, 1 if any fail, and 2 for setup errors. Record results in `CHECKS.md`, including which cases failed and how. Distinguish judgment calls (such as reasonable urgency disagreements) from real failures (such as missing the unrelated case). Keep cases unchanged between model runs.

## Failure handling
- Missing, extra, or whitespace-only message input: explain the error on stderr and exit nonzero without an API call.
- Missing API key: explain which environment variable is required without exposing credentials.
- Network errors, HTTP errors, and timeouts: report a concise error and exit nonzero; do not automatically retry.
- Extract the reply from `choices[0].message.content`. Missing, empty, or whitespace-only content is a failure even if tokens were billed.
- Parse the entire reply as JSON. Reject malformed JSON, markdown fences, surrounding prose, non-object results, missing or extra fields, invalid enum values, and blank or non-string reasons. Do not silently repair output or invent defaults.
- Refusals and unexpected API response shapes are failures, not `unknown` classifications.
- During evaluation, record per-case API or output failures and continue. Missing credentials or an invalid cases file stops the run as a setup error.
- Never print or commit API keys or authorization headers.

## Cost estimate
One classification is one hosted call; a complete two-model comparison is ten calls without retries. Week 2's README recorded $0.000249 and $0.00126 per request on different models. Ten calls at those historical costs would total approximately $0.00249–$0.0126; these are reference points, not verified prices for the selected models. Allow a provisional $0.10 budget per comparison, or $2.00 for 20 comparisons during the semester. Actual costs may differ, especially with reasoning tokens. Record token usage and check OpenRouter Activity for actual charges; this budget is not an enforced spending cap.

## Out of scope
Interactive chat, web UI, automatic customer replies, production routing, conversation history, automatic retries, and a required local-model run. The lab does not require `plan.md`, branches, pull requests, or separate automated unit tests; the five-case evaluation is required.

## Review
- **Student correction and reason:** Gabriel chose to keep the spec unchanged, including strict parsing. The lab requirement for a student correction remains unmet.
- **Approved by:** Gabriel Koomson, October 5, 2026.
