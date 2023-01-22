from fastapi import FastAPI

from SeleniumAgent import *
from fastapi import Security, Depends, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKey
from starlette.status import HTTP_403_FORBIDDEN

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


@app.get("/makePrediction{string}")
def demo_get(string: str, api_key: APIKey = Depends(get_api_key)):
    driver = createDriver()
    result = makePrediction(driver, string)
    return result
