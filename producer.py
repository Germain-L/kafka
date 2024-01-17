import json
import time
import requests
from kafka import KafkaProducer
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Kafka configuration
kafka_broker = 'localhost:9093'
producer = KafkaProducer(bootstrap_servers=[kafka_broker],
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# API endpoint
api_url = "https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/etat-du-trafic-en-temps-reel@rennes-metropole/records"

def fetch_traffic_data():
    response = requests.get(api_url)
    if response.status_code == 200:
        logging.info("Data fetched successfully")
        return response.json()
    else:
        logging.error(f"Failed to fetch data: {response.status_code}")
        return None

def produce_messages(data):
    for record in data.get('results', []):
        predefined_location_reference = record.get('predefinedlocationreference')
        if predefined_location_reference:
            key_bytes = predefined_location_reference.encode('utf-8')  # Encoding the key as bytes
            producer.send('vitesse_moyenne', key=key_bytes, value=record)
            producer.send('temps_trajet', key=key_bytes, value=record)
            producer.send('fiabilite_temps_trajet', key=key_bytes, value=record)
            producer.send('statut_trafic', key=key_bytes, value=record)
            producer.send('mesure_sonde_vehicule', key=key_bytes, value=record)
            producer.send('informations_geographiques', key=key_bytes, value=record)
            producer.send('hierarchie_route', key=str(record.get('id_rva_troncon_fcd_v1_1')).encode('utf-8'), value=record)
        logging.info(f"Messages produced for location reference: {predefined_location_reference}")


def main():
    while True:
        logging.info("Fetching traffic data...")
        data = fetch_traffic_data()
        if data:
            produce_messages(data)
        time.sleep(60)  # Poll every 60 seconds. Adjust as needed.

if __name__ == "__main__":
    main()
