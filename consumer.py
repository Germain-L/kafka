from kafka import KafkaConsumer
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Kafka configuration
kafka_broker = 'localhost:9093'
topics = ['vitesse_moyenne', 'temps_trajet', 'fiabilite_temps_trajet', 'statut_trafic', 'mesure_sonde_vehicule', 'informations_geographiques', 'hierarchie_route']

# Create a Kafka consumer
consumer = KafkaConsumer(
    *topics,
    bootstrap_servers=[kafka_broker],
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    value_deserializer=lambda m: m.decode('utf-8')  # Updated to handle plain text
)

def main():
    try:
        for message in consumer:
            # Display the key and value
            key = message.key.decode('utf-8') if message.key else None
            value = message.value
            logging.info(f"Received message: Key: {key}, Value: {value}")

            # Manually commit the offset
            consumer.commit()
    except KeyboardInterrupt:
        logging.info("Consumer stopped manually.")
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
