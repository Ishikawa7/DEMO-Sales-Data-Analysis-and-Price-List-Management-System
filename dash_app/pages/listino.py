# IMPORT LIBRARIES #####################################################################################################
import pandas as pd
import numpy as np
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
            dbc.Button( "LISTINO", id="button",),
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
                        width=8,
                    ),
                    dbc.Col(
                        [
                            html.H4('Discostamenti negativi'),
                            html.Div(id='discostamenti_negativi', children = [

                            ],
                            style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'space-between'})
                        ],
                        width=4,
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
                                html.H4('Form creazione preventivo'),
                                dbc.Card(
                                    html.Div(id='form', children=
                                        [
                                            dbc.Label("ID prodotto"),
                                            dbc.Input(id="id-input", value="017.PM419"),
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
    Output("collapse", "is_open", allow_duplicate=True),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
    prevent_initial_call=True,
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    [
        Output("clustering", "children", allow_duplicate=True),
        Output("discostamento_categorie", "children", allow_duplicate=True),
        Output("discostamenti_negativi", "children", allow_duplicate=True),
        Output("analytics_preventivo", "children", allow_duplicate=True),
    ],
    [Input("button", "n_clicks")],
    prevent_initial_call=True,
)
def update_visuals(n):
    df_pca =  pd.read_csv("listino/pca.csv")
    df_pca = df_pca[df_pca["Categoria"]!="Accessori"]
    fig_clustering = px.scatter(df_pca, x="PC1", y="PC2", color="Categoria", template="plotly_white", title="Clustering storico listino")
    graph_clustering = dcc.Graph(figure=fig_clustering)

    df_mean_deltas = pd.read_csv("listino/df_mean_deltas.csv")
    fig_deltas = px.bar(df_mean_deltas,x = "Categoria", y="Delta_avg", template="plotly_white", 
             title="Differenza media tra prezzi",
             labels={"Delta_avg":"Differenza media", "Categoria":"Categoria"}, color="Delta_avg", 
             color_continuous_scale=px.colors.sequential.Viridis, text="Delta_avg", height=800, width=1200)
    graph_deltas = dcc.Graph(figure=fig_deltas)


    discostamenti_negativi = pd.read_csv("listino/discostamenti_negativi.csv")
    discostamenti_negativi_table = dbc.Table.from_dataframe(discostamenti_negativi, striped=True, bordered=True, hover=True, color="warning", size= 'sm')

    df_listino = pd.read_csv("listino/df_listino.csv")
    storico = [41.56, 41.6, 42.21, 42.96, 43.3, 43.43, 44.02, 44.27, 44.93, 45.54, 45.81, 46.07, 46.52]#df_listino[df_listino["Codice_articolo"]=="017.PM419"]["Storico"][0]
    storico_vendita = [51.85, 54.1, 44.66, 76.63, 79.36, 78.13, 67.1, 67.18, 67.25, 67.28, 67.36, 67.46, 67.78]#df_listino[df_listino["Codice_articolo"]=="017.PM419"]["Vendita"][0]
    df_storico = pd.DataFrame()
    df_storico["storico"] = list(storico)
    df_storico["storico_vendita"] = list(storico_vendita)
    df_storico["discostamento"] = df_storico["storico_vendita"] - df_storico["storico"]
    for i in range(len(storico)-len(storico_vendita)):
        storico_vendita.append(storico_vendita[-1]+ np.random.rand()*storico_vendita[-1]*0.25)
    fig_storico = px.line(df_storico, y = df_storico.columns[:2], title="Storico prezzo listino e vendita articolo 017.PM419", markers=True, 
                          template="plotly_white", text=storico, labels={"x":"Mese", "y":"Prezzo"}, width=900)
    fig_storico.update_traces(textposition='top center')
    
    graph_storico = dcc.Graph(figure=fig_storico)


    fig_discostamento = px.bar(df_storico, y = "discostamento", title="Discostamento Storico prezzo listino e prezzo vendita articolo 017.PM419", 
                          template="plotly_white", text=storico, labels={"x":"Mese", "y":"Prezzo"}, width=900,
                          color= "discostamento", color_continuous_scale=px.colors.sequential.RdBu)
    graph_discostamento = dcc.Graph(figure=fig_discostamento)
    


    return graph_clustering,graph_deltas,[discostamenti_negativi_table], [graph_storico, graph_discostamento]



