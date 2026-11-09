
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

expected_result = [
    {
        "name": "Testland",
        "population": 0,
        "area": 0,
        "region": "Test",
        "capital": "Example",
        "languages": ["English"],
        "population_density": 0
    }
]

assert result == expected_result, (
    f"Test failed!\nExpected: {expected_result}\nGot: {result}"
)

print("All transformation tests passed!")
