# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import pandas
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
import Area


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
    html.H5("Simulation grid on map:"),
    html.Label("Longitude:"),
    html.Div(dcc.Input(id='input-lon', type='number', placeholder='-14')),
    html.Label("Latitude:"),
    html.Div(dcc.Input(id='input-lat', type='number', placeholder='120')),
    html.Label("Longitude delta:"),
    html.Div(dcc.Input(id='input-lon-delta', type='number', placeholder='1')),
    html.Label("Latitude delta:"),
    html.Div(dcc.Input(id='input-lat-delta', type='number', placeholder='1')),
    html.Label("Grid size:"),
    html.Div(dcc.Input(id='input-gridsize', type='number', placeholder='25')),
    html.Label("Runs:"),
    html.Div(dcc.Input(id='input-runs', type='number', placeholder='100')),
    html.Button('Submit', id='submit-val', n_clicks=0, title="locked"),
    dcc.Loading(
        id="loading",
        type="cube",
        children=html.Div(id="loading-output-1")),
    html.Hr(),
    html.Label("State of cell burned out:"),
    html.Div(dcc.Input(id='input-cell', type='number', placeholder='0.3')),
    html.Label("Speed of fire:"),
    html.Div(dcc.Input(id='input-fire', type='number', placeholder='11')),
    html.Div(children='Select markers to set cell values', id='count'),
    html.Button('Set', id='set-val', n_clicks=0, title="Set speed of fire and cell burned out values for selected map markers."),
    html.Button('Reset', id='reset-val', n_clicks=0, title="Reset update values.", style={'display': 'inline-block', 'margin-left': '2.5%'}),
    dcc.Loading(
        id="loading-2",
        children=html.Div(id="loading-output-2")),
    dcc.Loading(
        id="loading-3",
        children=html.Div(id="loading-output-3")),
], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-top': '2.5%'})



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
    html.Div(children=[
        dcc.Graph(
            id='example-graph',
            figure=fig
            , style={'display': 'inline-block'}
        ),
        button]),
    interval,
    html.Div(id="data-out"),
    html.Div(id="data-click")
])

#@app.callback(
#    Output("out-all-types", "children"),
#    [Input("input_{}".format(_), "value") for _ in ALLOWED_TYPES],
#)
#def cb_render(*vals):
#    return " | ".join((str(val) for val in vals if val))

@app.callback(
    Output('submit-val', 'title'),
    Output("loading-output-1", "loading_state"),
    [Input('submit-val', 'n_clicks')],
    [State('input-lon', 'value')],
    [State('input-lat', 'value')],
    [State('input-lon-delta', 'value')],
    [State('input-lat-delta', 'value')],
    [State('input-runs', 'value')],
    [State('input-gridsize', 'value')])
def update(n_clicks, lon, lat, lon_delta, lat_delta, runs, gridsize):
        if n_clicks > 0 and gridsize is not None:
            area = Area.new(lon, lat, lon_delta, lat_delta)
            main.run(runs, gridsize, area)
            return "Draw grid", {'is_loading': True}
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
    return data

@app.callback(
    Output('data-click', 'children'),
    [Input('example-graph', 'clickData')])
def click(clickData):
    data = json.dumps(clickData)
    return data

@app.callback(
    [Output('input-lon', 'value')],
    [Output('input-lat', 'value')],
    [Output('input-lon-delta', 'value')],
    [Output('input-lat-delta', 'value')],
    [Input('data-out', 'children')])
def setgrid(data):
    if data is not None and data != "null":
        selected_data = json.loads(data)
        if len(selected_data['points']) == 0 and len(selected_data['range']['mapbox']) == 2:
            lon = selected_data['range']['mapbox'][0][0]
            lat = selected_data['range']['mapbox'][0][1]
            lon_delta = abs(lon - selected_data['range']['mapbox'][1][0])
            lat_delta = abs(lat - selected_data['range']['mapbox'][1][1])
            return lon, lat, lon_delta, lat_delta
        else:
            raise PreventUpdate

@app.callback(
    [Output('count', 'children')],
    [Input('data-out', 'children')],
    [Input('data-click', 'children')])
def setcount(data, data_click):
    if data is not None or data_click is not None:
        count = 0
        if data_click != "null":
            count += 1
        if data != "null":
            points = len(json.loads(data)['points'])
            if points > 0:
                count += points
        if count > 0:
            return [html.Label(f"{count} marker{'s' if count > 1 else ''} selected")]
        else:
            return [html.Label("Select markers to set cell values")]
    else:
        return [html.Label("Select markers to set cell values")]

@app.callback(
    Output("loading-2", "loading_state"),
    [Input('set-val', 'n_clicks')],
    [State('data-out', 'children')],
    [State('data-click', 'children')],
    [State('input-cell', 'value')],
    [State('input-fire', 'value')])
def updatevalues(n_clicks, data, data_click, state, rateOfFire):
    if n_clicks > 0:
        if data is not None or data_click is not None:
            data_points = None
            click_point = None
            if data_click is not None and data_click != 'null':
                click_point = json.loads(data_click)['points']
            if data is not None and data != 'null':
                data_points = json.loads(data)['points']
            if data_points is not None and click_point is not None:
                data_points.update(click_point)
            if data_points is None and click_point is not None:
                data_points = click_point
            if state is None:
                state = 0
            if rateOfFire is None:
                rateOfFire = 0
            if state != 0 or rateOfFire != 0:
                records = []
                for point in data_points:
                    records.append({'longitude': point['lon'], 'latitude': point['lat'], 'state': state, 'speedOfFireSpread': rateOfFire})
                df = pandas.DataFrame(records)
                df.to_csv(r"data/temp/update_values.csv", mode='a', header=False)

@app.callback(
    Output("loading-3", "loading_state"),
    [Input('reset-val', 'n_clicks')])
def reset(n_clicks):
    if n_clicks > 0:
        path = r"data/temp/update_values.csv"
        f = open(path, "w")
        f.write(",longitude,latitude,state,speedOfFireSpread\n")
        f.close()


if __name__ == '__main__':
    app.run_server(debug=True)
