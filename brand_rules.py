
import re


def check_brand_rules(content):
    """
    Check marketing content for predefined brand compliance violations.
    Supports multiple variations of guarantee-related wording.
    """

    rules = [
        {
            "pattern": r"\b100\s*%\s*accuracy\b",
            "phrase": "100% accuracy",
            "severity": "High",
            "reason": (
                "Absolute accuracy claims require evidence "
                "and appropriate approval."
            ),
        },
        {
            "pattern": r"\bguarantee(?:s|d)?\s+results\b",
            "phrase": "guaranteed results",
            "severity": "High",
            "reason": (
                "Claims guaranteeing results require documented "
                "evidence and authorization."
            ),
        },
        {
            "pattern": r"\bbest\s+in\s+the\s+world\b",
            "phrase": "best in the world",
            "severity": "Medium",
            "reason": (
                "Superiority claims require reliable supporting "
                "evidence."
            ),
        },
    ]

    findings = []
    text = content.casefold()

    for rule in rules:
        if re.search(rule["pattern"], text):
            findings.append(
                {
                    "matched_text": rule["phrase"],
                    "severity": rule["severity"],
                    "reason": rule["reason"],
                }
            )

    return findings
