
from brand_rules import check_brand_rules

# Test 1: Content containing all three configured violations
problematic_content = (
    "Our product guarantees results with 100% accuracy. "
    "We are the best in the world."
)

findings = check_brand_rules(problematic_content)

print("TEST 1 — Content with issues")
print(findings)

assert len(findings) == 3, (
    f"Expected 3 findings, but got {len(findings)}"
)

matched_phrases = {
    finding["matched_text"] for finding in findings
}

assert "100% accuracy" in matched_phrases
assert "guaranteed results" in matched_phrases
assert "best in the world" in matched_phrases

# Test 2: Clean content
clean_content = (
    "Our team provides helpful technology solutions "
    "and customer support."
)

clean_findings = check_brand_rules(clean_content)

print("\nTEST 2 — Clean content")
print(clean_findings)

assert len(clean_findings) == 0, (
    "Clean content should not trigger any findings."
)

print("\nAll brand-rule tests passed!")
