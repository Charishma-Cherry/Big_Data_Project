from cassandra.cluster import Cluster
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib
import math

# Connect to Cassandra
cluster = Cluster(['127.0.0.1'])  # Replace if needed
session = cluster.connect()

# Set keyspace
session.set_keyspace("weather_keyspace")  # Replace with your keyspace name

# Fetch data
query = "SELECT city_x, date, allsky_sfc_sw_diff, allsky_sfc_sw_dwn, clrsky_sfc_sw_dwn, name, prcp, snow, station, tavg, tmax, tmin FROM weather_data"
rows = session.execute(query)
data = pd.DataFrame(rows, columns=['city_x', 'date', 'allsky_sfc_sw_diff', 'allsky_sfc_sw_dwn', 
                                   'clrsky_sfc_sw_dwn', 'name', 'prcp', 'snow', 'station', 'tavg', 'tmax', 'tmin'])

# Preprocess data
data['city_x'] = data['city_x'].astype('category').cat.codes
#data['date'] = pd.to_datetime(data['date'])
data['date'] = pd.to_datetime(data['date'].apply(lambda x: str(x)))
data['year'] = data['date'].dt.year
data['month'] = data['date'].dt.month
data['day'] = data['date'].dt.day
data.drop(columns=['date', 'name', 'station'], inplace=True)
data.fillna(data.mean(), inplace=True)

# Features and target
X = data.drop(columns=['tavg', 'tmax', 'tmin'])
y = data['tavg']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = math.sqrt(mse)
print(f"Root Mean Squared Error: {rmse}")

# Save model
joblib.dump(model, "weather_model.pkl")
print("Model saved as 'weather_model.pkl'")

# Shutdown Cassandra connection
cluster.shutdown()

