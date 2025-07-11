# Detailing-Bulls
🚘 Detailing Bulls - Enterprise-Grade Nationwide BI Dashboard (with Dash &amp; Plotly)

---

###                   💼 Overview

This project is a **comprehensive business intelligence dashboard** built using **Dash**, **Plotly**, and **Pandas**, designed for a fictional car detailing franchise, *Detailing Bulls*, which operates across several major Indian cities. This dashboard is a simulation of what an **enterprise-grade web-based reporting tool** would look like when used for **executive decision-making, operational monitoring, and strategic planning**.

The app is **modular**, **scalable**, and fully built in **Python** without needing JavaScript. It's ideal for data analysts, BI developers, and full-stack data science professionals looking to deliver highly interactive, real-time insights with minimal tech overhead.

---

##             📊 Live Dashboard Highlights

* ✅ Fully interactive layout using **Dash Core Components**
* 📍 Filters: Select **city**, **date range**, and **services**
* 📈 Visualizations: **Pie chart** by service revenue, **line chart** over time
* 💡 KPI Cards: Total revenue, number of transactions, average invoice
* 🗃️ Interactive table: Paginated and searchable with full transaction history
* ⚙️ Clean, professional layout (mobile-friendly with CSS customization)
* 🔁 Easy plug-in support for SQL/MongoDB or real APIs

---

## 🧠 Business Use Case

Detailing Bulls needs:

* A unified platform to view business performance by location
* A simple tool for branch managers to evaluate operations
* Real-time visualization of how each service performs
* Performance insights to support marketing, hiring, and pricing decisions

This dashboard delivers all of that by:

* Visualizing operations across 8 major cities
* Comparing service-wise contributions
* Showing revenue trends over time
* Providing transaction-level traceability

---

## 🧱 Tech Stack Used

| Tool / Library      | Purpose                                                     |
| ------------------- | ----------------------------------------------------------- |
| Dash (by Plotly)    | Web application framework for building dashboards in Python |
| Plotly Express      | High-level charting for interactive graphs                  |
| Pandas              | Data wrangling and filtering                                |
| NumPy               | Randomized data generation (synthetic dataset)              |
| Dash Table          | Component for rendering large tabular data                  |
| HTML/CSS (optional) | Additional layout & responsive UI (via `/assets`)           |

---

## 📂 Project Structure (Modular)

```
DetailingBullsDashboard/
│
├── app.py                      # Main Dash application logic
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── data/
│   └── detailing_data.csv      # Realistic synthetic dataset
│
├── components/
│   └── kpi_cards.py            # Custom KPI summary components
│
├── assets/
│   └── style.css               # Optional styling for layout
│
├── notebooks/
│   └── analysis.ipynb          # Optional EDA and data modeling
│
└── screenshots/
    └── dashboard_preview.png   # Dashboard UI preview
```

---

## 📄 Dataset Description

### ✅ `detailing_data.csv` (1500+ rows)

Generated using `NumPy` and `Pandas` to simulate real-world business operations.

| Column            | Description                                            |
| ----------------- | ------------------------------------------------------ |
| `Invoice ID`      | Unique transaction identifier (e.g., DB1021)           |
| `Date of Service` | Date of service from Jan 2023 to present               |
| `City`            | City where service was performed                       |
| `Service`         | Type of car service (Interior, Exterior, Coating)      |
| `Amount`          | Revenue generated from this transaction (₹500–₹10,000) |

---

## 💻 Code Overview

### `app.py` (Main App)

```python
# Importing required libraries
import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("data/detailing_data.csv")

# Unique cities
cities = df["City"].unique()

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Detailing Bulls Dashboard"
```

### 🔧 Layout Section

```python
app.layout = html.Div([
    html.H1("Detailing Bulls - Nationwide Dashboard", style={'textAlign': 'center'}),

    # City dropdown
    dcc.Dropdown(
        id="city-dropdown",
        options=[{"label": city, "value": city} for city in cities],
        placeholder="Select a City"
    ),

    # Date range picker
    dcc.DatePickerRange(
        id='date-picker',
        start_date=df["Date of Service"].min(),
        end_date=df["Date of Service"].max()
    ),

    # KPI Cards
    html.Div(id="kpi-container"),

    # Charts
    dcc.Graph(id="service-pie"),
    dcc.Graph(id="sales-line"),

    # Data Table
    dash_table.DataTable(
        id="transaction-table",
        columns=[{"name": col, "id": col} for col in df.columns],
        page_size=10,
        style_table={'overflowX': 'auto'}
    )
])
```

### 🔁 Callbacks for Interactivity

```python
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
    
    # Filtering
    if city:
        dff = dff[dff["City"] == city]
    if start_date and end_date:
        dff = dff[
            (dff["Date of Service"] >= start_date) &
            (dff["Date of Service"] <= end_date)
        ]

    # KPIs
    total_revenue = dff["Amount"].sum()
    transaction_count = dff.shape[0]
    avg_invoice = dff["Amount"].mean()

    kpi_layout = html.Div([
        html.Div(f"Total Revenue: ₹{total_revenue:,.2f}", style={'fontWeight': 'bold'}),
        html.Div(f"Transactions: {transaction_count}", style={'fontWeight': 'bold'}),
        html.Div(f"Average Ticket: ₹{avg_invoice:,.2f}", style={'fontWeight': 'bold'})
    ], style={'display': 'flex', 'justifyContent': 'space-around'})

    # Charts
    pie_fig = px.pie(dff, names="Service", values="Amount", title="Service Revenue Share")
    line_fig = px.line(
        dff.groupby("Date of Service")["Amount"].sum().reset_index(),
        x="Date of Service", y="Amount", title="Daily Revenue Trend"
    )

    return kpi_layout, pie_fig, line_fig, dff.to_dict("records")
```

### ▶️ Launch Server

```python
if __name__ == "__main__":
    app.run_server(debug=True)
```

---

## 📸 Screenshots

Include visuals in your GitHub repo for quick previews:

```markdown
![Dashboard Preview](screenshots/dashboard_preview.png)
```

---

## ⚙️ Installation Guide

```bash
# Clone repo
git clone https://github.com/yourusername/DetailingBullsDashboard.git
cd DetailingBullsDashboard

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Run the app
python app.py
```

Open `http://localhost:8050` in your browser.

---

## 🔮 Future Plans

* 🌐 Cloud deployment (Render, Heroku, Vercel)
* 📊 Admin login + user authentication
* 📤 PDF report export & auto-emailing
* 📱 Mobile optimization (Dash Bootstrap)
* 🔌 Database integration (MongoDB/PostgreSQL)

---

## 🤝 Contributions

You're welcome to:

* Fork the repo
* Submit pull requests
* Suggest improvements
* Open issues for bugs or feature requests

---

## 📄 License

This project is licensed under the **MIT License** — open for use, study, and extension.

---

## 🙋‍♂️ Author

Developed by **Pranjal Gurjar**
📫 Connect with me on [LinkedIn](https://linkedin.com/in/yourprofile)
💻 View more projects at [GitHub](https://github.com/yourusername)

---

