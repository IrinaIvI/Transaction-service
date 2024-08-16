from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, BIGINT, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

Base = declarative_base()

class TransactionType(PyEnum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"

class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    balance = Column(BIGINT, nullable=False)
    created_at = Column(TIMESTAMP, default=None)
    updated_at = Column(TIMESTAMP, default=None)

    user = relationship("User", back_populates="account")
    transactions = relationship("Transactions", back_populates="account")

class Transactions(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id'))
    amount = Column(BIGINT, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    balance_after = Column(BIGINT, nullable=False)
    created_at = Column(TIMESTAMP, default=None)

    account = relationship("Account", back_populates="transactions")
