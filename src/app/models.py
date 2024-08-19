from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, BIGINT, Enum, MetaData, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

metadata = MetaData()
Base = declarative_base(metadata=metadata)

class TransactionType(PyEnum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"

class AccountModel(Base):
    __tablename__ = "account_ivashko"
    __table_args__ = {"schema": "transaction_ivashko"}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('auth_schema_ivashko.users_ivashko.id'))
    balance = Column(BIGINT, nullable=False)
    created_at = Column(TIMESTAMP, default=None)
    updated_at = Column(TIMESTAMP, default=None)

class TransactionsModel(Base):
    __tablename__ = "transactions_ivashko"
    __table_args__ = {"schema": "transaction_ivashko"}

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('transaction_ivashko.account_ivashko.id'))
    amount = Column(BIGINT, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    balance_after = Column(BIGINT, nullable=False)
    created_at = Column(TIMESTAMP, default=None)
