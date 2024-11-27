from cassandra.cluster import Cluster
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.random_projection import SparseRandomProjection
from sklearn.neighbors import NearestNeighbors

# Step 1: Connect to Cassandra
cluster = Cluster(['127.0.0.1'])  # Replace with your Cassandra host
session = cluster.connect()

# Set the keyspace
keyspace = 'weather_keyspace'  # Replace with your keyspace name
session.set_keyspace(keyspace)

# Fetch data
query = """
SELECT STATION, NAME, DATE, TAVG, TMAX, TMIN, PRCP, SNOW, CITY_x, 
       ALLSKY_SFC_SW_DWN, CLRSKY_SFC_SW_DWN, ALLSKY_SFC_SW_DIFF 
FROM weather_data
"""
rows = session.execute(query)

# Step 2: Convert to Pandas DataFrame
columns = ['STATION', 'NAME', 'DATE', 'TAVG', 'TMAX', 'TMIN', 'PRCP', 'SNOW', 
           'CITY_x', 'ALLSKY_SFC_SW_DWN', 'CLRSKY_SFC_SW_DWN', 'ALLSKY_SFC_SW_DIFF']
data = pd.DataFrame(rows, columns=columns)

# Close the Cassandra connection
cluster.shutdown()

# Step 3: Preprocess Data
features = ['TAVG', 'TMAX', 'TMIN', 'PRCP', 'ALLSKY_SFC_SW_DWN', 'CLRSKY_SFC_SW_DWN', 'ALLSKY_SFC_SW_DIFF']
data_features = data[features]

# Fill missing values and standardize
data_features = data_features.fillna(data_features.mean())
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data_features)

# Step 4: Apply Sparse Random Projection for LSH
projector = SparseRandomProjection(n_components=5, random_state=42)
data_projected = projector.fit_transform(data_scaled)

# Step 5: Nearest Neighbors Search
n_neighbors = 5
nbrs = NearestNeighbors(n_neighbors=n_neighbors, metric="cosine").fit(data_projected)

# Query the dataset
query_index = 0  # Replace with your desired record index
distances, indices = nbrs.kneighbors([data_projected[query_index]])

# Print Results
print(f"Query Record: {data.iloc[query_index].to_dict()}")
print("\nMost Similar Records:")
for idx, distance in zip(indices[0], distances[0]):
    print(f"Index: {idx}, Distance: {distance:.4f}, Record: {data.iloc[idx].to_dict()}")

