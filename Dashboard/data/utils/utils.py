import psycopg2 as psg2
import yfinance as yf
import pandas as pd

def check_table(tablename,cursor):
    query = psg2.sql.SQL("""
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name = {}
                  );
        """).format(tablename)
    cursor.execute(query,(tablename))
    if cursor.fetchone()[0] =='f':
        response = False
    else: response = True
    
    return response
    
def daily_update():
    symbols = #take symbols from the db TODO
    today_data = yf.download(
        sp500,
        start=pd.Timestamp.today().date(),
        end=pd.Timestamp.today().date()
                             )['Adj Close']
    today_data = today_data.fillna(0.0)
    return today_data

def daily_prediction(model,label_encoder,cursor):
    query = psg2.sql.SQL("""
            SELECT * 
            FROM ADJ_CLOSE AC
            WHERE AC.DATE BETWEEN CURRENT_DATE - INTERVAL '60 days' AND CURRENT_DATE;
        """)
    cursor.execute(query)
    days_data = pd.Dataframe(cursor.fetchall(), columns=[desc[0] for desc in cursor.description]])
    
    
    
    
    
