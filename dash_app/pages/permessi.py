# IMPORT LIBRARIES #####################################################################################################
import pandas as pd
import dash
from dash import Dash, Input, Output, State, callback, html, dash_table, dcc
import dash_bootstrap_components as dbc

df_permessi = pd.read_csv('permessi/schema_permessi_utente.csv')

dash.register_page(
    __name__,
    path='/permessi',
    )

def create_permessi_layout():
    return dbc.Container(
        [
            dbc.Table.from_dataframe(df_permessi, striped=True, bordered=True, hover=True)
        ],
    )

layout = create_permessi_layout

