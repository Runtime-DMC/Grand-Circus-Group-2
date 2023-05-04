import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

import csv

remote_count = 0
hybrid_count = 0
onsite_count = 0
total_count = 0
total_jobs_count = 0

with open("C:/Users/battl/Documents/Dash Final Project/Combined CSVs/final_combined.csv", "r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        if row['type'] != '':
            if row['type'] == 'Remote':
                remote_count += 1
            elif row['type'] == 'Hybrid':
                hybrid_count += 1
            elif row['type'] == 'Onsite':
                onsite_count += 1
            total_count += 1
        total_jobs_count += 1

remote_percent = remote_count / total_count * 100
hybrid_percent = hybrid_count / total_count * 100
onsite_percent = onsite_count / total_count * 100

# Create the cards for each job type
remote_card = dbc.Card(
    [
        dbc.CardHeader("Remote Jobs"),
        dbc.CardBody(
            [
                html.H4(f"{remote_percent:.2f}%", className="card-title"),
                html.P(f"{remote_count} out of {total_count} jobs", className="card-text"),
            ]
        ),
    ]
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
    ]
)

onsite_card = dbc.Card(
    [
        dbc.CardHeader("Onsite Jobs"),
        dbc.CardBody(
            [
                html.H4(f"{onsite_percent:.2f}%", className="card-title"),
                html.P(f"{onsite_count} out of {total_count} jobs", className="card-text"),
            ]
        ),
    ]
)

# Add the cards to your app layout
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(remote_card, width=4),
                dbc.Col(hybrid_card, width=4),
                dbc.Col(onsite_card, width=4),
            ],
            className="mt-4",
        ),
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)