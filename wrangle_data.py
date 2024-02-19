import pandas as pd

df = pd.read_csv('data.csv')

# Remove the '%' and convert the Proportion column to a float
df['Proportion'] = df['Proportion'].str.rstrip('%').astype('float') / 100.0

# Compute statistics for each mutation
summary = df.groupby('Mutation').agg(
    count=('Proportion', 'size'),
    avg_proportion=('Proportion', 'mean'),
    median_proportion=('Proportion', 'median'),
    min_proportion=('Proportion', 'min'),
    max_proportion=('Proportion', 'max'),
    std_deviation=('Proportion', 'std')
)

# Convert the proportions back to percentages for the summary
summary = summary * 100
summary['avg_proportion'] = summary['avg_proportion'].round(2)
summary['std_deviation'] = summary['std_deviation'].round(2)

print(summary)
