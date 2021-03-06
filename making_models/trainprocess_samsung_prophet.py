# -*- coding: utf-8 -*-

import warnings
import os
import datetime
import json

import numpy as np
import pandas as pd
import FinanceDataReader as fdr
from prophet import Prophet
from dateutil.relativedelta import *
from prophet.serialize import model_to_json

from preprocessing import preprocess
from m_m_db import connect
from m_m_query import *



warnings.filterwarnings('ignore')
# db 연결
conn = connect()

# 주가 데이터 가져오기
# 삼성전자 주식코드: 005930
stock_code = '005930'
base_date = (datetime.datetime.today()+relativedelta(years=-1)).strftime('%Y-%m-%d')
stock = fdr.DataReader(stock_code, base_date)

# db에 데이터 넣기
stock.to_sql('stock_data', conn, if_exists='replace')

# 데이터 불러오기
data = pd.read_sql("select * from stock_data;", conn)
data = preprocess(data)

data['y'] = data['Close']
data['ds'] = data['Date']

m = Prophet()
m.fit(data)

model_path = '/Users/TFG5076XG/Desktop/learning_mlops/samsung_prophet_model.json'
with open(model_path, 'w') as fout:
    json.dump(model_to_json(m), fout)



# 모델 넣는 쿼리 실행
conn.execute(
    insert_or_update_model.format(
        mn='samsung_prophet_model', mf=model_path
    )
)


