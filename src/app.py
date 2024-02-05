import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import src.scrape as scrape

import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Dash, html, dcc, Input, Output
from plotly.subplots import make_subplots

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

stocks = scrape.clean_trending_ticker_data()


app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("Yahoo Finance Stocks"),
        html.Hr(),
        dbc.Button(
            "Regenerate graphs",
            color="primary",
            id="button",
            className="mb-3",
        ),
        dbc.Tabs(
            [
                dbc.Tab(label="Trending Tickers", tab_id="trending_tickers"),
                dbc.Tab(label="Price (Intraday)", tab_id="price"),
            ],
            id="tabs",
            active_tab="trending_tickers",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)


@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), Input("store", "data")],
)
def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab == "trending_tickers":
        return (
            [
                dcc.Graph(figure=px.bar(stocks, x='Name', y='% Change', color='% Change', title="Trending Tickers",
                                        color_continuous_scale='Bluered')
                          .update_layout(showlegend=False),
                          style={'height': '85vh'})
                # dcc.Graph(figure=px.bar(stocks.where(stocks['% Change'] >= 0), x='Name', y='% Change',
                #                             size='Market Cap',
                #                             hover_name="Name", title="Postitive % Change")
                #           .update_traces(marker_color=stocks["Color"]),
                #           style={'height': '85vh'}),
                # dcc.Graph(figure=px.bar(stocks.where(stocks['% Change'] < 0), x='Name', y='% Change',
                #                             hover_name="Name",
                #                             size='Market Cap',
                #                             title="Negative % Change").update_traces(marker_color=stocks["Color"]),
                #           style={'height': '85vh'}),
            ])
    elif active_tab == "price":
        return dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=px.bar()), width=6),
                # dbc.Col(dcc.Graph(figure=data["hist_2"]), width=6),
            ]
        )


if __name__ == '__main__':
    app.run(debug=True)