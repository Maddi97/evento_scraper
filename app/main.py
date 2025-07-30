from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Web Scraper API")

app.include_router(router)