
import pandas as pd
import matplotlib.pyplot as plt

df_total_jobs_by_site = pd.read_csv("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/final_combined.csv")

df_total_jobs_by_site.loc[:, 'origin']
pd.value_counts(df_total_jobs_by_site['origin'])

dice = 379
simply = 467
indeed = 836

x_labels = ['Dice.com','SimplyHired.com', 'Indeed.com']
data = [dice,simply, indeed]

plt.bar(x_labels, data)
plt.title('Job Listings by Source')
plt.xlabel('Source')
plt.ylabel('Number of Job Listings')
plt.show()
