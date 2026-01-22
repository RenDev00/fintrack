import uuid
from controller.edit_transaction_dialog_controller import (
    EditTransactionDialogController,
)
from controller.new_transaction_dialog_controller import NewTransactionDialogController
from model.finance_tracker import FinanceTracker
from model.transaction import Transaction, TransactionCategory, TransactionType
from view.edit_transaction_dialog_view import EditTransactionDialogView
from view.finance_tracker_view import FinanceTrackerView

from PySide6.QtWidgets import QTableWidgetItem, QMessageBox
from PySide6.QtCore import Qt

from view.new_transaction_dialog_view import NewTransactionDialogView


class FinanceTrackerController:
    def __init__(self, view: FinanceTrackerView, model: FinanceTracker):
        self.view = view
        self.model = model
        self.populate_transaction_table()

        # Signals
        self.view.button_new.clicked.connect(self.handle_new)
        self.view.button_edit.clicked.connect(self.handle_edit)
        self.view.button_delete.clicked.connect(self.handle_delete)
        self.view.line_edit_search_term.textChanged.connect(self.handle_search)
        self.view.combo_box_type.currentTextChanged.connect(self.handle_search)
        self.view.combo_box_category.currentTextChanged.connect(self.handle_search)

    def populate_transaction_table(self, transactions: list[Transaction] = None):
        if transactions == None:
            transactions = self.model.transactions

        for _ in range(self.view.table_transactions.rowCount()):
            self.view.table_transactions.removeRow(0)

        for row, t in enumerate(transactions):
            self.view.table_transactions.insertRow(row)
            for col, data in enumerate(
                [
                    str(t.uuid),
                    t.transaction_date,
                    t.transaction_type.name,
                    t.transaction_category.name,
                    f"{round(t.amount, 2):.2f}",
                    t.transaction_details,
                ]
            ):
                item = QTableWidgetItem(data)
                if col not in [4, 5]:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                elif col == 4:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )
                self.view.table_transactions.setItem(row, col, item)

        self.update_status_bar()
        self.view.table_transactions.resizeColumnToContents(1)

    def handle_new(self):
        dialog_view = NewTransactionDialogView(self.view)
        dialog_controller = NewTransactionDialogController(dialog_view, self.model)
        if dialog_controller.execute():
            self.handle_search()

    def handle_edit(self):
        current_table_row_index = self.view.table_transactions.currentRow()
        uuid_item = self.view.table_transactions.item(current_table_row_index, 0)
        id = uuid.UUID(uuid_item.text())
        transaction = self.model.get_transaction_by_uuid(id)

        dialog_view = EditTransactionDialogView(self.view)
        dialog_controller = EditTransactionDialogController(
            dialog_view, self.model, transaction
        )

        if dialog_controller.execute():
            self.handle_search()

    def handle_delete(self):
        current_table_row_index = self.view.table_transactions.currentRow()
        uuid_item = self.view.table_transactions.item(current_table_row_index, 0)
        id = uuid.UUID(uuid_item.text())

        dialog = QMessageBox(self.view)
        dialog.setWindowTitle("Finance Tracker | Delete")
        dialog.setText(
            f"Delete the following transaction?\n\n{self.model.get_transaction_by_uuid(id)}"
        )
        dialog.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        dialog.setIcon(QMessageBox.Icon.Question)

        if dialog.exec() == QMessageBox.StandardButton.Yes:
            self.model.delete_transaction_by_uuid(id)
            self.handle_search()

    def handle_search(self):
        search_term = self.view.line_edit_search_term.text().lower()
        type_filter = self.view.combo_box_type.currentText().strip().upper()
        category_filter = self.view.combo_box_category.currentText().strip().upper()

        transactions = self.model.transactions

        if search_term:
            transactions = [
                t for t in transactions if search_term in t.transaction_details.lower()
            ]
        if type_filter != "ALL":
            transactions = [
                t
                for t in transactions
                if t.transaction_type == TransactionType[type_filter]
            ]
        if category_filter != "ALL":
            transactions = [
                t
                for t in transactions
                if t.transaction_category == TransactionCategory[category_filter]
            ]

        self.populate_transaction_table(transactions)

    def update_status_bar(self):
        self.view.status_bar.showMessage(
            f"Balance: {round(self.model.get_balance(), 2):.2f} | Total Income: {round(self.model.get_total_income(), 2):.2f} | Total Expenses: {round(self.model.get_total_expenses(), 2):.2f}"
        )
