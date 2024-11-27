from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, avg, stddev, weekofyear, to_date, rand, to_timestamp
from pyspark.sql.types import StructType, StringType, FloatType, StructField
from pyspark.sql.window import Window

CASSANDRA_HOST = "localhost"  # Replace with the Cassandra host if not localhost
CASSANDRA_KEYSPACE = "weather_keyspace"
CASSANDRA_TABLE = "weather_data"

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
    .withColumn("DATE", to_date(col("DATE"), "yyyy-MM-dd")) \
    .select(
        "STATION", "NAME", "DATE", "TAVG", "TMAX", "TMIN", "PRCP", "SNOW",
        "CITY_x", "ALLSKY_SFC_SW_DWN", "CLRSKY_SFC_SW_DWN", "ALLSKY_SFC_SW_DIFF"
    )

processed_df = processed_df \
    .withColumnRenamed("STATION", "station") \
    .withColumnRenamed("NAME", "name") \
    .withColumnRenamed("DATE", "date") \
    .withColumnRenamed("TAVG", "tavg") \
    .withColumnRenamed("TMAX", "tmax") \
    .withColumnRenamed("TMIN", "tmin") \
    .withColumnRenamed("PRCP", "prcp") \
    .withColumnRenamed("SNOW", "snow") \
    .withColumnRenamed("CITY_x", "city_x") \
    .withColumnRenamed("ALLSKY_SFC_SW_DWN", "allsky_sfc_sw_dwn") \
    .withColumnRenamed("CLRSKY_SFC_SW_DWN", "clrsky_sfc_sw_dwn") \
    .withColumnRenamed("ALLSKY_SFC_SW_DIFF", "allsky_sfc_sw_diff")

processed_df = processed_df.fillna({'prcp': 0})  # Replace nulls with 0 for precipitation
processed_df = processed_df.fillna({'snow': 0})  # Replace nulls with 0 for snow

processed_df.printSchema()

# Time-based Aggregations (Daily, Weekly)
def time_based_aggregations(df):
    # Daily Aggregation
    daily_aggregated_df = df.groupBy("CITY_x", "DATE") \
        .agg(
            avg("TAVG").alias("avg_temp"),
            avg("PRCP").alias("avg_precipitation"),
            avg("SNOW").alias("avg_snowfall")
        )

    # Weekly Aggregation (Requires timestamp for windowing)
    weekly_aggregated_df = df.withColumn("timestamp", to_timestamp(col("DATE"), "yyyy-MM-dd")) \
        .withColumn("week", weekofyear("timestamp")) \
        .groupBy("CITY_x", "week") \
        .agg(
            avg("TAVG").alias("avg_temp"),
            avg("PRCP").alias("avg_precipitation"),
            avg("SNOW").alias("avg_snowfall")
        )
    
    # Drop the temporary timestamp column after use
    weekly_aggregated_df = weekly_aggregated_df.drop("timestamp")
    
    return daily_aggregated_df, weekly_aggregated_df

# Reservoir Sampling (Distributed approach)
def reservoir_sampling(batch_df, sample_size=100):
    # Create a column with a random number to help with the sampling
    sampled_df = batch_df.withColumn("rand", rand())
    
    # Order by the random column and take the top N samples
    sampled_df = sampled_df.orderBy("rand").limit(sample_size)
    
    return sampled_df

# Write results to console and store (without collect())
def write_to_console_and_store(df, epoch_id):
    print(f"Micro-batch {epoch_id}:")  # Print the micro-batch number
    df.show(5, truncate=False)  # Display the first few rows for monitoring

    # Apply time-based aggregations (daily and weekly)
    daily_aggregated_df, weekly_aggregated_df = time_based_aggregations(df)
    
    # Show daily aggregation results
    print("Daily Aggregated Data:")
    daily_aggregated_df.show(truncate=False)
    
    # Show weekly aggregation results
    print("Weekly Aggregated Data:")
    weekly_aggregated_df.show(truncate=False)

    # Apply Reservoir Sampling on the batch data (distributed)
    sampled_df = reservoir_sampling(df, sample_size=100)
    print("Reservoir Sampled Data:")
    sampled_df.show(truncate=False)


# Write to Cassandra
def write_to_cassandra(batch_df, batch_id):
    batch_df.write \
        .format("org.apache.spark.sql.cassandra") \
        .mode("append") \
        .options(table=CASSANDRA_TABLE, keyspace=CASSANDRA_KEYSPACE) \
        .save()
    
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
