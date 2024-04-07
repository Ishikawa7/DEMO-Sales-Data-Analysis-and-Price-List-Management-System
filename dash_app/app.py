import dash
from dash import Dash, Input, Output, State, callback, html, dcc
import dash_bootstrap_components as dbc

# css file for dash components
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# DASH APP #############################################################################################################
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.LUX, dbc_css]) #suppress_callback_exceptions=True

app.layout = dbc.Container(
    [
        dcc.Store(id='session', storage_type='session', data= {'current_project': None}),
        dcc.Store(id='view-info', storage_type='session', data= {'view_type': None}),
        dcc.Location(id='url', refresh=True),
        dbc.NavbarSimple(
            id = "navbar",
            children=[
                dbc.NavItem(dbc.NavLink("Pagina iniziale", href="/")),
            ],
            brand="Demo gestionale",
            brand_href="#",
            color="primary",
            dark=True,
        ),
        html.Hr(),
        html.Div(
	        dash.page_container,
            id="page-content",
        ),
        # add a footer
        html.Hr(),
        # use a jumbotron to add a description for the app
        html.Div(
            dbc.Container(
                [
                    html.H3("Informazioni utili"),
                ],
                fluid=True,
                className="py-3",
            ),
            className="p-3 bg-light rounded-3",
        )
    ],
    fluid=True,
)

# RUN THE APP ###########################################################################################################
if __name__ == "__main__":
    # shut down any running dash processes
    #os.system("taskkill /f /im python.exe")
    # start the dash app
    #app.run_server(host='0.0.0.0', port=8080, debug=False, use_reloader=False)
    app.run_server(debug=True, use_reloader=True)

# if Python [Errno 98] Address already in use 
# kill -9 $(ps -A | grep python | awk '{print $1}')