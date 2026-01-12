import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Define file paths (Raspberry Pi paths)
INPUT_PATH = "/home/pi/ProjectSem3_2025/data/sensor_data_preprocessed.csv"
MODEL_OUTPUT_PATH = "/home/pi/ProjectSem3_2025/models/linear_regression_model.pkl"
PLOT_OUTPUT_PATH = "/home/pi/ProjectSem3_2025/figures/lr_prediction_result.png"

# Main function: Build and evaluate linear regression model for 12-hour prediction
def main():
    print("Starting Linear Regression Model Training...")
    # Load preprocessed data
    try:
        data = pd.read_csv(INPUT_PATH)
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data['hour'] = data['timestamp'].dt.hour  # Extract hour as time feature
        print(f"Data loaded successfully (rows: {len(data)})")
    except FileNotFoundError:
        print(f"Error: Preprocessed data not found at {INPUT_PATH}")
        return
    
    # Prepare data: Predict 12-hour future humidity
    # Features: current hour, temperature, humidity; Target: humidity after 12 time steps
    X = data[['hour', 'temperature_normalized', 'humidity_normalized']].iloc[:-12]  # All except last 12 rows
    y = data['humidity_normalized'].iloc[12:]  # Last 12 rows (12-hour later)
    
    print(f"Training data shape: X={X.shape}, y={y.shape}")
    
    # Train Linear Regression model
    lr_model = LinearRegression()
    lr_model.fit(X, y)
    
    # Make predictions
    y_pred = lr_model.predict(X)
    
    # Evaluate model
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    
    print("\nLinear Regression Model Evaluation:")
    print(f"Mean Squared Error (MSE): {mse:.4f}")
    print(f"R-squared (R²): {r2:.4f}")
    
    # Save model
    joblib.dump(lr_model, MODEL_OUTPUT_PATH)
    print(f"Model saved to: {MODEL_OUTPUT_PATH}")
    
    # Plot prediction results
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(12, 6))
    plt.plot(range(len(y)), y, color='steelblue', linewidth=2, label='True Humidity')
    plt.plot(range(len(y_pred)), y_pred, color='darkorange', linewidth=2, linestyle='--', label='Predicted Humidity')
    plt.title('Linear Regression: 12-Hour Humidity Prediction', fontsize=14, fontweight='bold')
    plt.xlabel('Sample Index', fontsize=12)
    plt.ylabel('Normalized Humidity (0-1)', fontsize=12)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(PLOT_OUTPUT_PATH, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Prediction plot saved to: {PLOT_OUTPUT_PATH}")

if __name__ == '__main__':
    main()
