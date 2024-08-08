import pytest
from datetime import datetime
from app.transaction import Transactions, create_base, transactions, users, reports


@pytest.fixture
def create_test_base():
    transactions.clear()
    users.clear()
    reports.clear()
    create_base()
    yield

@pytest.mark.parametrize('user_id, amount, transaction_type',
 [pytest.param(1, 1000, '+',  id='is correct'),
  pytest.param(4, 1000, '+', id='is not correct', marks=pytest.mark.xfail()),
  pytest.param(1, -1000, '+', id='is not correct', marks=pytest.mark.xfail()),
  pytest.param(1, 1000, '?', id='is not correct', marks=pytest.mark.xfail()),
  ]
)
def test_create_transaction(user_id, amount, transaction_type, create_test_base):
    create_test_base
    transaction = Transactions().create_transaction(user_id, amount, transaction_type)
    assert transaction == 'Correct operation'

@pytest.mark.parametrize('user_id, start, end', [
    pytest.param(1, datetime.now().strftime('%Y-%m-%dT%H:%M:%S'), datetime.now().strftime('%Y-%m-%dT%H:%M:%S'), id='is correct'),
    pytest.param(4, datetime.now().strftime('%Y-%m-%dT%H:%M:%S'), datetime.now().strftime('%Y-%m-%dT%H:%M:%S'), id='is not correct', marks=pytest.mark.xfail())
])
def test_get_transaction(user_id, start, end, create_test_base):
    create_test_base
    Transactions().create_transaction(1, 1500, '-')
    transaction = transactions.get(user_id)[0]
    resulting_report = Transactions().get_transaction(user_id, start, end)
    report = [[500, transaction.time]]
    assert resulting_report == report
