import time
from dataclasses import dataclass
from typing import Union, NoReturn

tuple_time = (2019, 12, 7, 14, 30, 30, 5, 0, 0)
init_time = time.asctime(tuple_time)

users = {1: [2000, init_time],
         2: [3000, init_time],
         3: [4000, init_time],
        }

transactions = {}
reports = {}


class Transactions:
    """Класс для работы с транзакциями."""

    @dataclass
    class Transaction:
        """Класс транзакции."""

        _current_amount: Union[float, int] = 0
        _transaction_time: time = init_time

        @property
        def amount(self) -> Union[float, int]:
            """Получение текущей суммы транзакции."""
            return self._current_amount

        @property
        def time(self) -> time:
            """Получение даты совершения транзакции."""
            return self._transaction_time

    def create_transaction(self, user_id: int, amount: Union[float, int], trans_type: str) -> NoReturn:
        """Создание транзакции."""
        if user_id in users:
            current_balance = users.get(user_id)[0]
            if amount < 0:
                raise ValueError('Error, incorrect amount')
            else:
                if trans_type == '+':
                    current_balance += amount
                elif trans_type == '-' and current_balance >= amount:
                    current_balance -= amount
                else:
                    raise ValueError('Error, incorrect operation')

            users.get(user_id)[0] = current_balance

            tr = Transactions.Transaction(current_balance, time.ctime(time.time()))
            transactions.setdefault(user_id, []).append(tr)
        else:
            raise ValueError('Error, this user does not exist')

    def get_transaction(self, user_id: int, start: time, end: time) -> dict:
        """Получение транзакции."""
        report = []
        if start > end:
            raise ValueError('Error, incorrect time interval')
        if user_id not in transactions:
            raise ValueError('Error, this user does not exist')
        
        list_of_trans = transactions.get(user_id)
        for transaction in list_of_trans:
            if transaction.time >= start or transaction.time <= end:
                report.append([transaction.amount, transaction.time])
                reports.setdefault(id, []).append(report)
        return report
