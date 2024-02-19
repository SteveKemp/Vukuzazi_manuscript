import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV files
art_experienced = pd.read_csv('processed_data_ART_Experienced.csv')
art_naive = pd.read_csv('processed_data_ART_Naive.csv')

# Convert the Proportion column to float by removing the '%' sign
art_experienced['Proportion'] = art_experienced['Proportion'].str.rstrip('%').astype('float')
art_naive['Proportion'] = art_naive['Proportion'].str.rstrip('%').astype('float')

# Calculate the average mutation frequency for each dataset
average_art_experienced = art_experienced.groupby('Mutation')['Proportion'].mean()
average_art_naive = art_naive.groupby('Mutation')['Proportion'].mean()

# Load mutation categories
insti_mutations = pd.read_excel("INSTI.xlsx")
nnrti_mutations = pd.read_csv("NNRTI.csv")
nrti_mutations = pd.read_excel("NRTI.xlsx")
pi_mutations = pd.read_csv("PI.csv")

# Create a dictionary of mutations with prefixes
mutation_dict = {
    'insti': ['in' + mut for mut in insti_mutations.iloc[:, 0].tolist()],
    'nnrti': ['rt' + mut for mut in nnrti_mutations.iloc[:, 0].tolist()],
    'nrti': ['rt' + mut for mut in nrti_mutations.iloc[:, 0].tolist()],
    'pi': ['pr' + mut for mut in pi_mutations.iloc[:, 0].tolist()],
}

# Define colors for each drug class
color_mapping = {
    'insti': 'red',
    'nnrti': 'blue',
    'nrti': 'green',
    'pi': 'purple'
}

# Plotting
fig, axs = plt.subplots(2, 2, figsize=(15, 15))

for ax, (key, mutations) in zip(axs.ravel(), mutation_dict.items()):
    color = color_mapping[key]

    for mutation in mutations:
        if mutation in average_art_naive.index and mutation in average_art_experienced.index:
            x = average_art_naive[mutation]
            y = average_art_experienced[mutation]
            ax.plot(x, y, 'o', color=color, label=key)
            ax.text(x+0.5, y, mutation, va='center', fontsize=8)

    ax.plot([0, 100], [0, 100], 'k--')
    ax.set_title(key.upper())
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.grid(True)

# Setting common labels
fig.text(0.5, 0.08, 'ART-Naive Average Mutation Frequency (%)', ha='center')
fig.text(0.08, 0.5, 'ART-Experienced Average Mutation Frequency (%)', va='center', rotation='vertical')
fig.suptitle('Comparison of Mutation Frequency between ART-Naive and ART-Experienced by Drug Class', fontsize=16)

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(top=0.92)

# Save the figure with a DPI of 300
plt.savefig('mutation_comparison_subplots.png', dpi=300, bbox_inches="tight")

plt.show()
