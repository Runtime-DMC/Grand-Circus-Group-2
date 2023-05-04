import matplotlib.pyplot as plt
import pandas as pd

# Pie for Indeed Top 5 Job Titles
df = pd.read_csv("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/indeed_top_5_job_titles.csv")

# Group data by a specific column
grouped_data = df.groupby('title')['title'].count()

# Plot a pie chart
plt.pie(grouped_data.values, labels=grouped_data.index, autopct='%1.1f%%')
plt.axis('equal')  # Ensure the pie is drawn as a circle
plt.show()  # Display the chart


# Pie for Dice Top 5 Job Titles
df = pd.read_csv("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/dice_top_5_job_titles.csv")

# Group data by a specific column
grouped_data = df.groupby('title')['title'].count()

# Plot a pie chart
plt.pie(grouped_data.values, labels=grouped_data.index, autopct='%1.1f%%')
plt.axis('equal')  # Ensure the pie is drawn as a circle
plt.show()  # Display the chart


# Pie for Simply Hired Top 5 Job Titles
df = pd.read_csv("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/simply_hired_top_5_job_titles.csv")

# Group data by a specific column
grouped_data = df.groupby('title')['title'].count()

# Plot a pie chart
plt.pie(grouped_data.values, labels=grouped_data.index, autopct='%1.1f%%')
plt.axis('equal')  # Ensure the pie is drawn as a circle
plt.show()  # Display the chart