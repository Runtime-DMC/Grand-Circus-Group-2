import pandas as pd

# Read the CSV files
dice = pd.read_csv("C:/Users/battl/Documents/Combined CSVs/dice_cleaned.csv")
indeed = pd.read_csv("C:/Users/battl/Documents/Combined CSVs/Indeed_cleaned.csv")
simplyhired = pd.read_csv("C:/Users/battl/Documents/Combined CSVs/simplyhiredjobs_cleaned.csv")

# Drop the unnecessary columns
columns_to_drop = {'index', 'description'}

dice.drop(columns_to_drop.intersection(dice.columns), axis=1, inplace=True)
indeed.drop(columns_to_drop.intersection(indeed.columns), axis=1, inplace=True)
simplyhired.drop(columns_to_drop.intersection(simplyhired.columns), axis=1, inplace=True)

# Standardize column names
column_mapping = {
    'job_type': 'type',
    'sal_type': 'salary_type',
    'sal_min': 'salary_min',
    'sal_max': 'salary_max',
    'sal_median': 'salary_median'
}

indeed.rename(columns=column_mapping, inplace=True)
simplyhired.rename(columns=column_mapping, inplace=True)

# Combine the datasets
combined_data = pd.concat([dice, indeed, simplyhired], ignore_index=True)

# Merge the columns
columns_to_merge = [
    'salary_min', 'salary_max', 'salary_median', 'salary_type'
]

for column in columns_to_merge:
    combined_data[column] = combineddata.apply(
        lambda row: row[column] if pd.isna(row['sal' + column.split('')[-1]]) else row['sal' + column.split('_')[-1]],
        axis=1
    )
    combineddata.drop('sal' + column.split('_')[-1], axis=1, inplace=True)

# Define the desired column order
column_order = [
    'title', 'company', 'skills', 'city', 'state', 'type', 'salary',
    'salary_type', 'salary_min', 'salary_max', 'salary_median', 'posted_date', 'origin'
]

# Reorder the columns
combined_data = combined_data[column_order]

# Remove duplicates
combined_data.drop_duplicates(inplace=True)

# Remove rows with mostly missing values
threshold = int(0.5 * len(combined_data.columns))  # 50% of the columns
combined_data.dropna(thresh=threshold, inplace=True)

# Save the combined dataset to a new CSV file
combined_data.to_csv('dice_indeed_simplyhired_combined_v2.csv', index=False)
