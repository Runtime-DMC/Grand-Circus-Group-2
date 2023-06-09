# app.py
# executable dash app

# Import required libraries and modules
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from data_visualization import job_title_wordcloud, skills_wordcloud, create_bar_chart
from data_visualization import create_job_type_cards, make_logo
from callbacks import get_callbacks

# Create a Dash app instance with external_stylesheets
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
# (Above) indeed-job-title-dropdown, job-title-dropdown, indeed-salary-graph & salary-graph not found
# If you are assigning callbacks to components that are generated by other callbacks 
# (and therefore not in the initial layout), you can suppress this exception by 
# setting suppress_callback_exceptions=True`.

get_callbacks(app)

# Get the base64 encoded wordcloud image
wordcloud_base64 = job_title_wordcloud()

# Define the app layout with various components
app.layout = html.Div(style={'backgroundColor': '#e6e6fa'}, children=[
    html.Div([

    html.H1("Grand Circus Final Project - Team Die Hard", style={'text-align': 'center', 'margin-top': '50px', 'margin': '0'}),
    html.Hr(),

    # Create job type cards
    create_job_type_cards(),

    # Add a div with a specified height
    html.Div(style={'height': '30px'}),

    # Add tabs for Descriptive Analytics and Predictive Analytics
    dcc.Tabs([
        dcc.Tab(label='Descriptive Analytics', children=[
            html.Div(style={'height': '30px'}),

            #Specifying the row & columns w/ dash bootstrap components
            #Allows wordcloud images to be displayed next to each other
            dbc.Row([
                dbc.Col([
                    html.H3("Job Title Wordcloud", style={'text-align': 'center', 'margin-top': '50px'}),
                    html.Img(src='data:image/png;base64,{}'.format(job_title_wordcloud()), style={'width': '100%'})
                ], width=6),
                dbc.Col([
                    html.H3("Skills Wordcloud", style={'text-align': 'center', 'margin-top': '50px'}),
                    html.Img(src='data:image/png;base64,{}'.format(skills_wordcloud()), style={'width': '100%'})
                ], width=6)
            ]),
            html.Hr(),

            # Companies with Most Job Listings (w/ Pictures) Header & logo function calls to display pictures
            html.H2("2023 Companies with Most Data Job Listings", style={'text-align': 'center', 'margin-top': '50px'}),
            html.Div(style={'height': '20px'}),
            html.Div([
                make_logo("Randstad Technologies"),
                make_logo("Motion Recruitment"),
                make_logo("TikTok"),
                make_logo("Comcast")
            ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'margin-bottom': '50px'}),
            html.Hr(),

            # 2023 Job Listings Header
            html.H1("2023 Data Job Listings", style={'text-align': 'center', 'margin-top': '50px'}),
            html.Div(style={'height': '20px'}),

            # 2023 Job Listings Assumption section
            html.Div([
                html.H3("Assumption:"),
                html.P("Our analysis was used to compare the number of jobs in the USA organized by the state, based on all three job sites: Indeed.com, Dice.com and SimplyHired.com. The analysis started with the assumption that New York and California would have the top number of data analysis type jobs. Also, the assumption that all the states in the USA would have some data related job postings."),
            ], className="2023-assumption-section"),
            html.Div(style={'height': '20px'}),

            # Radio buttons to select between Job Listings by Source and by State
            dcc.RadioItems(
                id='job-listings-radio',
                options=[
                    {'label': 'Jobs by State', 'value': 'by_state'},
                    {'label': 'Jobs by Source', 'value': 'by_source'},
                    {'label': 'Top 10 Job States', 'value': 'highest_jobs_by_state'},
                    {'label': 'Bottom 10 Job States', 'value': 'lowest_jobs_by_state'}
                ],
                value='by_state',
                style={
                    'display': 'flex',
                    'flex-direction': 'column',
                    'align-items': 'center'
                }
            ),

            # Container for the Job Listings graph
            html.Div(id='job-listings-container'),

            # 2023 Job Listings Conclusion section
            html.Div([
                html.H3("Conclusion:"),
                # Using dcc.Markdown in a Dash app allows you to write text using Markdown syntax and have it rendered as HTML in your app.
                # The .p component uses explicit HTML tags to apply styles, while the .markdown component uses Markdown syntax for formatting the text.
                dcc.Markdown("""
                    Our analysis found that not only were New York and California the highest in tech job postings, but Texas also had a very high number of tech jobs available. It was also determined that a cluster of states (Wyoming, South Dakota and Montana) as well as Oklahoma and Hawaii have zero technology jobs available at the point of the data collection. 

                    For technology companies, there could be a potential pool of untapped technology professionals in those states. Also, if you are job-seeking, companies in California, New York and Texas would be your best options for finding potential employment. What was surprising here was that both CA and GA had the largest number of Data Architect positions, with NY being a close 3rd. In conclusion, California seems to be the best option for Data Scientist positions, while New York seems to be best option if you’re looking for a Data Analyst position.
                """)
            ], className="2023-conclusion-section"),
            html.Div(style={'height': '20px'}),
            html.Hr(),

            # Job Titles by State & Salary Header
            html.H1("2023 Prevalent Data Job Salaries", style={'text-align': 'center', 'margin-top': '50px'}),
            html.Div(style={'height': '20px'}),

            # Radio buttons to select between Simply Hired, Indeed & Dice
            dcc.RadioItems(
                id='job-source',
                options=[
                    {'label': 'Simply Hired', 'value': 'simply_hired'},
                    {'label': 'Indeed', 'value': 'indeed'},
                    {'label': 'Dice', 'value': 'dice'}
                ],
                value='simply_hired',
                style={
                    'display': 'flex',
                    'flex-direction': 'column',
                    'align-items': 'center'
                }
            ),

            # Salary by Source/State/Top 5 Title Assumption section
            html.Div([
                html.H3("Assumption:"),
                html.P("Our analysis aimed to compare the salaries of the most prevalent job titles on Indeed, Simply Hired, and Dice job websites, organized by state. The salary range was assumed to be between $75k and $110k annually, with the expectation that California would have higher salaries compared to other states due to its thriving tech industry."),
            ], className="SST-Salary-assumption-section"),
            html.Div(style={'height': '20px'}),

            html.Div(id='job-selection-container'),
            # (Above) This container is used to hold and display the content related to job selection, 
            # specifically the dropdown and the graph for job titles by state and salary.

            # Salary by Source/State/Top 5 Title Conclusion section
            html.Div([
                html.H3("Conclusion:"),
                html.P("After completing our analysis, we found that the actual salary range was higher than our initial assumption, coming in closer to $80k and $130k annually. Additionally, we discovered that Simply Hired was the only site where an entry-level position was in the top job postings. Furthermore, we found that the state of Virginia offered higher salaries compared to other states, contrary to our initial assumption about California.")
            ], className="SST-Salary-conclusion-section"),
            html.Div(style={'height': '20px'}),
            html.Hr(),
            
            # Dropdowns for median salaries per job title header
            html.H1("2023 Median Data Job Salaries", style={'text-align': 'center', 'margin-top': '50px'}),
            html.Div(style={'height': '20px'}),
            
            # Assumption for Median Salaries
            html.Div([
            html.H3("Assumption:"),
                html.P("Our analysis aimed to compare the median salaries of the most prevalent job titles on Indeed, Simply Hired, and Dice job websites, organized by state. We assumed the salary range would be between $75k and $110k annually, with the expectation that California would have higher salaries compared to other states due to its thriving tech industry."),
            ], className="median-assumption-section"),
            html.Div(style={'height': '20px'}),

            html.Div([
                dcc.Dropdown(
                    id='type-dropdown',
                    options=[{'label': job_type, 'value': job_type} for job_type in ['Remote', 'Hybrid', 'Onsite']],
                    value='Onsite',
                    style={
                        'backgroundColor': '#d1c4e9',  # Set the background color of the dropdown
                        'color': 'black',  # Set the color of the text
                    }
                ),
                dcc.Dropdown(
                    id='title-dropdown',
                    options=[{'label': job_title, 'value': job_title} for job_title in ['Data Engineer', 'Data Analyst', 'Data Scientist', 'Data Architect']],
                    value='Data Engineer',
                    style={
                        'backgroundColor': '#d1c4e9',  # Set the background color of the dropdown
                        'color': 'black',  # Set the color of the text
                    }
                ),
                dcc.Dropdown(
                    id='salary_type-dropdown',
                    options=[{'label': salary_type, 'value': salary_type} for salary_type in ['Yearly', 'Hourly']],
                    value='Yearly',
                    style={
                        'backgroundColor': '#d1c4e9',  # Set the background color of the dropdown
                        'color': 'black',  # Set the color of the text
                    }
                ),

                # Graph for Median Salaries
                dcc.Graph(id='median-salary-graph')
            ]),

            # Conclusion for Median Salaries
            html.Div([
            html.H3("Conclusion:"),
                html.P("After completing our analysis, we found that the actual salary range was higher than our initial assumption, coming in closer to $80k and $130k annually. Additionally, we discovered that Simply Hired was the only site where an entry-level position was in the top job postings. Furthermore, we found that the state of Virginia offered higher salaries compared to other states, contrary to our initial assumption about California."),
            ], className="median-conclusion-section"),
            html.Div(style={'height': '20px'}),
            html.Hr(),

            # Top 5 Job Titles by Source
            html.H1("2023 Prevalent Data Job Titles", style={'text-align': 'center', 'margin-top': '50px'}),
            html.Div(style={'height': '20px'}),

            # Assumption for Top 5 Salaries
            html.Div([
            html.H3("Assumption:"),
                html.P("The top 5 job listings by title on the job search websites Indeed, Dice, and Simply Hired are a representative sample of the overall job market for data-related positions in the United States, and provide valuable insights into the most in-demand job titles in the field. While the specific job titles listed may vary across different job search websites and platforms, the overall trends and patterns observed in this analysis are likely to be reflective of the broader job market."),
            ], className="top-five-assumption-section"),
            html.Div(style={'height': '20px'}),

            dcc.RadioItems(
                id='top-5-source-radio',
                options=[
                    {'label': 'Indeed', 'value': 'indeed'},
                    {'label': 'Simply Hired', 'value': 'simply_hired'},
                    {'label': 'Dice', 'value': 'dice'}
                ],
                value='indeed',
                style={
                    'display': 'flex',
                    'flex-direction': 'column',
                    'align-items': 'center'
                }
            ),
            html.Div(id='top-5-source-container'),

            # Conclusion for Top 5 Salaries
            html.Div([
            html.H3("Conclusion:"),
                html.P("Based on the pie charts of the top 5 job listings by title on each site, it can be concluded that Data Analyst, Data Engineer, Data Scientist, and Data Architect are among the most common job titles for data-related positions on all three job search websites. Furthermore, it appears that senior positions such as Senior Data Analyst and Senior Data Scientist are also in high demand. The presence of Entry Level Data Analyst on Simply Hired suggests that there are opportunities for those seeking entry-level positions in the field. Overall, these insights can help job seekers and employers better understand the current job market for data-related positions and make more informed decisions about their job search and hiring strategies."),
            ], className="top-five-conclusion-section"),
            html.Div(style={'height': '20px'}),
            html.Hr(),

        ], style={'backgroundColor': '#d1c4e9'}, selected_style={'backgroundColor': '#e6e6fa'}),



        #Predictive Analytics tab
        dcc.Tab(label='Predictive Analytics', children=[
            
            # Bar chart for jobs by posted_date
            html.H1("Jobs Timeline by Date", style={'text-align': 'center', 'margin-top': '50px'}),
            html.Div(style={'height': '20px'}),

            # Assumption for Jobs by Posted Date
            html.Div([
            html.H3("Assumption:"),
                html.P("Based on our analysis of job postings from January to April 2023, we predict that there will be a steady increase in the number of data-related jobs being posted throughout the remainder of the year. This trend is likely due to the growing demand for data professionals across various industries."),
            ], className="posted-date-assumption-section"),
            html.Div(style={'height': '20px'}),

            dcc.Graph(
                id='jobs-by-posted-date',
                figure=create_bar_chart()
            ),

            # Conclusion for Jobs by Posted Date
            html.Div([
            html.H3("Conclusion:"),
                html.P("Job seekers interested in data-related positions may want to consider starting their job search in the second quarter of the year. Based on our data, it appears that there is a higher likelihood of job openings being posted during this time period. Additionally, the upward trend in job postings from February to April suggests that the number of job openings will continue to rise throughout the year."),
            ], className="posted-date-conclusion-section"),
            html.Div(style={'height': '20px'}),

        ], style={'backgroundColor': '#d1c4e9'}, selected_style={'backgroundColor': '#e6e6fa'}),
    ]),

    # *****Overall Assumption/Conclusion for entire project*****
    html.Div([
        html.Div(style={'height': '20px'}),
        html.H1("Overall Assumption & Conclusion:"),
        html.Div(style={'height': '20px'}),
            dcc.Markdown("""
            Our analysis of data job postings on Indeed, Dice, and Simply Hired has provided valuable insights into the current state of the data-related job market in the United States. Our analysis has challenged some of our initial assumptions, such as the idea that California has the highest salaries in the tech industry and the assumption that every state in the US has some data-related job postings. We found that Texas also has a high number of data-related jobs, and there are some states that have no such job postings.

            Furthermore, we discovered that the most prevalent job titles for data-related positions across all three job search websites are Data Analyst, Data Engineer, Data Scientist, and Data Architect, with senior positions such as Senior Data Analyst and Senior Data Scientist also in high demand. Additionally, we found that there is a growing demand for data professionals across various industries, indicating that the data job market is likely to continue growing.

            Based on our analysis, we recommend that job seekers interested in data-related positions should start their job search in the second quarter of the year, as there is a higher likelihood of job openings being posted during this time period. The upward trend in job postings from February to April suggests that the number of job openings will continue to rise throughout the year.

            In conclusion, our analysis provides useful information for both job seekers and employers in the data-related job market. It highlights the most in-demand job titles and the states with the most job openings, as well as providing insights into salary ranges and the best time to start a job search.
            """),
        ], className="posted-date-conclusion-section")

])

])

# Starts the Dash application server & enables debug mode, which provides additional 
# information and error messages for debugging purposes.
if __name__ == '__main__':
    app.run_server(debug=True)
