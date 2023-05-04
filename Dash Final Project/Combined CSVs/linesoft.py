import pandas as pd
import plotly.express as px
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

# Create dataframe
df = pd.DataFrame({
    'soft_skill': ['Organized', 'Communication', 'Leadership', 'Creativity', 'Integrity', 'Humility', 'Teamwork', 'Responsibility', 'Problem-solving', 'Adaptability', 'Self-management'],
    '2023': [212, 45, 28, 25, 17, 10, 8, 7, 6, 6, 2],
    '2024': [220, 50, 30, 50, 20, 12, 25, 8, 7, 15, 3],
    '2025': [230, 60, 35, 150, 25, 15, 35, 20, 8, 25, 4],
    '2026': [250, 75, 40, 250, 30, 18, 50, 26, 9, 50, 5],
    '2027': [280, 110, 60, 280, 50, 20, 90, 45, 10, 110, 6]
})

# Rename column
df = df.rename(columns={'soft_skill': 'Soft skills'})

# Melt dataframe to long format
df_melted = pd.melt(df, id_vars=['Soft skills'], var_name='year', value_name='count')

# Create animated bubble chart
fig = px.scatter(df_melted, x='Soft skills', y='count', size='count', color='Soft skills', animation_frame='year', animation_group='Soft skills', range_y=[0, 300], log_y=False)

# Set marker opacity and line width
fig.update_traces(marker=dict(opacity=0.8, line=dict(width=0.5, color='DarkSlateGrey')))

# Set layout
fig.update_layout(
    xaxis=dict(title='Soft Skill'),
    yaxis=dict(title='Popularity'),
    title='Soft Skill Growth Over Time',
    font=dict(size=18),
    hovermode='closest',
    updatemenus=[dict(
        type='buttons',
        showactive=False,
        buttons=[dict(
            label='Play',
            method='animate',
            args=[None, dict(frame=dict(duration=500, redraw=True), fromcurrent=True, transition=dict(duration=0))]
        ), dict(
            label='Pause',
            method='animate',
            args=[[None], dict(frame=dict(duration=0, redraw=False), mode='immediate', transition=dict(duration=0))]
        )]
    )]
)

# Create Dash app
app = dash.Dash(__name__)

# Add figure to app
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
