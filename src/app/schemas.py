from typing import Optional

from pydantic import BaseModel
from datetime import datetime

class ReportScheme(BaseModel):
    """Схема отчета о транзакциях."""

    amount: int
    balance_after: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True



