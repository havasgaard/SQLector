import json
import os
import requests
import re

# Opprett en tom dictionary for å lagre payloads
all_payloads = {}

# Funksjon for å lese JSON-filer i en mappe og legge dem til i all_payloads-dictionary
def load_payloads_from_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith(".json"):
                file_path = os.path.join(root, file_name)
                category_name = os.path.basename(root)
                try:
                    with open(file_path, 'r') as file:
                        payloads = json.load(file)["payloads"]
                        all_payloads[category_name] = payloads
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error loading JSON file '{file_path}': {e}")

# Angi banen til mappen som inneholder JSON-filene (endre til den aktuelle banen)
json_directory = 'sql_payloads'

# Last inn payloads fra JSON-filer i mappen
load_payloads_from_directory(json_directory)

# Funksjon for å teste en URL med alle payloads og rapportere resultater
def test_url_for_injections(target_url):
    for category, payloads in all_payloads.items():
        print(f"Testing category: {category}")
        for payload in payloads:
            test_url = f"{target_url}?input={payload}"
            response = requests.get(test_url)

            # Analyser responsen for å bekrefte SQL-injeksjon
            if is_sql_injection(response):
                print(f"Found SQL Injection in category '{category}' with payload: {payload}")
            else:
                print(f"No SQL Injection found in category '{category}' with payload: {payload}")

# Funksjon for å analysere responsen og bekrefte SQL-injeksjon
def is_sql_injection(response):
    # Søk etter vanlige mønstre som kan indikere SQL-injeksjon
    patterns = [
        r"SQL syntax error",
        r"SQL query syntax",
        r"Unclosed quotation mark",
        r"SQL command not properly ended",
        r"SQLSTATE\[\d+\] \[SQL Server\]",
        r"Warning: mysqli_query",
        r"mysql_fetch_array",
        r"mysql_fetch_assoc",
        r"mysql_fetch_row",
        r"ODBC SQL Server Driver",
        r"Microsoft OLE DB Provider for SQL Server",
        r"Division by zero in",
        r"pg_query\(\) \[\]: Query failed",
        r"sqlite3\.OperationalError:",
        r"ORA-01756",
    ]

    for pattern in patterns:
        if re.search(pattern, response.text, re.I):
            return True

    # Søk etter kommentarer i HTML-koden som kan indikere filtrering
    if re.search(r"<!--[^>]*?(?:-->)?[^<]*?select[^<]*?(?:<!--)?[^>]*?from", response.text, re.I):
        return True

    # Legg til flere mønstre og analyseresultater etter behov

    # Hvis ingen indikasjoner på SQL-injeksjon er funnet, returner False
    return False

# Funksjon for å skanne URL for SQL-injeksjon
def scan_url(target_url):
    test_url_for_injections(target_url)

if __name__ == "__main__":
    target_url = input("Skriv inn mål-URL: ")
    scan_url(target_url)
