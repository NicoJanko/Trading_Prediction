from dash import html, dcc, callback, Output, Input, register_page
import psycopg2 as psg2
import plotly.express as px
import pandas as pd



register_page(
    __name__,
    name='TradingDash',
    top_nav=True,
    path='/tradingdash'
)

#localhost
#@host.docker.internal:5432
con_string = 'postgresql://janko80:Jankojanko80@host.docker.internal:5432/tradingdash'
psg2_conn = psg2.connect(con_string)
query = 'SELECT * FROM "ADJ_CLOSE" LIMIT 1'
df = pd.read_sql(query,psg2_conn)
df = df.drop(labels=['Date'],axis=1)
stock_name = df.columns
psg2_conn.close()



def layout():
    layout = html.Div([
    html.H1('Trading Dash',
            style={'textAlign':'center'}),
    dcc.Dropdown(stock_name,
                 id='dropdown',
                 style = {'width':'45%'}),
    dcc.Graph(id='graph',
              style={'height': '80vh'}
              )
])
    return layout

@callback(
    Output('graph','figure'),
    Input('dropdown','value')
    )
def update_graph(value):
    con_string = 'postgresql://janko80:Jankojanko80@host.docker.internal:5432/tradingdash'
    psg2_conn = psg2.connect(con_string)
    if value:
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
        fig = px.line(full_data, x='Date', y=full_data.columns)
        fig.update_layout(margin={'t': 20, 'b': 20, 'l': 20, 'r': 20})
        return fig
    else:
        return px.line(title='Choisir une action')
    
