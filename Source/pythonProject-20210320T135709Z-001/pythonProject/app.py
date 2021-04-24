# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import Area
import time
import Grid
import Data
import main
import datetime
import json


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
token = open(".mapbox_token").read()
px.set_mapbox_access_token(token)

#app.config['suppress_callback_exceptions'] = True

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
    html.Button('Submit', id='submit-val', n_clicks=0, title="locked"),
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

interval = html.Div([dcc.Interval(id='interval', interval=500000, n_intervals=0)])



app.layout = html.Div(children=[
    html.H1(children='Bushfire propagation simulation'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    button,
    interval,
    html.Div(id="data-out")
])

#@app.callback(
#    Output("out-all-types", "children"),
#    [Input("input_{}".format(_), "value") for _ in ALLOWED_TYPES],
#)
#def cb_render(*vals):
#    return " | ".join((str(val) for val in vals if val))

@app.callback(
    Output('submit-val', 'title'),
    [Input('submit-val', 'n_clicks')],
    [State('input-on-submit', 'value')])
def update(n_clicks, value):
        if n_clicks > 0 and value is not None:
            main.run(value)
            return "Draw grid"
        else:
            raise PreventUpdate

@app.callback(
    Output('example-graph', 'figure'),
    [Input('submit-val', 'title')],
    [Input('interval', 'n_intervals')])
def draw(title, n_intervals):
    fig = px.scatter_mapbox(pd.read_csv(grid), lon="longitude", lat="latitude",
                            mapbox_style="satellite", width=1600, height=800, animation_frame="gridid",
                            color="state")
    return fig

@app.callback(
    Output('data-out', 'children'),
    [Input('example-graph', 'selectedData')])
def get(selectedData):
    data = json.dumps(selectedData)
    return selectedData


if __name__ == '__main__':
    app.run_server(debug=True)
