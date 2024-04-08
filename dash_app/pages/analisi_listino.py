# IMPORT LIBRARIES #####################################################################################################
import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import Dash, Input, Output, State, callback, html, dash_table, dcc
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path='/analisi_listino',
    )
def create_layout_listino():
    return dbc.Container(
        [
            html.H4('Analitica Listino'),
            dbc.Input(placeholder="Inserisci nome prodotto", type="text", id="input"),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H4(["ID prodotto:", dbc.Badge("027.101TEL.H", className="ms-1",color="primary")]),

                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            html.H4(["Codice variante", dbc.Badge("0", className="ms-1",color="primary")]),

                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            html.H4(["Descrizione", dbc.Badge("TELAIO PER PORTA LEGNO 898x2977", className="ms-1",color="secondary")]),

                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            html.H4(["Data_riferimento", dbc.Badge("2022-11-28", className="ms-1",color="secondary")]),

                        ],
                        width=3,
                    ),
                ],
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(id='analytics_1', children=
                                [
                                ],
                            ),
                            html.Div(id='analytics_2', children=
                                [
                                ],
                            ),                             
                        ],
                        width=9,
                    ),
                    dbc.Col(
                        [
                            html.Br(),
                            html.H5(
                                ["Previsione media a tre mesi", 
                                 dbc.Badge("115.79", className="ms-1",color="info", style={"font-size":"30px", "font-weight":"bold"})
                                 ]),
                            html.Br(),
                            html.Br(),
                            html.H5(["Prezzo attuale listino", dbc.Badge("70.00", className="ms-1",color="dark", style={"font-size":"20px", "font-weight":"bold"})]),
                            html.Br(),
                            html.Br(),
                            html.H5(["Prezzo medio ultimi tre mesi", dbc.Badge("118.88", className="ms-1",color="warning", style={"font-size":"20px", "font-weight":"bold"})]),
                            html.Br(),
                            html.Br(),
                            html.H5(["Prezzo massimo ultimi sei mesi", dbc.Badge("155.00", className="ms-1",color="danger", style={"font-size":"20px", "font-weight":"bold"})]),
                            html.Br(),
                            html.Br(),
                            html.H5(["Prezzo minimo ultimi sei mesi", dbc.Badge("80.00", className="ms-1",color="success", style={"font-size":"20px", "font-weight":"bold"})]),
                            html.Br(),
                            html.Br(),
                            dbc.Alert("ALLERT: PREZZO LISTINO DA AGGIUSTARE!", color="danger", style={"font-size":"20px", "font-weight":"bold"}),
                        ],
                        width=3,
                    ),
                ],
            ),
        ],
        fluid=True,
    )
layout = create_layout_listino

@callback(
    [
        Output("analytics_1", "children", allow_duplicate=True),
        Output("analytics_2", "children", allow_duplicate=True),
    ],
    [Input("input", "value")],
    prevent_initial_call=True,
)
def update_analytics(value):
    df_027 =  pd.read_csv("db/esempio_prod.csv", index_col=0)
    # round all values to 2 decimal places
    df_027 = df_027.round(2)
    fig_line1 = px.line(df_027, x=df_027.index, y=['Prezzo_netto_vu', 'Prezzo_netto_vu_MA', 'Prezzo_listino', 'Prediction_Prezzo_netto_vu_MA'],
                         title="Prezzo articolo 017.PM419", width=900, template="plotly_white", markers=True, labels={'value':'Prezzo', 'index':'Data'},
                         )
    graph_1 = dcc.Graph(figure=fig_line1)

    # drop nan on the column 'Discostamento'
    df_discostamento = df_027.dropna(subset=['Discostamento'])
    fig_discostamento = px.line(df_discostamento, y = "Discostamento", title="Discostamento prezzo listino e prezzo acquisto articolo 017.PM419", 
                      template="plotly_white", text='Discostamento',  width=700, markers=True, labels={'value':'Discostamento', 'index':'Data'},
                      color_discrete_sequence=['brown'])
    fig_discostamento.update_traces(textposition='top center')
    graph_discostamento = dcc.Graph(figure=fig_discostamento)
    


    return graph_1, graph_discostamento



