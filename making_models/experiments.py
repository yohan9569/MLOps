import itertools
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
from prophet.diagnostics import cross_validation, performance_metrics

# Define the sweep # sweep_config.yaml

# Initialize the sweep
sweep_id = wandb.sweep(sweep_config, project="mlops_prophet")
n_cups = multiprocessing.cpu_count()

# 데이터 불러오기
conn = connect()
data = pd.read_sql("select * from stock_data;", conn)

# 전처리
data = preprocess(data)

# 실험 함수
def experiment():
    with wandb.init() as run:

        # metrics = {"cv_rmse": }
        wandb.log(metrics)


# 실험 실행 Run the sweep agent
count = 5
wandb.login(key="638bebf7fb7de2d84c427979c5808703b7eee6f4")
wandb.agent(sweep_id, function=experiment, count=count)

# db에 기록?


# 3. Initialize a sweep
# wandb sweep sweep.yaml
# 4. Launch agent(s)
# wandb agent your-sweep-id
# 5. Visualize results
#
