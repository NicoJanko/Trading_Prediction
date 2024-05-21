from dash import Dash, html, dcc, callback, Output, Input

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Bebou!'),

    html.Div(children='''
        Bebou!
    '''),

    html.Img(src='/assets/bebou.jpg')
])

if __name__ == '__main__':
    app.run_server(debug=True, host = "0.0.0.0", port=8080)