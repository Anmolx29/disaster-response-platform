"""
AI-Powered Disaster Prediction Engine
Flood, Earthquake, Cloudburst, Avalanche prediction (Random Forest models)
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

class DisasterPredictor:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.load_models()

    def load_models(self):
        """Try to load pre-trained models (optional)"""
        for name in ['flood', 'earthquake', 'cloudburst', 'avalanche']:
            try:
                self.models[name] = joblib.load(f"models/{name}_model.pkl")
                self.scalers[name] = joblib.load(f"models/{name}_scaler.pkl")
                print(f"✅ Loaded pre-trained {name} model")
            except:
                print(f"⚠️ No pre-trained model found for {name}. Will train new one.")

    ### FLOOD
    def train_flood_model(self, data: pd.DataFrame):
        X = data[['rainfall', 'river_level', 'soil_moisture', 'temperature', 'humidity']]
        y = data['flood_occurred']
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
        model.fit(X_scaled, y)
        os.makedirs('models', exist_ok=True)
        joblib.dump(model, 'models/flood_model.pkl')
        joblib.dump(scaler, 'models/flood_scaler.pkl')
        self.models['flood'] = model
        self.scalers['flood'] = scaler
        return model.score(X_scaled, y)

    def predict_flood_risk(self, rainfall, river_level, soil_moisture, temperature, humidity):
        features = np.array([[rainfall, river_level, soil_moisture, temperature, humidity]])
        features_scaled = self.scalers['flood'].transform(features)
        probability = self.models['flood'].predict_proba(features_scaled)[0][1]
        severity = "critical" if probability > 0.8 else "high" if probability > 0.6 else "medium" if probability > 0.3 else "low"
        return {"disaster_type": "flood", "probability": float(probability), "severity": severity}

    def generate_sample_flood_data(self):
        np.random.seed(42)
        return pd.DataFrame({
            'rainfall': np.random.uniform(0, 300, 1000),
            'river_level': np.random.uniform(0, 20, 1000),
            'soil_moisture': np.random.uniform(10, 100, 1000),
            'temperature': np.random.uniform(15, 40, 1000),
            'humidity': np.random.uniform(40, 100, 1000),
            'flood_occurred': np.random.randint(0, 2, 1000)
        })

    ### EARTHQUAKE
    def train_earthquake_model(self, data: pd.DataFrame):
        X = data[['magnitude', 'depth', 'distance_from_fault', 'peak_ground_accel']]
        y = data['quake_occurred']
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_scaled, y)
        os.makedirs('models', exist_ok=True)
        joblib.dump(model, 'models/earthquake_model.pkl')
        joblib.dump(scaler, 'models/earthquake_scaler.pkl')
        self.models['earthquake'] = model
        self.scalers['earthquake'] = scaler
        return model.score(X_scaled, y)

    def predict_earthquake_risk(self, magnitude, depth, distance_from_fault, peak_ground_accel):
        features = np.array([[magnitude, depth, distance_from_fault, peak_ground_accel]])
        features_scaled = self.scalers['earthquake'].transform(features)
        probability = self.models['earthquake'].predict_proba(features_scaled)[0][1]
        severity = "critical" if probability > 0.8 else "high" if probability > 0.6 else "medium" if probability > 0.3 else "low"
        return {"disaster_type": "earthquake", "probability": float(probability), "severity": severity}

    def generate_sample_earthquake_data(self):
        np.random.seed(42)
        return pd.DataFrame({
            'magnitude': np.random.uniform(3, 9, 1000),
            'depth': np.random.uniform(1, 70, 1000),
            'distance_from_fault': np.random.uniform(0, 100, 1000),
            'peak_ground_accel': np.random.uniform(0.01, 1.0, 1000),
            'quake_occurred': np.random.randint(0, 2, 1000)
        })

    ### CLOUD BURST
    def train_cloudburst_model(self, data: pd.DataFrame):
        X = data[['rainfall_rate', 'duration', 'cloud_water_content', 'temp_diff']]
        y = data['cloudburst_occurred']
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_scaled, y)
        os.makedirs('models', exist_ok=True)
        joblib.dump(model, 'models/cloudburst_model.pkl')
        joblib.dump(scaler, 'models/cloudburst_scaler.pkl')
        self.models['cloudburst'] = model
        self.scalers['cloudburst'] = scaler
        return model.score(X_scaled, y)

    def predict_cloudburst_risk(self, rainfall_rate, duration, cloud_water_content, temp_diff):
        features = np.array([[rainfall_rate, duration, cloud_water_content, temp_diff]])
        features_scaled = self.scalers['cloudburst'].transform(features)
        probability = self.models['cloudburst'].predict_proba(features_scaled)[0][1]
        severity = "critical" if probability > 0.8 else "high" if probability > 0.6 else "medium" if probability > 0.3 else "low"
        return {"disaster_type": "cloudburst", "probability": float(probability), "severity": severity}

    def generate_sample_cloudburst_data(self):
        np.random.seed(42)
        return pd.DataFrame({
            'rainfall_rate': np.random.uniform(50, 200, 1000), # mm/hr
            'duration': np.random.uniform(10, 60, 1000),       # minutes
            'cloud_water_content': np.random.uniform(10, 50, 1000), # g/m3
            'temp_diff': np.random.uniform(2, 15, 1000),       # deg C
            'cloudburst_occurred': np.random.randint(0, 2, 1000)
        })
    
    ### AVALANCHE
    def train_avalanche_model(self, data: pd.DataFrame):
        X = data[['snow_depth', 'slope_angle', 'temperature', 'wind_speed']]
        y = data['avalanche_occurred']
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_scaled, y)
        os.makedirs('models', exist_ok=True)
        joblib.dump(model, 'models/avalanche_model.pkl')
        joblib.dump(scaler, 'models/avalanche_scaler.pkl')
        self.models['avalanche'] = model
        self.scalers['avalanche'] = scaler
        return model.score(X_scaled, y)

    def predict_avalanche_risk(self, snow_depth, slope_angle, temperature, wind_speed):
        features = np.array([[snow_depth, slope_angle, temperature, wind_speed]])
        features_scaled = self.scalers['avalanche'].transform(features)
        probability = self.models['avalanche'].predict_proba(features_scaled)[0][1]
        severity = "critical" if probability > 0.8 else "high" if probability > 0.6 else "medium" if probability > 0.3 else "low"
        return {"disaster_type": "avalanche", "probability": float(probability), "severity": severity}

    def generate_sample_avalanche_data(self):
        np.random.seed(42)
        return pd.DataFrame({
            'snow_depth': np.random.uniform(50, 300, 1000),    # cm
            'slope_angle': np.random.uniform(25, 50, 1000),    # degrees
            'temperature': np.random.uniform(-15, 5, 1000),    # degC
            'wind_speed': np.random.uniform(0, 30, 1000),      # m/s
            'avalanche_occurred': np.random.randint(0, 2, 1000)
        })

if __name__ == "__main__":
    predictor = DisasterPredictor()

    print("\nTraining flood model...")
    flood_data = predictor.generate_sample_flood_data()
    print("Flood Model Accuracy:", predictor.train_flood_model(flood_data))
    print("Sample flood risk:", predictor.predict_flood_risk(120, 12, 80, 28, 90))

    print("\nTraining earthquake model...")
    eq_data = predictor.generate_sample_earthquake_data()
    print("Earthquake Model Accuracy:", predictor.train_earthquake_model(eq_data))
    print("Sample earthquake risk:", predictor.predict_earthquake_risk(6.5, 20, 10, 0.4))

    print("\nTraining cloudburst model...")
    cb_data = predictor.generate_sample_cloudburst_data()
    print("Cloudburst Model Accuracy:", predictor.train_cloudburst_model(cb_data))
    print("Sample cloudburst risk:", predictor.predict_cloudburst_risk(140, 30, 35, 7))

    print("\nTraining avalanche model...")
    av_data = predictor.generate_sample_avalanche_data()
    print("Avalanche Model Accuracy:", predictor.train_avalanche_model(av_data))
    print("Sample avalanche risk:", predictor.predict_avalanche_risk(150, 35, -5, 12))
