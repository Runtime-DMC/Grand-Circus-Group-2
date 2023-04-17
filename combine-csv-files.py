import pandas as pd

# Load the CSV files into pandas dataframes
df1 = pd.read_csv('C:/Users/melbr/Desktop/dice_data_with_skills.csv')
df2 = pd.read_csv('C:/Users\melbr/Desktop/simplyhiredjobs.csv')

# Concatenate the dataframes
result = pd.concat([df1, df2])

# Write the concatenated dataframe to a new CSV file
result.to_csv('combined.csv', index=True)