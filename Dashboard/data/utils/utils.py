import psycopg2 as psg2
from psycopg2 import sql
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import tensorflow as tf 


class DataUpdater:
    def __init__(self,tablename,cursor):
        self.tablename = tablename
        self.cursor = cursor

    def check_table(self):
        query = sql.SQL("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = %s
                );
                """)
        self.cursor.execute(query, (self.tablename,))
        return self.cursor.fetchone()[0]
    
    def daily_update(self): 
        query = sql.SQL("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'public'
                AND table_name = %s;
            """)
        self.cursor.execute(query, (self.tablename,))
    
        symbols = [row[0] for row in self.cursor.fetchall()]
        symbols.remove('Date')
        today_data = yf.download(
            symbols,
            start='2010-01-01',
           end=pd.Timestamp.today().date()
                        )['Adj Close']
        today_data = today_data.fillna(0.0)
        return today_data

    def full_update(self):
        sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
        symbols = sp500['Symbol'].tolist()
        full_data = yf.download(symbols,start='2010-01-01', end=pd.Timestamp.today().date())['Adj Close']
        full_data = full_data.dropna(axis=1, how='all')
        full_data = full_data.fillna(0.0)
        return full_data
    

    def prediction_data(self): 
        query = sql.SQL("""
                SELECT * 
                FROM "ADJ_CLOSE" AC
                WHERE AC."Date"::Date BETWEEN CURRENT_DATE - INTERVAL '120 days' AND CURRENT_DATE;
            """)
        self.cursor.execute(query)
        days_data = pd.DataFrame(self.cursor.fetchall(), columns=[desc[0] for desc in self.cursor.description])
        days_data = days_data.drop(labels=['Date','GEV'],axis=1)
        return days_data
    

class Predictor:
    def __init__(self,data,model,label_encoder):
        self.data = data
        self.model = model
        self.label_encoder = label_encoder

    def make_pred(self,days):
        scaler = MinMaxScaler(feature_range=(0, 1))
        stock_names = self.data.columns.values
        stock_name_to_int = self.label_encoder.transform(stock_names)
        stock_name_to_int_dict = {stock: stock_int for stock, stock_int in zip(self.data.columns, stock_name_to_int)}
        
        all_predictions = {}

        for stock in self.data.columns:
            stock_data = self.data[stock].values.reshape(-1, 1)
            scaled_stock_data = scaler.fit_transform(stock_data)
            stock_label = stock_name_to_int_dict[stock]
            
            # Create batches with stock label included
            current_batch = scaled_stock_data[-60:].reshape(1, 60, 1)
            stock_label_batch = np.full((1, 60, 1), stock_label).astype(np.float32)
            current_batch_with_label = np.concatenate((current_batch, stock_label_batch), axis=2)
            
            predicted_prices = []
            for _ in range(days):
                next_prediction = self.model.predict(current_batch_with_label)
                next_prediction_reshaped = next_prediction.reshape(1, 1, 1)
                stock_label_reshaped = np.array(stock_label).reshape(1, 1, 1)
                next_prediction_with_label = np.concatenate((next_prediction_reshaped, stock_label_reshaped), axis=2)
                current_batch_with_label = np.append(current_batch_with_label[:, 1:, :], next_prediction_with_label, axis=1)
                predicted_prices.append(scaler.inverse_transform(next_prediction)[0, 0])
            
            all_predictions[stock] = predicted_prices
        all_predictions = pd.DataFrame(all_predictions)
        dates = []
        for i in range(1,16):
            dates.append(pd.Timestamp.today().date() + pd.Timedelta(days=i))
        all_predictions['DATE'] = dates
        all_predictions = all_predictions.reset_index(drop=True)
        all_predictions = all_predictions.set_index('DATE')
        return all_predictions
            