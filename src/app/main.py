from fastapi import FastAPI
from app.routers import router

app = FastAPI(title='transaction_service')
app.include_router(router)
