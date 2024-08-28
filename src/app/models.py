from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, BIGINT, Enum, Table, MetaData
from enum import Enum as PyEnum
from sqlalchemy.orm import registry
from sqlalchemy.ext.declarative import declarative_base
from .database import engine

metadata = MetaData(schema="ivashko_schema")
Base = declarative_base(metadata=metadata)

mapper_registry = registry()

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

user_table = Table('users_ivashko', Base.metadata, autoload_with=engine, schema='ivashko_schema')

class User:
    pass

mapper_registry.map_imperatively(User, user_table)
