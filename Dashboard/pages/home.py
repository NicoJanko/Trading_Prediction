from dash import html, dcc, callback, Output, Input, register_page

register_page(
    __name__,
    name='Home',
    top_nav=True,
    path='/'
)


def layout():
    layout = html.Div([
        html.H1(
            [
                "Home Page"
            ]
        )
    ])
    return layout