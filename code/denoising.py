import pandas as pd
import numpy as np

# Define file paths (Raspberry Pi paths)
INPUT_PATH = "/home/pi/ProjectSem3_2025/data/sensor_data.csv"
OUTPUT_PATH = "/home/pi/ProjectSem3_2025/data/sensor_data_denoised.csv"

# Moving Average Denoising function (window size = 3)
def moving_average_denoise(series, window_size=3):
    """
    Apply moving average filtering to reduce noise in time-series data.
    Fill missing values with backward and forward fill.
    """
    return series.rolling(window=window_size, center=True).mean().fillna(method='bfill').fillna(method='ffill')

# Main function: Load raw data, denoise, and save
def main():
    print("Starting data denoising...")
    # Load raw sensor data
    try:
        raw_data = pd.read_csv(INPUT_PATH)
        print(f"Successfully loaded raw data (rows: {len(raw_data)}, columns: {raw_data.shape[1]})")
    except FileNotFoundError:
        print(f"Error: Raw data file not found at {INPUT_PATH}")
        return
    
    # Apply denoising to humidity and temperature columns
    raw_data['humidity_denoised'] = moving_average_denoise(raw_data['humidity_raw'])
    raw_data['temperature_denoised'] = moving_average_denoise(raw_data['temperature_celsius'])
    
    # Save denoised data
    raw_data.to_csv(OUTPUT_PATH, index=False, encoding='utf-8')
    print(f"Denoising completed. Denoised data saved to: {OUTPUT_PATH}")
    
    # Print sample comparison (first 5 rows)
    print("\nSample comparison (raw vs denoised):")
    sample = raw_data[['humidity_raw', 'humidity_denoised', 'temperature_celsius', 'temperature_denoised']].head()
    print(sample)

if __name__ == '__main__':
    main()
