from kafka import KafkaConsumer
from pyspark.sql import SparkSession
import json
from config.config import KAFKA_SERVER, TOPIC_NAME

# Initialize PySpark session
spark = SparkSession.builder \
    .appName("KafkaToSpark") \
    .getOrCreate()

# Create Kafka consumer instance
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=[KAFKA_SERVER],
    group_id='weather_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Create an empty list to hold data for PySpark DataFrame
data_list = []

def process_weather_data(data_list):
    """
    Process the incoming weather data by converting it to a DataFrame, applying transformations, and returning the processed DataFrame.
    """
    # Convert list of data into PySpark DataFrame
    df = spark.createDataFrame(data_list, ["STATION", "NAME", "DATE", "TAVG", "TMAX", "TMIN", "PRCP", "CITY"])

    # Perform transformations with PySpark (e.g., filter rows where TAVG > 50)
    df_filtered = df.filter(df.TAVG > 50)  # Filter rows with TAVG > 50

    # You can apply additional transformations here if necessary
    # e.g., aggregating data, adding columns, etc.

    # Return the filtered DataFrame for further processing
    return df_filtered

# Consume messages from Kafka and send to PySpark
for message in consumer:
    data = message.value  # Get the data sent by the producer
    
    # Extract columns
    station = data.get("STATION", "Unknown")
    name = data.get("NAME", "Unknown")
    date = data.get("DATE", "Unknown")
    tavg = data.get("TAVG", "Unknown")
    tmax = data.get("TMAX", "Unknown")
    tmin = data.get("TMIN", "Unknown")
    prcp = data.get("PRCP", "Unknown")
    city = data.get("CITY", "Unknown")
    
    # Add the data to the list
    data_list.append((station, name, date, tavg, tmax, tmin, prcp, city))

    # Once data has been collected, process it with PySpark
    if len(data_list) >= 10:  # Process every 10 messages (can adjust)
        processed_df = process_weather_data(data_list)

        # Return the processed DataFrame to the next step or team member
        processed_df.show()

        # Clear the list for the next batch of data
        data_list.clear()
