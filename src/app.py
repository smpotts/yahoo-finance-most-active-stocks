from io import StringIO

import requests
from bs4 import BeautifulSoup
import pandas as pd
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import src.scrape as scrape

import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Dash, html, dcc, Input, Output
from plotly.subplots import make_subplots


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

stocks = scrape.scrape_data()

# Create a bar chart for the volume of the most active stocks
# fig_volume = px.bar(most_active_stocks, x='Name', y='Volume', title='Volume of Most Active Stocks')
# fig_volume.update_layout(plot_bgcolor='#111', paper_bgcolor='#111', font_color='white')
# fig_volume.show()

# fig = make_subplots(rows=1, cols=1, subplot_titles=['% Change'])

# % Change visualization
# fig_change = px.bar(most_active_stocks, x='Name', y='% Change', text='% Change')
# for trace in fig_change['data']:
#     fig.add_trace(trace, row=1, col=1)

# fig.update_layout(showlegend=False, plot_bgcolor='#111', paper_bgcolor='#111', font_color='white')
# fig.update_traces(marker_color='skyblue', marker_line_color='white', marker_line_width=1.5, opacity=0.6)
# fig.show()

# fig_percent_change = px.bar(most_active_stocks, x='Name', y='% Change', text='% Change')
# fig_percent_change.update_layout(showlegend=False, plot_bgcolor='#111', paper_bgcolor='#111', font_color='white', yaxis=dict(range=[-10, 10]))
# fig_percent_change.update_traces(marker_color='skyblue', marker_line_color='white', marker_line_width=1.5, opacity=0.6)
# fig_percent_change.show()

app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("Yahoo Finance Most Active Stocks"),
        html.Hr(),
        dbc.Button(
            "Regenerate graphs",
            color="primary",
            id="button",
            className="mb-3",
        ),
        dbc.Tabs(
            [
                dbc.Tab(label="% Change", tab_id="pct_change"),
                dbc.Tab(label="Price (Intraday)", tab_id="price"),
            ],
            id="tabs",
            active_tab="pct_change",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)


@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), Input("store", "data")],
)
def render_tab_content(active_tab, data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    # if active_tab and data is not None:
    if active_tab == "pct_change":
        return dcc.Graph(figure=px.bar(stocks, x='Name', y='% Change').update_traces(marker_color=stocks["Color"]),
                         style={'height': '100vh'})
    elif active_tab == "price":
        return dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=px.bar()), width=6),
                    # dbc.Col(dcc.Graph(figure=data["hist_2"]), width=6),
                ]
            )
    # return "No tab selected"


if __name__ == '__main__':
    # scrape.scrape_data()
    app.run(debug=True)