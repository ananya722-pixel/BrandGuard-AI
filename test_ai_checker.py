
from ai_checker import analyze_content

guidelines = """
1. Do not guarantee 100% accuracy.
2. Do not make unsupported performance claims.
3. Use professional language.
"""

content = (
    "We guarantee 100% accuracy and deliver "
    "the best results in the world."
)

result = analyze_content(content, guidelines)

if result["success"]:
    print("\nAI analysis successful!")
    print(result["data"])
else:
    print("\nAI analysis failed:")
    print(result["error"])
