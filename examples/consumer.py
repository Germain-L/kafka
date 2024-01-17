from kafka import KafkaConsumer
import json

mem = { c : 0 for c in 'ABCDEF'}
consumer = KafkaConsumer('triplets', group_id='triplets-v', bootstrap_servers='localhost:9093')
for msg in consumer:
    numbers = json.loads(msg.value)
    mem[msg.key.decode()] = numbers["val1"]
    print(mem)