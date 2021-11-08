import pandas as pd

def preprocess(data):
    # fill na
    data = data.fillna(method="ffill")

    return data
