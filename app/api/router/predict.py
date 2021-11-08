
import json
from enum import Enum

import numpy as np
import pandas as pd
from prophet import Prophet
from prophet.serialize import model_from_json
from fastapi import APIRouter

from app.database import engine
from app.query import *

router = APIRouter()


class ModelName(str, Enum):
    prophet = 'prophet'



# 여기에 라우터 연결해서 여기다가 구현하는 게 맞을까? 그게 더 편할 것 같네
@router.get("/models/{model_name}/predict")
async def predict_model(model_name: ModelName, periods: int = 30):
    # return {"Hello": "World"}
    if model_name.value == 'prophet':
        # periods 받아서 예측 모듈 실행, 결과값 리턴
        preds = predict(periods)

        return {"model_name": model_name, "predictions": preds}



def predict(periods=30):

    # db 연결하기
    # db에서 모델 경로 가져오기 # 꺼내오는 쿼리 만들기
    model_path = engine.execute(
        SELECT_MODEL_PATH.format(
            mn='samsung_prophet_model'
        )
    ).first() # fetchone은 다음 줄 꺼내도록 기다림. 난 한 줄만 필요.
    # 얘도 추상화?


    with open(model_path[0], 'r') as fin:
        m = model_from_json(json.load(fin))

    future = m.make_future_dataframe(periods=periods, freq='b')
    forecast = m.predict(future)

    return forecast # 데이터 프레임을 던져도 되려나? - 괜춘









