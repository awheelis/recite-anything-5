from fastapi import FastAPI

from app.routes import bible

app = FastAPI(title="Recite Anything", version="0.1.0")

app.include_router(bible.router, prefix="/api/bible", tags=["bible"])
