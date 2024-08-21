#from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
import logging
from app.models import AccountModel, TransactionsModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import Annotated, List
from fastapi import Depends, HTTPException
from app.database import get_db
from app.schemas import ReportScheme
from fastapi.responses import JSONResponse


class Transactions:
    """Класс для работы с транзакциями."""

    def create_account(self, id: int, db: Annotated[Session, Depends(get_db)]):
        """Создание аккаунта пользователя."""
        try:
            existing_account = db.query(AccountModel).filter(AccountModel.user_id == id).first()
            if existing_account is None:
                new_account = AccountModel(
                    user_id=id,
                    balance=0,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.add(new_account)
                db.commit()
                logging.info(f"Создан новый аккаунт для пользователя {id} с балансом 0")
            else:
                logging.info(f"Аккаунт для пользователя {id} уже существует")
        except Exception as e:
            db.rollback()
            logging.error(f"Ошибка при создании аккаунта: {e}")
            return 'Ошибка при создании аккаунта'

    def create_transaction(self, user_id: int, amount: Decimal, operation: str, db: Annotated[Session, Depends(get_db)]):
        """Создание транзакции."""
        account = db.query(AccountModel).filter(AccountModel.user_id == user_id).one_or_none()

        if amount < 0:
            raise HTTPException(status_code=400, detail="Сумма меньше нуля")

        verified_query = text("""SELECT verified FROM ivashko_schema.users_ivashko
                        WHERE id = :user_id;""")
        result = db.execute(verified_query, {'user_id': user_id})
        verified_user_row = result.fetchone()

        if verified_user_row is None:
            raise HTTPException(status_code=400, detail=f"Пользователь с айди {user_id} не найден")

        verified_user = verified_user_row[0]
        db.commit()

        if operation == 'DEBIT':
            new_balance = account.balance + amount
        elif account.balance >= amount or verified_user:
            new_balance = account.balance - amount
        else:
            raise HTTPException(status_code=400, detail="Недостаточно средств на балансе и пользователь не верифицирован")

        update_query = text("""
            UPDATE ivashko_schema.account_ivashko
            SET balance = :new_balance, updated_at = :updated_at
            WHERE user_id = :user_id
        """)
        db.execute(update_query, {
            'new_balance': new_balance,
            'updated_at': datetime.now(),
            'user_id': user_id
        })

        insert_transaction_query = text("""
            INSERT INTO ivashko_schema.transactions_ivashko
            (account_id, amount, "type", balance_after, created_at)
            VALUES (:account_id, :amount, :type, :balance_after, :created_at)
        """)
        db.execute(insert_transaction_query, {
            'account_id': account.id,
            'amount': amount,
            'type': operation,
            'balance_after': new_balance,
            'created_at': datetime.now()
        })
        db.commit()
        return JSONResponse(content={"status": "Операция корректная"}, status_code=200)


    def get_transaction(self, user_id: int, start: datetime, end: datetime, db: Annotated[Session, Depends(get_db)]) -> List[ReportScheme]:
        """Получение транзакции."""
        account = db.query(AccountModel).filter(AccountModel.user_id == user_id).first()
        list_of_trans = db.query(TransactionsModel).filter(
            TransactionsModel.account_id == account.id,
            TransactionsModel.created_at >= start,
            TransactionsModel.created_at <= end
            ).all()

        report = [ReportScheme(
        amount=transaction.amount,
        balance_after=transaction.balance_after,
        created_at=transaction.created_at
        ) for transaction in list_of_trans]

        if report:
            return report
        else:
            return {'status': 'За определенный промежуток операций не было'}
