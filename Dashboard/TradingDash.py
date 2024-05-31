from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc
from dash_auth import BasicAuth
import os
from navbar import create_navbar


data_up_path = 'data/data_update.py'
os.system(f'python {data_up_path}')

VALID_USERNAME_PASSWORD_PAIRS = {
    'username': 'password',
    'admin': 'admin'
}

app = Dash(__name__,use_pages=True)
server = app.server
NAVBAR = create_navbar()

auth = BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)


app.layout = dcc.Loading(  # <- Wrap App with Loading Component
    id='loading_page_content',
    children=[
        html.Div(
            [
                NAVBAR,
                page_container
            ]
        )
    ],
    color='primary',  # <- Color of the loading spinner
    fullscreen=True  # <- Loading Spinner should take up full screen
)
    
    


if __name__ == '__main__':
    app.run_server(debug=True, host = "0.0.0.0", port=8080)