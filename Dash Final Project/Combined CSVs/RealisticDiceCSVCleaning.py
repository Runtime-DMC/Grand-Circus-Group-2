import pandas as pd

df = pd.read_csv("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/Diced_Title_Salary_State2.csv")

# remove non-numeric characters from salary column
df["Salary"] = df["Salary"].str.replace('[^\d.]', '', regex=True)

# convert salary column to numeric
df["Salary"] = pd.to_numeric(df["Salary"], errors='coerce')

# remove decimal points from salary and convert to integer
df["Salary"] = df["Salary"].astype(int)

# update unrealistic salary types to "Yearly"
df.loc[df["Salary"] > 200, "Salary Type"] = "Yearly"

# add commas and dollar signs back to salary column
df["Salary"] = df["Salary"].apply(lambda x: '${:,.0f}'.format(x))

# save updated file to new path
df.to_csv("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/Diced_Title_Salary_State3.csv", index=False)