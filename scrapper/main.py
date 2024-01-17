import requests
import csv
import schedule
import time
import logging
from datetime import datetime, timedelta

# Configuration
api_url = "https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/etat-du-trafic-en-temps-reel@rennes-metropole/records"
end_time = datetime.now() + timedelta(days=1)  # Durée d'exécution de 24 heures

# Setup logging
logging.basicConfig(filename='traffic_data_log.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def fetch_and_save_traffic_data():
    if datetime.now() >= end_time:
        logging.info("Scheduled job completed.")
        return schedule.CancelJob

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code

        data = response.json().get('results', [])
        if data:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"traffic_data_{timestamp}.csv"
            with open(filename, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            logging.info(f"Data saved in {filename}")
        else:
            logging.warning("No data to save.")
    except requests.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")

# Execute immediately and then schedule every 10 minutes
fetch_and_save_traffic_data()
schedule.every(10).minutes.do(fetch_and_save_traffic_data)

# Run the script for the specified duration
while datetime.now() < end_time:
    schedule.run_pending()
    time.sleep(1)

logging.info("Data collection completed.")
