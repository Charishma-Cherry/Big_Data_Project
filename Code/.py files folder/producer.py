from kafka import KafkaProducer
import csv
import json
import time

# Kafka Configuration
TOPIC_NAME = 'weather_solar_data'
BROKER = 'localhost:9092'

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize as JSON
)

# Stream Data
with open('./data/merged_cleaned_data.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        producer.send(TOPIC_NAME, value=row)
        # print(f"Sent: {row}")
        time.sleep(1)  # Adjust for simulation speed