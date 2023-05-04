import pandas as pd
import plotly.express as px
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import base64

# Load data
df = pd.read_csv("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/final_combined.csv")

# Get the top 4 companies
top_companies = df['company'].value_counts().nlargest(4)

# Define a function to create a logo element
def make_logo(company):
    with open(f"{company}.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return html.Div([
        html.P(f"{top_companies[company]}", 
               style={'text-align': 'center', 'margin-top': '5px', 'font-size': '14px'}),
        html.Img(src=f"data:image/png;base64,{encoded_string}", 
                 style={'width': '70px', 'height': '70px'},
                 title=f"{company}: {top_companies[company]} job listings")
    ], style={'display': 'inline-block', 'text-align': 'center', 'justify-content': 'center'})

# Create app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Top Companies with Most Jobs"), width={'size': 6, 'offset': 3},
                style={'text-align': 'center', 'margin-top': '50px', 'white-space': 'nowrap'}),
    ]),
    dbc.Row([
        dbc.Col(html.H5(""), width={'size': 6, 'offset': 3},
                style={'text-align': 'center', 'margin-bottom': '35px'})
    ]),
    dbc.Row([
        dbc.Col(make_logo("Randstad Technologies"), width={'size': 3, 'offset': 1}),
        dbc.Col(make_logo("Motion Recruitment"), width={'size': 3}),
        dbc.Col(make_logo("TikTok"), width={'size': 2}),
        dbc.Col(make_logo("Comcast"), width={'size': 3}),
    ], style={'text-align': 'center', 'margin-bottom': '50px', 'justify-content': 'center'})
])

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
