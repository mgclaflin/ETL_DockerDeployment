
import os
import json
import requests
from dotenv import load_dotenv


# loading environment variables (API key)
def load_env_api(ENV_PATH):
    try:
        # load envrionment variables from the .env file
        load_dotenv(ENV_PATH)
        # get the API key from the .env file
        api_key = os.getenv("API_KEY")
        if not api_key:
            raise ValueError("API_KEY is missing in the env variables")
        print("Successfully loaded API key")
        return api_key
    except Exception as e:
        print(f"Error loading API key: {e}")
        raise

# function to execute the API call
# api call to get the current weather 
def get_weather(api_key, city, lat, lon, exclude='minutely,daily,hourly', units='imperial', lang='en'):
    # Build the base URL for the OneCall API
    api_url = f"https://api.openweathermap.org/data/3.0/onecall"
    
    # Prepare the parameters for the API call
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': units,  # 'imperial' for Fahrenheit, 'metric' for Celsius
        'lang': lang      # Language for the response
    }
    
    # Add the 'exclude' parameter if it's provided
    if exclude:
        params['exclude'] = exclude
        
    try:
        # Make the API request
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        # Check if the request was successful
        data = response.json()
        # Print or process the data
        data['City']=city
        print(f"Successfully fetched weather data for {city}")
        print(data)
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error: {response.status_code}, {response.text}")
        print(f"Error fetching data from {api_url}: {e}")
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON response for {city}: {e}")
    return None
    

# function to run the API call based upon cities in config file
def city_weather_data_extraction(CITIES_CONFIG_PATH, ENV_PATH):
    try:
        # Step 1: Load the config file
        with open(CITIES_CONFIG_PATH, 'r') as f:
            config_data = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading cities config file: {e}")
        raise

    weather_data = []

    # Step 2: Loop through each city and use the data for API requests
    for city in config_data['cities']:
        api_key = load_env_api(ENV_PATH)
        latitude = city['latitude']
        longitude = city['longitude']
        city_name = city['name']
        
        if not all([city_name,latitude,longitude]):
            print(f"skipping city due to missing data: {city}")
            continue

        weather_data.append(get_weather(api_key, city_name, latitude, longitude))
        
    return weather_data

# writing the extracted data to the raw_weather_data.json file
def write_raw_data(weather_data, RAW_DATA_PATH):

    try:
        #ensure the directory exists
        os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)

        # Check if the file exists to decide whether to append or create new
        if os.path.exists(RAW_DATA_PATH):
            # If the file exists, load the existing data, then append new data
            with open(RAW_DATA_PATH, 'r') as json_file:
                existing_data = json.load(json_file)
                existing_data.extend(weather_data)

            # Append to the file
            with open(RAW_DATA_PATH, 'w') as json_file:
                json.dump(existing_data, json_file, indent=4)
        else:
            # If the file doesn't exist, create it and write the new data
            with open(RAW_DATA_PATH, 'w') as json_file:
                json.dump(weather_data, json_file, indent=4)

        print(f"Data saved to {RAW_DATA_PATH}")
        print(f"Weather data successfully saved to {RAW_DATA_PATH}")
    except (IOError, json.JSONDecodeError, ValueError) as e:
        print(f"Error writing to {RAW_DATA_PATH}: {e}")
        raise

    
# writing the extracted data to the raw_compiled_data.json file
def write_compiled_raw_data(weather_data, RAW_COMPILED_PATH):
    
    try:
        # Check if the file exists to decide whether to append or create new
        if os.path.exists(RAW_COMPILED_PATH):
            # If the file exists, load the existing data, then append new data
            with open(RAW_COMPILED_PATH, 'r') as json_file:
                existing_data = json.load(json_file)
                existing_data.extend(weather_data)

            # Append to the file
            with open(RAW_COMPILED_PATH, 'w') as json_file:
                json.dump(existing_data, json_file, indent=4)
        else:
            # If the file doesn't exist, create it and write the new data
            with open(RAW_COMPILED_PATH, 'w') as json_file:
                json.dump(weather_data, json_file, indent=4)

        print(f"Data saved to {RAW_COMPILED_PATH}")
        print(f"Weather data successfully saved to {RAW_COMPILED_PATH}")
    except (IOError, json.JSONDecodeError, ValueError) as e:
        print(f"Error writing to {RAW_COMPILED_PATH}: {e}")
        raise

