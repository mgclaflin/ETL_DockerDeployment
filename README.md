# Weather ETL Pipeline

This project demonstrates an **ETL (Extract, Transform, Load)** pipeline that collects weather data from an API, processes it, and stores it in a **PostgreSQL** database for later analysis. The pipeline is automated to run regularly, updating the database with fresh weather data at specified intervals. This project utilizes **Apache Airflow** for scheduling and Docker for containerization, making it easy to deploy and manage.

## Project Overview

The main goal of this project is to showcase **data engineering** skills, including:
- Extracting data from an API (Weather API)
- Transforming data into the desired format
- Loading the data into a **PostgreSQL** database
- Automating the ETL process with **Apache Airflow** for scheduling
- Containerizing the entire application using **Docker** for portability and ease of deployment

## Features
- **Data Extraction**: Weather data is fetched from a public weather API (e.g., OpenWeatherMap).
- **Data Transformation**: Data is cleaned and transformed to fit the schema of the PostgreSQL database.
- **Data Loading**: Transformed data is inserted into a PostgreSQL database for storage.
- **Automation**: The ETL process is automated and scheduled using **Apache Airflow**.
- **Containerization**: The project is containerized using **Docker** to ensure consistent environments across different systems.

## Prerequisites

Before setting up the project, ensure you have the following installed:
- **Docker** and **Docker Compose** for containerization and orchestration.
- **Python 3.x**
- **PostgreSQL database** (either locally or using a Docker container).
- Access to a weather API (e.g., OpenWeatherMap, WeatherAPI)
- Required Python libraries (listed below)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/weather-etl-pipeline.git
   cd weather-etl-pipeline
   ```

2. **Set up Docker containers**:
   - Ensure Docker and Docker Compose are installed.
   - In the project root, create a `.env` file to store environment variables for your database and API credentials. Example:

     ```env
     AIRFLOW_UID=50000
     AIRFLOW_GID=50000
     WEATHER_API_KEY=your_api_key_here
     POSTGRES_HOST=localhost
     POSTGRES_USER=weather_user
     POSTGRES_PASSWORD=weather_password
     POSTGRES_DB=weather
     ```

3. **Build and start the containers**:
   - Use Docker Compose to build and start the containers for the project, including Airflow and PostgreSQL.

     ```bash
     docker-compose up --build
     ```

   This will start Airflow, PostgreSQL, and any other necessary services defined in the `docker-compose.yml`.

4. **Set up PostgreSQL database**:
   - Airflow will automatically handle the creation of the necessary tables when the DAG runs.
   - Alternatively, you can manually create the database and tables by running the `schema.sql` script if needed.

5. **Configure the Weather API**:
   - Sign up for an API key from your chosen weather service (e.g., [OpenWeatherMap](https://openweathermap.org/)).
   - Set the API key and other configuration details in the `config.py` file or via environment variables.

## Usage

### Running the ETL Pipeline with Airflow

1. **Start the Airflow Web UI**:
   - Once the containers are running, you can access the Airflow web UI at `http://localhost:8080`.
   - Log in using the default credentials (`airflow` / `airflow` or custom ones from `.env`).

2. **Running the ETL Process**:
   - Airflow will automatically pick up the defined DAGs (ETL workflows). The pipeline will run at the scheduled intervals.
   - You can manually trigger the DAG from the Airflow UI if you want to run it immediately.

3. **Viewing the Data**:
   - After the ETL process runs, data will be stored in the PostgreSQL database.
   - You can query the data using SQL in a tool like pgAdmin or via the `psql` command line.

### Automating the ETL Process
- The ETL process is scheduled to run automatically at specified intervals using Apache Airflow. You can modify the DAG scheduling settings as per your requirements.

## Dependencies

- **Apache Airflow**: For scheduling and automating the ETL pipeline.
- **requests**: For making HTTP requests to the weather API.
- **psycopg2**: For PostgreSQL database interaction.
- **pandas**: For data manipulation and transformation.
- **dotenv**: For loading environment variables (API keys, DB credentials).
- **SQLAlchemy**: For database connection handling with Airflow.

To install the dependencies, including Airflow and the necessary Python packages, run:

```bash
pip install -r requirements.txt
```

Alternatively, Docker Compose will install dependencies in the Airflow container automatically when you bring the services up.

## Docker Commands

- To start the services (Airflow, PostgreSQL, etc.):

  ```bash
  docker-compose up
  ```

- To shut down the services:

  ```bash
  docker-compose down
  ```

- To rebuild the containers (after making changes to Dockerfiles or `docker-compose.yml`):

  ```bash
  docker-compose up --build
  ```

## Conclusion

This project demonstrates how to build a scalable, automated weather ETL pipeline using **Apache Airflow** for scheduling and **Docker** for deployment. With the ability to extract, transform, and load weather data into a PostgreSQL database, the project showcases essential data engineering practices in a real-world scenario.
