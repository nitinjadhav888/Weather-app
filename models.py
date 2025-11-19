import xgboost as xgb
import pandas as pd
import numpy as np

# Mock data fusion: given lat, lon, generate synthetic weather features
def fuse_data(lat, lon):
    np.random.seed(int((lat+lon)*1000)%1000)  # deterministic randomness
    temp = np.random.uniform(15, 40)           # Temp in Celsius
    humidity = np.random.uniform(40, 100)      # Percent
    radar_intensity = np.random.uniform(0, 10)
    satellite_cover = np.random.uniform(0, 100)
    crowd_rain_reports = np.random.randint(0, 5)
    df = pd.DataFrame([{
        'temp': temp,
        'humidity': humidity,
        'radar': radar_intensity,
        'satellite': satellite_cover,
        'crowd_rain': crowd_rain_reports
    }])
    return df

# Train simple models on mock data
def train_model():
    # Generate mock training data - 1000 samples
    data = pd.DataFrame({
        'temp': np.random.uniform(15, 40, 1000),
        'humidity': np.random.uniform(40, 100, 1000),
        'radar': np.random.uniform(0, 10, 1000),
        'satellite': np.random.uniform(0, 100, 1000),
        'crowd_rain': np.random.randint(0, 5, 1000),
        'rain_prob': np.random.uniform(0, 1, 1000),  # Target 1
        'rain_mm': np.random.uniform(0, 20, 1000)    # Target 2
    })
    X = data[['temp', 'humidity', 'radar', 'satellite', 'crowd_rain']]
    y_prob = data['rain_prob']
    y_mm = data['rain_mm']

    model_prob = xgb.XGBRegressor(objective ='reg:squarederror')
    model_prob.fit(X, y_prob)

    model_mm = xgb.XGBRegressor(objective ='reg:squarederror')
    model_mm.fit(X, y_mm)

    return model_prob, model_mm

# Global models to avoid retraining every predict call
model_prob, model_mm = train_model()

def predict_rain(lat, lon):
    input_data = fuse_data(lat, lon)
    prob = model_prob.predict(input_data)[0]
    mm = model_mm.predict(input_data)[0]
    return max(0, min(prob, 1)), max(0, mm)  # Clamp values