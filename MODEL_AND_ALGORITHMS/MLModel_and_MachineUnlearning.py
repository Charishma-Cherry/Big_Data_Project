{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "232847d3-b9e4-4c71-b3d6-ab254e7bd0de",
   "metadata": {},
   "source": [
    "RANDOM FOREST REGRESSOR MODEL"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "395a4fef-e000-4e85-80bd-06ba601d0601",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "Model Evaluation:\n",
      "  RMSE: 0.8660\n",
      "  R² Score: 0.8242\n",
      "\n",
      "Feature Importances:\n",
      "     Feature  Importance\n",
      "5      Month    0.234959\n",
      "1       TMAX    0.197796\n",
      "8  is_winter    0.183304\n",
      "0       TAVG    0.130909\n",
      "3       PRCP    0.097260\n",
      "2       TMIN    0.070599\n",
      "7  is_summer    0.054563\n",
      "6        Day    0.028640\n",
      "4       SNOW    0.001970\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/sklearn/metrics/_regression.py:492: FutureWarning: 'squared' is deprecated in version 1.4 and will be removed in 1.6. To calculate the root mean squared error, use the function'root_mean_squared_error'.\n",
      "  warnings.warn(\n"
     ]
    },
    {
     "data": {
      "image/png": "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hqFx48apcuXK8vHxUbt27XTw4MGSPASUMsV9zsXExMhisTgtHTp0KMlDQClTmHNu3759evjhhxUWFiaLxaJZs2Zd95gwn+I+5yZMmJDv37natWuX4BGgtCnMOff222/r7rvvVrly5VSuXDm1a9cuX3/+nkNxIwzehP73v/9pxIgRGj9+vHbu3KmGDRsqOjpap0+fLrD/pk2b1KtXLw0cOFCJiYl68MEH9eCDD+q7775z9JkxY4Zee+01zZ07V1u3bpWvr6+io6N18eLFG3VYuImVxDknSR06dFBycrJjWbJkyY04HJQChT3nMjIyVL16dU2fPl1BQUHFMibMpSTOOUmqV6+e079zGzZsKKlDQClT2HMuISFBvXr10tq1a7V582aFhITo3nvv1S+//OLow99zKHYGbjpNmzY1nnzyScfnnJwcIzg42Jg2bVqB/bt372507tzZqa1Zs2bG448/bhiGYeTm5hpBQUHGv//9b8f68+fPG15eXsaSJUtK4AhQ2hT3OWcYhtG/f3/jgQceKJF6UfoV9pz7s9DQUOOVV14p1jFx6yuJc278+PFGw4YNi7FK3Equ99+kS5cuGX5+fsaCBQsMw+DvOZQMZgZvMllZWdqxY4fatWvnaCtTpozatWunzZs3F7jN5s2bnfpLUnR0tKN/UlKSTp486dTHbrerWbNmlx0T5lES51yehIQEVaxYUbVq1dKQIUN05syZ4j8AlDpFOedcMSZuHSV5fhw8eFDBwcGqXr26evfurWPHjl1vubgFFMc5l5GRoezsbAUEBEji7zmUDMLgTea3335TTk6OKlWq5NReqVIlnTx5ssBtTp48ecX+ef8tzJgwj5I456Q/LhFduHCh1qxZoxdffFHr1q1Tx44dlZOTU/wHgVKlKOecK8bEraOkzo9mzZopPj5eq1ev1pw5c5SUlKS7775baWlp11sySrniOOeee+45BQcHO8Iff8+hJLi7ugAAt6aePXs6fm7QoIEiIyNVo0YNJSQk6J577nFhZQBQPDp27Oj4OTIyUs2aNVNoaKjee+89DRw40IWVobSbPn26li5dqoSEBHl7e7u6HNzCmBm8yQQGBsrNzU2nTp1yaj916tRlb2APCgq6Yv+8/xZmTJhHSZxzBalevboCAwN16NCh6y8apVpRzjlXjIlbx406P/z9/VWzZk3+ncN1nXMvvfSSpk+fri+++EKRkZGOdv6eQ0kgDN5kPD091bhxY61Zs8bRlpubqzVr1qh58+YFbtO8eXOn/pL05ZdfOvpXq1ZNQUFBTn1SU1O1devWy44J8yiJc64gP//8s86cOaPKlSsXT+EotYpyzrliTNw6btT5kZ6ersOHD/PvHIp8zs2YMUOTJ0/W6tWr1aRJE6d1/D2HEuHqJ9ggv6VLlxpeXl5GfHy88f333xuPPfaY4e/vb5w8edIwDMPo27evMXr0aEf/jRs3Gu7u7sZLL71k7N+/3xg/frzh4eFh7N2719Fn+vTphr+/v/Hxxx8be/bsMR544AGjWrVqxu+//37Djw83n+I+59LS0oyRI0camzdvNpKSkoyvvvrKuOOOO4yIiAjj4sWLLjlG3FwKe85lZmYaiYmJRmJiolG5cmVj5MiRRmJionHw4MFrHhPmVhLn3LPPPmskJCQYSUlJxsaNG4127doZgYGBxunTp2/48eHmU9hzbvr06Yanp6fx/vvvG8nJyY4lLS3NqQ9/z6E4EQZvUq+//rpRtWpVw9PT02jatKmxZcsWx7qoqCijf//+Tv3fe+89o2bNmoanp6dRr14949NPP3Van5uba4wdO9aoVKmS4eXlZdxzzz3GgQMHbsShoJQoznMuIyPDuPfee40KFSoYHh4eRmhoqDF48GD+KIeTwpxzSUlJhqR8S1RU1DWPCRT3OdejRw+jcuXKhqenp1GlShWjR48exqFDh27gEeFmV5hzLjQ0tMBzbvz48Y4+/D2H4mYxDMNwwYQkAAAAAMCFuGcQAAAAAEyIMAgAAAAAJkQYBAAAAAATIgwCAAAAgAkRBgEAAADAhAiDAAAAAGBChEEAAAAAMCHCIAAAAACYEGEQAAAAAEyIMAgAQCHFxMTowQcfdHUZBTp69KgsFot27drl6lIAADc5wiAAALeIrKwsV5cAAChFCIMAAFyH1q1b66mnntLw4cNVrlw5VapUSW+//bYuXLigAQMGyM/PT+Hh4Vq1apVjm4SEBFksFn366aeKjIyUt7e37rzzTn333XdOY3/wwQeqV6+evLy8FBYWppdfftlpfVhYmCZPnqx+/frJZrPpscceU7Vq1SRJjRo1ksViUevWrSVJ27ZtU/v27RUYGCi73a6oqCjt3LnTaTyLxaJ33nlHDz30kMqWLauIiAitWLHCqc++ffvUpUsX2Ww2+fn56e6779bhw4cd69955x3VqVNH3t7eql27tmbPnn3d3zEAoGQQBgEAuE4LFixQYGCgvv32Wz311FMaMmSIunXrprvuuks7d+7Uvffeq759+yojI8Npu1GjRunll1/Wtm3bVKFCBd13333Kzs6WJO3YsUPdu3dXz549tXfvXk2YMEFjx45VfHy80xgvvfSSGjZsqMTERI0dO1bffvutJOmrr75ScnKyli9fLklKS0tT//79tWHDBm3ZskURERHq1KmT0tLSnMabOHGiunfvrj179qhTp07q3bu3zp49K0n65Zdf1KpVK3l5eenrr7/Wjh07FBsbq0uXLkmSFi1apHHjxmnKlCnav3+/pk6dqrFjx2rBggXF/p0DAIqBAQAACqV///7GAw88YBiGYURFRRktW7Z0rLt06ZLh6+tr9O3b19GWnJxsSDI2b95sGIZhrF271pBkLF261NHnzJkzho+Pj/G///3PMAzDePTRR4327ds77XfUqFFG3bp1HZ9DQ0ONBx980KlPUlKSIclITEy84jHk5OQYfn5+xieffOJok2T861//cnxOT083JBmrVq0yDMMwxowZY1SrVs3IysoqcMwaNWoYixcvdmqbPHmy0bx58yvWAgBwDWYGAQC4TpGRkY6f3dzcVL58eTVo0MDRVqlSJUnS6dOnnbZr3ry54+eAgADVqlVL+/fvlyTt379fLVq0cOrfokULHTx4UDk5OY62Jk2aXFONp06d0uDBgxURESG73S6bzab09HQdO3bsssfi6+srm83mqHvXrl26++675eHhkW/8Cxcu6PDhwxo4cKCsVqtjeeGFF5wuIwUA3DzcXV0AAACl3V/DkcVicWqzWCySpNzc3GLft6+v7zX169+/v86cOaNXX31VoaGh8vLyUvPmzfM9dKagY8mr28fH57Ljp6enS5LefvttNWvWzGmdm5vbNdUIALixCIMAALjIli1bVLVqVUnSuXPn9OOPP6pOnTqSpDp16mjjxo1O/Tdu3KiaNWteMVx5enpKktPsYd62s2fPVqdOnSRJx48f12+//VaoeiMjI7VgwQJlZ2fnC42VKlVScHCwjhw5ot69exdqXACAaxAGAQBwkUmTJql8+fKqVKmSnn/+eQUGBjreX/jss8/qb3/7myZPnqwePXpo8+bNeuONN676dM6KFSvKx8dHq1ev1m233SZvb2/Z7XZFRETo3XffVZMmTZSamqpRo0ZdcaavIEOHDtXrr7+unj17asyYMbLb7dqyZYuaNm2qWrVqaeLEiRo2bJjsdrs6dOigzMxMbd++XefOndOIESOK+jUBAEoI9wwCAOAi06dP19NPP63GjRvr5MmT+uSTTxwze3fccYfee+89LV26VPXr19e4ceM0adIkxcTEXHFMd3d3vfbaa3rrrbcUHBysBx54QJI0b948nTt3TnfccYf69u2rYcOGqWLFioWqt3z58vr666+Vnp6uqKgoNW7cWG+//bZjlnDQoEF65513FBcXpwYNGigqKkrx8fGO110AAG4uFsMwDFcXAQCAmSQkJKhNmzY6d+6c/P39XV0OAMCkmBkEAAAAABMiDAIAAACACXGZKAAAAACYEDODAAAAAGBChEEAAAAAMCHCIAAAAACYEGEQAAAAAEyIMAgAAAAAJkQYBAAAAAATIgwCAAAAgAkRBgEAAADAhP4f15OIwzEaDmIAAAAASUVORK5CYII=",
      "text/plain": [
       "<Figure size 1000x600 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.ensemble import RandomForestRegressor\n",
    "from sklearn.metrics import mean_squared_error, r2_score\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "# Load and Clean the Dataset\n",
    "file_path = r'/Users/sushma/Documents/BigData/bd_project/Big_Data_Project/kafka_project/data/merged_cleaned_data.csv'\n",
    "\n",
    "data = pd.read_csv(file_path)\n",
    "data.replace(-999, pd.NA, inplace=True)\n",
    "data_cleaned = data.dropna().copy()  \n",
    "\n",
    "# Feature Engineering\n",
    "data_cleaned['DATE'] = pd.to_datetime(data_cleaned['DATE'])  # Convert 'DATE' column to datetime\n",
    "data_cleaned['Month'] = data_cleaned['DATE'].dt.month       # Extract month\n",
    "data_cleaned['Day'] = data_cleaned['DATE'].dt.day           # Extract day\n",
    "data_cleaned['is_summer'] = data_cleaned['Month'].apply(lambda x: 1 if x in [6, 7, 8] else 0)\n",
    "data_cleaned['is_winter'] = data_cleaned['Month'].apply(lambda x: 1 if x in [12, 1, 2] else 0)\n",
    "\n",
    "# Define Features and Target\n",
    "features = ['TAVG', 'TMAX', 'TMIN', 'PRCP', 'SNOW', 'Month', 'Day', 'is_summer', 'is_winter']\n",
    "target = 'ALLSKY_SFC_SW_DWN'\n",
    "\n",
    "X = data_cleaned[features]\n",
    "y = data_cleaned[target]\n",
    "\n",
    "#  Train-Test Split\n",
    "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n",
    "\n",
    "# Train the Random Forest Model\n",
    "rf_model = RandomForestRegressor(\n",
    "    n_estimators=500,\n",
    "    max_depth=20,\n",
    "    max_features='sqrt',\n",
    "    min_samples_split=10,\n",
    "    min_samples_leaf=2,\n",
    "    random_state=100\n",
    ")\n",
    "rf_model.fit(X_train, y_train)\n",
    "\n",
    "# Predictions and Evaluation\n",
    "y_test_pred = rf_model.predict(X_test)\n",
    "test_rmse = mean_squared_error(y_test, y_test_pred, squared=False)\n",
    "test_r2 = r2_score(y_test, y_test_pred)\n",
    "\n",
    "print(\"\\nModel Evaluation:\")\n",
    "print(f\"  RMSE: {test_rmse:.4f}\")\n",
    "print(f\"  R² Score: {test_r2:.4f}\")\n",
    "\n",
    "# Feature Importance\n",
    "feature_importances = pd.DataFrame({\n",
    "    'Feature': features,\n",
    "    'Importance': rf_model.feature_importances_\n",
    "}).sort_values(by='Importance', ascending=False)\n",
    "\n",
    "print(\"\\nFeature Importances:\")\n",
    "print(feature_importances)\n",
    "\n",
    "plt.figure(figsize=(10, 6))\n",
    "plt.barh(feature_importances['Feature'], feature_importances['Importance'], color='skyblue')\n",
    "plt.title('Feature Importances')\n",
    "plt.xlabel('Importance')\n",
    "plt.ylabel('Feature')\n",
    "plt.gca().invert_yaxis()\n",
    "plt.show()\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "52397655-bb88-4a19-b762-0d2c873df872",
   "metadata": {},
   "source": [
    "PREDICTING SOLAR RADIATION AND ENERGY GENERATED BY TAKING USER INPUTS"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "29b71f39-c068-445e-ad36-41015adb9667",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Enter the following features:\n"
     ]
    },
    {
     "name": "stdin",
     "output_type": "stream",
     "text": [
      "TAVG:  25\n",
      "TMAX:  30\n",
      "TMIN:  20\n",
      "PRCP:  0\n",
      "SNOW:  0\n",
      "Month:  7\n",
      "Day:  4\n",
      "\n",
      "Enter the solar panel efficiency (e.g., 0.18 for 18%):  0.16\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "Predicted Solar Radiation (ALLSKY_SFC_SW_DWN) : 6.71 kWh/m²/day\n",
      "Predicted Solar Energy Output: 1074128.41 kWh/day\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "(np.float64(6.713302535692306), np.float64(1074128.4057107691))"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "def predict_solar_energy_with_location(model, data):\n",
    "\n",
    "    # # Get unique cities from the dataset\n",
    "    # cities = data['CITY_x'].unique()\n",
    "\n",
    "    # Define the input features\n",
    "    feature_names = ['TAVG', 'TMAX', 'TMIN', 'PRCP', 'SNOW', 'Month', 'Day', 'is_summer', 'is_winter']\n",
    "    \n",
    "    print(\"Enter the following features:\")\n",
    "    input_features = []\n",
    "\n",
    "    # Loop through other features\n",
    "    for feature in feature_names[:-2]:  \n",
    "        value = float(input(f\"{feature}: \"))\n",
    "        input_features.append(value)\n",
    "\n",
    "    # Add seasonal flags based on the input month\n",
    "    month = int(input_features[5])  \n",
    "    is_summer = 1 if month in [6, 7, 8] else 0\n",
    "    is_winter = 1 if month in [12, 1, 2] else 0\n",
    "\n",
    "    # Append seasonal flags to the feature set\n",
    "    input_features.append(is_summer)\n",
    "    input_features.append(is_winter)\n",
    "\n",
    "    # Add solar panel efficiency\n",
    "    efficiency = float(input(\"\\nEnter the solar panel efficiency (e.g., 0.18 for 18%): \"))\n",
    "    \n",
    "    # Create a DataFrame for prediction\n",
    "    input_df = pd.DataFrame([input_features], columns=feature_names)\n",
    "    \n",
    "    # Predict solar radiation\n",
    "    predicted_radiation = model.predict(input_df)[0]\n",
    "    \n",
    "    # Calculate energy output\n",
    "    area_sq_km = 1  # Assume 1 square kilometer\n",
    "    area_sq_m = area_sq_km * 1e6  # Convert to square meters\n",
    "    solar_energy = predicted_radiation * area_sq_m * efficiency\n",
    "\n",
    "    # Display results\n",
    "    print(f\"\\nPredicted Solar Radiation (ALLSKY_SFC_SW_DWN) : {predicted_radiation:.2f} kWh/m²/day\")\n",
    "    print(f\"Predicted Solar Energy Output: {solar_energy:.2f} kWh/day\")\n",
    "\n",
    "    return predicted_radiation, solar_energy\n",
    "\n",
    "\n",
    "\n",
    "#  Prediction Function\n",
    "predict_solar_energy_with_location(rf_model, data_cleaned)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "9d6c9630-80c4-4a44-83fb-332df3fe7a10",
   "metadata": {},
   "source": [
    "MACHINE UNLEARNING (REMOVING BAKERSFEILD DATA)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "b7cfa287-77f5-4632-923f-298c140fa810",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/sklearn/metrics/_regression.py:492: FutureWarning: 'squared' is deprecated in version 1.4 and will be removed in 1.6. To calculate the root mean squared error, use the function'root_mean_squared_error'.\n",
      "  warnings.warn(\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "Updated Model Evaluation After Unlearning Bakersfield Data:\n",
      "  RMSE: 0.9047\n",
      "  R² Score: 0.8018\n",
      "Enter the following features:\n"
     ]
    },
    {
     "name": "stdin",
     "output_type": "stream",
     "text": [
      "TAVG:  25\n",
      "TMAX:  30\n",
      "TMIN:  20\n",
      "PRCP:  0\n",
      "SNOW:  0\n",
      "Month:  7\n",
      "Day:  4\n",
      "\n",
      "Enter the solar panel efficiency (e.g., 0.18 for 18%):  0.16\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "Predicted Solar Radiation (ALLSKY_SFC_SW_DWN): 6.63 kWh/m²/day\n",
      "Predicted Solar Energy Output: 1061084.67 kWh/day\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "(np.float64(6.6317792046667075), np.float64(1061084.6727466732))"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Machine Unlearning - Remove Rows Related to Bakersfield\n",
    "rows_to_remove = data_cleaned[data_cleaned['CITY_x'] == 'Bakersfield']\n",
    "data_unlearned = data_cleaned.drop(rows_to_remove.index)\n",
    "\n",
    "# Define Features and Target for the Updated Dataset\n",
    "X_unlearned = data_unlearned[features]\n",
    "y_unlearned = data_unlearned[target]\n",
    "\n",
    "# Train-Test Split After Unlearning\n",
    "X_train_unlearned, X_test_unlearned, y_train_unlearned, y_test_unlearned = train_test_split(\n",
    "    X_unlearned, y_unlearned, test_size=0.2, random_state=42\n",
    ")\n",
    "\n",
    "# Retrain the Model with the Updated Data\n",
    "rf_model_unlearned = RandomForestRegressor(\n",
    "    n_estimators=500,\n",
    "    max_depth=20,\n",
    "    max_features='sqrt',\n",
    "    min_samples_split=10,\n",
    "    min_samples_leaf=2,\n",
    "    random_state=100\n",
    ")\n",
    "rf_model_unlearned.fit(X_train_unlearned, y_train_unlearned)\n",
    "\n",
    "# Evaluate the Updated Model\n",
    "y_test_pred_unlearned = rf_model_unlearned.predict(X_test_unlearned)\n",
    "test_rmse_unlearned = mean_squared_error(y_test_unlearned, y_test_pred_unlearned, squared=False)\n",
    "test_r2_unlearned = r2_score(y_test_unlearned, y_test_pred_unlearned)\n",
    "\n",
    "print(\"\\nUpdated Model Evaluation After Unlearning Bakersfield Data:\")\n",
    "print(f\"  RMSE: {test_rmse_unlearned:.4f}\")\n",
    "print(f\"  R² Score: {test_r2_unlearned:.4f}\")\n",
    "\n",
    "# Prediction Function with Updated Model\n",
    "def predict_solar_energy_with_location(model, data):\n",
    "\n",
    "    # Define the input features\n",
    "    feature_names = ['TAVG', 'TMAX', 'TMIN', 'PRCP', 'SNOW', 'Month', 'Day', 'is_summer', 'is_winter']\n",
    "    \n",
    "    print(\"Enter the following features:\")\n",
    "    input_features = []\n",
    "\n",
    "    # Loop through other features\n",
    "    for feature in feature_names[:-2]:  \n",
    "        value = float(input(f\"{feature}: \"))\n",
    "        input_features.append(value)\n",
    "\n",
    "    # Add seasonal flags based on the input month\n",
    "    month = int(input_features[5])  \n",
    "    is_summer = 1 if month in [6, 7, 8] else 0\n",
    "    is_winter = 1 if month in [12, 1, 2] else 0\n",
    "\n",
    "    # Append seasonal flags to the feature set\n",
    "    input_features.append(is_summer)\n",
    "    input_features.append(is_winter)\n",
    "\n",
    "    # Add solar panel efficiency\n",
    "    efficiency = float(input(\"\\nEnter the solar panel efficiency (e.g., 0.18 for 18%): \"))\n",
    "    \n",
    "    # Create a DataFrame for prediction\n",
    "    input_df = pd.DataFrame([input_features], columns=feature_names)\n",
    "    \n",
    "    # Predict solar radiation\n",
    "    predicted_radiation = model.predict(input_df)[0]\n",
    "    \n",
    "    # Calculate energy output\n",
    "    area_sq_km = 1  # Assume 1 square kilometer\n",
    "    area_sq_m = area_sq_km * 1e6  # Convert to square meters\n",
    "    solar_energy = predicted_radiation * area_sq_m * efficiency\n",
    "\n",
    "    # Display results\n",
    "    print(f\"\\nPredicted Solar Radiation (ALLSKY_SFC_SW_DWN): {predicted_radiation:.2f} kWh/m²/day\")\n",
    "    print(f\"Predicted Solar Energy Output: {solar_energy:.2f} kWh/day\")\n",
    "\n",
    "    return predicted_radiation, solar_energy\n",
    "\n",
    "# Manual Predictions After Unlearning\n",
    "predict_solar_energy_with_location(rf_model_unlearned, data_unlearned)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "fdd80d76-782b-4a13-87f9-99196e183897",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
