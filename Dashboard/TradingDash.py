from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc
from dash_auth import BasicAuth
import os
from navbar import create_navbar


#data_up_path = 'data/data_update.py'
#os.system(f'python {data_up_path}')

VALID_USERNAME_PASSWORD_PAIRS = {
    'username': 'password',
    'admin': 'admin'
}
FA621 = "https://use.fontawesome.com/releases/v6.2.1/css/all.css"


app = Dash(__name__,
           #suppress_callback_exceptions=True,
           external_stylesheets=[
            dbc.themes.FLATLY,  # Dash Themes CSS
            FA621  # Font Awesome Icons CSS
    ],
           use_pages=True)
server = app.server
NAVBAR = create_navbar()

auth = BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)


app.layout =html.Div(
            [
                NAVBAR,
                page_container
            ]
        )
   
    
    


if __name__ == '__main__':
    app.run_server(debug=True, host = "0.0.0.0", port=8080)