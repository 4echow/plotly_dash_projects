import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Sample Data
df_timeseries = pd.DataFrame(
    {
        "Date": pd.date_range(start="2023-01-01", periods=365, freq="D"),
        "Value1": np.random.randn(365).cumsum(),
        "Value2": np.random.randn(365).cumsum(),
    }
)


# Function to create 12 marks for the slider, corresponding to the months
def create_marks(df):
    n_marks = 12  # We want exactly 12 marks
    step = len(df) // n_marks  # Calculate step size to pick 12 evenly spaced dates
    marks = {
        i: date.strftime("%b %Y") for i, date in enumerate(df["Date"]) if i % step == 0
    }
    return marks


df_boxplot = pd.DataFrame(
    {
        "Category": pd.Categorical(np.random.choice(["A", "B", "C", "D"], size=200)),
        "Value": np.random.randn(200),
    }
)

df_bar = pd.DataFrame(
    {
        "Category": ["A", "B", "C", "D", "E", "F"],
        "Value1": np.random.randint(1, 100, 6),
        "Value2": np.random.randint(1, 100, 6),
    }
)


# Initialize Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(
    [
        html.H1("Dashboard with Interactive Graphs", style={"textAlign": "center"}),
        # First row with two time series graphs and their respective sliders
        html.Div(
            className="row",
            children=[
                # Card 1: Time Series Graph 1 with its slider
                html.Div(
                    className="card",
                    children=[
                        html.H3("Time Series Graph 1", className="card-header"),
                        dcc.RangeSlider(
                            id="date-slider1",
                            min=0,
                            max=len(df_timeseries) - 1,
                            value=[0, len(df_timeseries) - 1],
                            step=1,
                            marks=create_marks(df_timeseries),
                        ),
                        dcc.Graph(id="timeseries-graph1"),
                    ],
                    style={
                        "width": "32%",
                        "display": "inline-block",
                        "padding": "10px",
                    },
                ),
                # Card 2: Time Series Graph 2 with its slider
                html.Div(
                    className="card",
                    children=[
                        html.H3("Time Series Graph 2", className="card-header"),
                        dcc.RangeSlider(
                            id="date-slider2",
                            min=0,
                            max=len(df_timeseries) - 1,
                            value=[0, len(df_timeseries) - 1],
                            step=1,
                            marks=create_marks(df_timeseries),
                            included=False,
                        ),
                        dcc.Graph(id="timeseries-graph2"),
                    ],
                    style={
                        "width": "32%",
                        "display": "inline-block",
                        "padding": "10px",
                    },
                ),
                # Card 3: Box Plot 1
                html.Div(
                    className="card",
                    children=[
                        html.H3("Box Plot 1", className="card-header"),
                        dcc.Graph(id="boxplot1"),
                    ],
                    style={
                        "width": "32%",
                        "display": "inline-block",
                        "padding": "10px",
                    },
                ),
            ],
        ),
        # Second row with three more box plots
        html.Div(
            className="row",
            children=[
                # Card 4: Box Plot 2
                html.Div(
                    className="card",
                    children=[
                        html.H3("Box Plot 2", className="card-header"),
                        dcc.Graph(id="boxplot2"),
                    ],
                    style={
                        "width": "32%",
                        "display": "inline-block",
                        "padding": "10px",
                    },
                ),
                # Card 5: Bar Plot 1
                html.Div(
                    className="card",
                    children=[
                        html.H3("Bar Plot 1", className="card-header"),
                        dcc.Graph(id="barplot1"),
                    ],
                    style={
                        "width": "32%",
                        "display": "inline-block",
                        "padding": "10px",
                    },
                ),
                # Card 6: Bar Plot 2
                html.Div(
                    className="card",
                    children=[
                        html.H3("Bar Plot 2", className="card-header"),
                        dcc.Graph(id="barplot2"),
                    ],
                    style={
                        "width": "32%",
                        "display": "inline-block",
                        "padding": "10px",
                    },
                ),
            ],
        ),
    ]
)


# Define callbacks to update the time series graphs
@app.callback(Output("timeseries-graph1", "figure"), Input("date-slider1", "value"))
def update_timeseries_graph1(slider_range):
    start_date = df_timeseries["Date"].iloc[slider_range[0]]
    end_date = df_timeseries["Date"].iloc[slider_range[1]]

    filtered_df = df_timeseries[
        (df_timeseries["Date"] >= start_date) & (df_timeseries["Date"] <= end_date)
    ]

    fig = px.line(filtered_df, x="Date", y="Value1", title="Time Series Graph 1")
    return fig


@app.callback(Output("timeseries-graph2", "figure"), Input("date-slider2", "value"))
def update_timeseries_graph2(slider_range):
    start_date = df_timeseries["Date"].iloc[slider_range[0]]
    end_date = df_timeseries["Date"].iloc[slider_range[1]]

    filtered_df = df_timeseries[
        (df_timeseries["Date"] >= start_date) & (df_timeseries["Date"] <= end_date)
    ]

    fig = px.line(filtered_df, x="Date", y="Value2", title="Time Series Graph 2")
    return fig


# Define callbacks to update the box plot graphs
@app.callback(
    Output("boxplot1", "figure"),
    Output("boxplot2", "figure"),
    [
        Input("boxplot1", "id"),
        Input("boxplot2", "id"),
    ],
)
def update_box_plots(_, __):
    fig1 = px.box(df_boxplot, x="Category", y="Value", title="Box Plot 1")
    fig2 = px.box(df_boxplot, x="Category", y="Value", title="Box Plot 2")

    return fig1, fig2


@app.callback(
    Output("barplot1", "figure"),
    Output("barplot2", "figure"),
    [
        Input("barplot1", "id"),
        Input("barplot2", "id"),
    ],
)
def update_bar_plots(_, __):
    fig1 = px.bar(df_bar, x="Category", y="Value1", title="Bar Plot 1")
    fig2 = px.bar(df_bar, x="Category", y="Value2", title="Bar Plot 2")

    return fig1, fig2


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
