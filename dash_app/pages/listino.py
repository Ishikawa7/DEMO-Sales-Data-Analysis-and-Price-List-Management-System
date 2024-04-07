# IMPORT LIBRARIES #####################################################################################################
import os
import pandas as pd
import plotly.express as px
import dash
from dash import Dash, Input, Output, State, callback, html, dash_table, dcc
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path='/project_home',
    )
layout = dbc.Container(
    [
        html.Div(id='header'),
        html.Br(),
        html.Hr(),
        html.Br(),
        dbc.Row(
            [
                html.H4('Caricare tutti i file necessari per l''analisi'),
                html.Div(id='output-data-upload', children=[html.P('Nessun file caricato')], style={'margin-top': '10px', "align": "center"}),
            ],
        ),
        html.Br(),
        dbc.Row(
            [
                
            ],
            style={'margin-top': '10px', 'width': '100%', "align": "center"},
        ),
        # add vertical space
        html.Br(),
        html.Hr(),
        html.Br(),
        dbc.Row(
            [
                html.H4('Schede del progetto'),
                html.Div(id='project-cards', style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'space-between'})
            ]
        ),
    ],
)

