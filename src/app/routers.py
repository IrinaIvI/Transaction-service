from fastapi import APIRouter, Depends
from typing import Annotated
from decimal import Decimal
from datetime import datetime
from fastapi.responses import JSONResponse

from app.transaction import Transactions, create_base

router = APIRouter(
    prefix="/transaction_service",
)

@router.post('/create_transaction')
def create_transaction(result: Annotated[int, Decimal, str, Depends(Transactions().create_transaction)]):
    return result

@router.get('/get_transaction')
def get_transaction(report: Annotated[int, datetime, datetime, Depends(Transactions().get_transaction)]):
    return report

@router.get('/create_base')
def router_create_base():
    create_base()
    return "База очищена и создана"

@router.get('/health/ready')
async def health_check():
    return JSONResponse(status_code=200, details='succes')
