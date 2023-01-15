from fastapi import FastAPI

app = FastAPI(docs_url="/docs",
              title="Marmara Stock Market Analyzer Back End.",
              description="An API for analyzing given stock",
              version="1.0.0")


@app.get("/test")
def root():
    return "Yusuf2"
