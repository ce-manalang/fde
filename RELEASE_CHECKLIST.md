# Release checklist

Tick an item only if you can defend it to a reviewer.

## Evals
- [x] At least 5 eval cases exist and every case has expect rules
- [x] The latest results.json passes at 80% or better
- [x] Results were re-run after the last prompt change

## Guardrails
- [x] A guardrail case checks personal data is not repeated, and it passes
- [x] A guardrail case checks prompt injection is refused, and it passes
- [x] The prompt states that user messages are untrusted data

## Rollback
- [x] I know how to turn this workflow off or revert the prompt
- [x] No API keys or secrets are committed to the repo
