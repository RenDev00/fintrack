from datetime import datetime
from enum import StrEnum
import uuid


class TransactionType(StrEnum):
    INCOME = "Income"
    EXPENSE = "Expense"


class TransactionCategory(StrEnum):
    NEED = "Need"
    WANT = "Want"
    SAVING = "Saving"
    OTHER = "Other"


class Transaction:
    def __init__(
        self,
        amount: float,
        transaction_type: TransactionType,
        transaction_category: TransactionCategory,
        transaction_details: str,
        transaction_date: str = None,
        id: uuid.UUID = None,
    ):
        self.uuid = id if id else uuid.uuid4()
        self.amount = amount
        self.transaction_type = transaction_type
        self.transaction_category = transaction_category
        self.transaction_details = transaction_details
        self.transaction_date = (
            transaction_date
            if transaction_date
            else datetime.now().strftime("%Y-%m-%d %H:%M")
        )

    def __str__(self):
        return f"{self.transaction_date} | {self.transaction_type.name.capitalize().ljust(7)} | {self.amount:>8.2f} | {self.transaction_category}"

    def as_dict(self) -> dict:
        return {
            "uuid": str(self.uuid),
            "amount": self.amount,
            "type": self.transaction_type.name,
            "category": self.transaction_category.name,
            "details": self.transaction_details,
            "date": self.transaction_date,
        }
