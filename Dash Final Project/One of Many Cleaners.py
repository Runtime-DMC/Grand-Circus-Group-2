import pandas as pd

# Load the CSV files into pandas dataframes
df1 = pd.read_csv('C:/Users/melbr/Desktop/dice_data_with_skills.csv')
df2 = pd.read_csv('C:/Users\melbr/Desktop/simplyhiredjobs.csv')

# The concat() function from pandas is used to concatenate the two dataframes 
# df1 and df2 into a new dataframe result, stacking them on top of each other. 
# This function takes a list of dataframes to concatenate as its argument.
result = pd.concat([df1, df2])

# Write the concatenated dataframe to a new CSV file
result.to_csv('combined.csv', index=True)