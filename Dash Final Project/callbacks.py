#callbacks.py

from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from data_visualization import create_jobs_by_source_bar_chart, create_choropleth_map, update_simply_figure
from data_visualization import get_unique_job_titles_simply, get_unique_job_titles_indeed, update_indeed_figure
from data_visualization import create_salary_box_plot, get_valid_options, update_dice_figure, get_unique_job_titles_dice
from data_visualization import indeed_pie_chart, simply_hired_pie_chart, dice_pie_chart, generate_stacked_bar_chart


def get_callbacks(app):
    # This callback updates the 'job-selection-container' based on the selected value from the 'job-source' radio buttons.
    @app.callback(
        Output('job-listings-container', 'children'),
        Input('job-listings-radio', 'value')
    )
    def update_job_listings_container(job_listings_value):
        if job_listings_value == 'by_source':
            return dcc.Graph(
                id='jobs-by-source',
                figure=create_jobs_by_source_bar_chart()
            )
        elif job_listings_value == 'by_state':
            return dcc.Graph(
                id='jobs-by-state',
                figure=create_choropleth_map()
            )
        elif job_listings_value == 'highest_jobs_by_state':
            return dcc.Graph(
                id='highest-jobs-by-state',
                figure=generate_stacked_bar_chart(top_states_flag=True, n_largest=10)
            )
        elif job_listings_value == 'lowest_jobs_by_state':
            return dcc.Graph(
                id='lowest-jobs-by-state',
                figure=generate_stacked_bar_chart(top_states_flag=False, n_smallest=10)
            )

    # This callback updates the 'job-selection-container' based on the selected value from the 'job-source' radio buttons.
    @app.callback(
        Output('job-selection-container', 'children'),
        Input('job-source', 'value')
    )
    def update_job_selection_container(job_source):
        if job_source == 'simply_hired':
            return [
                html.Div(style={'height': '20px'}),
                dcc.Dropdown(
                    id='job-title-dropdown',
                    options=[{'label': job_title, 'value': job_title} for job_title in get_unique_job_titles_simply()],
                    value='Data Engineer',
                    style={
                        'backgroundColor': '#d1c4e9',  # Set the background color of the dropdown
                        'color': 'black',  # Set the color of the text
                    }
                ),
                dcc.Graph(id='salary-graph'),
            ]
        elif job_source == 'indeed':
            return [
                html.Div(style={'height': '20px'}),
                dcc.Dropdown(
                    id='indeed-job-title-dropdown',
                    options=[{'label': job_title, 'value': job_title} for job_title in get_unique_job_titles_indeed()],
                    value='Data Engineer',
                    style={
                        'backgroundColor': '#d1c4e9',  # Set the background color of the dropdown
                        'color': 'black',  # Set the color of the text
                    }
                ),
                dcc.Graph(id='indeed-salary-graph'),
            ]
        else:  # Assuming job_source == 'dice'
            return [
                html.Div(style={'height': '20px'}),
                dcc.Dropdown(
                    id='dice-job-title-dropdown',
                    options=[{'label': job_title, 'value': job_title} for job_title in get_unique_job_titles_dice()],
                    value='Data Engineer',
                    style={
                        'backgroundColor': '#d1c4e9',  # Set the background color of the dropdown
                        'color': 'black',  # Set the color of the text
                    }
                ),
                dcc.Graph(id='dice-salary-graph'),
            ]

    # This callback updates the 'salary-graph' figure based on the selected value from the 'job-title-dropdown' (Simply Hired).
    @app.callback(
        Output('salary-graph', 'figure'),
        Input('job-title-dropdown', 'value')
    )
    def display_figure(selected_job_title):
        return update_simply_figure(selected_job_title)

    # This callback updates the 'indeed-salary-graph' figure based on the selected value from the 'indeed-job-title-dropdown'.
    @app.callback(
        Output('indeed-salary-graph', 'figure'),
        Input('indeed-job-title-dropdown', 'value')
    )
    def display_indeed_figure(selected_job_title):
        return update_indeed_figure(selected_job_title)
    
    # Add a new callback for the 'update_dice_figure' figure
    @app.callback(
        Output('dice-salary-graph', 'figure'),
        Input('dice-job-title-dropdown', 'value')
    )
    def display_dice_figure(selected_job_title):
        return update_dice_figure(selected_job_title)

    # This callback updates the 'median-salary-graph' figure based on the selected values from the dropdowns.
    @app.callback(
        Output('median-salary-graph', 'figure'),
        [Input('type-dropdown', 'value'), Input('title-dropdown', 'value'), Input('salary_type-dropdown', 'value')]
    )
    def update_salary_graph(selected_job_type, selected_job_title, selected_salary_type):
        return create_salary_box_plot(selected_job_type, selected_job_title, selected_salary_type)

    # This callback updates the options of the dropdowns to prevent invalid combinations that would result in empty graphs.
    @app.callback(
        [Output('type-dropdown', 'options'),
        Output('title-dropdown', 'options'),
        Output('salary_type-dropdown', 'options')],
        Input('type-dropdown', 'value'),
        Input('title-dropdown', 'value'),
        Input('salary_type-dropdown', 'value')
    )
    def update_dropdown_options(selected_job_type, selected_job_title, selected_salary_type):
        # Get the valid options from the data source using the imported get_valid_options function
        valid_options = get_valid_options()

        # Filter the valid options based on the current selections
        # Note: We use the OR operator (|) to include any row that matches at least one of the conditions
        valid_options = valid_options[(valid_options['type'] == selected_job_type) |
                                    (valid_options['title'] == selected_job_title) |
                                    (valid_options['salary_type'] == selected_salary_type)]

        # Extract unique values for each dropdown from the filtered valid options
        job_type_options = valid_options['type'].unique()
        job_title_options = valid_options['title'].unique()
        salary_type_options = valid_options['salary_type'].unique()

        # Return the updated dropdown options as lists of dictionaries with 'label' and 'value' keys
        return [{'label': opt, 'value': opt} for opt in job_type_options], \
            [{'label': opt, 'value': opt} for opt in job_title_options], \
            [{'label': opt, 'value': opt} for opt in salary_type_options]

    # This callback updates the 'top-5-source-container' based on the selected value from the 'top-5-source-radio'.
    @app.callback(
        Output('top-5-source-container', 'children'),
        Input('top-5-source-radio', 'value')
    )
    def update_top_5_source_container(top_5_source_value):
        if top_5_source_value == 'indeed':
            return dcc.Graph(id='indeed-top-5-pie', figure=indeed_pie_chart())
        elif top_5_source_value == 'simply_hired':
            return dcc.Graph(id='simply-hired-top-5-pie', figure=simply_hired_pie_chart())
        else:
            return dcc.Graph(id='dice-top-5-pie', figure=dice_pie_chart())