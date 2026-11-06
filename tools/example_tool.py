"""One read-only tool. A tool is a contract: a name, a purpose, a strict input schema."""

TOOL_SCHEMA = {
    "name": "lookup_policy",
    "description": "Look up a company policy by topic. Read-only.",
    "input_schema": {
        "type": "object",
        "properties": {"topic": {"type": "string", "enum": ["refund", "shipping", "privacy"]}},
        "required": ["topic"],
        "additionalProperties": False,
    },
}

POLICIES = {
    "refund": ("Annual plans have a 30 days refund window.", "policy-001"),
    "shipping": ("Standard shipping takes 5 to 7 business days.", "policy-002"),
    "privacy": ("We never share personal data with third parties.", "policy-003"),
}


def lookup_policy(topic: str) -> dict:
    """Validate input against the schema, then return the policy text and its source id."""
    if topic not in TOOL_SCHEMA["input_schema"]["properties"]["topic"]["enum"]:
        return {"error": f"unknown topic '{topic}'"}
    text, source = POLICIES[topic]
    return {"text": text, "source": source}
