import time, json, random
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9093')
while True:
    key = random.choice("ABCDEF")
    msg = {
        'val0' : random.randint(-50, 50),
        'val1' : random.randint(-50, 50),
        'val2' : random.randint(-50, 50),
    }

    print(f'Envoi de : {msg}')
    res = producer.send("triplets", json.dumps(msg).encode(), key.encode())