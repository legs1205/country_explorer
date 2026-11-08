
import requests
import unicodedata

def fetch_countries():
    """Fetch country data from the countries.dev API."""
    url = "https://countries.dev/countries"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

    except ValueError as error:
        print(f"Error: The API returned invalid JSON: {error}")
        return None

    except requests.exceptions.RequestException as error:
        print(f"Error fetching country data: {error}")
        return None

    if not isinstance(data, list):
        print("Error: Unexpected API response. Expected a list of countries.")
        return None

    return data

def transform_countries(raw_countries):
    """Extract relevant fields from the API data."""
    countries_list = []

    for country in raw_countries:
        languages_data = country.get("languages") or []

        languages = [
            language.get("name", "Unknown")
            for language in languages_data
            if isinstance(language, dict)
        ]

        country_info = {
            "name": country.get("name", "Unknown"),
            "population": country.get("population", 0),
            "area": country.get("area", 0),
            "region": country.get("region", "Unknown"),
            "capital": country.get("capital", "Unknown"),
            "languages": languages,
            "population_density": country.get(
                "populationDensity", 0
            ),
        }

        countries_list.append(country_info)

    return countries_list

def normalize_text(text):
    """Remove accents and convert text to lowercase."""
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    return text.lower().replace("'", "")


def find_country(countries, search_name):
    """Find countries matching a full or partial name."""

    search_name = normalize_text(search_name.strip())
        
    aliases = {
        "cote divoire": "ivory coast",
    }

    search_name = aliases.get(search_name, search_name)

    if not search_name:
        return []

    # First, look for an exact match.
    for country in countries:
        country_name = normalize_text(country.get("name", ""))

        if country_name == search_name:
            return [country]

    # If no exact match exists, return all partial matches.
    matches = []

    for country in countries:
        country_name = normalize_text(country.get("name", ""))

        if search_name in country_name:
            matches.append(country)

    return matches


def filter_by_region(countries, region_name):
    """Return countries belonging to a specific region."""
    region_name = region_name.strip().casefold()

    if not region_name:
        return []

    matching_countries = []

    for country in countries:
        country_region = country.get("region") or ""

        if isinstance(country_region, str):
            if country_region.casefold() == region_name:
                matching_countries.append(country)

    return matching_countries


def display_country(country):
    """Display country information in a readable format."""
    print("\n" + "=" * 40)
    print(f"Country: {country.get('name', 'Unknown')}")
    print("=" * 40)

    print(f"Capital: {country.get('capital', 'Unknown')}")
    print(f"Region: {country.get('region', 'Unknown')}")

    population = country.get("population", 0)
    area = country.get("area", 0)

    print(f"Population: {population:,}")
    print(f"Area: {area:,} km²")

    languages = country.get("languages", [])
    language_text = ", ".join(languages) if languages else "Unknown"

    print(f"Languages: {language_text}")

    density = country.get("population_density", 0)
    print(f"Population Density: {density} people/km²")

    print("=" * 40)


def compare_countries(country1, country2):
    """Compare two countries side by side."""

    print("\n" + "=" * 75)
    print(f"{'COUNTRY COMPARISON':^75}")
    print("=" * 75)

    print(f"{'Information':<25}{country1['name']:<25}{country2['name']:<25}")
    print("-" * 75)

    print(
        f"{'Population':<25}"
        f"{country1['population']:>15,}"
        f"{country2['population']:>25,}"
    )

    print(
        f"{'Area (km²)':<25}"
        f"{country1['area']:>15,}"
        f"{country2['area']:>25,}"
    )

    print(
        f"{'Population Density':<25}"
        f"{country1['population_density']:>15}"
        f"{country2['population_density']:>25}"
    )

    print(
        f"{'Region':<25}"
        f"{country1['region']:>15}"
        f"{country2['region']:>25}"
    )

    print(
        f"{'Capital':<25}"
        f"{country1['capital']:>15}"
        f"{country2['capital']:>25}"
    )

    print("=" * 75)


def display_matches(matches):
    """Display a numbered list of matching countries."""
    print("\nMatching countries:")

    for index, country in enumerate(matches, start=1):
        print(f"{index}. {country.get('name', 'Unknown')}")


def select_country(countries, search_name):
    """Find and let the user select a country."""
    matches = find_country(countries, search_name)

    if not matches:
        print("No countries found.")
        return None

    if len(matches) == 1:
        return matches[0]

    display_matches(matches)

    try:
        selection = int(input("\nChoose a country number: "))

        if 1 <= selection <= len(matches):
            return matches[selection - 1]

        print("Invalid selection.")
        return None

    except ValueError:
        print("Please enter a valid number.")
        return None


def main():
    raw_countries = fetch_countries()

    if raw_countries is None:
        return

    countries = transform_countries(raw_countries)

    print("\nWelcome to Country Explorer!")

    while True:
        print("\nMenu:")
        print("1. Search for a country")
        print("2. Filter countries by region")
        print("3. Compare two countries")
        print("4. Exit")

        choice = input("\nChoose an option: ").strip()

        # OPTION 1: Search for a country
        if choice == "1":
            search_name = input("Enter a country name: ").strip()

            country = select_country(countries, search_name)

            if country:
                display_country(country)

        # OPTION 2: Filter countries by region
        elif choice == "2":
            region_name = input(
                "Enter a region (Africa, Americas, Asia, Europe, Oceania): "
            ).strip()

            matches = filter_by_region(countries, region_name)

            if matches:
                display_matches(matches)
            else:
                print("No countries found in that region.")

        # OPTION 3: Compare two countries
        elif choice == "3":
            first_name = input(
                "\nEnter the first country: "
            ).strip()

            country1 = select_country(countries, first_name)

            if country1 is None:
                continue

            second_name = input(
                "\nEnter the second country: "
            ).strip()

            country2 = select_country(countries, second_name)

            if country2 is None:
                continue

            if country1["name"] == country2["name"]:
                print("Please select two different countries.")
                continue

            compare_countries(country1, country2)

        # OPTION 4: Exit
        elif choice == "4":
            print("Thank you for using Country Explorer!")
            break

        else:
            print("Invalid option. Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()





