#!/usr/bin/env python
# coding: utf-8

# Step 1 : Load Weather and Solar data

# In[33]:


import pandas as pd

# Load weather data
weather_bakersfield = pd.read_csv("bakersfield_weather.csv")
weather_la = pd.read_csv("la_weather.csv")
weather_phoenix = pd.read_csv("phoenix_weather.csv")
weather_sf = pd.read_csv("sf_weather.csv")
weather_chicago = pd.read_csv("chicago_weather.csv")
weather_ny = pd.read_csv("ny_weather.csv")
weather_miami = pd.read_csv("miami_weather.csv")
weather_denver = pd.read_csv("denver_weather.csv")

# Load solar data
solar_bakersfield = pd.read_csv("solar_bakersfield.csv")
solar_la = pd.read_csv("solar_la.csv")
solar_phoenix = pd.read_csv("solar_phoenix.csv")
solar_miami = pd.read_csv("solar_miami.csv")
solar_ny = pd.read_csv("solar_ny.csv")
solar_sf = pd.read_csv("solar_sf.csv")
solar_denver = pd.read_csv("solar_denver.csv")
solar_chicago = pd.read_csv("solar_chicago.csv")


# Display a few rows of each dataset
print("Weather - Bakersfield:")
print(weather_bakersfield.head())
print("\nSolar - Bakersfield:")
print(solar_bakersfield.head())

#Different format weather city files
print("Weather - San Francisco:")
print(weather_sf.head())
print("\nSolar - San Francisco:")
print(solar_sf.head())


# Step 2: Clean and Standardize Weather and Solar Data

# In[34]:


# Check a few rows to identify date format inconsistencies
print(weather_bakersfield['DATE'].head(10))  # Check first 20 rows for Bakersfield

#Another format
print(weather_sf['date'].head(10))


# In[35]:


#Converting the new cities file to existing cities file format

# San Francisco
weather_sf["STATION"] = "KSFKO"
weather_sf["NAME"] = "San Francisco International Airport"
weather_sf = weather_sf.rename(
    columns={
        "date": "DATE",
        "tavg": "TAVG",
        "tmin": "TMIN",
        "tmax": "TMAX",
        "prcp": "PRCP",
        "snow": "SNOW",
        "wdir": "WDF2",
        "wspd": "AWND",
        "wpgt": "WSF2",
    }
)
sf_missing_columns = [
    "DAPR", "MDPR", "PGTM", "SNWD", "TOBS", "WDF5", "WESD", "WESF",
    "WSF5", "WT01", "WT02", "WT03", "WT05", "WT07", "WT08", "WT11"
]
for col in sf_missing_columns:
    weather_sf[col] = None
weather_sf = weather_sf[[
    "STATION", "NAME", "DATE", "AWND", "DAPR", "MDPR", "PGTM", "PRCP", "SNOW",
    "SNWD", "TAVG", "TMAX", "TMIN", "TOBS", "WDF2", "WDF5", "WESD", "WESF",
    "WSF2", "WSF5", "WT01", "WT02", "WT03", "WT05", "WT07", "WT08", "WT11"
]]

# New York
weather_ny["STATION"] = "KWO-35"
weather_ny["NAME"] = "New York Wall Street"
weather_ny = weather_ny.rename(
    columns={
        "date": "DATE",
        "tavg": "TAVG",
        "tmin": "TMIN",
        "tmax": "TMAX",
        "prcp": "PRCP",
        "snow": "SNOW",
        "wdir": "WDF2",
        "wspd": "AWND",
        "wpgt": "WSF2",
    }
)
for col in sf_missing_columns:
    weather_ny[col] = None
weather_ny = weather_ny[[
    "STATION", "NAME", "DATE", "AWND", "DAPR", "MDPR", "PGTM", "PRCP", "SNOW",
    "SNWD", "TAVG", "TMAX", "TMIN", "TOBS", "WDF2", "WDF5", "WESD", "WESF",
    "WSF2", "WSF5", "WT01", "WT02", "WT03", "WT05", "WT07", "WT08", "WT11"
]]

# Chicago
weather_chicago["STATION"] = "KMDW"
weather_chicago["NAME"] = "Chicago Midway International Airport"
weather_chicago = weather_chicago.rename(
    columns={
        "date": "DATE",
        "tavg": "TAVG",
        "tmin": "TMIN",
        "tmax": "TMAX",
        "prcp": "PRCP",
        "snow": "SNOW",
        "wdir": "WDF2",
        "wspd": "AWND",
        "wpgt": "WSF2",
    }
)
for col in sf_missing_columns:
    weather_chicago[col] = None
weather_chicago = weather_chicago[[
    "STATION", "NAME", "DATE", "AWND", "DAPR", "MDPR", "PGTM", "PRCP", "SNOW",
    "SNWD", "TAVG", "TMAX", "TMIN", "TOBS", "WDF2", "WDF5", "WESD", "WESF",
    "WSF2", "WSF5", "WT01", "WT02", "WT03", "WT05", "WT07", "WT08", "WT11"
]]

# Miami
weather_miami["STATION"] = "KMIA"
weather_miami["NAME"] = "Miami International Airport"
weather_miami = weather_miami.rename(
    columns={
        "date": "DATE",
        "tavg": "TAVG",
        "tmin": "TMIN",
        "tmax": "TMAX",
        "prcp": "PRCP",
        "snow": "SNOW",
        "wdir": "WDF2",
        "wspd": "AWND",
        "wpgt": "WSF2",
    }
)
for col in sf_missing_columns:
    weather_miami[col] = None
weather_miami = weather_miami[[
    "STATION", "NAME", "DATE", "AWND", "DAPR", "MDPR", "PGTM", "PRCP", "SNOW",
    "SNWD", "TAVG", "TMAX", "TMIN", "TOBS", "WDF2", "WDF5", "WESD", "WESF",
    "WSF2", "WSF5", "WT01", "WT02", "WT03", "WT05", "WT07", "WT08", "WT11"
]]

# Denver
weather_denver["STATION"] = "KDEN"
weather_denver["NAME"] = "Denver International Airport (DEN)"
weather_denver = weather_denver.rename(
    columns={
        "date": "DATE",
        "tavg": "TAVG",
        "tmin": "TMIN",
        "tmax": "TMAX",
        "prcp": "PRCP",
        "snow": "SNOW",
        "wdir": "WDF2",
        "wspd": "AWND",
        "wpgt": "WSF2",
    }
)
for col in sf_missing_columns:
    weather_denver[col] = None
weather_denver = weather_denver[[
    "STATION", "NAME", "DATE", "AWND", "DAPR", "MDPR", "PGTM", "PRCP", "SNOW",
    "SNWD", "TAVG", "TMAX", "TMIN", "TOBS", "WDF2", "WDF5", "WESD", "WESF",
    "WSF2", "WSF5", "WT01", "WT02", "WT03", "WT05", "WT07", "WT08", "WT11"
]]


# In[36]:


#Checking the file format

print("Weather - San Francisco:")
print(weather_sf.head())


# A. Converting Dates to a Uniform Format

# In[38]:


# Standardizing weather data dates with mixed or ambiguous formats
weather_bakersfield['DATE'] = pd.to_datetime(weather_bakersfield['DATE'], dayfirst=True, errors='coerce')
weather_la['DATE'] = pd.to_datetime(weather_la['DATE'], dayfirst=True, errors='coerce')
weather_phoenix['DATE'] = pd.to_datetime(weather_phoenix['DATE'], dayfirst=True, errors='coerce')


print(weather_bakersfield['DATE'].head())
print("Missing Dates")
print(weather_bakersfield['DATE'].isna().sum())  # Count missing dates

print("New cities format check of date field")
print(weather_sf['DATE'].head())
print(weather_sf['DATE'].isna().sum())  # Count missing dates


# In[39]:


# Check for invalid YEAR, MO, DY combinations
print(solar_bakersfield[['YEAR', 'MO', 'DY']].head())
print(solar_bakersfield[['YEAR', 'MO', 'DY']].isna().sum())  # Ensure no missing values


# In[40]:


# Creating DATE column in solar data
solar_bakersfield['DATE'] = pd.to_datetime(
    solar_bakersfield[['YEAR', 'MO', 'DY']].astype(str).agg('-'.join, axis=1)
)
solar_la['DATE'] = pd.to_datetime(
    solar_la[['YEAR', 'MO', 'DY']].astype(str).agg('-'.join, axis=1)
)
solar_phoenix['DATE'] = pd.to_datetime(
    solar_phoenix[['YEAR', 'MO', 'DY']].astype(str).agg('-'.join, axis=1)
)
solar_sf['DATE'] = pd.to_datetime(
    solar_sf[['YEAR', 'MO', 'DY']].astype(str).agg('-'.join, axis=1)
)
solar_ny['DATE'] = pd.to_datetime(
    solar_ny[['YEAR', 'MO', 'DY']].astype(str).agg('-'.join, axis=1)
)
solar_chicago['DATE'] = pd.to_datetime(
    solar_chicago[['YEAR', 'MO', 'DY']].astype(str).agg('-'.join, axis=1)
)
solar_denver['DATE'] = pd.to_datetime(
    solar_denver[['YEAR', 'MO', 'DY']].astype(str).agg('-'.join, axis=1)
)
solar_miami['DATE'] = pd.to_datetime(
    solar_miami[['YEAR', 'MO', 'DY']].astype(str).agg('-'.join, axis=1)
)


# In[41]:


# Drop YEAR, MO, DY columns after creating DATE
solar_bakersfield.drop(['YEAR', 'MO', 'DY'], axis=1, inplace=True)
solar_la.drop(['YEAR', 'MO', 'DY'], axis=1, inplace=True)
solar_phoenix.drop(['YEAR', 'MO', 'DY'], axis=1, inplace=True)
solar_sf.drop(['YEAR', 'MO', 'DY'], axis=1, inplace=True)
solar_ny.drop(['YEAR', 'MO', 'DY'], axis=1, inplace=True)
solar_chicago.drop(['YEAR', 'MO', 'DY'], axis=1, inplace=True)
solar_miami.drop(['YEAR', 'MO', 'DY'], axis=1, inplace=True)
solar_denver.drop(['YEAR', 'MO', 'DY'], axis=1, inplace=True)


# B. Filtering Relevant Columns

# In[42]:


# Select relevant weather columns
weather_columns = ['STATION', 'NAME', 'DATE', 'TAVG', 'TMAX', 'TMIN', 'PRCP' , 'SNOW']
weather_bakersfield = weather_bakersfield[weather_columns]
weather_la = weather_la[weather_columns]
weather_phoenix = weather_phoenix[weather_columns]
weather_sf = weather_sf[weather_columns]
weather_ny = weather_ny[weather_columns]
weather_chicago = weather_chicago[weather_columns]
weather_miami = weather_miami[weather_columns]
weather_denver = weather_denver[weather_columns]

# Select relevant solar columns
solar_columns = ['DATE', 'ALLSKY_SFC_SW_DWN', 'CLRSKY_SFC_SW_DWN', 'ALLSKY_SFC_SW_DIFF']
solar_bakersfield = solar_bakersfield[solar_columns]
solar_la = solar_la[solar_columns]
solar_phoenix = solar_phoenix[solar_columns]
solar_sf = solar_sf[solar_columns]
solar_ny = solar_ny[solar_columns]
solar_chicago = solar_chicago[solar_columns]
solar_miami = solar_miami[solar_columns]
solar_denver = solar_denver[solar_columns]


# C. Checking and Handling Missing Values

# In[43]:


# Check missing values

# Bakersfield
print("Weather - Bakersfield Missing Values:")
print(weather_bakersfield.isnull().sum())
print("\nSolar - Bakersfield Missing Values:")
print(solar_bakersfield.isnull().sum())


#LA
print("\nWeather - LA Missing Values:")
print(weather_la.isnull().sum())
print("\nSolar - LA Missing Values:")
print(solar_la.isnull().sum())

#Phoenix
print("\nWeather - Phoenix Missing Values:")
print(weather_phoenix.isnull().sum())
print("\nSolar - Phoenix Missing Values:")
print(solar_phoenix.isnull().sum())


# In[44]:


#SF
print("\nWeather - SF Missing Values:")
print(weather_sf.isnull().sum())
print("\nSolar - SF Missing Values:")
print(solar_sf.isnull().sum())


#NY
print("\nWeather - NY Missing Values:")
print(weather_ny.isnull().sum())
print("\nSolar - NY Missing Values:")
print(solar_ny.isnull().sum())

#Chicago
print("\nWeather - Chicago Missing Values:")
print(weather_chicago.isnull().sum())
print("\nSolar - Chicago Missing Values:")
print(solar_chicago.isnull().sum())


#Miami
print("\nWeather - Miami Missing Values:")
print(weather_miami.isnull().sum())
print("\nSolar - Miami Missing Values:")
print(solar_miami.isnull().sum())


#Denver
print("\nWeather - Denver Missing Values:")
print(weather_denver.isnull().sum())
print("\nSolar - Denver Missing Values:")
print(solar_denver.isnull().sum())


# In[45]:


# Droping rows with missing DATE and TAVG

#Bakersfield
weather_bakersfield.dropna(subset=['DATE', 'TAVG'], inplace=True)
solar_bakersfield.dropna(subset=['DATE', 'ALLSKY_SFC_SW_DWN'], inplace=True)

#LA
weather_la.dropna(subset=['DATE', 'TAVG'], inplace=True)
solar_la.dropna(subset=['DATE', 'ALLSKY_SFC_SW_DWN'], inplace=True)

#Phoenix
weather_phoenix.dropna(subset=['DATE', 'TAVG'], inplace=True)
solar_phoenix.dropna(subset=['DATE', 'ALLSKY_SFC_SW_DWN'], inplace=True)


#SF
weather_sf.dropna(subset=['DATE', 'TAVG'], inplace=True)
solar_sf.dropna(subset=['DATE', 'ALLSKY_SFC_SW_DWN'], inplace=True)


#NY
weather_ny.dropna(subset=['DATE', 'TAVG'], inplace=True)
solar_ny.dropna(subset=['DATE', 'ALLSKY_SFC_SW_DWN'], inplace=True)


#Chicago
weather_chicago.dropna(subset=['DATE', 'TAVG'], inplace=True)
solar_chicago.dropna(subset=['DATE', 'ALLSKY_SFC_SW_DWN'], inplace=True)


#Miami
weather_miami.dropna(subset=['DATE', 'TAVG'], inplace=True)
solar_miami.dropna(subset=['DATE', 'ALLSKY_SFC_SW_DWN'], inplace=True)


#Denver
weather_denver.dropna(subset=['DATE', 'TAVG'], inplace=True)
solar_denver.dropna(subset=['DATE', 'ALLSKY_SFC_SW_DWN'], inplace=True)


# D. Adding City Column for Context

# In[46]:


# Add CITY column to weather data
weather_bakersfield['CITY'] = 'Bakersfield'
weather_la['CITY'] = 'Los Angeles'
weather_phoenix['CITY'] = 'Phoenix'
weather_sf['CITY'] = "San Francisco"
weather_ny['CITY'] = "New York"
weather_chicago['CITY'] =  "Chicago"
weather_miami['CITY'] = "Miami"
weather_denver['CITY'] = "Denver"

# Add CITY column to solar data
solar_bakersfield['CITY'] = 'Bakersfield'
solar_la['CITY'] = 'Los Angeles'
solar_phoenix['CITY'] = 'Phoenix'
solar_sf['CITY'] = "San Francisco"
solar_ny['CITY'] = "New York"
solar_chicago['CITY'] =  "Chicago"
solar_miami['CITY'] = "Miami"
solar_denver['CITY'] = "Denver"


# In[47]:


# Checking after cleaning

print(weather_bakersfield.head())
print(solar_bakersfield.head())


# E. Cross Checking If any Duplicates based on Date are present

# In[49]:


# Find duplicates by DATE
duplicates = weather_bakersfield[weather_bakersfield.duplicated(subset=['DATE'], keep=False)]
print(duplicates.head())  # Inspect duplicate rows

#la
# Find rows where DATE is duplicated (ignoring other columns)
duplicates = weather_la[weather_la.duplicated(subset=['DATE'], keep=False)]
print(duplicates.head())  # Inspect duplicate rows


#Phoenix
duplicates = weather_phoenix[weather_phoenix.duplicated(subset=['DATE'], keep=False)]
print(duplicates.head())  # Inspect duplicate rows

#Sf
duplicates = weather_sf[weather_sf.duplicated(subset=['DATE'], keep=False)]
print(duplicates.head())  # Inspect duplicate rows

#Ny
duplicates = weather_ny[weather_ny.duplicated(subset=['DATE'], keep=False)]
print(duplicates.head())  # Inspect duplicate rows

#Chicago
duplicates = weather_chicago[weather_chicago.duplicated(subset=['DATE'], keep=False)]
print(duplicates.head())  # Inspect duplicate rows

#Miami
duplicates = weather_miami[weather_miami.duplicated(subset=['DATE'], keep=False)]
print(duplicates.head())  # Inspect duplicate rows

#Denver
duplicates = weather_denver[weather_denver.duplicated(subset=['DATE'], keep=False)]
print(duplicates.head())  # Inspect duplicate rows


# For Pheonix and LA: a) Removing exact duplicates

# In[50]:


# Remove exact duplicates based on 'DATE'
weather_phoenix_cleaned = weather_phoenix.drop_duplicates(subset=['DATE'], keep='first')
weather_la_cleaned = weather_la.drop_duplicates(subset=['DATE'], keep='first')


# b) If there are multiple stations aggregating duplicate entries by date 

# In[62]:


# Phoenix Aggregation
weather_phoenix_aggregated = weather_phoenix_cleaned.groupby('DATE').agg({
    'STATION': 'first',  # Taking the first station
    'NAME': 'first',     # Taking the first name
    'TAVG': 'mean',
    'TMAX': 'mean',
    'TMIN': 'mean',
    'PRCP': 'mean',
    'SNOW': 'mean',      # Aggregating SNOW with mean (or use 'first' or another method if needed)
    'CITY': 'first'      # Taking the first city
}).reset_index()

# Ensure the columns are in the correct order
weather_phoenix_aggregated = weather_phoenix_aggregated[['STATION', 'NAME', 'DATE', 'TAVG', 'TMAX', 'TMIN', 'PRCP', 'SNOW', 'CITY']]

# Sort data by DATE to preserve chronological order
weather_phoenix_aggregated = weather_phoenix_aggregated.sort_values(by='DATE').reset_index(drop=True)

# LA Aggregation
weather_la_aggregated = weather_la_cleaned.groupby('DATE').agg({
    'STATION': 'first',  # Taking the first station
    'NAME': 'first',     # Taking the first name
    'TAVG': 'mean',
    'TMAX': 'mean',
    'TMIN': 'mean',
    'PRCP': 'mean',
    'SNOW': 'mean',      # Aggregating SNOW with mean (or use 'first' or another method if needed)
    'CITY': 'first'      # Taking the first city
}).reset_index()

# Ensure the columns are in the correct order
weather_la_aggregated = weather_la_aggregated[['STATION', 'NAME', 'DATE', 'TAVG', 'TMAX', 'TMIN', 'PRCP', 'SNOW', 'CITY']]

# Sort data by DATE to preserve chronological order
weather_la_aggregated = weather_la_aggregated.sort_values(by='DATE').reset_index(drop=True)

# Inspect the cleaned data
print(weather_phoenix_aggregated.head())
print(weather_la_aggregated.head())


# Step 3 : Merging Weather and Solar Data

# A. Ensuring Date Formats Match

# In[63]:


# Convert the 'DATE' columns to datetime format for both weather and solar data
weather_bakersfield['DATE'] = pd.to_datetime(weather_bakersfield['DATE'])
weather_la_aggregated['DATE'] = pd.to_datetime(weather_la_aggregated['DATE'])
weather_phoenix_aggregated['DATE'] = pd.to_datetime(weather_phoenix_aggregated['DATE'])
weather_sf['DATE'] = pd.to_datetime(weather_sf['DATE'])
weather_ny['DATE'] = pd.to_datetime(weather_ny['DATE'])
weather_chicago['DATE'] = pd.to_datetime(weather_chicago['DATE'])
weather_miami['DATE'] = pd.to_datetime(weather_miami['DATE'])
weather_denver['DATE'] = pd.to_datetime(weather_denver['DATE'])




solar_bakersfield['DATE'] = pd.to_datetime(solar_bakersfield['DATE'])
solar_la['DATE'] = pd.to_datetime(solar_la['DATE'])
solar_phoenix['DATE'] = pd.to_datetime(solar_phoenix['DATE'])
solar_sf['DATE'] = pd.to_datetime(solar_sf['DATE'])
solar_ny['DATE'] = pd.to_datetime(solar_ny['DATE'])
solar_chicago['DATE'] = pd.to_datetime(solar_chicago['DATE'])
solar_miami['DATE'] = pd.to_datetime(solar_miami['DATE'])
solar_denver['DATE'] = pd.to_datetime(solar_denver['DATE'])


# B. Merging the Data for Each City

# In[64]:


# Merging weather and solar data for each city

# Bakersfield
merged_bakersfield = pd.merge(weather_bakersfield, solar_bakersfield, on='DATE', how='inner')
# Los Angeles
merged_la = pd.merge(weather_la_aggregated, solar_la, on='DATE', how='inner')
# Phoenix
merged_phoenix = pd.merge(weather_phoenix_aggregated, solar_phoenix, on='DATE', how='inner')
#Sf
merged_sf = pd.merge(weather_sf, solar_sf, on='DATE', how='inner')
#Ny
merged_ny = pd.merge(weather_ny, solar_ny, on='DATE', how='inner')
#Chicago
merged_chicago = pd.merge(weather_chicago, solar_chicago, on='DATE', how='inner')
#Miami
merged_miami = pd.merge(weather_miami, solar_miami, on='DATE', how='inner')
#Denver
merged_denver = pd.merge(weather_denver, solar_denver, on='DATE', how='inner')


# Checking the merged data for few cities
print("\nMerged Bakersfield:")
print(merged_bakersfield.head())

print("\nMerged Los Angeles:")
print(merged_la.head())

print("\nMerged Phoenix:")
print(merged_phoenix.head())

print("\nMerged San Francisco:")
print(merged_sf.head())


# C. Combine All City Data

# In[65]:


# Combine all merged city data into one DataFrame
merged_all_cities = pd.concat([merged_bakersfield, merged_la, merged_phoenix, merged_sf, merged_ny , merged_chicago , merged_miami , merged_denver], ignore_index=True)

# Inspect the final merged dataset
print("Merged Data for All Cities:")
print(merged_all_cities.head())


# D. Exporting the Final Dataset

# In[66]:


# Export the final merged data to CSV
merged_all_cities.to_csv('merged_cleaned_data.csv', index=False)


# In[ ]:




