# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import Area
import time
import Grid
import Data
import main


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
token = open(".mapbox_token").read()
px.set_mapbox_access_token(token)

elevation = r"data/temp/elevation.csv"
fire = r"data/fires/fire_archive_M6_96619.csv"
grid = r"data/temp/test_grid.csv"

lock = False

fig = px.scatter_mapbox(pd.read_csv(grid), lon="longitude", lat="latitude",
                        mapbox_style="satellite", width=1600, height=800, animation_frame="gridid", color="state")
ALLOWED_TYPES = (
    "text", "range",
)

button = html.Div([
    html.Div(dcc.Input(id='input-on-submit', type='number')),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children='Enter a value and press submit')
])


input = html.Div(
    [
        dcc.Input(
            id="input_{}".format(_),
            type=_,
            placeholder="input type {}".format(_),
        )
        for _ in ALLOWED_TYPES
    ]
    + [button]
    + [html.Div(id="out-all-types")]
)

app.layout = html.Div(children=[
    html.H1(children='Bushfire propagation simulation'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    button
])

@app.callback(
    Output("out-all-types", "children"),
    [Input("input_{}".format(_), "value") for _ in ALLOWED_TYPES],
)
def cb_render(*vals):
    return " | ".join((str(val) for val in vals if val))

@app.callback(
    dash.dependencies.Output('example-graph', 'figure'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('input-on-submit', 'value')])
def update_output(n_clicks, value):
    main.run(value)
    fig = px.scatter_mapbox(pd.read_csv(grid), lon="longitude", lat="latitude",
                            mapbox_style="satellite", width=1600, height=800, animation_frame="gridid", color="state")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
