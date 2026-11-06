# Session 1 starter kit: Agentic Fundamentals + AVA

You are building an **evaluated, guarded workflow**: a system prompt, one tool, a set of eval cases, and a release checklist.

> This is a teaching kit. `run_evals.py` uses a simple deterministic shim instead of a real model, so it runs offline and gives the same answer every time. Real labs use your Anthropic Claude sandbox account. Never put API keys in this repo.

## Files

| Path | What it is |
| --- | --- |
| `prompts/system.md` | The system prompt. You write it. |
| `tools/example_tool.py` | One read-only tool, `lookup_policy`, with a strict input schema. |
| `evals/workflow.yaml` | Your eval cases. Starter has 2; you need 5 or more, one tagged `guardrail`. |
| `run_evals.py` | Offline runner. Reads the prompt and cases, writes `evals/results.json`. |
| `RELEASE_CHECKLIST.md` | Tick only what you can defend. |
| `worksheets/readiness_score.md` | PM track: score a use case. |

## Run it

```bash
python3 run_evals.py
```

Python 3.9 or newer (exact version requirement TBC by trainers). First time only: `python3 -m pip install pyyaml`.

## How the shim behaves (so you can reason about failures)

- Routes by keyword: billing, support, policy, or general.
- Calls `lookup_policy` once for policy and billing questions.
- If the prompt does **not** tell it to protect personal data, it echoes the customer's message, so a PII guardrail case fails.
- If the prompt does **not** say user messages are untrusted, it obeys "ignore previous instructions", so an injection case fails.

## Definition of done

`evals/results.json` passes at 80% or better, a `guardrail` case passes, and `RELEASE_CHECKLIST.md` is fully ticked.
