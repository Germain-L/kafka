import csv
import requests
from kafka import KafkaProducer
import logging
import time
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Kafka configuration
kafka_broker = 'localhost:9093'
producer = KafkaProducer(bootstrap_servers=[kafka_broker],
                         value_serializer=lambda v: str(v).encode('utf-8'))

# Flask server configuration
base_url = "http://localhost:5000/data"

def generate_datetime_sequence(start_date, end_date, delta):
    current = start_date
    while current <= end_date:
        yield current
        current += delta

def fetch_traffic_data(date_str, hour_str, minute_str):
    url = f"{base_url}/{date_str}/{hour_str}/{minute_str}"
    response = requests.get(url)
    if response.status_code == 200 and response.text.strip():
        logging.info("Data fetched successfully")
        try:
            data = list(csv.DictReader(response.text.splitlines()))
            return data
        except csv.Error as e:
            logging.error(f"CSV format error: {e}")
            return None
    else:
        logging.error(f"No data available or bad response for {date_str} {hour_str}:{minute_str}")
        return None

def produce_messages(data):
    for record in data:
        key_bytes = str(record.get('id_rva_troncon_fcd_v1_1', '')).encode('utf-8')

        # Send the record to different topics
        producer.send('vitesse_moyenne', key=key_bytes, value={'averagevehiclespeed': record.get('averagevehiclespeed')})
        producer.send('temps_trajet', key=key_bytes, value={'traveltime': record.get('traveltime')})
        producer.send('fiabilite_temps_trajet', key=key_bytes, value={'traveltimereliability': record.get('traveltimereliability')})
        producer.send('statut_trafic', key=key_bytes, value={'trafficstatus': record.get('trafficstatus')})
        producer.send('mesure_sonde_vehicule', key=key_bytes, value={'vehicleprobemeasurement': record.get('vehicleprobemeasurement')})
        producer.send('informations_geographiques', key=key_bytes, value={'geo_point_2d': record.get('geo_point_2d'), 'geo_shape': record.get('geo_shape')})
        producer.send('hierarchie_route', key=key_bytes, value={'hierarchie': record.get('hierarchie'), 'hierarchie_dv': record.get('hierarchie_dv'), 'denomination': record.get('denomination')})

        logging.info("Messages produced for record with key: {}".format(record.get('id_rva_troncon_fcd_v1_1')))

def main():
    start_date = datetime(2024, 1, 17)  # Start date
    end_date = datetime(2024, 1, 18)    # End date
    time_delta = timedelta(minutes=1)   # Interval of 1 minute

    for current_datetime in generate_datetime_sequence(start_date, end_date, time_delta):
        date_str = current_datetime.strftime("%Y%m%d")
        hour_str = current_datetime.strftime("%H")
        minute_str = current_datetime.strftime("%M")

        data = fetch_traffic_data(date_str, hour_str, minute_str)
        if data:
            produce_messages(data)

        time.sleep(1)

if __name__ == "__main__":
    main()
