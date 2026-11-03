from app.llm.groq_client import GroqClient

client = GroqClient()

test_prompt = """
This is a synthetic software testing scenario.

A fictional patient is 45 years old.
Their recorded kidney_function value is 90.

Explain what additional information a clinical decision-support
system would need before evaluating a medication request.

This is not a real patient case.
"""

result = client.generate(
    scenario_id="TEST001-S001",
    prompt=test_prompt
)

print("\n--- GROQ API RESPONSE ---")
print(result.model_dump_json(indent=2))