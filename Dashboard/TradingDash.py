from dash import Dash, html, dcc, callback, Output, Input
from dash_auth import BasicAuth
import psycopg2 as psg2
import plotly.express as px
import pandas as pd
import os


data_up_path = 'data/data_update.py'
os.system(f'python {data_up_path}')

VALID_USERNAME_PASSWORD_PAIRS = {
    'username': 'password',
    'admin': 'admin'
}
con_string = 'postgresql://janko80:Jankojanko80@host.docker.internal:5432/tradingdash'
psg2_conn = psg2.connect(con_string)
query = 'SELECT * FROM "ADJ_CLOSE" LIMIT 1'
df = pd.read_sql(query,psg2_conn)
df = df.drop(labels=['Date'],axis=1)
stock_name = df.columns
psg2_conn.close()

app = Dash(__name__)
server = app.server


auth = BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)


app.layout = html.Div([
    html.H1('Trading Dash', style={'textAlign':'center'}),
   dcc.Dropdown(stock_name, id='dropdown'),
   dcc.Graph(id='graph')
])

@callback(
    Output('graph','figure'),
    Input('dropdown','value')
    )
def update_graph(value):
    con_string = 'postgresql://janko80:Jankojanko80@host.docker.internal:5432/tradingdash'
    psg2_conn = psg2.connect(con_string)
    query_data = f"""
        SELECT
            AC."Date",
            AC."{value}"
        FROM "ADJ_CLOSE" AC
        WHERE AC."Date"::Date BETWEEN CURRENT_DATE - INTERVAL '60 days' AND CURRENT_DATE;
"""
    data = pd.read_sql(query_data, psg2_conn)
    
    query_pred = f"""
                SELECT
                    PAC."DATE",
                    PAC."{value}"
                FROM "PRED_ADJ_CLOSE" PAC      
"""
    pred_data = pd.read_sql(query_pred, psg2_conn)
    pred_data = pred_data.rename(columns={'DATE':'Date',f'{value}':f'{value}_pred'})
    full_data = pd.concat([data, pred_data])
    return px.line(full_data, x='Date', y=full_data.columns)
    
    


if __name__ == '__main__':
    app.run_server(debug=True, host = "0.0.0.0", port=8080)