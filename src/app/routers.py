from fastapi import APIRouter, Depends
from typing import Annotated, List
from decimal import Decimal
from datetime import datetime
from fastapi.responses import JSONResponse
from app.schemas import ReportScheme
from app.transaction import Transactions

router = APIRouter(
    prefix="/transaction_service",
)

@router.post('/create_transaction')
def create_transaction(result: Annotated[int, Decimal, str, Depends(Transactions().create_transaction)]):
    return result

@router.get('/get_transaction', response_model=List[ReportScheme])
def get_transaction(report: Annotated[int, datetime, datetime, Depends(Transactions().get_transaction)]):
    return report

@router.get('/health/ready')
async def health_check():
    return JSONResponse(status_code=200, content={"message": "success"})
