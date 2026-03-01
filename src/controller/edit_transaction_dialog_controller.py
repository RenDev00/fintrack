from model.finance_tracker import FinanceTracker
from model.transaction import Transaction, TransactionCategory, TransactionType
from view.edit_transaction_dialog_view import EditTransactionDialogView

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QDateTime


class EditTransactionDialogController:
    def __init__(
        self,
        view: EditTransactionDialogView,
        model: FinanceTracker,
        transaction: Transaction,
    ):
        self.view = view
        self.model = model
        self.transaction = transaction

        # Setup
        self.view.spin_box_amount.setValue(self.transaction.amount)
        self.view.date_time_edit.setDateTime(
            QDateTime.fromString(self.transaction.transaction_date, "yyyy-MM-dd HH:mm")
        )
        self.view.combo_box_type.setCurrentText(
            self.transaction.transaction_type.name.capitalize()
        )
        self.update_category_combo_box(self.view.combo_box_type.currentText())
        self.view.combo_box_category.setCurrentText(
            self.transaction.transaction_category.name.capitalize()
        )
        self.view.line_edit_details.setText(
            self.transaction.transaction_details.strip()
        )

        # Signals
        self.view.button_ok.clicked.connect(self.view.accept)
        self.view.button_cancel.clicked.connect(self.view.reject)

    def update_category_combo_box(self, typeText: str) -> None:
        self.view.combo_box_category.clear()
        if typeText == TransactionType.EXPENSE:
            self.view.combo_box_category.addItems(["Need", "Want", "Saving"])
        elif typeText == TransactionType.INCOME:
            self.view.combo_box_category.addItems(
                ["Salary", "Scholarship", "Pocket Money", "Other"]
            )

    def execute(self) -> bool:
        if self.view.exec_() == QDialog.Rejected:
            return False

        amount = self.view.spin_box_amount.value()
        t_type = TransactionType[self.view.combo_box_type.currentText().upper()]
        t_category = TransactionCategory[
            self.view.combo_box_category.currentText().upper().replace(" ", "_")
        ]
        t_details = self.view.line_edit_details.text().strip()
        t_date = self.view.date_time_edit.dateTime().toString("yyyy-MM-dd HH:mm")
        self.model.edit_transaction_by_uuid(
            self.transaction.uuid, amount, t_type, t_category, t_details, t_date
        )
        return True
