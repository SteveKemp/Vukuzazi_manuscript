import pandas as pd

def summarize_data(filename, total_samples):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(filename)

    # Group by the mutation and calculate the count and mean viral load
    summary = df.groupby('Mutation').agg(
        Occurrences=('Mutation', 'size'),
        Avg_Viral_Load=('Viral Load', 'mean')
    ).reset_index()

    # Calculate the frequency of mutations as a percentage
    summary['Frequency (%)'] = (summary['Occurrences'] / total_samples) * 100
    # Format the frequency to 1 decimal place
    summary['Frequency (%)'] = summary['Frequency (%)'].round(1)

    # Sort by the number of occurrences in descending order
    summary = summary.sort_values(by='Occurrences', ascending=False)

    return summary

# Total samples for ART naive and ART experienced
total_art_naive = 467
total_art_experienced = 583

# Summarize ART-Naive data
summary_art_naive = summarize_data("processed_data_ART_Naive.csv", total_art_naive)
print("Summary for ART-Naive:\n", summary_art_naive)

# Summarize ART-Experienced data
summary_art_experienced = summarize_data("processed_data_ART_Experienced.csv", total_art_experienced)
print("\nSummary for ART-Experienced:\n", summary_art_experienced)

# Save the summarized data to separate CSV files
summary_art_naive.to_csv("summary_ART_Naive.csv", index=False)
summary_art_experienced.to_csv("summary_ART_Experienced.csv", index=False)
