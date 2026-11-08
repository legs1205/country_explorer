from main import transform_countries

sample_data = [
    {
        "name": "Testland",
        "population": "not a number",
        "area": None,
        "populationDensity": "unknown",
        "region": "Test",
        "capital": "Example",
        "languages": [{"name": "English"}, "invalid"]
    },
    "invalid country record",
    None
]

result = transform_countries(sample_data)

print("Transformation test result:")
print(result)