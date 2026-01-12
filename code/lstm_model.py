import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping

# Define file paths (Raspberry Pi paths)
INPUT_PATH = "/home/pi/ProjectSem3_2025/data/sensor_data_preprocessed.csv"
MODEL_OUTPUT_PATH = "/home/pi/ProjectSem3_2025/models/lstm_model.h5"
LOSS_PLOT_PATH = "/home/pi/ProjectSem3_2025/figures/lstm_training_loss.png"
PRED_PLOT_PATH = "/home/pi/ProjectSem3_2025/figures/lstm_prediction_result.png"

# Create time-series sequences for LSTM
def create_sequences(data, seq_length=6, pred_length=1):
    """
    Convert time-series data into input sequences and target values.
    Input: [t-seq_length, ..., t-1] → Target: [t]
    """
    X, y = [], []
    for i in range(len(data) - seq_length - pred_length + 1):
        sequence = data[i:i+seq_length]
        target = data[i+seq_length:i+seq_length+pred_length]
        X.append(sequence)
        y.append(target)
    return np.array(X), np.array(y)

# Main function: Build and evaluate LSTM model for periodic prediction
def main():
    print("Starting LSTM Model Training...")
    # Load preprocessed data
    try:
        data = pd.read_csv(INPUT_PATH)
        humidity_data = data['humidity_normalized'].values.reshape(-1, 1)  # Reshape to (n_samples, 1)
        print(f"Data loaded successfully (humidity data shape: {humidity_data.shape})")
    except FileNotFoundError:
        print(f"Error: Preprocessed data not found at {INPUT_PATH}")
        return
    
    # Create sequences (sequence length = 6 → use 6 past values to predict 1 future value)
    seq_len = 6
    X, y = create_sequences(humidity_data, seq_len)
    y = y.reshape(-1, 1)  # Flatten target to (n_samples, 1)
    
    # Split into training (80%) and test (20%) sets
    train_size = int(0.8 * len(X))
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    
    print(f"Training set shape: X={X_train.shape}, y={y_train.shape}")
    print(f"Test set shape: X={X_test.shape}, y={y_test.shape}")
    
    # Build lightweight LSTM model
    model = Sequential()
    model.add(LSTM(32, input_shape=(seq_len, 1), return_sequences=False))  # Input: (seq_len, features)
    model.add(Dense(16, activation='relu'))
    model.add(Dense(1))  # Output layer: predict 1 value
    
    # Compile model
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    # Early stopping to prevent overfitting
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=3,
        restore_best_weights=True,
        verbose=1
    )
    
    # Train model
    print("\nTraining started (will stop early if validation loss plateaus)...")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=50,
        batch_size=8,
        callbacks=[early_stopping],
        verbose=1
    )
    
    # Make predictions
    y_pred_train = model.predict(X_train, verbose=0)
    y_pred_test = model.predict(X_test, verbose=0)
    
    # Evaluate model
    train_mse = mean_squared_error(y_train, y_pred_train)
    test_mse = mean_squared_error(y_test, y_pred_test)
    train_r2 = r2_score(y_train, y_pred_train)
    test_r2 = r2_score(y_test, y_pred_test)
    
    print("\nLSTM Model Evaluation:")
    print(f"Training MSE: {train_mse:.4f} | Training R²: {train_r2:.4f}")
    print(f"Test MSE: {test_mse:.4f} | Test R²: {test_r2:.4f}")
    
    # Save model
    model.save(MODEL_OUTPUT_PATH)
    print(f"Model saved to: {MODEL_OUTPUT_PATH}")
    
    # Plot training loss curve
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(10, 4))
    plt.plot(history.history['loss'], color='steelblue', linewidth=2, label='Training Loss')
    plt.plot(history.history['val_loss'], color='darkred', linewidth=2, label='Validation Loss')
    plt.title('LSTM Training Loss Curve', fontsize=14, fontweight='bold')
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('Mean Squared Error (MSE)', fontsize=12)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(LOSS_PLOT_PATH, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    # Plot test set prediction results
    plt.figure(figsize=(12, 6))
    plt.plot(range(len(y_test)), y_test, color='steelblue', linewidth=2, label='True Humidity')
    plt.plot(range(len(y_pred_test)), y_pred_test, color='darkorange', linewidth=2, linestyle='--', label='Predicted Humidity')
    plt.title('LSTM Model: Periodic Humidity Prediction (Test Set)', fontsize=14, fontweight='bold')
    plt.xlabel('Sample Index', fontsize=12)
    plt.ylabel('Normalized Humidity (0-1)', fontsize=12)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(PRED_PLOT_PATH, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"Training loss plot saved to: {LOSS_PLOT_PATH}")
    print(f"Test prediction plot saved to: {PRED_PLOT_PATH}")

if __name__ == '__main__':
    main()
