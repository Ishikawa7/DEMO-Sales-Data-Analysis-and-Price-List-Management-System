# IMPORT LIBRARIES #####################################################################################################
import pandas as pd
import plotly.express as px
import dash
from dash import Dash, Input, Output, State, callback, html, dash_table, dcc
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path='/listino',
    )
def create_layout_listino():
    return dbc.Container(
        [
            # create a hidden button
            dbc.Button(id="button"),
            dbc.Row(
                [
                    html.Div(id='clustering', children=[

                    ], 
                    style={'margin-top': '10px', "align": "center"}),
                ],
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H4('Listino'),
                            html.Div(id='discostamento_categorie', children=[

                            ],
                            style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'space-between'})
                        ],
                        width=6,
                    ),
                    dbc.Col(
                        [
                            html.H4('Discostamenti negativi'),
                            html.Div(id='discostamenti_negativi', children = [

                            ],
                            style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'space-between'})
                        ],
                        width=6,
                    ),
                ],
                style={'margin-top': '10px', 'width': '100%', "align": "center"},
            ),
            # add vertical space
            html.Br(),
            html.Hr(),
            html.Br(),
            dbc.Button(
                "Crea preventivo",
                id="collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
            ),
            dbc.Collapse(
                [
                    dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H4('Form'),
                                dbc.Card(
                                    html.Div(id='form', children=
                                        [
                                            dbc.Label("ID prodotto"),
                                            dbc.Input(id="id-input", value=""),
                                            dbc.Label("ID cliente"),
                                            dbc.Input(id="id_cliente-input", value=""),
                                            dbc.Label("......"),
                                            dbc.Input(id="id_cliente-input", value="..."),
                                            dbc.Label("......"),
                                            dbc.Input(id="id_cliente-input", value="..."),
                                            dbc.Label("......"),
                                            dbc.Input(id="id_cliente-input", value="..."),
                                            dbc.Label("......"),
                                            dbc.Input(id="id_cliente-input", value="..."),
                                        ],
                                    #style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'space-between'}
                                    ),
                                    style={"padding-right": "50px", "padding-left": "50px", "padding-top": "50px", "padding-bottom": "50px"},
                                    color="secondary",
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                html.Div(id='analytics_preventivo', children=[

                                ],
                                style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'space-between'})
                            ],
                            width=6,
                        ),
                    ],
                    style={'margin-top': '10px', 'width': '100%', "align": "center"},
                    ),
                ],
                id="collapse",
                is_open=False,
            ),
        ],
        fluid=True,
    )
layout = create_layout_listino

@callback(
    Output("collapse", "is_open"),# Output('analytics_preventivo','children')],
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open#, []

@callback(
    [
        #Output("clustering", "children"),
        #Output("discostamento_categorie", "children"),
        Output("discostamenti_negativi", "children"),
    ],
    [Input("button", "n_clicks")],
)
def update_visuals(n):
    df_listino = pd.read_csv("listino/df_listino.csv")
    df_mean_deltas = pd.read_csv("listino/df_mean_deltas.csv")
    discostamenti_negativi = pd.read_csv("listino/discostamenti_negativi.csv")
    discostamenti_negativi_table = dbc.Table.from_dataframe(discostamenti_negativi, striped=True, bordered=True, hover=True)
    return discostamenti_negativi_table



