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
    expected_response = JSONResponse(content={"status": "Операция корректная"}, status_code=200)
    mock_create_transaction.return_value = expected_response
    transaction = Transactions().create_transaction(user_id, amount, transaction_type)
    assert transaction.body.decode() == expected_response.body.decode()
    assert transaction.status_code == expected_response.status_code

@pytest.mark.parametrize('user_id, start, end', [
    pytest.param(1, datetime.now(), datetime.now(), id='is correct'),
    pytest.param(-1, datetime.now(), datetime.now(), id='is not correct', marks=pytest.mark.xfail())
])
@patch('app.transaction.Transactions.get_transaction')
@patch('app.transaction.Transactions.create_transaction')
def test_get_transaction(mock_create_transaction, mock_get_transaction, user_id, start, end):
    mock_create_transaction.return_value = JSONResponse(content={"status": "Операция корректная"}, status_code=200)
    fixed_datetime = datetime(2024, 8, 30, 12, 22, 46)
    mock_get_transaction.return_value = [{'amount': 500, 'balance_after': 500, 'created_at': fixed_datetime}]
    Transactions().create_transaction(1, 500, 'DEBIT')
    resulting_report = Transactions().get_transaction(user_id, start, end)
    expected_report = [{'amount': 500, 'balance_after': 500, 'created_at': fixed_datetime}]
    assert resulting_report == expected_report
