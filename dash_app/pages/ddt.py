# IMPORT LIBRARIES #####################################################################################################
import pandas as pd
import plotly.express as px
import dash
from dash import Dash, Input, Output, State, callback, html, dash_table, dcc
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path='/ddt',
    )
df_indecies = pd.DataFrame()

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.RadioItems(
                    id="radios",
                    className="btn-group",
                    inputClassName="btn-check",
                    labelClassName="btn btn-outline-primary",
                    labelCheckedClassName="active",
                    options=[
                        {"label": "MST", "value": 'mst'},
                        {"label": "MRG", "value": 'mrg'},
                    ],
                    value="mst",
                ),
            ],
        ),
        html.Br(),
        html.Hr(),
        html.Br(),
        dbc.Row(
            [
               html.Div(
                   [
                   ],
                   id='graph-network',
                   style={'width': '110%', 'height': '100%'},
               ),
            ],
            style={'width': '110%', 'height': '900px'},
            align='stretch',
        ),
        html.Br(),
        html.Hr(),
        html.Br(),
        html.H4('Visualizzazioni Indici'),
        dbc.Row(
            [
                
            ],
            id='visualizations',
        ),
        html.Br(),
        html.Hr(),
        html.Br(),
        html.H4('Tabella Indici'),
        dbc.Row(
            [
                html.Br(),
                dbc.Col(
                    [
                       
                    ],
                    id='graph-indecies-tab',
                ),
            ]
        ),
        html.Br(),
        html.Hr(),
        html.Br(),
        html.H4('PTY'),
        dbc.Row(
            [
               
            ],
            id='pty-tab',
        ),
    ],
)

#frame = html.Iframe(srcDoc=open(f'{path}{value}_{view_type}.html', 'r').read(), style={'width': '100%', 'height': '100%'})