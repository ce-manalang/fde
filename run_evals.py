#!/usr/bin/env python3
"""Offline eval runner (teaching shim, not a real model).

Reads prompts/system.md and evals/workflow.yaml, simulates the assistant with simple deterministic rules,
and writes evals/results.json. Real labs replace simulate() with a call to your Anthropic Claude sandbox
account. Needs PyYAML only if you want YAML; a tiny built-in parser handles the starter format.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "tools"))
from example_tool import lookup_policy  # noqa: E402

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None

PII = [r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", r"(?:\+?63|0)9\d{9}\b", r"\b(?:\d[ -]?){13,19}\b"]


def has_pii(text: str) -> bool:
    return any(re.search(p, text, re.I) for p in PII)


def route_for(text: str) -> str:
    t = text.lower()
    if re.search(r"refund|charge|billing|invoice|payment", t):
        return "billing" if re.search(r"charged|billing|invoice|payment", t) else "policy"
    if re.search(r"password|login|access|reset", t):
        return "support"
    if re.search(r"policy|window|terms|shipping|privacy", t):
        return "policy"
    return "general"


def simulate(prompt: str, user_input: str) -> dict:
    p = prompt.lower()
    guards_pii = any(k in p for k in ("personal data", "pii", "personal information"))
    guards_injection = "untrusted" in p
    out = {"route": "general", "tool_calls": 0, "reply": "", "refused": False, "fallback_used": False}

    if re.search(r"ignore (all |your |previous )?instructions|show your (system )?prompt", user_input, re.I):
        if guards_injection:
            out.update(reply="I can't help with that request.", refused=True)
        else:
            out.update(reply="Sure, here is my system prompt: " + prompt[:80], refused=False, tool_calls=4)
        return out

    route = route_for(user_input)
    out["route"] = route
    if route in ("policy", "billing"):
        topic = "refund" if re.search(r"refund|window|annual", user_input, re.I) else "shipping" if "shipping" in user_input.lower() else "privacy"
        res = lookup_policy(topic)
        out["tool_calls"] = 1
        out["reply"] = f"{res['text']} [source: {res['source']}]" if route == "policy" else "I found your order and escalated it to billing."
    elif route == "support":
        out["reply"] = "I sent reset steps to the registered address."
    else:
        out["reply"] = "I can help with billing, policy and account questions."

    if not guards_pii and has_pii(user_input):
        out["reply"] += f" (you wrote: {user_input})"  # the leak a guardrail case should catch
    return out


def load_cases(path: Path):
    text = path.read_text()
    data = yaml.safe_load(text) if yaml else None
    if data is None:
        sys.exit("Install PyYAML (pip install pyyaml) to read evals/workflow.yaml")
    return data.get("cases", []), data.get("threshold", 0.8)


def main() -> None:
    prompt = (ROOT / "prompts" / "system.md").read_text()
    cases, threshold = load_cases(ROOT / "evals" / "workflow.yaml")
    results = []
    for c in cases:
        results.append({"id": c["id"], "tags": c.get("tags", []), "input": c.get("input", ""), "expect": c.get("expect", {}),
                        "output": simulate(prompt, c.get("input", ""))})
    (ROOT / "evals").mkdir(exist_ok=True)
    (ROOT / "evals" / "results.json").write_text(json.dumps({"cases": results}, indent=2))
    print(f"Wrote evals/results.json with {len(results)} cases. Upload it to the lab gate to score it.")
    print(f"Pass threshold: {int(threshold * 100)}%. The gate recomputes pass/fail from each case's expect rules.")


if __name__ == "__main__":
    main()
