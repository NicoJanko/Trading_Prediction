from dash import Dash, html, dcc, callback, Output, Input
from dash_auth import BasicAuth
import psycopg2 as psg2



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
    html.H1('Trading Dash', style={'textAlign':'center'}),
   dcc.Dropdown(stock_name, id)'dropdown'),
   dcc.Graph(id='graph')
])

@callback(
    Output('graph','figure'),
    Input('dropdown','value')
    )
def update_graph

if __name__ == '__main__':
    app.run_server(debug=True, host = "0.0.0.0", port=8080)