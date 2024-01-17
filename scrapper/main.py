import requests
import csv
import schedule
import time
from datetime import datetime, timedelta

# Configuration
api_url = "https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/etat-du-trafic-en-temps-reel@rennes-metropole/records"
end_time = datetime.now() + timedelta(days=1)  # Durée d'exécution de 24 heures

def fetch_and_save_traffic_data():
    if datetime.now() >= end_time:
        return schedule.CancelJob

    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json().get('results', [])
        if data:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"traffic_data_{timestamp}.csv"
            with open(filename, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            print(f"Data saved in {filename} at {datetime.now()}")
        else:
            print(f"No data to save at {datetime.now()}")
    else:
        print(f"Failed to fetch data at {datetime.now()}: {response.status_code}")

# Planifier l'exécution toutes les 5 minutes
schedule.every(3).minutes.do(fetch_and_save_traffic_data)

# Exécuter le script pour la durée spécifiée
while datetime.now() < end_time:
    schedule.run_pending()
    time.sleep(1)

print("Data collection completed.")
