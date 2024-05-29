import pandas as pd
import psycopg2 as psg2
from sqlalchemy import create_engine
import yfinance as yf
from utils import DataUpdater, Predictor
import pickle as pk
import keras

def main():
    #connect to database

    con_string = 'postgres://janko80:Jankojanko80@localhost/tradingdash'
    sqla_eng = create_engine(con_string)
    sqla_conn = con_string.connect()
    psg2_conn = psg2.connect(con_string)
    cur = psg2_conn.cursor()
    #check if the table exist
    data_updater = DataUpdater('ADJ_CLOSE',cur)
    adj_close_exist = data_updater.check_table()

    if adj_close_exist:
        #update with today's data
        daily_update = data_updater.daily_update()
        daily_update.to_sql('ADJ_CLOSE',con=sqla_conn,if_exists='append')
        #make pred with today's data
        prediction_data = data_updater.prediction_data()
        model = keras.saving.load_model('prod_model.keras')
        with open('prod_label_encoder.pkl','rb') as file:
            label_encoder = pk.load(file)
        predictor = Predictor(prediction_data, model, label_encoder)
        #make pred
        predicted_data = predictor.make_pred(days=15)
        #insert data
        predicted_data.to_sql('PRED_ADJ_CLOSE',con=sqla_conn,if_exists='replace')

    else:
        #update with data from 2010
        full_update = data_updater.full_update()
        #insert data
        full_update.to_sql('ADJ_CLOSE',con=sqla_conn,if_exists='replace')
        
    sqla_conn.close()
    psg2_conn.close()
    
if __name__ == "__main__":
    main()
    

    