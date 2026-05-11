"""
Comprehensive ML pipeline for AQI prediction.
Includes data preprocessing, feature engineering, model training, and evaluation.
Run: python ml/train_model.py
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os


DATA_PATH = os.path.join(os.path.dirname(__file__), "sample_data", "air_quality_sample.csv")
MODEL_OUT = os.path.join(os.path.dirname(__file__), "..", "backend", "models", "model.joblib")


def load_and_preprocess():
    """Load and preprocess data"""
    print("Loading data...")
    df = pd.read_csv(DATA_PATH)
    
    print(f"Data shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Handle missing values
    df = df.fillna(df.mean(numeric_only=True))
    
    # Feature engineering: add derived features
    df['temp_humidity_interaction'] = df['temperature'] * df['humidity']
    df['temp_rainfall_interaction'] = df['temperature'] * df['rainfall']
    
    return df


def train_model(df):
    """Train ML model"""
    print("\nPreparing features...")
    
    # Features and target
    feature_cols = ['temperature', 'humidity', 'rainfall', 'temp_humidity_interaction', 'temp_rainfall_interaction']
    X = df[feature_cols].fillna(0)
    y = df['aqi']
    
    print(f"Features: {feature_cols}")
    print(f"Target variable: AQI")
    print(f"Samples: {len(X)}")
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )
    
    print(f"\nTraining set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # Train model (using LinearRegression for interpretability; RandomForest for better accuracy)
    print("\nTraining Linear Regression model...")
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nModel Performance:")
    print(f"  MSE:  {mse:.4f}")
    print(f"  RMSE: {rmse:.4f}")
    print(f"  MAE:  {mae:.4f}")
    print(f"  R²:   {r2:.4f}")
    
    # Feature importances (coefficients for linear model)
    print(f"\nModel Coefficients:")
    for feat, coef in zip(feature_cols, model.coef_):
        print(f"  {feat}: {coef:.4f}")
    print(f"  Intercept: {model.intercept_:.4f}")
    
    return model


def main():
    df = load_and_preprocess()
    model = train_model(df)
    
    # Save model
    os.makedirs(os.path.dirname(MODEL_OUT), exist_ok=True)
    joblib.dump(model, MODEL_OUT)
    print(f"\n✓ Model saved to {MODEL_OUT}")


if __name__ == "__main__":
    main()
