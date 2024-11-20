from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_timestamp
from pyspark.sql.types import StructType, StringType, FloatType, StructField

# Define the schema of the incoming JSON data
schema = StructType([
    StructField("STATION", StringType()),
    StructField("NAME", StringType()),
    StructField("DATE", StringType()),
    StructField("TAVG", StringType()),  
    StructField("TMAX", StringType()),
    StructField("TMIN", StringType()),
    StructField("PRCP", StringType()),
    StructField("SNOW", StringType()),
    StructField("CITY_x", StringType()),
    StructField("ALLSKY_SFC_SW_DWN", StringType()),
    StructField("CLRSKY_SFC_SW_DWN", StringType()),
    StructField("ALLSKY_SFC_SW_DIFF", StringType()),
    StructField("CITY_y", StringType())
])

# Initialize Spark Session with Kafka package
spark = SparkSession.builder \
    .appName("KafkaSparkStream") \
    .master("local[*]") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3") \
    .getOrCreate()

# Set log level to reduce verbosity
spark.sparkContext.setLogLevel("WARN")

# Read messages from Kafka
kafka_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "weather_solar_data") \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .load()

# Deserialize and parse JSON data
parsed_df = kafka_df \
    .select(from_json(col("value").cast("string"), schema).alias("data")) \
    .select("data.*")

# Convert string fields to appropriate types
processed_df = parsed_df \
    .withColumn("TAVG", col("TAVG").cast(FloatType())) \
    .withColumn("TMAX", col("TMAX").cast(FloatType())) \
    .withColumn("TMIN", col("TMIN").cast(FloatType())) \
    .withColumn("PRCP", col("PRCP").cast(FloatType())) \
    .withColumn("SNOW", col("SNOW").cast(FloatType())) \
    .withColumn("ALLSKY_SFC_SW_DWN", col("ALLSKY_SFC_SW_DWN").cast(FloatType())) \
    .withColumn("CLRSKY_SFC_SW_DWN", col("CLRSKY_SFC_SW_DWN").cast(FloatType())) \
    .withColumn("ALLSKY_SFC_SW_DIFF", col("ALLSKY_SFC_SW_DIFF").cast(FloatType())) \
    .withColumn("TIMESTAMP", to_timestamp(col("DATE"), "yyyy-MM-dd")) \
    .select(
        "STATION", "NAME", "TIMESTAMP", "TAVG", "TMAX", "TMIN", "PRCP", "SNOW",
        "CITY_x", "ALLSKY_SFC_SW_DWN", "CLRSKY_SFC_SW_DWN", "ALLSKY_SFC_SW_DIFF"
    )

# Write to console and memory
def write_to_console_and_store(df, epoch_id):
    print(f"Micro-batch {epoch_id}:")  # Print the micro-batch number
    df.show(5, truncate=False)  # Display the first few rows for monitoring

# Start streaming and write each micro-batch to console
query = processed_df \
    .writeStream \
    .foreachBatch(write_to_console_and_store) \
    .outputMode("append") \
    .start()

# Keep the application running
try:
    query.awaitTermination()
except KeyboardInterrupt:
    query.stop()
finally:
    spark.stop()
