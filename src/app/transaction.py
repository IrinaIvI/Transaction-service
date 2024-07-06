import time
from dataclasses import dataclass

tuple_time = (2019, 12, 7, 14, 30, 30, 5, 0, 0)
init_time = time.asctime(tuple_time)

users = {1: [2000, init_time],
         2: [3000, init_time],
         3: [4000, init_time],
        }

transactions = {}
reports = {}


@dataclass
class Transaction:
    """Класс транзакции."""

    current_amount: float
    transaction_time: time

    def get_amount(self) -> float:
        """Получение текущей суммы транзакции."""
        return self.current_amount

    def get_time(self) -> time:
        """Получение даты совершения транзакции."""
        return self.transaction_time


class Transactions:
    """Класс для работы с транзакциями."""

    def create_transaction(self, user_id: int, amount: float, trans_type: str) -> str:
        """Создание транзакции."""
        if user_id in users:
            current_balance = users.get(user_id)[0]
            if trans_type == '+':
                current_balance += amount
            elif trans_type == '-' and current_balance >= amount:
                current_balance -= amount
            else:
                return 'Error, incorrect operation'

            users.get(user_id)[0] = current_balance

            tr = Transaction(current_balance, time.ctime(time.time()))
            transactions.setdefault(user_id, []).append(tr)
        else:
            return 'Error, this user is not exist'

    def get_transaction(self, user_id: int, start: time, end: time) -> dict:
        """Получение транзакции."""
        report = []
        lst = transactions.get(user_id)
        for el in lst:
            if el.get_time() >= start or el.get_time() <= end:
                report.append([el.get_amount(), el.get_time()])
                reports.setdefault(id, []).append(report)
        return report
