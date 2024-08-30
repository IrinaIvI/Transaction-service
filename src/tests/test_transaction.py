from unittest.mock import patch
import pytest
from app.transaction import Transactions
from fastapi.responses import JSONResponse
from datetime import datetime

@pytest.mark.parametrize('user_id, amount, transaction_type',
 [pytest.param(1, 1000, 'DEBIT', id='is correct'),
  pytest.param(4, 1000, 'debit', id='is not correct', marks=pytest.mark.xfail()),
  pytest.param(1, -1000, 'DEBIT', id='is not correct', marks=pytest.mark.xfail()),
  pytest.param(1, 1000, '?', id='is not correct', marks=pytest.mark.xfail()),
  ]
)
@patch('app.transaction.Transactions.create_transaction')
def test_create_transaction(mock_create_transaction, user_id, amount, transaction_type):
    mock_create_transaction.return_value = JSONResponse(content={"status": "Операция корректная"}, status_code=200)

    transaction = Transactions().create_transaction(user_id, amount, transaction_type)
    assert transaction == JSONResponse(content={"status": "Операция корректная"}, status_code=200)

@pytest.mark.parametrize('user_id, start, end', [
    pytest.param(1, datetime.now(), datetime.now(), id='is correct'),
    pytest.param(-1, datetime.now(), datetime.now(), id='is not correct', marks=pytest.mark.xfail())
])
@patch('app.transaction.Transactions.get_transaction')
@patch('app.transaction.Transactions.create_transaction')
def test_get_transaction(mock_create_transaction, mock_get_transaction, user_id, start, end):
    mock_create_transaction.return_value = None
    mock_get_transaction.return_value = [{'amount': 500, 'balance_after': 500, 'created_at': datetime.now()}]

    Transactions().create_transaction(1, 500, 'DEBIT')
    resulting_report = Transactions().get_transaction(user_id, start, end)
    report = [{'amount': 500, 'balance_after': 500, 'created_at': datetime.now()}]
    assert resulting_report == report
