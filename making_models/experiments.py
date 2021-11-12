import multiprocessing
import os
import warnings
from os.path import join

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import wandb
from m_m_db import connect
from m_m_query import *
from preprocessing import preprocess
from prophet import Prophet

sweep_config = {}

sweep_id = wandb.sweep(sweep_config, project="mlops_prophet")
n_cups = multiprocessing.cpu_count()

# 데이터 불러오기
conn = connect()
data = pd.read_sql("select * from stock_data;", conn)

# 전처리
data = preprocess(data)

# 실험 함수
def experiment():

    metrics = {}
    wandb.log(metrics)


# 실험 실행
count = 5
wandb.agent(sweep_id, function=experiment, count=count)

# db에 기록?
