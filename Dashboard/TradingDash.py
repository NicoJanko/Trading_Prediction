from dash import Dash, html, dcc, callback, Output, Input
from dash_auth

AUTH = {'admin':'p4sSw0#rD!'}

app = Dash(__name__)

app.layout = html.Div(children=[
])

if __name__ == '__main__':
    app.run_server(debug=True, host = "0.0.0.0", port=8080)