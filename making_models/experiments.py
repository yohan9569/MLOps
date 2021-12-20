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


# 실험 함수
def experiment():
    with wandb.init() as run:
        # 실험할 파라미터 범위 불러오기
        params = wandb.config

        # db 연결하기
        conn = connect()

        # 주가 데이터 가져오기
        # 삼성전자 주식코드: 005930
        stock_code = "005930"
        base_date = (
            datetime.datetime.today() + relativedelta(years=-1)
        ).strftime("%Y-%m-%d")
        stock = fdr.DataReader(stock_code, base_date)

        # db에 데이터 넣기
        stock.to_sql("stock_data", conn, if_exists="replace")

        # 데이터 불러오기
        data = pd.read_sql("select * from stock_data;", conn)

        # 전처리
        data = preprocess(data)

        # 학습 ### cv 구현해야 함.
        m = Prophet()
        m.fit(data)

        # 모델 저장 ### 어떻게 베스트 버전 파일만 저장할까?
        # 모델 파일 만들기 ### 버전마다 이름 다르게 해야 함.
        model_path = (
            "/Users/TFG5076XG/Desktop/MLOps/samsung_prophet_model.json"
        )
        with open(model_path, "w") as fout:
            json.dump(model_to_json(m), fout)

        # db에 모델 넣기
        conn.execute(
            insert_or_update_model.format(
                mn="samsung_prophet_model", mf=model_path
            )
        )

        metrics = {"cv_rmse": cv_rmse}
        wandb.log(metrics)


# 실험 실행 Run the sweep agent
count = 5
wandb.login(key="638bebf7fb7de2d84c427979c5808703b7eee6f4")
wandb.agent(sweep_id, function=experiment, count=count)


### 이 아래 항목들 위랑 겹치는 것 같다. 출처가 다른 곳에서 가져온 프로세스라서 헷갈림.
# 3. Initialize a sweep
# wandb sweep sweep_config.yaml
# 4. Launch agent(s)
# wandb agent your-sweep-id
# 5. Visualize results


### 211220 현재 고민
# 자동 로그인?
# cv 돌리는 법 -> prophet docs 봐가면서
# metric 구하기
# metric 기준으로 좋은 애만 파일 남기기 -> db에 저장된 게 아니라 drop 하기 까다롭
## 일단 metric만 저장하고 best 나오면 그걸로 한번 더 학습해서 model file 남길까?
### db에 기록?
# 뭘 기록? -> 실험 내용 기록, 언제 무슨 실험한 건지도?(실험 명 같은 걸로 기록하면 따로 테이블 만들 건 없을 듯)
# 어디에 기록? -> 따로 테이블 만들기
# 함수에 기록하는 기능도 넣어야 할 듯.
