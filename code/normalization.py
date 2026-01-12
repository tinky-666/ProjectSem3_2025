import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib

# Define file paths (Raspberry Pi paths)
INPUT_PATH = "/home/pi/ProjectSem3_2025/data/sensor_data_denoised.csv"
OUTPUT_DATA_PATH = "/home/pi/ProjectSem3_2025/data/sensor_data_preprocessed.csv"
OUTPUT_SCALER_PATH = "/home/pi/ProjectSem3_2025/models/scaler.pkl"

# Main function: Normalize denoised data to [0, 1] range
def main():
    print("Starting data normalization...")
    # Load denoised data
    try:
        denoised_data = pd.read_csv(INPUT_PATH)
        print(f"Successfully loaded denoised data (rows: {len(denoised_data)})")
    except FileNotFoundError:
        print(f"Error: Denoised data file not found at {INPUT_PATH}")
        return
    
    # Initialize MinMaxScaler (scale to [0, 1])
    scaler = MinMaxScaler(feature_range=(0, 1))
    
    # Select columns to normalize
    columns_to_normalize = ['humidity_denoised', 'temperature_denoised']
    normalized_array = scaler.fit_transform(denoised_data[columns_to_normalize])
    
    # Add normalized columns to original data
    denoised_data['humidity_normalized'] = normalized_array[:, 0]
    denoised_data['temperature_normalized'] = normalized_array[:, 1]
    
    # Save preprocessed data (denoised + normalized)
    denoised_data.to_csv(OUTPUT_DATA_PATH, index=False, encoding='utf-8')
    print(f"Preprocessed data saved to: {OUTPUT_DATA_PATH}")
    
    # Save scaler for future inverse transformation
    joblib.dump(scaler, OUTPUT_SCALER_PATH)
    print(f"Scaler saved to: {OUTPUT_SCALER_PATH}")
    
    # Print normalization statistics
    print("\nNormalization statistics (normalized columns):")
    print(denoised_data[['humidity_normalized', 'temperature_normalized']].describe())

if __name__ == '__main__':
    main()
