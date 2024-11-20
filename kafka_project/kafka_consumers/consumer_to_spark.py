from kafka import KafkaConsumer
import json

# Kafka Configuration
TOPIC_NAME = 'weather_solar_data'
BROKER = 'localhost:9092'

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=BROKER,
    value_deserializer=lambda v: v.decode('utf-8'),  # Temporarily treat as plain text
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='weather_consumer_group'
)

print("Starting Consumer...")
try:
    for message in consumer:
        raw_message = message.value  # Raw message from Kafka
        print(f"Raw Message: {raw_message}")  # Debug: Print the raw message
        try:
            # Attempt JSON deserialization
            deserialized_message = json.loads(raw_message)
            print(f"Deserialized Message: {deserialized_message}")
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e} - Raw Message: {raw_message}")
except KeyboardInterrupt:
    print("\nConsumer interrupted by user")
finally:
    print("Closing Consumer...")