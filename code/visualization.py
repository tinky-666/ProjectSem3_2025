import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Define file paths (Raspberry Pi paths)
INPUT_PATH = "/home/pi/ProjectSem3_2025/data/sensor_data_preprocessed.csv"
OUTPUT_PLOT_PATH = "/home/pi/ProjectSem3_2025/figures/time_series_plots.png"

# Main function: Generate time-series plots for humidity and temperature
def main():
    print("Generating time-series visualizations...")
    # Load preprocessed data
    try:
        data = pd.read_csv(INPUT_PATH)
        # Convert timestamp to datetime format
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        print(f"Successfully loaded data (time range: {data['timestamp'].min()} to {data['timestamp'].max()})")
    except FileNotFoundError:
        print(f"Error: Preprocessed data file not found at {INPUT_PATH}")
        return
    
    # Set plot style and font (compatible with Raspberry Pi)
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['font.size'] = 10
    plt.rcParams['figure.figsize'] = (12, 8)  # Width: 12 inches, Height: 8 inches
    
    # Create subplots (2 rows, 1 column)
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    
    # Plot 1: Humidity time series
    ax1.plot(data['timestamp'], data['humidity_normalized'], color='steelblue', linewidth=2, label='Normalized Humidity')
    ax1.set_title('Soil Humidity Trend (48 Hours)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Normalized Humidity (0-1)', fontsize=12)
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Temperature time series
    ax2.plot(data['timestamp'], data['temperature_normalized'], color='darkred', linewidth=2, label='Normalized Temperature')
    ax2.set_title('Ambient Temperature Trend (48 Hours)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Time', fontsize=12)
    ax2.set_ylabel('Normalized Temperature (0-1)', fontsize=12)
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)
    
    # Format x-axis (show date and time clearly)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    ax2.xaxis.set_major_locator(mdates.HourLocator(interval=6))  # Show tick every 6 hours
    plt.xticks(rotation=45, ha='right')
    
    # Adjust layout to prevent overlap
    plt.tight_layout()
    
    # Save plot (high resolution: 300 DPI)
    plt.savefig(OUTPUT_PLOT_PATH, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Time-series plots saved to: {OUTPUT_PLOT_PATH}")

if __name__ == '__main__':
    main()
