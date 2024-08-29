import pytest
from datetime import datetime
from app.transaction import Transactions
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
from app.models import Base


@pytest.fixture(scope='session')
def setup_test_database():
    engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/test_db')
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)
    yield engine
    drop_database(engine.url)

@pytest.mark.parametrize('user_id, amount, transaction_type',
 [pytest.param(1, 1000, 'DEBIT',  id='is correct'),
  pytest.param(4, 1000, 'debit', id='is not correct', marks=pytest.mark.xfail()),
  pytest.param(1, -1000, 'DEBIT', id='is not correct', marks=pytest.mark.xfail()),
  pytest.param(1, 1000, '?', id='is not correct', marks=pytest.mark.xfail()),
  ]
)
def test_create_transaction(user_id, amount, transaction_type, setup_test_database):
    setup_test_database
    transaction = Transactions().create_transaction(user_id, amount, transaction_type)
    assert transaction == JSONResponse(content={"status": "Операция корректная"}, status_code=200)

@pytest.mark.parametrize('user_id, start, end', [
    pytest.param(1, datetime.now(), datetime.now(), id='is correct'),
    pytest.param(-1, datetime.now(), datetime.now(), id='is not correct', marks=pytest.mark.xfail())
])
def test_get_transaction(user_id, start, end, setup_test_database):
    setup_test_database
    Transactions().create_transaction(1, 500, 'DEBIT')
    resulting_report = Transactions().get_transaction(user_id, start, end)
    report = [{'amount': 500, 'balance_after': 500, 'created_at': datetime.now()}]
    assert resulting_report == report
