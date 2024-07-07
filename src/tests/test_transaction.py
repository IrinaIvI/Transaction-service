import pytest
import time
from app.transaction import Transactions

# @pytest.fixture
# def create_base():
#     tuple_time = (2019, 12, 7, 14, 30, 30, 5, 0, 0)
#     init_time = time.asctime(tuple_time)
#     users = {1: [2000, init_time],
#              2: [3000, init_time],
#              3: [4000, init_time],
#             }

@pytest.mark.parametrize('user_id, amount, transaction_type',
 [pytest.param(1, 1000, '+',  id='is correct'),
  pytest.param(4, 1000, '+', id='is not correct', marks=pytest.mark.xfail()),
  pytest.param(1, -1000, '+', id='is not correct', marks=pytest.mark.xfail()),
  pytest.param(1, 1000, '?', id='is not correct', marks=pytest.mark.xfail()),
  ]
)
def test_create_transaction(user_id, amount, transaction_type):
    assert Transactions().create_transaction(user_id, amount, transaction_type) == None

@pytest.mark.parametrize('user_id, start, end', [
    pytest.param(1, time.time(), time.time())
])
def test_get_transaction(user_id, start, end):
    #Transactions().create_transaction(1, 1500, '-')
    assert Transactions().get_transaction(user_id, start, end) == [[500, time.time()], [1000, time.time()]]
