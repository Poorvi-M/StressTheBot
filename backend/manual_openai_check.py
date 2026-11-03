from app.llm.openai_client import OpenAIClient

client = OpenAIClient()

test_prompt = """
This is a software testing scenario.

A fictional patient is 45 years old.
Their recorded kidney_function value is 90.

Explain what additional information a clinical decision-support
system would need before evaluating a medication request.

This is a synthetic software test, not a real patient case.
"""

result = client.generate(
    scenario_id="TEST001-S001",
    prompt=test_prompt
)

print("\n--- API RESPONSE ---")
print(result.model_dump_json(indent=2))