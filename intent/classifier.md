# Intent: Support-message classifier

## Goal
Build a command-line program that classifies one short customer-support message per command and prints JSON containing a category, urgency, and a one-sentence reason. Compare its behavior on five known cases using two hosted models.

## Who it is for
A user who wants a suggested category and priority for a support message instead of assigning them manually. This is a Week 3 learning exercise, not a production support system.

## Constraints
- Implement in Python, continuing from the Week 2 client, using only the standard library.
- Compare `minimax/minimax-m3` and `xiaomi/mimo-v2.6-flash` through OpenRouter on the same five cases.
- Output fields: `category`, `urgency`, and `reason`.
- Category is `billing`, `technical`, `sales`, or `unknown`.
- Urgency is `low`, `medium`, or `high`: high for issues needing immediate attention, medium for routine problems, and low for general inquiries or unrelated messages.
- An unrelated message must produce `unknown` and `low`, with a brief reason explaining that it is not a support request.
- When a message reasonably fits two categories, either is acceptable if the reason explains the choice.
- Follow the lab's standard-library restriction (Java may use one JSON library) and use OpenRouter for the two hosted-model evaluation runs. Keep API keys out of the repository.
- Complete intent and spec before implementation. The lab deadline is October 5, 2026, at 1:30 PM.

## Not in scope
An interactive conversation loop, a web interface, automatic replies to customers, and production ticket routing. A local-model comparison is optional.

## Success looks like
1. One command accepts one message and returns JSON with the three required fields and allowed values.
2. Five evaluation cases cover clear billing, technical, and sales requests, an ambiguous request accepting either of two categories, and an unrelated message requiring `unknown` and `low`.
3. The same cases run against two hosted models, with PASS/FAIL results, failure details, and token usage recorded honestly, including unresolved failures.

## Open questions
None remaining from the intent interview. Error handling and evaluation details will be defined in the spec.

**Approved by:** Gabriel Koomson, October 5, 2026.
