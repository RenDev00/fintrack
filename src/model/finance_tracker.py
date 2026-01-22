import json
import os
import uuid

from model.transaction import Transaction, TransactionCategory, TransactionType


class FinanceTracker:
    def __init__(self, finance_data_path: str):
        self.finance_data_path = finance_data_path
        self.transactions = self.load_transactions()

    def add_transaction(
        self,
        amount: float,
        transaction_type: TransactionType,
        transaction_category: TransactionCategory,
        transaction_details: str,
        transaction_date: str = None,
    ):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")

        new_transaction = Transaction(
            amount,
            transaction_type,
            transaction_category,
            transaction_details,
            transaction_date,
        )
        self.transactions.append(new_transaction)
        self.save_transactions()
        print("Transaction added!")

    def get_transaction_by_uuid(self, uuid: uuid.UUID):
        return next(t for t in self.transactions if t.uuid == uuid)

    def edit_transaction_by_uuid(
        self,
        uuid: uuid.UUID,
        amount: float,
        transaction_type: TransactionType,
        transaction_category: TransactionCategory,
        transaction_details: str,
        transaction_date: str,
    ):
        transaction = self.get_transaction_by_uuid(uuid)
        transaction.amount = amount
        transaction.transaction_type = transaction_type
        transaction.transaction_category = transaction_category
        transaction.transaction_details = transaction_details
        transaction.transaction_date = transaction_date
        self.save_transactions()

    def delete_transaction_by_uuid(self, uuid: uuid.UUID):
        self.transactions.remove(self.get_transaction_by_uuid(uuid))
        self.save_transactions()

    def load_transactions(self) -> list[Transaction]:
        if not os.path.exists(self.finance_data_path):
            return []

        with open(self.finance_data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [
                Transaction(
                    float(t["amount"]),
                    TransactionType[t["type"]],
                    TransactionCategory[t["category"]],
                    t["details"],
                    t["date"],
                    uuid.UUID(t["uuid"]),
                )
                for t in data
            ]

    def save_transactions(self):
        with open(self.finance_data_path, "w", encoding="utf-8") as f:
            json.dump(
                [transaction.as_dict() for transaction in self.transactions],
                f,
                indent=4,
            )

    def get_transactions_by_type(
        self, transaction_type: TransactionType
    ) -> list[Transaction]:
        return [t for t in self.transactions if t.transaction_type == transaction_type]

    def get_transactions_by_category(
        self, transaction_category: TransactionCategory
    ) -> list[Transaction]:
        return [
            t
            for t in self.transactions
            if t.transaction_category == transaction_category
        ]

    def get_total_income(self) -> float:
        return sum(
            [t.amount for t in self.get_transactions_by_type(TransactionType.INCOME)]
        )

    def get_total_expenses(self) -> float:
        return sum(
            [t.amount for t in self.get_transactions_by_type(TransactionType.EXPENSE)]
        )

    def get_balance(self) -> float:
        return self.get_total_income() - self.get_total_expenses()
