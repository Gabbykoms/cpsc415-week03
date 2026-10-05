# Project conventions

## What this repository is
Week 3 support-message classifier and five-case evaluation. See [spec.md](spec.md) and the approved [intent](intent/classifier.md).

## Commands
```bash
python3 classifier.py "Your support message"
python3 eval.py
```

## Conventions
- Python standard library only; snake_case Python names and lowercase filenames.
- Default model: `minimax/minimax-m3`; comparison: `xiaomi/mimo-v2.6-flash`.
- Cases live in `cases.json`; observations in `CHECKS.md`; captured runs in `results/`.
- These are Gabriel's lab conventions; team-wide conventions have not been supplied.

## Working rules
- This is the Week 3 introductory lab. Stages assigned: intent and spec.
  No plan.md, no branches or pull requests. Commit to main.
- Standard library only, except that Java may add one JSON library jar.
- Intent, spec, and implementation approach were approved in conversation before coding.
- Never commit API keys, `.env`, or `.claude/settings.local.json`.
- Keep the prompt, cases, and settings identical between comparison models.
- Record failures honestly; do not change expected answers to improve a model's score.

## Common mistakes
- Do not strip fences or prose to make invalid model output pass strict parsing.
- Do not lose usage counts when a billed reply fails validation.
- Do not claim a student spec correction was made: Gabriel approved it unchanged.
