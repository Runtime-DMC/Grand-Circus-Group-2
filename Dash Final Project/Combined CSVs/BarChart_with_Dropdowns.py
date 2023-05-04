import plotly.express as px
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

df = pd.read_csv("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/final_combined.csv")

def get_job_type(type):
    if pd.isnull(type):
        return 'Unknown'
    elif 'remote' in type.lower():
        return 'Remote'
    elif 'hybrid' in type.lower():
        return 'Hybrid'
    else:
        return 'Onsite'
    
def get_job_title(title):
    if 'data scientist' in title.lower():
        return 'Data Scientist'
    elif 'data engineer' in title.lower():
        return 'Data Engineer'
    elif 'data architect' in title.lower():
        return 'Data Architect'
    elif 'data analyst' in title.lower():
        return 'Data Analyst'
    else:
        return 'Other'
    
def get_salary_types(salary_type):
    if pd.isnull(salary_type):
        return salary_type
    elif 'yearly' in salary_type.lower():
        return 'Yearly'
    elif 'hourly' in salary_type.lower():
        return 'Hourly'
    elif 'daily' in salary_type.lower():
        return 'Daily'
    else:
        return 'Monthly'
    
df['title'] = df['title'].apply(get_job_title)
df['salary_type'] = df['salary_type'].apply(get_salary_types)
df['salary_type'] = df['salary_type'].fillna('Unknown')
df['type'] = df['type'].apply(get_job_type)
df['type'] = df['type'].fillna('Unknown')

job_types = ['Remote', 'Hybrid', 'Onsite']
job_titles = ['Data Engineer', 'Data Analyst', 'Data Scientist', 'Data Architect']
salary_types = ['Yearly', 'Hourly', 'Daily', 'Monthly']


app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='type-dropdown',
        options=[{'label': job_type, 'value': job_type} for job_type in job_types],
        value='Onsite'
    ),
    dcc.Dropdown(
        id='title-dropdown',
        options=[{'label': job_title, 'value': job_title} for job_title in job_titles],
        value='Data Engineer'
    ),
    dcc.Dropdown(
        id='salary_type-dropdown',
        options=[{'label': salary_type, 'value': salary_type} for salary_type in salary_types],
        value='Yearly'
    ),

    dcc.Graph(id='salary-graph')
])

@app.callback(
    Output('salary-graph', 'figure'),
    [Input('type-dropdown', 'value'), Input('title-dropdown', 'value'), Input('salary_type-dropdown', 'value')]
)
def update_graph(selected_job_type, selected_job_title, selected_salary_type):
    filtered_df = df[(df['type'] == selected_job_type) & (df['title'] == selected_job_title)
    & (df['salary_type'] == selected_salary_type)]
    fig = px.bar(filtered_df, x='salary_median', y='state', color='type',
                 color_discrete_sequence=['#1f77b4', '#990099', '#6666FF'])
    fig.update_layout(xaxis_tickangle=-45, title_text='Median Salaries per Job Title', showlegend=False)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
