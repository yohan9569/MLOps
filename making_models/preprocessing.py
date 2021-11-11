import pandas as pd

def preprocess(data):
    # 결측치 처리
    data = data.fillna(method="ffill")

    # prophet 요구 컬럼 생성
    data['y'] = data['Close']
    data['ds'] = data['Date']

    return data
