import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess

def plot_viral_load_vs_time_with_loess(filename, title, output_filename, dpi=150):
    df = pd.read_csv(filename)

    # Convert the 'Collection Date' column to datetime objects
    df['Collection Date'] = pd.to_datetime(df['Collection Date'])

    # Extract the required data
    x_data = df['Collection Date']
    y_data = np.log10(df['Viral Load'])

    # Apply Loess smoothing on the numerical representation of dates
    loess_result = lowess(y_data, np.array(x_data.astype(np.int64) // 10**9), frac=0.3)  # Adjust the frac parameter if needed

    # Convert the numeric loess result back to datetime for plotting
    loess_x = pd.to_datetime(loess_result[:, 0]*10**9)

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.scatter(x_data, y_data, s=5, color='blue', label='Data')
    plt.plot(loess_x, loess_result[:, 1], color='red', label='Loess Fit')
    plt.xlabel('Collection Date')
    plt.ylabel('Log10 Viral Load')

    # Set y-axis ticks and labels
    y_ticks = np.arange(1, 7)  # Adjust the range as needed
    plt.yticks(y_ticks, [f"1x10^{int(tick)}" for tick in y_ticks])

    plt.title(title)
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.tight_layout()
    plt.xticks(rotation=45)

    plt.savefig(output_filename, dpi=dpi)
    plt.close()

# Usage:
plot_viral_load_vs_time_with_loess("processed_data_ART_Naive.csv", "Viral Load vs Time (ART-Naive)", "ART_Naive_plot_loess.png")
plot_viral_load_vs_time_with_loess("processed_data_ART_Experienced.csv", "Viral Load vs Time (ART-Experienced)", "ART_Experienced_plot_loess.png")
