from app.scenario_generator.renderer import render_scenario

patient_profile = {
    "age": 45,
    "kidney_function": 90
}

template = (
    "A patient aged {age} has a recorded "
    "kidney_function value of {kidney_function}."
)

prompt = render_scenario(patient_profile, template)

print("Generated scenario:")
print(prompt)