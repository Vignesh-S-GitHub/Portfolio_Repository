from kafka import KafkaProducer
import time, os
import csv
import json

def kafka_producer():
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize data to JSON
    )
    topic = 'transactions'

    with open(os.path.join(os.getcwd(), 'data_Pipeline', 'transactions.csv'), 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            producer.send(topic, row)  # Send row as JSON
            print(f"Sent: {row}")  # Log the message sent
            time.sleep(10)  # Simulate real-time streaming
    producer.close()

if __name__ == "__main__":
    kafka_producer()
