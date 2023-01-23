from fastapi import FastAPI

from SeleniumAgent import *
from fastapi import Security, Depends, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKey
from starlette.status import HTTP_403_FORBIDDEN
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(docs_url="/docs",
              title="Marmara Stock Market Analyzer Back End.",
              description="An API for analyzing given stock",
              version="1.0.0")

TOKEN = "canavarYusuf"
api_key_query = APIKeyQuery(name="token", auto_error=False)


async def get_api_key(api_key_query: str = Security(api_key_query)):
    if api_key_query == TOKEN:
        return api_key_query
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials")

class days(BaseModel):
    Kapanis: float
    Min: float
    Max: float
    Aof: float
    Hacim: float
    Sermaye: float
    USDTRY: float
    Bist100: float
    Piyasa_degeri_mn_TL: float
    Piyasa_degeri_mn_USD: float
    Halka_acik_PD_mn_TL: float
    Halka_acik_PD_mn_USD: float
class stock(BaseModel):
    stock_code: str
    prediction: float
    days: list[days]


@app.get("/makePrediction/{string}")
def demo_get(string: str, api_key: APIKey = Depends(get_api_key)):
    driver = createDriver()
    result = makePrediction(driver, string)
    print(type(result))
    print(result)
    print(type(result["prediction"]))
    return stock.parse_obj(result)
