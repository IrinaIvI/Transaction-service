from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, BIGINT, Enum, Table, MetaData
from enum import Enum as PyEnum
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData(schema="ivashko_schema")
Base = declarative_base(metadata=metadata)

class TransactionType(PyEnum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"

class AccountModel(Base):
    __tablename__ = "account_ivashko"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('ivashko_schema.users_ivashko.id'))
    balance = Column(BIGINT, nullable=False)
    created_at = Column(TIMESTAMP, default=None)
    updated_at = Column(TIMESTAMP, default=None)

class TransactionsModel(Base):
    __tablename__ = "transactions_ivashko"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('ivashko_schema.account_ivashko.id'))
    amount = Column(BIGINT, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    balance_after = Column(BIGINT, nullable=False)
    created_at = Column(TIMESTAMP, default=None)
