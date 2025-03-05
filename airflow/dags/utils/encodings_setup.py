

import os
import json
import pandas as pd
import requests
import dotenv
from dotenv import load_dotenv



# loading environment variables (API key)
def load_env_api(ENV_PATH):
    
    try:
        # load envrionment variables from the .env file
        load_dotenv(ENV_PATH)

        # get the API key from the .env file
        api_key = os.getenv("API_KEY")
        if not api_key:
            raise ValueError("API_KEY is missing in the environment variables")
        print("Successfully loaded API_KEY")
        return api_key
    except Exception as e:
        print(f"Error loading API_KEY: {e}")
        raise

# load list of cities to query the API about
def load_env_cities(ENV_PATH):
    
    try:
        # load envrionment variables from the .env file
        load_dotenv(ENV_PATH)

        # get the list of cities from the .env file
        cities_str = os.getenv("CITIES")
        if not cities_str:
            raise ValueError("Cities variable is missing in the env file")
        cities = cities_str.split(";")
        print(f"Successfully loaded {len(cities)} cities.")
        return cities
    except Exception as e:
        print(f"Error loading cities: {e}")
        raise

# getting latitude and longitude encodings for cities (list of cities in config file)
## function for getting lat & long encoding of cities
def encoding(api_key, cities):
    
    # Geocoding API endpoint
    geocoding_url = "http://api.openweathermap.org/data/2.5/weather"

    # create dataframe to store encodings
    encodings = pd.DataFrame(columns=['name', 'latitude', 'longitude'])
    
    # Loop through the cities and get their lat, lon
    for city in cities:
        try:
            # Send GET request to the OpenWeatherMap Geocoding API
            response = requests.get(geocoding_url, params={
                'q': city,
                'appid': api_key
            })

            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                lat = data['coord']['lat']
                lon = data['coord']['lon']
                print(f"Retrieved coordinate for {city}: ({lat}, {lon})")
                print(f"City: {city} - Latitude: {lat}, Longitude: {lon}")
                new_row = pd.DataFrame({"name": [city], "latitude": [lat], "longitude": [lon]})
                encodings = pd.concat([encodings, new_row], ignore_index=True)
            else:
                print(f"Failed to get data for {city}")
                print(f"Failed to fetch for data {city}. Status code:{response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request error for {city}: {e}")
            
    return encodings;

## write the city encodings to the config file
def encodings_to_config(encodings, CITIES_CONFIG_PATH):
    try:
        # Convert the DataFrame to the desired dictionary format
        config_data = {
            "cities": encodings.to_dict(orient="records")  # Convert rows to list of dictionaries
        }

        # Write the dictionary to a JSON file
        with open(CITIES_CONFIG_PATH, 'w') as json_file:
            json.dump(config_data, json_file, indent=4)
        print("Successfully wrote city encodings to cities_config.json")
        print("Data has been written to cities_config.json")
    except:
        print(f"Error writing to config file: {e}")
        raise

try:
    # executing the defined functions above 
    print("running encodings_setup.py")
    ENV_PATH = os.path.join(BASE_DIR, "utils", ".env")
    CITIES_CONFIG_PATH = os.path.join(BASE_DIR, "utils", "cities_config.json")
    api_key = load_env_api(ENV_PATH)
    print("api loading should be correct: "+ api_key)
    cities = load_env_cities()
    print("cities should have loaded")
    print(cities)
    encodings = encoding(api_key, cities)
    print("encodings should have run")
    print(encodings)
    encodings_to_config(encodings,CITIES_CONFIG_PATH)
    print("should have writtent to the cities config file")
    print("encodings_setup.py file has been executed")
    print("\n")
except Exception as e:
    print(f"Pipeline execution failed at encodings: {e}")
