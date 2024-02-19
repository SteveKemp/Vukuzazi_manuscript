import pandas as pd
import matplotlib.pyplot as plt

# Load the rule sets from the files
insti_rules = pd.read_excel('INSTI.xlsx')['Rule'].tolist()
nnrti_rules = pd.read_csv('NNRTI.csv')['Rule'].tolist()
nrti_rules = pd.read_excel('NRTI.xlsx')['Rule'].tolist()
pi_rules = pd.read_csv('PI.csv')['Rule'].tolist()

# Create a mapping based on prefix
prefix_mapping = {
    "in": insti_rules,
    "rt_nnrti": nnrti_rules,
    "rt_nrti": nrti_rules,
    "pr": pi_rules
}

def categorize_mutation(mutation):
    # Get the prefix of the mutation
    prefix = mutation[:2]  # Assuming the format is like "rtK103N", so we take the first two characters

    if prefix == "rt":
        if mutation[2:] in nnrti_rules:
            return "rt_nnrti"
        elif mutation[2:] in nrti_rules:
            return "rt_nrti"
    elif prefix == "pr" and mutation[2:] in pi_rules:
        return "pr"
    elif prefix == "in" and mutation[2:] in insti_rules:
        return "in"

    print(f"{mutation} not categorized")  # Debug line for any uncategorized mutations
    return None

# Read the CSV files into pandas DataFrames
experienced_df = pd.read_csv("summary_ART_Experienced.csv")
naive_df = pd.read_csv("summary_ART_Naive.csv")

# Categorize mutations
experienced_df['Category'] = experienced_df['Mutation'].apply(categorize_mutation)
naive_df['Category'] = naive_df['Mutation'].apply(categorize_mutation)

# Merge and plot for NNRTI and NRTI separately
for category in ["rt_nnrti", "rt_nrti"]:
    merged_df = pd.merge(
        experienced_df[experienced_df['Category'] == category],
        naive_df[naive_df['Category'] == category],
        on="Mutation", how="inner", suffixes=('_exp', '_naive')
    )

    print(f"Shared Mutations for {category}:")
    print(merged_df)
    print("\n" + "="*50 + "\n")

    # Extract shared mutation frequencies for plotting
    x_values = merged_df["Frequency (%)_exp"]
    y_values = merged_df["Frequency (%)_naive"]
    labels = merged_df["Mutation"]

    # Plotting
    plt.figure(figsize=(10, 10))
    plt.scatter(x_values, y_values, color='blue')
    plt.title(f'Shared Mutations ({category}): Experienced vs Naive')
    plt.xlabel('Experienced Frequency (%)')
    plt.ylabel('Naive Frequency (%)')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Annotate each point with its mutation label
    for i, label in enumerate(labels):
        plt.annotate(label, (x_values[i], y_values[i]), fontsize=9, ha='right')

    plt.show()
