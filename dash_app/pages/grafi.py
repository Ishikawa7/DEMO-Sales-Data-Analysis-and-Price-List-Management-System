# IMPORT LIBRARIES #####################################################################################################
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import json
import dash
from dash import Dash, Input, Output, State, callback, html, dash_table, dcc
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path='/grafi',
    )

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.RadioItems(
                            id="radios",
                            className="btn-group",
                            inputClassName="btn-check",
                            labelClassName="btn btn-outline-primary",
                            labelCheckedClassName="active",
                            options=[
                                {"label": "all", "value": 'all'},
                                {"label": "money", "value": 'money'},
                                {"label": "materia", "value": 'materia'},
                                {"label": "document", "value": 'document'},
                                {"label": "prod", "value": 'prod'},
                                {"label": "work", "value": 'work'},
                            ],
                            value="all",
                        ),
                        html.Div(
                            [
                            ],
                            id='graph-network',
                            style={'width': '100%', 'height': '100%'},
                        ),
                    ],
                    width=8,
                ),
                dbc.Col(
                    [
                        dbc.RadioItems(
                            id="radios2",
                            className="btn-group",
                            inputClassName="btn-check",
                            labelClassName="btn btn-outline-primary",
                            labelCheckedClassName="active",
                            options=[
                                {"label": "metrics_money", "value": 'metrics_money'},
                                {"label": "metrics_product", "value": 'metrics_product'},
                            ],
                            value="metrics_money",
                        ),
                        html.Div(
                            [
                            ],
                            id='indicies',
                            style={'width': '100%', 'height': '100%'},
                        ),
                    ],
                    width=4,
                ),  
            ],
            style={'width': '100%', 'height': '100%'},
        ),
        ##align='stretch',
        html.Hr(),
        html.H4('Visualizzazioni di flusso'),
         dbc.Row(
            [
                html.Div(
                    [
                    ],
                    id='flusso',
                    style={'width': '100%', 'height': '100%'},
                ),
            ],
            style={'width': '100%', 'height': '100%'},
        ),
    ],
    fluid=True,
)

@callback(
    Output('graph-network', 'children'),
    Input('radios', 'value'),
)
def update_graph(value):
    path = 'grafi/'
    frame = html.Iframe(srcDoc=open(f'{path}{value}.html', 'r').read(), style={'width': '100%', 'height': '100%'})
    return frame

@callback(
    Output('indicies', 'children'),
    Input('radios2', 'value'),
)
def update_indicies(value):
    df_metrics = pd.read_csv('grafi/'+value+'.csv', index_col=0)
    # remove all rows with index starting with "mangini"
    df_metrics = df_metrics[~df_metrics.index.str.contains('mangini')]
    fig_betweenness = px.bar(df_metrics, x=df_metrics.index, y='betweenness', title='Betweenness', template='plotly_white', color='betweenness', color_continuous_scale='Viridis')
    fig_closeness = px.bar(df_metrics, x=df_metrics.index, y='closeness', title='Closeness', template='plotly_white', color='betweenness', color_continuous_scale='Viridis')
    fig_in_degree = px.bar(df_metrics, x=df_metrics.index, y='in_degree', title='In Degree', template='plotly_white', color='betweenness', color_continuous_scale='Viridis')
    fig_out_degree = px.bar(df_metrics, x=df_metrics.index, y='out_degree', title='Out Degree', template='plotly_white', color='betweenness', color_continuous_scale='Viridis')
    graph_betweenness = dcc.Graph(figure=fig_betweenness)
    graph_closeness = dcc.Graph(figure=fig_closeness)
    graph_in_degree = dcc.Graph(figure=fig_in_degree)
    graph_out_degree = dcc.Graph(figure=fig_out_degree)
    return [graph_betweenness, graph_closeness, graph_in_degree, graph_out_degree]

@callback(
    Output('flusso', 'children'),
    Input('radios', 'value'),
)
def update_flusso(value):
    with open('db/dict_entities.json', 'r') as f:
        db_dict = json.load(f)
    graph_db_product = nx.DiGraph()
    for key in db_dict.keys():
        key_start = key.split('_')[0]

        if key_start == 'documento':
            cod_fornitore = db_dict[key]['cod_fornitore']
            fornitore = "fornitore_"+ str(cod_fornitore)
            importo = db_dict[key]['importo']
            if not graph_db_product.has_node(fornitore):
                graph_db_product.add_node(fornitore, type='fornitore')
            for prod in db_dict[key]['venduto']:
                codice_articolo = prod['codice_articolo']
                articolo = "prod_" + codice_articolo
                if not graph_db_product.has_node(articolo):
                    graph_db_product.add_node(articolo, type='materia', label= articolo, name= articolo, weight= 1)
            graph_db_product.add_edge(articolo, fornitore, type='money_neg', label= importo, name= importo, weight= importo)

        elif key_start == 'fattura':
            cliente = db_dict[key]['id_cliente']
            importo = db_dict[key]['importo']
            if not graph_db_product.has_node(cliente):
                graph_db_product.add_node(cliente, type='cliente')
            for prod in db_dict[key]['venduto']:
                codice_articolo = prod['codice_articolo']
                articolo = "prod_" + codice_articolo
                if not graph_db_product.has_node(articolo):
                    graph_db_product.add_node(articolo, type='materia', label= codice_articolo, name= codice_articolo, weight= 1)
                graph_db_product.add_edge(cliente, articolo, type='money_pos', label= importo, name= importo, weight= importo)
    
    df_product = pd.DataFrame(graph_db_product.edges(data=True), columns=['source', 'target', 'data'])
    df_product['type'] = df_product['data'].apply(lambda x: x['type'])
    df_product['label'] = df_product['data'].apply(lambda x: x['label'])
    df_product['label'] = df_product['label'].apply(lambda x: round(float(x), 2) if isinstance(x, str) else x)
    money_neg_sum = df_product[df_product['type'] == 'money_neg']["label"].sum()
    money_pos_sum = df_product[df_product['type'] == 'money_pos']["label"].sum()
    df_product["label_percentage"] = df_product.apply(lambda x: x['label']/money_neg_sum if x['type'] == 'money_neg' else x['label']/money_pos_sum, axis=1)
    df_product.drop(columns=['data'], inplace=True)
    entities = list(set(df_product['source'].unique().tolist() + df_product['target'].unique().tolist()))
    entity_dict = {entities[i]: i for i in range(len(entities))}
    entity_type = {entities[i]: graph_db_product.nodes[entities[i]]['type'] for i in range(len(entities))}
    entity_color = {'fornitore': '#e0e098', 'cliente': '#9d6ec9', 'materia': '#686868'}
    entity_colors = [entity_color[entity_type[entity]] for entity in entities]
    df_product['source_id'] = df_product['source'].apply(lambda x: entity_dict[x])
    df_product['target_id'] = df_product['target'].apply(lambda x: entity_dict[x])
    df_product['color'] = df_product['type'].apply(lambda x: '#ff7c7f' if x == 'money_neg' else '#7cff96')

    sources = df_product['source_id'].to_list()
    targets = df_product['target_id'].to_list()
    nodes = list(set(sources + targets))
    values = df_product['label_percentage'].to_list()
    values = [round(x, 2) for x in values]
    edge_colors = df_product['color'].to_list()
    fig = go.Figure(
        data=
        [
          go.Sankey(
            valueformat = ".2%",
            #valuesuffix = "%",
            #arrangement='snap',
            # Define nodes
            node = dict(
              pad = 15,
              thickness = 15,
              line = dict(color = "black", width = 0.5),
              label =  list(entity_dict.keys()),
              color =  entity_colors,
              #align="left",
            ),
            # Add links
            link = dict(
              arrowlen=10,
              source = sources,
              target =  targets,
              value =  values,
              #label =  df_product['label_percentage'].to_list(),
              color =  edge_colors
            )
          )
        ]
    )

    fig.update_layout(title_text="Products money flow",
                  font_size=10, height=600, width=1500)
    
    frame = dcc.Graph(figure=fig)
    return frame

#graph_analysis/all.html
#graph_analysis/money.html
#graph_analysis/materia.html
#graph_analysis/document.html
#graph_analysis/prod.html