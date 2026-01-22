from model.finance_tracker import FinanceTracker
from model.transaction import Transaction, TransactionCategory, TransactionType
from view.new_transaction_dialog_view import NewTransactionDialogView
from PySide6.QtWidgets import QDialog, QMessageBox


class NewTransactionDialogController:
    def __init__(self, view: NewTransactionDialogView, model: FinanceTracker):
        self.view = view
        self.model = model

        # Signals
        self.view.button_ok.clicked.connect(self.view.accept)
        self.view.button_cancel.clicked.connect(self.view.reject)

    def execute(self) -> bool:
        if self.view.exec_() == QDialog.Rejected:
            return False

        amount = self.view.spin_box_amount.value()
        t_type = TransactionType[self.view.combo_box_type.currentText().upper()]
        t_category = TransactionCategory[
            self.view.combo_box_category.currentText().upper()
        ]
        t_date = self.view.date_time_edit.dateTime().toString("yyyy-MM-dd HH:mm")
        t_details = self.view.line_edit_details.text().strip()
        self.model.add_transaction(amount, t_type, t_category, t_details, t_date)
        return True
