import pandas as pd

# Define file path (Raspberry Pi path)
INPUT_PATH = "/home/pi/ProjectSem3_2025/data/sensor_data_preprocessed.csv"
OUTPUT_STATS_PATH = "/home/pi/ProjectSem3_2025/data/descriptive_statistics.csv"

# Main function: Compute descriptive statistics for preprocessed data
def main():
    print("Starting descriptive data analysis...")
    # Load preprocessed data
    try:
        preprocessed_data = pd.read_csv(INPUT_PATH)
        print(f"Successfully loaded preprocessed data (rows: {len(preprocessed_data)})")
    except FileNotFoundError:
        print(f"Error: Preprocessed data file not found at {INPUT_PATH}")
        return
    
    # Select columns for analysis (normalized data)
    analysis_columns = ['humidity_normalized', 'temperature_normalized']
    stats = preprocessed_data[analysis_columns].describe()
    
    # Print statistics to terminal
    print("\nDescriptive Statistics:")
    print(stats)
    
    # Save statistics to CSV
    stats.to_csv(OUTPUT_STATS_PATH, encoding='utf-8')
    print(f"\nStatistics saved to: {OUTPUT_STATS_PATH}")

if __name__ == '__main__':
    main()

