import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Load data
df = pd.read_csv('Indeed_Title_Salary_State.csv')

# Define app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("Indeed Job Title by State and Salary"),
    dcc.Dropdown(
        id='job-title-dropdown',
        options=[{'label': job_title, 'value': job_title} for job_title in df['Title'].unique()],
        value='Data Engineer'
    ),
    dcc.Graph(id='salary-graph')
])

# Define callback
@app.callback(
    Output('salary-graph', 'figure'),
    Input('job-title-dropdown', 'value')
)
def update_figure(selected_job_title):
    filtered_df = df[df['Title'] == selected_job_title]
    fig = px.scatter(
        filtered_df, x='State', y='Salary', color='Salary Type',
        title=f"{selected_job_title} Salary Data by State", 
        labels={'Salary': 'Salary ($)'},
        color_discrete_map={'Hourly': 'blue', 'Yearly': 'red'},
        hover_data={'Salary': ':$,2f'}
    )
    fig.update_traces(marker=dict(size=10))
    fig.update_layout(xaxis={'categoryorder':'array', 'categoryarray': sorted(filtered_df['State'].unique())})
    return fig

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)