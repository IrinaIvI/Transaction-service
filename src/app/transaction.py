from datetime import datetime
from decimal import Decimal
from typing import Annotated, List

from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import AccountModel, TransactionsModel
from app.database import get_db
from app.schemas import ReportScheme

HTTP_OK_STATUS = 200
HTTP_BAD_REQUEST_STATUS = 400


class Transactions:
    """Класс для работы с транзакциями."""

    def create_account(
        self,
        user_id: int,
        db: Annotated[Session, Depends(get_db)],
    ):
        """Создание аккаунта пользователя."""
        existing_account = db.query(AccountModel).filter(
            AccountModel.user_id == user_id,
        ).first()
        if existing_account is None:
            new_account = AccountModel(
                user_id=user_id,
                balance=0,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            db.add(new_account)
            db.commit()
        return 'Ошибка при создании аккаунта'

    def create_transaction(
        self,
        user_id: int,
        amount: Decimal,
        operation: str,
        db: Annotated[Session, Depends(get_db)],
    ):
        """Создание транзакции."""
        account = db.query(AccountModel).filter(
            AccountModel.user_id == user_id,
        ).one_or_none()

        if account is None:
            account = self.create_account(user_id=user_id, db=db)

        if amount < 0:
            raise HTTPException(
                status_code=HTTP_BAD_REQUEST_STATUS,
                detail='Сумма меньше нуля',
            )

        verified_query = text("""
            SELECT verified
            FROM ivashko_schema.users_ivashko
            WHERE id = :user_id;
        """)
        verified_result = db.execute(verified_query, {'user_id': user_id})
        verified_user_row = verified_result.fetchone()

        if verified_user_row is None:
            raise HTTPException(
                status_code=HTTP_BAD_REQUEST_STATUS,
                detail=f'Пользователь с айди {user_id} не найден',
            )

        verified_user = verified_user_row[0]

        if operation.upper() == 'DEBIT':
            new_balance = account.balance + amount
        elif account.balance >= amount or verified_user:
            new_balance = account.balance - amount
        else:
            raise HTTPException(
                status_code=HTTP_BAD_REQUEST_STATUS,
                detail='Недостаточно средств на балансе и пользователь не верифицирован',
            )

        update_query = text("""
            UPDATE ivashko_schema.account_ivashko
            SET balance = :new_balance, updated_at = :updated_at
            WHERE user_id = :user_id
        """)
        db.execute(update_query, {
            'new_balance': new_balance,
            'updated_at': datetime.now(),
            'user_id': user_id,
        })

        insert_transaction_query = text("""
            INSERT INTO ivashko_schema.transactions_ivashko
            (account_id, amount, "type", balance_after, created_at)
            VALUES (:account_id, :amount, :type, :balance_after, :created_at)
        """)
        db.execute(insert_transaction_query, {
            'account_id': account.id,
            'amount': amount,
            'type': operation.upper(),
            'balance_after': new_balance,
            'created_at': datetime.now(),
        })
        db.commit()
        return JSONResponse(
            content={'status': 'Операция корректная'},
            status_code=HTTP_OK_STATUS,
        )

    def get_transaction(
        self,
        user_id: int,
        start: datetime,
        end: datetime,
        db: Annotated[Session, Depends(get_db)],
    ) -> List[ReportScheme]:
        """Получение транзакции."""
        account = db.query(AccountModel).filter(
            AccountModel.user_id == user_id,
        ).first()
        list_of_trans = db.query(TransactionsModel).filter(
            TransactionsModel.account_id == account.id,
            TransactionsModel.created_at >= start,
            TransactionsModel.created_at <= end,
        ).all()

        report = [
            ReportScheme(
                amount=transaction.amount,
                balance_after=transaction.balance_after,
                created_at=transaction.created_at,
            )
            for transaction in list_of_trans
        ]

        if report:
            return report

        return JSONResponse(
            content={'status': 'За определенный промежуток операций не было'},
            status_code=HTTP_OK_STATUS,
        )
