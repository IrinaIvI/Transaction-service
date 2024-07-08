import pytest
import time
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
    #Arrange
    create_test_base
    #Act
    transaction = Transactions().create_transaction(user_id, amount, transaction_type)
    #Assert
    assert transaction == None

@pytest.mark.parametrize('user_id, start, end', [
    pytest.param(1, time.ctime(time.time()), time.ctime(time.time()), id='is correct'),
    pytest.param(4, time.ctime(time.time()), time.ctime(time.time()), id='is not correct', marks=pytest.mark.xfail())
])
def test_get_transaction(user_id, start, end, create_test_base):
    #Arange
    create_test_base
    Transactions().create_transaction(1, 1500, '-')
    transaction = transactions.get(user_id)[0]
    #Act
    resulting_report = Transactions().get_transaction(user_id, start, end)
    report = [[500, transaction.time]]
    #Assert
    assert resulting_report == report
