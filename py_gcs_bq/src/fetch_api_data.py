import os
import json
import requests

def fetch_and_save_data():
    """
    Fetches data from the specified API URL and saves it to the provided file path.
    Handles potential errors during data retrieval and file writing.
    """
    try:
        response = requests.get('https://sampleapis.com/api-list/playstation/games')
        response.raise_for_status()
        data = response.json()

        if isinstance(data, (dict, list)):
            try:
                with open('./data/playstation.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4)
                print(f"Data saved successfully to: './data/playstation.json'")
            except OSError as err:
                print(f"Error saving data: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Error fetching data: {err}")
        return
