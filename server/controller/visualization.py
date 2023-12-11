# -*- coding: utf-8 -*-
from dash import Dash
# import dash_html_components as html
from dash import html
from flask import Flask
# import dash_core_components as dcc
from dash import dcc
from plotly.graph_objs import *

""" 
    This module encapsulated all visualization instances from dash 
    and the creation of specific layouts for each instance.
    
"""

server = Flask(__name__)
histogram1 = Dash(__name__, server=server, url_base_pathname='/histogram1/')
histogram1.layout = html.Div()
histogram2 = Dash(__name__, server=server, url_base_pathname='/histogram2/')
histogram2.layout = html.Div()


def create_histogram1():
    trace1 = Bar(
        x=["Emoji A", "Emoji B", "Emoji C", "Emoji D", "Emoji E", "Emoji F", "Emoji G", "Emoji H", "Emoji I",
           "Emoji J"],
        y=[150, 100, 94, 56, 43, 31, 22, 15, 10, 2],
        marker={
            "color": "rgb(204, 255, 204)",
            "line": {
                "color": "rgb(102, 153, 153)",
                "width": 1.5
            }
        },
        opacity=0.6,
        text=["Emoji A", "Emoji B", "Emoji C", "Emoji D", "Emoji E", "Emoji F", "Emoji G", "Emoji H", "Emoji I",
              "Emoji J"],
    )

    data = [trace1]
    layout = {"title": "Top 10 Emojis Clusters"}
    fig = Figure(data=data, layout=layout)

    histogram1.layout = html.Div(children=[
        dcc.Graph(
            id='example-graph',
            figure=fig
        )
    ])


def create_histogram2():
    trace1 = Bar(
        x=["Emoji A", "Emoji B", "Emoji C"],
        y=[23, 20, 14],
        marker={
            "color": "rgb(158,202,225)",
            "line": {
                "color": "rgb(8,48,107)",
                "width": 1.5
            }
        },
        opacity=0.6,
        text=["Emoji 1", "Emoji 2", "Emoji 3"],
    )

    data = [trace1]
    layout = {"title": "Top 3 Repeated Emojis"}
    fig = Figure(data=data, layout=layout)

    histogram2.layout = html.Div(children=[
        dcc.Graph(
            id='example-graph',
            figure=fig
        )
    ])
