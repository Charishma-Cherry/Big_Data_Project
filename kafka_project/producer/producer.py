from kafka import KafkaProducer
import pandas as pd
import json
from config.config import KAFKA_SERVER, TOPIC_NAME

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Load the merged data CSV
merged_data = pd.read_csv("data/merged_data.csv")  

# Send each row of the merged data to Kafka
for _, row in merged_data.iterrows():
    message = {
        'STATION': row['STATION'],
        'NAME': row['NAME'],
        'DATE': row['DATE'],
        'TAVG': row['TAVG'],
        'TMAX': row['TMAX'],
        'TMIN': row['TMIN'],
        'PRCP': row['PRCP'],
        'CITY': row['CITY']
    }
    # Send message to Kafka topic
    producer.send(TOPIC_NAME, value=message)

# Close producer
producer.close()
