from typing import Optional
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel

from app.api.router import predict


app = FastAPI()


# 라우터 등록
app.include_router(predict.router)



class Item(BaseModel):  # tutorial_contents
    name: str
    price: float
    is_offer: Optional[bool] = None


class ModelName(str, Enum):
    prophet = 'prophet'



@app.get("/")
async def rad_root():
    return {"Hello":"World"}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name.value == 'prophet':
        return {"model_name": model_name,
                "message": "Prophet is open source software released by Facebook’s Core Data Science team. It is available for download on CRAN and PyPI."}
    return {"model_name": model_name, "message": "enjoy it!"}




# uvicorn main:app --reload
