# data_visualization.py
# module for data visualization

# Import necessary libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import dash_bootstrap_components as dbc
import numpy as np
from PIL import Image
import base64
import io
from dash import html

# Function to create job type cards (Onsite, Remote, Hybrid)
def create_job_type_cards():
    # Read the CSV file and count the number of jobs for each job type
    df = pd.read_csv("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/final_combined.csv")

    onsite_count = df[df['type'] == 'Onsite'].shape[0]
    remote_count = df[df['type'] == 'Remote'].shape[0]
    hybrid_count = df[df['type'] == 'Hybrid'].shape[0]
    total_count = onsite_count + remote_count + hybrid_count

    onsite_percent = onsite_count / total_count * 100
    remote_percent = remote_count / total_count * 100
    hybrid_percent = hybrid_count / total_count * 100

    onsite_card = dbc.Card(
        [
            dbc.CardHeader("Onsite Jobs"),
            dbc.CardBody(
                [
                    html.H4(f"{onsite_percent:.2f}%", className="card-title"),
                    html.P(f"{onsite_count} out of {total_count} jobs", className="card-text"),
                ]
            ),
        ], style={'backgroundColor': '#d1c4e9'}
    )

    remote_card = dbc.Card(
        [
            dbc.CardHeader("Remote Jobs"),
            dbc.CardBody(
                [
                    html.H4(f"{remote_percent:.2f}%", className="card-title"),
                    html.P(f"{remote_count} out of {total_count} jobs", className="card-text"),
                ]
            ),
        ], style={'backgroundColor': '#d1c4e9'}
    )

    hybrid_card = dbc.Card(
        [
            dbc.CardHeader("Hybrid Jobs"),
            dbc.CardBody(
                [
                    html.H4(f"{hybrid_percent:.2f}%", className="card-title"),
                    html.P(f"{hybrid_count} out of {total_count} jobs", className="card-text"),
                ]
            ),
        ], style={'backgroundColor': '#d1c4e9'}
    )

    return dbc.Row([
        dbc.Col(onsite_card, width=4),
        dbc.Col(remote_card, width=4),
        dbc.Col(hybrid_card, width=4)
    ], className="mt-4")

# Bar Chart for Jobs by Source
def create_jobs_by_source_bar_chart():
    df_total_jobs_by_site = pd.read_csv("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/final_combined.csv")
    job_counts = pd.value_counts(df_total_jobs_by_site['origin']).to_frame(name='job_count').reset_index()
    job_counts.rename(columns={'index': 'origin'}, inplace=True)

    num_unique_sources = len(job_counts['origin'].unique())
    custom_viridis_colors = create_custom_viridis_color_scale(num_unique_sources)

    fig = go.Figure(go.Bar(
        x=job_counts['origin'],
        y=job_counts['job_count'],
        text=job_counts['job_count'],
        textposition='auto',
        marker_color=custom_viridis_colors
    ))

    fig.update_layout(
        xaxis_title='Source',
        yaxis_title='Number of Job Listings',
        plot_bgcolor='#e6e6fa', 
        paper_bgcolor='#e6e6fa',
    )

    return fig

# Choropleth map for # of jobs by state
def create_choropleth_map():
     # Read the CSV file and create a choropleth map for the number of jobs by state
    df_median_salary = pd.read_csv("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/state_count.csv")

    fig = go.Figure(data=go.Choropleth(
        locations=df_median_salary['state'],
        z=df_median_salary['job_count'].astype(int),
        locationmode='USA-states',
        colorscale='Viridis',
        colorbar_title="# of Jobs",
    ))

    fig.update_layout(
        geo_scope='usa',
        plot_bgcolor='#e6e6fa', 
        paper_bgcolor='#e6e6fa',
        geo=dict(bgcolor='#e6e6fa')
    )

    return fig

# Scatterplot from Simply Hired
df_simply = pd.read_csv("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/SimplyHired_Title_Salary_State.csv")
df_simply['State'] = df_simply['State'].str.upper()
df_simply['State'] = df_simply['State'].apply(lambda x: 'RE' if 'USA' in x else x)

# Function to get unique job titles from Simply Hired
def get_unique_job_titles_simply():
    #.filter(lambda x: len(x) > 0) filters out any groups that have no data (i.e. have a length of 0).
    job_titles_with_data = df_simply.groupby('Title').filter(lambda x: len(x) > 0)['Title'].unique()
    return job_titles_with_data

def update_simply_figure(selected_job_title):
    # Filter the DataFrame by selected job title and create a scatter plot for salary data by state
    filtered_df = df_simply[df_simply['Title'] == selected_job_title]
    fig = px.scatter(
        filtered_df, x='State', y='Salary', color='Salary Type',
        # title=f"{selected_job_title} Salary Data by State", 
        labels={'Salary': 'Salary ($)'},
        color_discrete_map={'Hourly': 'purple', 'Yearly': 'teal'},
        hover_data={'Salary': ':$,2f'},
        category_orders={'Salary Type': ['Yearly', 'Hourly']}
    )
    fig.update_traces(marker=dict(size=10))
    fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': sorted(filtered_df['State'].unique())},
                      yaxis={'type': 'log', 'autorange': True},
                      plot_bgcolor='#e6e6fa', 
                      paper_bgcolor='#e6e6fa',
                      )
    return fig

# Scatterplot from Indeed
df_indeed = pd.read_csv("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/Indeed_Title_Salary_State.csv")
df_indeed['State'] = df_indeed['State'].str.upper()
df_indeed['State'] = df_indeed['State'].apply(lambda x: 'RE' if 'UNITED STATES' in x else x)

# Function to get unique job titles from Indeed
def get_unique_job_titles_indeed():
    #.filter(lambda x: len(x) > 0) filters out any groups that have no data (i.e. have a length of 0).
    job_titles_with_data = df_indeed.groupby('Title').filter(lambda x: len(x) > 0)['Title'].unique()
    return job_titles_with_data

def update_indeed_figure(selected_job_title):
    # Filter the DataFrame by selected job title and create a scatter plot for salary data by state
    filtered_df = df_indeed[df_indeed['Title'] == selected_job_title]
    fig = px.scatter(
        filtered_df, x='State', y='Salary', color='Salary Type',
        # title=f"{selected_job_title} Salary Data by State",
        labels={'Salary': 'Salary ($)'},
        color_discrete_map={'Hourly': 'purple', 'Yearly': 'teal'},
        hover_data={'Salary': ':$,2f'},
        category_orders={'Salary Type': ['Yearly', 'Hourly']}
    )
    fig.update_traces(marker=dict(size=10))
    fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': sorted(filtered_df['State'].unique())},
                      yaxis={'type': 'log', 'autorange': True},
                      plot_bgcolor='#e6e6fa', 
                      paper_bgcolor='#e6e6fa',
                      )
    return fig

#Scatterplot from Dice
df_dice = pd.read_csv("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/Diced_Title_Salary_State3.csv")

# Function to get unique job titles from Indeed
def get_unique_job_titles_dice():
    #.filter(lambda x: len(x) > 0) filters out any groups that have no data (i.e. have a length of 0).
    job_titles_with_data = df_dice.groupby('Title').filter(lambda x: len(x) > 0)['Title'].unique()
    return job_titles_with_data

def update_dice_figure(selected_job_title):
    filtered_df = df_dice[df_dice['Title'] == selected_job_title]
    fig = px.scatter(
        filtered_df, x='State', y='Salary', color='Salary Type',
        # title=f"{selected_job_title} Salary Data by State", 
        labels={'Salary': 'Salary ($)'},
        color_discrete_map={'Hourly': 'purple', 'Yearly': 'teal'},
        hover_data={'Salary': ':$,2f'},
        category_orders={'Salary Type': ['Yearly', 'Hourly']}
    )
    fig.update_traces(marker=dict(size=10))
    fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': sorted(filtered_df['State'].unique())},
                      yaxis={'type': 'log', 'autorange': True},
                      plot_bgcolor='#e6e6fa', 
                      paper_bgcolor='#e6e6fa',
                      )
    return fig

# Bar chart by posted date
def create_bar_chart():
    # Read the CSV file and create a bar chart for the number of jobs by posted date
    df_new2 = pd.read_csv("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/final_combined.csv")
    df_new2['posted_date'] = pd.to_datetime(df_new2['posted_date'])
    df_new2 = df_new2.groupby('posted_date').count()
    df_new2.reset_index(inplace=True)

    # Get a Viridis colorscale
    viridis_colors = px.colors.sequential.Viridis * (len(df_new2) // len(px.colors.sequential.Viridis) + 1)
    viridis_colors = viridis_colors[:len(df_new2)]

    # Create the bar chart
    fig = go.Figure()

    fig.add_trace(go.Bar(x=df_new2['posted_date'],
                         y=df_new2['title'],
                         name='Number of Jobs',
                         marker=dict(color=viridis_colors)))  # Use Viridis colors for the bar chart

    # Create the trendline
    z = np.polyfit(df_new2.index, df_new2['title'], 1)
    p = np.poly1d(z)

    trendline_values = p(df_new2.index)
    trendline_values[trendline_values < 0] = 0  # Truncate the trendline at zero

    fig.add_trace(go.Scatter(x=df_new2['posted_date'],
                             y=trendline_values,
                             mode='lines',
                             name='Trendline',
                             line=dict(color='black', dash='dot')))

    # Update axis labels
    fig.update_layout(xaxis_title='Posted Date',
                      yaxis_title='Number of Jobs',
                      plot_bgcolor='#e6e6fa',
                      paper_bgcolor='#e6e6fa',
                      )

    return fig

# Bar chart by the job type, the job title, and the salary type. Outputs the states and the median salary
df_median_salary = pd.read_csv("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/final_combined.csv")

# Functions to process the data for the box plot
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
        return None

def get_job_type(job_type):
    if pd.isnull(job_type):
        return None
    elif 'remote' in job_type.lower():
        return 'Remote'
    elif 'hybrid' in job_type.lower():
        return 'Hybrid'
    else:
        return 'Onsite'

def get_salary_types(salary_type, salary_value):
    if pd.isnull(salary_type):
        return None
    elif 'yearly' in salary_type.lower():
        return 'Yearly'
    elif 'hourly' in salary_type.lower():
        if salary_value > 500:  # Assuming an unrealistic hourly wage, move to yearly
            return 'Yearly'
        return 'Hourly'
    else:
        return None

def convert_salary(salary):
    if not pd.isnull(salary):
        salary = salary.strip().replace(",", "")
        if not salary.startswith("$"):
            salary = "$" + salary
        return salary
    return np.nan

# Process the DataFrame to prepare the data for the Box Plot
def data_processing(df):
    # Applies the get_job_title function.
    df['title'] = df['title'].apply(get_job_title)
    # The lambda function checks if the value in each row of the column is not null (pd.notnull(x)), and if it's not, it converts the value to lowercase using the lower() method of the string object. If the value is null, it leaves it unchanged.
    df['salary_type'] = df['salary_type'].apply(lambda x: x.lower() if pd.notnull(x) else x)
    # Converts the salary_median column of the DataFrame df to a numeric data type using the pd.to_numeric() function. The errors='coerce' parameter tells the function to convert any non-numeric values to NaN.
    df['salary_median'] = pd.to_numeric(df['salary_median'], errors='coerce')
    # The lambda function takes the salary_type and salary_median values from each row and passes them to the get_salary_types function.
    df['salary_type'] = df.apply(lambda row: get_salary_types(row['salary_type'], row['salary_median']), axis=1)
    # This line applies the get_job_type function to the 'type' column of the DataFrame.
    df['type'] = df['type'].apply(get_job_type)
    # This line drops any rows from the DataFrame df that have missing values (NaN) in the title, type, salary_type, or salary_median columns.
    df = df.dropna(subset=['title', 'type', 'salary_type', 'salary_median'])
    
    # Add these lines to update the DataFrame
    df.loc[(df['state'] == 'USA') & (df['type'] == 'Onsite'), 'type'] = 'Remote'
    df.loc[(df['state'] == 'USA') & (df['type'] == 'Remote'), 'state'] = 'RE'
    
    return df

# Apply the data_processing function to your DataFrame
df_median_salary = data_processing(df_median_salary)

# Remove invalid combinations of job type, job title, and salary type from the DataFrame
def remove_invalid_combinations(df):
    invalid_combinations = [
        ('Remote', 'Data Architect', 'Hourly'),
        ('Remote', 'Data Scientist', 'Hourly'),
        ('Remote', 'Data Engineer', 'Yearly'),
        ('Hybrid', 'Data Architect', 'Hourly'),
        ('Hybrid', 'Data Architect', 'Yearly'),
        ('Hybrid', 'Data Scientist', 'Hourly'),
        ('Hybrid', 'Data Analyst', 'Hourly')
    ]

    for job_type, job_title, salary_type in invalid_combinations:
        df = df[~((df['type'] == job_type) & (df['title'] == job_title) & (df['salary_type'] == salary_type))]
    # (Above For-Loop) For each tuple in the list, the loop unpacks the three values 
    # into the variables job_type, job_title, and salary_type.

    # The code then filters out any rows in the df DataFrame that match the current tuple by 
    # creating a boolean mask with the conditions df['type'] == job_type, df['title'] == job_title, 
    # and df['salary_type'] == salary_type, and using the ~ (tilde) operator to invert the mask. 
    # This effectively selects all rows in the DataFrame that do not match the current tuple.

    return df

# Get the valid options for job type, job title, and salary type from the DataFrame
def get_valid_options():
    df = df_median_salary.copy()
    df = remove_invalid_combinations(df)
    return df

job_types = ['Remote', 'Hybrid', 'Onsite']
job_titles = ['Data Engineer', 'Data Analyst', 'Data Scientist', 'Data Architect']
salary_types = ['Yearly', 'Hourly']

# Function to filter the DataFrame by selected job type, job title, and salary type, then create a box plot for median salaries by state
def create_salary_box_plot(selected_job_type, selected_job_title, selected_salary_type):
    valid_options = get_valid_options()
    filtered_df = valid_options[(valid_options['type'] == selected_job_type) & (valid_options['title'] == selected_job_title)
                                   & (valid_options['salary_type'] == selected_salary_type)]

    if filtered_df.empty:
        return go.Figure().update_layout(title_text="No data available for the selected combination",
                                         plot_bgcolor='#e6e6fa', 
                                         paper_bgcolor='#e6e6fa',
                                         xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
                                         yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
                                         showlegend=False,
                                         margin=dict(l=0, r=0, t=30, b=0),
                                         )

    filtered_df = filtered_df.sort_values(by='salary_median', ascending=False)

    # Get a Viridis colorscale
    viridis_colors = px.colors.sequential.Viridis

    # Get the unique states and calculate the number of states
    states = filtered_df['state'].unique()
    num_states = len(states)

    # Assign a Viridis color to each state
    state_colors = {state: viridis_colors[i * len(viridis_colors) // num_states] for i, state in enumerate(states)}

    # Create a boxplot with colorful boxes
    fig = go.Figure()

    for state in states:
        fig.add_trace(go.Box(
            y=filtered_df[filtered_df['state'] == state]['salary_median'],
            name=state,
            marker_color=state_colors[state],
        ))

    # Update axis labels and format
    fig.update_layout(xaxis_tickangle=-45, showlegend=False, plot_bgcolor='#e6e6fa', paper_bgcolor='#e6e6fa')
    fig.update_yaxes(tickprefix="$", tickformat=",.")
    if selected_salary_type == 'Yearly':
        fig.update_yaxes(tickformat=",.0f")
    elif selected_salary_type == 'Hourly':
        fig.update_yaxes(tickformat=",.2f")

    return fig

# Function to create a wordcloud for job titles
def job_title_wordcloud():
    # Read in the CSV file containing top words for job titles
    words = pd.read_csv(r"C:/Users/battl/Documents/Dash Final Project/Combined CSVs/top_words.csv")
    comment_words = ''
    stopwords = set(STOPWORDS)

    # Process words from the CSV file
    for val in words.word:
        val = str(val)
        tokens = val.split()
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        comment_words += " ".join(tokens)+" "

    # Load the image mask for the wordcloud
    mask = Image.open("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/PythonSymbol.png")
    mask = mask.resize((800, 800), resample=Image.BILINEAR)
    mask = np.array(mask)
    # Generate the wordcloud
    wordcloud = WordCloud(width=mask.shape[1], height=mask.shape[0],
                background_color ='#E6E6FA',
                stopwords = stopwords,
                min_font_size = 10,
                mask = mask,
                contour_width=3,
                contour_color='#000033').generate(comment_words)

    # Convert the wordcloud to an image and encode it as a base64 string
    img = Image.fromarray(wordcloud.to_array())
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

    return img_base64

# Function to create a wordcloud for skills
def skills_wordcloud():
    # Read in the CSV file containing sorted skills
    skills = pd.read_csv(r"C:/Users/battl/Documents/Dash Final Project/Combined CSVs/sorted_skills.csv")
    comment_words = ''
    stopwords = set(STOPWORDS)

    # Process skills from the CSV file
    for val in skills.skill:
        val = str(val)
        tokens = val.split()
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        comment_words += " ".join(tokens)+" "

    # Load the image mask for the wordcloud
    mask = Image.open("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/stormtrooper_mask.png")
    mask = mask.resize((800, 800), resample=Image.BILINEAR)
    mask = np.array(mask)
    # Generate the wordcloud
    wordcloud = WordCloud(width=mask.shape[1], height=mask.shape[0],
                background_color ='#E6E6FA',
                stopwords = stopwords,
                min_font_size = 10,
                mask = mask,
                contour_width=3,
                contour_color='#000033').generate(comment_words)

    # Convert the wordcloud to an image and encode it as a base64 string
    img = Image.fromarray(wordcloud.to_array())
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

    return img_base64

# Function to create a pie chart for top 5 job titles
def create_pie_chart(df):
    grouped_data = df.groupby('title')['title'].count()
    
    num_unique_titles = len(grouped_data.unique()) 
    custom_viridis_colors = create_custom_viridis_color_scale(num_unique_titles)

    fig = go.Figure(
        go.Pie(labels=grouped_data.index,
               values=grouped_data.values,
               textinfo='label+percent',
               insidetextorientation='radial',
               marker=dict(colors=custom_viridis_colors))  # Use Viridis colors for the pie chart
    )

    fig.update_layout(plot_bgcolor='#e6e6fa', paper_bgcolor='#e6e6fa')
    
    return fig

# Function to create a pie chart for Indeed job titles
def indeed_pie_chart():
    df = pd.read_csv("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/indeed_top_5_job_titles.csv")
    return create_pie_chart(df)

# Function to create a pie chart for Dice job titles
def dice_pie_chart():
    df = pd.read_csv("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/dice_top_5_job_titles.csv")
    return create_pie_chart(df)

# Function to create a pie chart for Simply Hired job titles
def simply_hired_pie_chart():
    df = pd.read_csv("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/simply_hired_top_5_job_titles.csv")
    return create_pie_chart(df)

# Function to normalize the job roles (Cleaning/Filtering purposes)
# Used in the Stacked Bar Chart below.
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
    
def create_custom_viridis_color_scale(num_colors):
    viridis_colors = np.array(px.colors.sequential.Viridis)
    indices = np.linspace(0, len(viridis_colors) - 1, num=num_colors, dtype=int)
    custom_viridis_colors = viridis_colors[indices].tolist()
    return custom_viridis_colors

# Function to generate a stacked bar chart
def generate_stacked_bar_chart(top_states_flag=True, n_largest=None, n_smallest=None):
    data = pd.read_csv("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/final_clean_titles.csv")
    
    # Remove rows with NaN values in the 'state' column
    data = data.dropna(subset=['state'])

    # Check if the chart is for the top or bottom states based on the number of jobs
    if top_states_flag:
        if n_largest:
            states = data.groupby('state')['title'].count().nlargest(n_largest).index.tolist()
        else:
            states = data['state'].unique()
        #chart_title = 'Top States with Most Jobs by Job Title'
    else:
        if n_smallest:
            states = data.groupby('state')['title'].count().nsmallest(n_smallest).index.tolist()
        else:
            states = data['state'].unique()
        #chart_title = 'Top States with Least Jobs by Job Title'

    # Filter data for selected states
    filtered_data = data[data['state'].isin(states)]
    filtered_data['title'] = filtered_data['title'].apply(combine_titles)
    stacked_data = filtered_data.groupby(['state', 'title']).size().reset_index(name='count')

    # Sort the stacked_data dataframe by the state column based on the count of job titles
    total_jobs_by_state = data.groupby('state')['title'].count()
    states_sorted = total_jobs_by_state.loc[states].sort_values(ascending=False).index.tolist()

    num_unique_titles = len(stacked_data['title'].unique())
    custom_viridis_colors = create_custom_viridis_color_scale(num_unique_titles)

    # Create the stacked bar chart
    fig = px.bar(stacked_data, x='state', y='count', color='title', barmode='stack',
                 color_discrete_sequence=custom_viridis_colors,
                 category_orders={'state': states_sorted})
    
    fig.update_layout(title={'x': 0.5, 'y': 0.95, 'font': {'size': 20}})

    fig.update_xaxes(title_text="State")
    fig.update_yaxes(title_text="Number of Job Listings")
    fig.update_layout(legend_title_text="Job Title", plot_bgcolor='#e6e6fa', paper_bgcolor='#e6e6fa')

    return fig

# Read in the CSV file containing the final combined data to count values for top companies
df_logo = pd.read_csv("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/final_combined.csv")
# Counts the company name values and keeps the 4 largest.
top_companies = df_logo['company'].value_counts().nlargest(4)

# Function to create a logo with the job listing
def make_logo(company):
    image_path = ""
    # Set the image path based on the company name
    if company == "Randstad Technologies":
        image_path = "C:/Users/battl/Documents/Dash Final Project/Combined CSVs/Randstad_Technologies.png"
    elif company == "Motion Recruitment":
        image_path = "C:/Users/battl/Documents/Dash Final Project/Combined CSVs/Motion_Recruitment.png"
    elif company == "TikTok":
        image_path = "C:/Users/battl/Documents/Dash Final Project/Combined CSVs/TikTok.png"
    elif company == "Comcast":
        image_path = "C:/Users/battl/Documents/Dash Final Project/Combined CSVs/Comcast.png"

    # Get the job listing count for the specified company
    count = top_companies[company]
    
    # Read the company logo image file and encode it as a base64 string
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Return an HTML Div containing the company logo and the job listing count
    return html.Div([
        html.P(f"{count}", 
               style={'text-align': 'center', 'margin-top': '5px', 'font-size': '14px',
                      'display': 'block', 'width': '70px', 'margin': '0 auto'}),
        html.Img(src=f"data:image/png;base64,{encoded_string}", 
                 style={'max-width': '150px', 'max-height': '150px', 'object-fit': 'contain'},
                 title=f"{company}: {count} job listings")
    ], style={'display': 'inline-block', 'text-align': 'center', 'justify-content': 'center', 'vertical-align': 'top'})
