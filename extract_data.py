import pandas as pd

# Load the Excel file into a DataFrame
df = pd.read_excel('Final_Vuku_Dataset.xlsx')

# Print the first few rows of the DataFrame
print(df.head())

# Check if 'collection_date' exists in the columns
if 'collection_date' not in df.columns:
    print("The column 'collection_date' does not exist!")
    print("Existing columns are:", df.columns)
    exit()

# Empty lists to store the processed rows
processed_data_art_naive = []
processed_data_art_experienced = []

# Iterate through each row in the DataFrame
for idx, row in df.iterrows():
    # Split the 'Mut' column by '|'
    mutations = str(row['Mut']).split('|')

    for mutation in mutations:
        # Check if mutation is NaN
        if mutation == 'nan':
            continue

        # Extract the mutation name and proportion
        mutation_name = mutation.split(';')[0]
        proportion = float(mutation.split(';')[-1]) * 100

        if "rtM184V" in mutation_name:
            print(f"Found rtM184V with proportion {proportion:.2f}% in row {idx}")

        # Append the processed data based on HIV_status
        data_row = {
            'Mutation': mutation_name,
            'Proportion': f'{proportion:.2f}%',
            'Collection Date': row['collection_date'],
            'Viral Load': row['vl']
        }

        if row['HIV_status'] == 'VL Detect ART Naive':
            processed_data_art_naive.append(data_row)
        elif row['HIV_status'] in ['VL Detect on ART', 'VL Detect prior ART']:
            processed_data_art_experienced.append(data_row)

# Convert the processed data into DataFrames
processed_df_art_naive = pd.DataFrame(processed_data_art_naive)
processed_df_art_experienced = pd.DataFrame(processed_data_art_experienced)

# Save the DataFrames to separate CSV files
processed_df_art_naive.to_csv("processed_data_ART_Naive.csv", index=False)
processed_df_art_experienced.to_csv("processed_data_ART_Experienced.csv", index=False)

print("ART-Naive data:\n", processed_df_art_naive)
print("\nART-Experienced data:\n", processed_df_art_experienced)
