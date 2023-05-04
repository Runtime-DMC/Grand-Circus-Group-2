import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

data = pd.read_csv("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/final_clean_titles.csv")

top_states = data.groupby('state')['title'].count().nlargest(10).index.tolist()
filtered_data = data[data['state'].isin(top_states)]

# Create a function to combine job titles with the specified keywords
def combine_titles(title):
    title_lower = title.lower()
    if 'data engineer' in title_lower:
        return 'Data Engineer'
    elif 'data analyst' in title_lower:
        return 'Data Analyst'
    elif 'data scientist' in title_lower:
        return 'Data Scientist'
    elif 'data architect' in title_lower:
        return 'Data Architect'
    else:
        return title

# Apply the function to the job_title column
filtered_data['title'] = filtered_data['title'].apply(combine_titles)

# Group the data by state and job title
stacked_data = filtered_data.groupby(['state', 'title']).size().reset_index(name='count')

# Use plotly express to create a stacked bar chart with a title
fig = px.bar(stacked_data, x='state', y='count', color='title', barmode='stack', title='Top States with Most Jobs by Job Title')

# Update the layout to adjust the title position and font size
fig.update_layout(
    title={
        'x': 0.5, # Set the x position to the center of the chart
        'y': 0.95, # Set the y position just above the chart
        'font': {'size': 20} # Set the font size of the title
    }
)

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        id='stacked-bar-chart',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)