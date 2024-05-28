import pandas as pd
import psycopg2 as psg2
import yfinance as yf
import utils

#take the sp500 symbols
sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
symbols = sp500['Symbol'].tolist()

#connect to database
psql_user = 'janko80'
psql_pass = 'Jankojanko80'
psql_host = 'localhost'
psql_db = 'tradingdash'

conn = psg2.connect(
    dbname=psql_db,
    user = psql_user,
    password = psql_pass,
    host = psql_host
    )
cur = conn.cursor()
#check if the table exist
adj_close = utils.check_table('ADJ_CLOSE',cur)


