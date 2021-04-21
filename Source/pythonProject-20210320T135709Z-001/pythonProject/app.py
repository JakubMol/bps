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


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
token = open(".mapbox_token").read()
px.set_mapbox_access_token(token)
Data.todataframe()
elevation = r"data/temp/elevation.csv"
fire = r"data/fires/fire_archive_M6_96619.csv"
fig = px.scatter_mapbox(pd.read_csv(fire), lon="longitude", lat="latitude",
                        mapbox_style="satellite", width=1600, height=800, animation_frame="acq_date", color="brightness")
ALLOWED_TYPES = (
    "text", "range",
)

input = html.Div(
    [
        dcc.Input(
            id="input_{}".format(_),
            type=_,
            placeholder="input type {}".format(_),
        )
        for _ in ALLOWED_TYPES
    ]
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
    input
])

@app.callback(
    Output("out-all-types", "children"),
    [Input("input_{}".format(_), "value") for _ in ALLOWED_TYPES],
)
def cb_render(*vals):
    return " | ".join((str(val) for val in vals if val))

if __name__ == '__main__':
    app.run_server(debug=True)
