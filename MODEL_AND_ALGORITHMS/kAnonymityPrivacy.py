from cassandra.cluster import Cluster
import pandas as pd
from datetime import datetime


# Step 1: Connect to Cassandra
cluster = Cluster(['127.0.0.1'])  # Replace with your Cassandra host IP
session = cluster.connect('weather_keyspace')  # Replace 'your_keyspace' with your keyspace

# Step 2: Fetch data from the Cassandra table
query = """
SELECT city_x, date, tavg, tmax, tmin, prcp, snow
FROM weather_data
"""
rows = session.execute(query)

# Step 3: Convert data to a Pandas DataFrame
columns = ['city_x', 'date', 'tavg', 'tmax', 'tmin', 'prcp', 'snow']
data = pd.DataFrame(rows, columns=columns)

# Close the Cassandra connection
cluster.shutdown()

# Step 4: Generalize 'date' to mm-yyyy format
#data['date'] = pd.to_datetime(data['date']).dt.strftime('%m-%Y')
data['date'] = data['date'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d'))
data['date'] = data['date'].dt.strftime('%m-%Y')
#print(data)
print(data.info())

# Step 5: Group by 'city_x' and 'date' and aggregate
grouped = data.groupby(['city_x', 'date'])
aggregated_data = grouped.agg({
    'tavg': 'mean',  # Average temperature
    'tmax': 'max',   # Maximum temperature
    'tmin': 'min',   # Minimum temperature
    'prcp': 'count', # Count precipitation records
    'snow': 'count'  # Count snowfall records
}).rename(columns={'prcp': 'prcp_count', 'snow': 'snow_count'})

# Reset the index for better readability
aggregated_data.reset_index(inplace=True)

# Output the aggregated data
print("Aggregated Dataset:")
print(aggregated_data)

# Step 6: Check K-Anonymity
equivalence_class_sizes = grouped.size()
min_size = equivalence_class_sizes.min()
desired_k = 4  # Replace with your desired K value

print(f"\nEquivalence Class Sizes:\n{equivalence_class_sizes}")
print(f"\nMinimum Equivalence Class Size: {min_size}")

if min_size >= desired_k:
    print(f"The dataset satisfies {desired_k}-Anonymity.")
else:
    print(f"The dataset does NOT satisfy {desired_k}-Anonymity.")
    print("Classes failing K-Anonymity:")
    print(equivalence_class_sizes[equivalence_class_sizes < desired_k])

