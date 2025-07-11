# app.py
import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from components.kpi_cards import generate_kpi_cards

# Load dataset
df = pd.read_csv("data/detailing_data.csv")

# Extract unique city list for dropdown
cities = sorted(df["City"].unique())

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Detailing Bulls Dashboard"

# Define layout
app.layout = html.Div([
    html.Div([
        html.H1("Detailing Bulls - Nationwide Performance Dashboard", className="main-title"),
    ], className="header"),

    html.Div([
        html.Div([
            html.Label("Select City"),
            dcc.Dropdown(
                id="city-dropdown",
                options=[{"label": c, "value": c} for c in cities],
                placeholder="Choose a city",
                className="dropdown"
            ),
        ], className="three columns"),

        html.Div([
            html.Label("Select Date Range"),
            dcc.DatePickerRange(
                id='date-picker',
                start_date=df["Date of Service"].min(),
                end_date=df["Date of Service"].max(),
                display_format='YYYY-MM-DD'
            )
        ], className="six columns")
    ], className="row filters"),

    html.Div(id="kpi-container", className="row kpis"),

    html.Div([
        html.Div([
            dcc.Graph(id="service-pie")
        ], className="six columns"),

        html.Div([
            dcc.Graph(id="sales-line")
        ], className="six columns")
    ], className="row graphs"),

    html.Div([
        html.H3("Detailed Transactions Table"),
        dash_table.DataTable(
            id="transaction-table",
            columns=[{"name": col, "id": col} for col in df.columns],
            style_table={'overflowX': 'auto'},
            page_size=10,
            style_cell={'textAlign': 'left'},
            style_header={'backgroundColor': 'black', 'color': 'white'},
        )
    ], className="data-table")
])

# Interactivity through callbacks
@app.callback(
    Output("kpi-container", "children"),
    Output("service-pie", "figure"),
    Output("sales-line", "figure"),
    Output("transaction-table", "data"),
    Input("city-dropdown", "value"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date")
)
def update_dashboard(city, start_date, end_date):
    dff = df.copy()

    # Apply filters
    if city:
        dff = dff[dff["City"] == city]
    if start_date and end_date:
        dff = dff[
            (dff["Date of Service"] >= start_date) &
            (dff["Date of Service"] <= end_date)
        ]

    # Generate KPIs
    total_revenue = dff["Amount"].sum()
    total_transactions = dff.shape[0]
    avg_ticket = dff["Amount"].mean()

    kpis = generate_kpi_cards(total_revenue, total_transactions, avg_ticket)

    # Pie Chart: Revenue by Service Type
    pie_fig = px.pie(dff, names="Service", values="Amount", title="Service-wise Revenue Distribution")

    # Line Chart: Daily Revenue Trend
    daily_sales = dff.groupby("Date of Service")["Amount"].sum().reset_index()
    line_fig = px.line(daily_sales, x="Date of Service", y="Amount", title="Daily Revenue Trend")

    # Return table data
    table_data = dff.to_dict("records")

    return kpis, pie_fig, line_fig, table_data

# Run server
if __name__ == "__main__":
    app.run_server(debug=True)
