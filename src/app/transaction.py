from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

init_time = datetime(2019, 12, 7, 14, 30).strftime('%Y-%m-%dT%H:%M:%S')
users = {}
transactions = {}
reports = {}


def create_base():
    """Функция создания контейнера с данными юзеров."""
    transactions.clear()
    reports.clear()
    users.clear()

    users[1] = [2000, init_time]
    users[2] = [3000, init_time]
    users[3] = [4000, init_time]


create_base()


class Transactions:
    """Класс для работы с транзакциями."""

    @dataclass
    class Transaction:
        """Класс транзакции."""

        _current_amount: Decimal = 0
        _transaction_time: datetime = init_time

        @property
        def amount(self) -> Decimal:
            """Получение текущей суммы транзакции."""
            return self._current_amount

        @property
        def time(self) -> datetime:
            """Получение даты совершения транзакции."""
            return self._transaction_time

    def create_transaction(self, user_id: int, amount: Decimal, operation: str):
        """Создание транзакции."""
        if user_id in users:
            current_balance = users.get(user_id)[0]
            if amount < 0:
                raise ValueError('Error, incorrect amount')
            else:
                if operation == '+':
                    current_balance += amount
                elif operation == '-' and current_balance >= amount:
                    current_balance -= amount
                else:
                    raise ValueError('Error, incorrect operation')

            users.get(user_id)[0] = current_balance

            tr = Transactions.Transaction(current_balance, datetime.now())
            transactions.setdefault(user_id, []).append(tr)
            return 'Correct operation'
        raise ValueError('Error, this user is not exist')

    def get_transaction(self, user_id: int, start: datetime, end: datetime) -> list:
        """Получение транзакции."""
        report = []
        list_of_trans = transactions.get(user_id, [])
        for transaction in list_of_trans:
            if start <= transaction.time <= end:
                report.append([transaction.amount, transaction.time])

        if report:
            reports.setdefault(user_id, []).append(report)
            return report
        else:
            return 'There is no any report'
        # """Получение транзакции."""
        # report = []
        # list_of_trans = transactions.get(user_id)
        # for transaction in list_of_trans:
        #     if transaction.time >= start and transaction.time <= end:
        #         report.append([transaction.amount, transaction.time])
        #         reports.setdefault(user_id, []).append(report)
        #     else:
        #         return 'There is no any report'
        # return report
