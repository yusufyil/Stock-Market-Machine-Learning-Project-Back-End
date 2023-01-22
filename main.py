from fastapi import FastAPI

from SeleniumAgent import *

app = FastAPI(docs_url="/docs",
              title="Marmara Stock Market Analyzer Back End.",
              description="An API for analyzing given stock",
              version="1.0.0")


@app.get("/makePrediction{string}")
def demo_get(string: str):
    driver = createDriver()
    result = makePrediction(driver, string)
    return result
