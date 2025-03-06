import sys
import os
import pandas as pd
import psycopg2
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.hooks.base import BaseHook
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# function to read the clean_data file and return a dataframe
def read_clean_data(CLEAN_DATA_PATH):
    try:
        df_db = pd.read_csv(CLEAN_DATA_PATH)
        print(f"Successfully loaded clean data from {CLEAN_DATA_PATH}")
        return df_db
    except FileNotFoundError:
        print(f"Error: the file {CLEAN_DATA_PATH} does not exist")
    except pd.errors.EmptyDataError:
        print(f"Error: the file {CLEAN_DATA_PATH} is empty")
    except Exception as e:
        print(f"Unexpected error while reading clean data: {e}")
    return None

# function to load env variables & establish database connection
def env_db_connection():
    print("\n")
    print("Trying to connect with postgres_hook")
    try:
        postgres_hook = PostgresHook(postgres_conn_id='postgres_weather_conn')
        conn = postgres_hook.get_conn()
        return conn
    except Exception as e:
        print("there was an error connecting to the connection/db \n")
        print(e)
        print(f"Error connecting to database: {e}")
        return None
        

# function to insert weather data into the location database table
# Insert or get Location_ID
def get_or_insert_location(cursor, lat, lon, city, timezone, tz_offset):
    try:
        cursor.execute(
            "SELECT Location_ID FROM Locations WHERE Lat=%s AND Long=%s;",
            (lat, lon)
        )
        location = cursor.fetchone()
        if location:
            print("location is already stored in the database")
            return location[0]
        else:
            cursor.execute(
                "INSERT INTO Locations (Lat, Long, City, Timezone, Timezone_offset) VALUES (%s, %s, %s, %s, %s) RETURNING Location_ID;",
                (lat, lon, city, timezone, tz_offset)
            )
            return cursor.fetchone()[0]
    except Exception as e:
        print(f"Error inserting location: {e}")
    return None

# function to insert weather data into the weather database table
# Insert or get Weather_ID
def get_or_insert_weather(cursor, weather_id, main, description):
    try:
        cursor.execute(
            "SELECT Weather_ID FROM Weather where Weather_ID=%s;",
            (weather_id,)
        )
        weather = cursor.fetchone()
        if weather:
            print("weather is already stored in the database")
            return weather[0]
        else:
            cursor.execute(
                "INSERT INTO Weather (Weather_ID, Main, Description) VALUES (%s, %s, %s) RETURNING Weather_ID;",
                (weather_id, main, description)
            )
            return cursor.fetchone()[0]
    except Exception as e:
        print(f"Error inserting weather data: {e}")
    return None

# function to insert weather data into the record database table
# Insert Record
def insert_record(cursor, location_id, weather_id, row):
    try:
        if not isinstance(location_id, int) or not isinstance(weather_id, int):
            print("Invalid location_id or weather_id: skipping weather insertion")
            return None
        
        cursor.execute(
        """
        INSERT INTO Records (Location_ID, Weather_ID, Local_time, Sunrise, Sunset, Temp_F, Feels_like_F, 
                            Humidity, Dew_Point, UVI, Clouds, Visibility, Wind_speed_mph, Wind_deg, Wind_gust_mph)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING Record_ID;
        """,
        (location_id, weather_id, row['current_time'], row['sunrise'], row['sunset'], row['temp_F'],
            row['feels_like_F'], row['humidity'], row['dew_point'], row['uvi'], row['clouds'], row['visibility'], 
            row['wind_speed_mph'], row['wind_deg'], row['wind_gust_mph'])
        )
        print("record has been inserted into the table")
        print("Record has been inserted into the table")
        return cursor.fetchone()[0]
    except Exception as e:
        print(f"Error inserting record: {e}")
    return None

# function to insert weather data into the alert database table
# Insert Alert
def insert_alert(cursor, record_id, alert_description):
    try:
        cursor.execute(
            "INSERT INTO Alerts (Record_ID, Description) VALUES (%s, %s);",
            (record_id, alert_description)
        )
        print("alert has been inserted into the table")
        print("alert has been inserted into the table")
    except Exception as e:
        print(f"Error inserting alert: {e}")

# function to delete the clean_data csv file once the data has been uploaded to avoid duplication of data loading/records
def delete_clean_data(CLEAN_DATA_PATH):
    try:
        if os.path.exists(CLEAN_DATA_PATH):
            os.remove(CLEAN_DATA_PATH)
            print("File deleted successfully")
            print.info(f"File {CLEAN_DATA_PATH} deleted successfully")
        else:
            print("File does not exist")
            print(f"File {CLEAN_DATA_PATH} does not exist")
    except Exception as e:
        print(f"Error deleting file {CLEAN_DATA_PATH}: {e}")
        
# function to delete the raw_data csv file once the data has been uploaded to avoid duplication of data loading/records
def delete_raw_data(RAW_DATA_PATH):
    try:
        if os.path.exists(RAW_DATA_PATH):
            os.remove(RAW_DATA_PATH)
            print("File deleted successfully")
            print(f"File {RAW_DATA_PATH} deleted successfully")
        else:
            print("File does not exist")
            print(f"File {RAW_DATA_PATH} does not exisit")
    except Exception as e:
        print(f"Error deleting file {RAW_DATA_PATH}: {e}")