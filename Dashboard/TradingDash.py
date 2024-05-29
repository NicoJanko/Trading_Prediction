from dash import Dash, html, dcc, callback, Output, Input
from dash_auth import BasicAuth


VALID_USERNAME_PASSWORD_PAIRS = {
    'username': 'password',
    'admin': 'admin'
}


app = Dash(__name__)
server = app.server


auth = BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)


app.layout = html.Div([
    html.H1('Hello, Dash!'),
    html.Div('This is a simple Dash dashboard with basic authentication.')
])

if __name__ == '__main__':
    app.run_server(debug=True, host = "0.0.0.0", port=8080)