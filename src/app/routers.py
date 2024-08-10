from fastapi import APIRouter, Depends
from typing import Annotated
from decimal import Decimal
from datetime import datetime

from app.transaction import Transactions

router = APIRouter(
    prefix="/transaction_service",
)


@router.post('/create_transaction')
def create_transaction(result: Annotated[int, Decimal, str, Depends(Transactions().create_transaction)]):
    return result

@router.get('/get_transaction')
def get_transaction(report: Annotated[int, datetime, datetime, Depends(Transactions().get_transaction)]):
    return report

