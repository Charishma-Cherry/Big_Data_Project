# """ 
# Solar Intensity Prediction Dashboard 
# ---------------------------------- 
# Data Description: 
# - Historical weather data from 2015-2024 for multiple cities 
# - Features include temperature, precipitation, and solar radiation measurements 
# Solar Viability Categorization: 
# - Low: Solar intensity < 3 kWh/m²/day 
# - Medium: Solar intensity between 3-6 kWh/m²/day 
# - High: Solar intensity > 6 kWh/m²/day 
# Model Details: 
# - Algorithm: Random Forest Classifier 
# - Features used: Month, Year, City (encoded) 
# - Target: Solar intensity category (low/medium/high) 
# - Training: 80% data for training, 20% for testing 
# - Prediction target: Year 2025 
# Key Metrics Used: 
# 1. ALLSKY_SFC_SW_DWN: Total sunlight energy reaching ground (includes cloudy conditions) 
# 2. CLRSKY_SFC_SW_DWN: Maximum potential sunlight under clear skies 
# 3. Temperature metrics (TAVG, TMAX, TMIN) 
# 4. Precipitation (PRCP) 
# Visualizations: 
# 1. Solar Energy Analysis: Compares actual vs clear sky solar potential 
# 2. Temperature Analysis: Shows temperature distribution patterns 
# 3. Solar Radiation Components: Analyzes direct vs diffuse radiation 
# Additional Features: 
# - City-specific analysis 
# - Monthly predictions 
# - Rainfall impact assessment 
# - Temperature correlation with solar intensity 
# """ 

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt
import base64

# Function to add background image to the Streamlit app
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/jpeg;base64,{encoded_string.decode()});
                background-size: cover;
            }}
            .big-font {{
                font-size: 24px !important;
                font-weight: bold;
                color: white;
                text-shadow: 2px 2px 4px #000000;
                background-color: rgba(0,0,0,0.8);
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 0.5rem;
            }}
            .standard-font {{
                color: white;
                text-shadow: 1px 1px 2px #000000;
                background-color: rgba(0,0,0,0.8);
                padding: 5px;
                border-radius: 3px;
                margin: 0;
                margin-top: 0.5rem;
                margin-bottom: -0.5rem;
            }}
            div[data-baseweb="select"] {{
                margin-top: -1rem;
            }}
            .stSelectbox {{
                margin-top: -1rem;
            }}
            .stMarkdown {{
                margin-bottom: -1rem;
            }}
            </style>
            """, unsafe_allow_html=True)

# Add background image to the app
add_bg_from_local('solar.jpg')

# Load and preprocess data with caching for performance optimization
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('weather_data.csv') # Attempt to load the CSV file
    except FileNotFoundError:
        st.error("Error: The data file was not found.")
        return pd.DataFrame() # Return an empty DataFrame to avoid further errors
    except pd.errors.EmptyDataError:
        st.error("Error: The data file is empty.")
        return pd.DataFrame()
    
    df['date'] = pd.to_datetime(df['date']) # Convert date column to datetime format
    df['month'] = df['date'].dt.month # Extract month from date
    df['year'] = df['date'].dt.year # Extract year from date
    return df

df = load_data() # Call the load_data function to get the DataFrame

# Feature engineering to categorize solar intensity based on measurements
def engineer_features(df):
    df['solar_intensity'] = pd.cut(df['allsky_sfc_sw_dwn'], bins=[0, 3, 6, float('inf')], labels=['Low', 'Medium', 'High'])
    return df

df = engineer_features(df) # Apply feature engineering

# Model training function using Random Forest Classifier
def train_model(df):
    df['city_encoded'] = LabelEncoder().fit_transform(df['city_x']) # Encode city names into numerical values
    X = df[['month', 'year', 'city_encoded']] # Features for the model
    y = df['solar_intensity'] # Target variable for prediction
    
    le = LabelEncoder() # Initialize label encoder for target variable
    y = le.fit_transform(y) # Encode target variable into numerical values
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) # Split data into training and testing sets
    
    model = RandomForestClassifier(n_estimators=100, random_state=42) # Initialize Random Forest model with specified parameters
    model.fit(X_train, y_train) # Train the model on training data
    
    return model, le # Return trained model and label encoder

model, le = train_model(df) # Train the model and get the outputs

# Streamlit UI setup for displaying the dashboard title
st.markdown('<h1 class="big-font">🌞 Solar Intensity Prediction Dashboard</h1>', unsafe_allow_html=True)

# Description of the Model and Categories displayed on the dashboard
st.markdown("""
<div class='standard-font'>
<b>Solar Intensity Categories:</b> <br>
• Low: < 3 kWh/m²/day <br>
• Medium: 3-6 kWh/m²/day <br>
• High: > 6 kWh/m²/day <br>
<i>Predictions are based on historical data from 2015-2024</i>
</div>
""", unsafe_allow_html=True)

# User Input Section for selecting city, month and maximum rainfall allowed
col1, col2, col3 = st.columns(3)
with col1:
    city_names = df['city_x'].unique() # Get unique city names from DataFrame
    st.markdown('<p class="standard-font">🏙️ Select City</p>', unsafe_allow_html=True)
    city = st.selectbox('', city_names) # Dropdown for selecting city

with col2:
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] # List of month names for display
    st.markdown('<p class="standard-font">📅 Select Month</p>', unsafe_allow_html=True)
    month_index = st.selectbox('', range(1, 13), format_func=lambda x: month_names[x-1]) # Dropdown for selecting month

with col3:
    rainfall_options = [0.0, 0.1, 0.2, 0.5, 1.0, 2.0] # Options for maximum rainfall selection
    st.markdown('<p class="standard-font">🌧️ Select Maximum Rainfall</p>', unsafe_allow_html=True)
    selected_rainfall = st.selectbox('', rainfall_options) # Dropdown for selecting maximum rainfall

filtered_data = df[(df['city_x'] == city) & (df['prcp'] <= selected_rainfall)] # Filter data based on user selections

if selected_rainfall > filtered_data['prcp'].max():
    st.warning("Selected rainfall exceeds available data. Please choose a lower value.") 

# Prediction and Historical Data function to predict solar intensity based on user input
def predict_solar_intensity(model, le, city, month):
    city_encoded = LabelEncoder().fit(df['city_x']).transform([city])[0] # Encode selected city name into numerical value
    prediction = model.predict([[month, 2025, city_encoded]]) # Make prediction using the trained model for year 2025
    return le.inverse_transform(prediction)[0] # Decode numerical prediction back to original category

prediction = predict_solar_intensity(model, le, city, month_index) # Get prediction based on user input

# Display Predictions with Explanation in the dashboard
st.markdown('<p class="big-font">🔮 Predicted Solar Intensity for 2025</p>', unsafe_allow_html=True)
st.markdown(f"""
<div class='standard-font'>
<h2 style='color: #FF5733;'>{prediction}</h2>
<i>This prediction is for {month_names[month_index-1]} 2025 based on historical patterns</i>
</div>
""", unsafe_allow_html=True)

# Historical Data Analysis to calculate average solar intensity based on filtered data
historical_avg = filtered_data[filtered_data['month'] == month_index]['allsky_sfc_sw_dwn'].mean() # Calculate historical average solar intensity for selected month

st.markdown(f"""
<div class='standard-font'>
<b>Historical Average Solar Intensity:</b> {historical_avg:.2f} kWh/m²/day <br>
<i>Based on data from 2015-2024 for {city} in {month_names[month_index-1]}</i>
</div>
""", unsafe_allow_html=True)

# Temperature Analysis with Explanation to show temperature metrics in the dashboard
average_temperature = filtered_data[filtered_data['month'] == month_index]['tavg'].mean() # Calculate average temperature for selected month
max_temperature = filtered_data[filtered_data['month'] == month_index]['tmax'].mean() # Calculate maximum temperature for selected month
min_temperature = filtered_data[filtered_data['month'] == month_index]['tmin'].mean() # Calculate minimum temperature for selected month

st.markdown(f"""
<div class='standard-font'>
<b>Temperature Profile:</b> <br>
• Average: {average_temperature:.2f}°F <br>
• Maximum: {max_temperature:.2f}°F <br>
• Minimum: {min_temperature:.2f}°F <br>
<i>Temperature variations can affect solar panel efficiency</i>
</div>
""", unsafe_allow_html=True)

# Temperature Visualization using Matplotlib and Seaborn to display temperature metrics graphically
plt.figure(figsize=(12, 6))
plt.style.use('dark_background') # Set dark background style for better visibility of plots

temperature_metrics = [average_temperature, max_temperature, min_temperature] # Prepare temperature metrics for plotting
temperature_labels = ['Average', 'Maximum', 'Minimum'] 

sns.barplot(x=temperature_labels, y=temperature_metrics, palette='YlOrRd') # Create bar plot of temperature metrics
plt.title(f'Temperature Distribution in {city} - {month_names[month_index-1]}', fontsize=16)
plt.ylabel('Temperature (°F)', fontsize=14)
plt.grid(True, alpha=0.3) # Add grid lines to plot for better readability

st.pyplot(plt) # Display the plot in Streamlit app

# Solar Radiation Analysis to calculate monthly radiation averages and visualize them in the dashboard
monthly_radiation = filtered_data.groupby('month').agg({
    'allsky_sfc_sw_dwn': 'mean',
    'allsky_sfc_sw_diff': 'mean'
}).reset_index() 

monthly_radiation['direct_radiation'] = monthly_radiation['allsky_sfc_sw_dwn'] - monthly_radiation['allsky_sfc_sw_diff'] 

st.markdown("""
<div class='standard-font'>
<b>Solar Radiation Components:</b> <br>
• Direct Radiation: Primary solar energy reaching the surface <br>
• Diffuse Radiation: Scattered sunlight from clouds and atmosphere </div>
""", unsafe_allow_html=True)

plt.figure(figsize=(12, 6)) 

plt.stackplot(monthly_radiation['month'], [monthly_radiation['direct_radiation'], monthly_radiation['allsky_sfc_sw_diff']], labels=['Direct Radiation', 'Diffuse Radiation']) 

plt.title(f'Solar Radiation Components in {city}', fontsize=16)
plt.xlabel('Month')
plt.ylabel('Solar Radiation (kWh/m²/day)')
plt.xticks(range(1,13), month_names, rotation=45) # Set x-ticks to show month names rotated for clarity

plt.legend() # Add legend to differentiate between direct and diffuse radiation components

plt.grid(True, alpha=0.3)

st.pyplot(plt) 

# Rainfall impact analysis section with visualization of its effect on solar intensity displayed in the dashboard.
st.markdown('<p class="big-font">🌧️ Rainfall Impact on Solar Intensity</p>', unsafe_allow_html=True)

plt.figure(figsize=(12, 6)) 

plt.style.use('dark_background') 

rainfall_bins = [0, 0.1, 0.2, 0.5, 1.0, 2.0] # Define bins for categorizing rainfall amounts into ranges.
rainfall_labels = ['0-0.1', '0.1-0.2', '0.2-0.5', '0.5-1.0', '1.0-2.0'] 

filtered_data['rainfall_category'] = pd.cut(filtered_data['prcp'], bins=rainfall_bins,
                                             labels=rainfall_labels) 

rainfall_impact = filtered_data.groupby('rainfall_category')['allsky_sfc_sw_dwn'].mean() 

sns.barplot(x=rainfall_impact.index,
            y=rainfall_impact.values,
            palette='YlOrRd_r') 

plt.title(f'Impact of Rainfall on Solar Intensity in {city}', fontsize=16)
plt.xlabel('Rainfall Range (inches)', fontsize=14)
plt.ylabel('Average Solar Intensity (kWh/m²/day)', fontsize=14)
plt.grid(True,
         alpha=0.3)

for i,v in enumerate(rainfall_impact.values): 
    plt.text(i,v,f'{v:.2f}',ha='center',va='bottom') 

st.pyplot(plt)

st.markdown(f"""
<div class='standard-font'>
<b>Rainfall Impact Analysis:</b> <br>
• Higher rainfall generally leads to lower solar intensity <br>
• Minimal rainfall (0-0.1 inches) shows highest solar potential <br>
• Significant decrease in solar intensity with rainfall > 0.5 inches </div>
""", unsafe_allow_html=True)
