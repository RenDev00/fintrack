from PySide6.QtWidgets import (
    QDialog,
    QPushButton,
    QComboBox,
    QDoubleSpinBox,
    QLineEdit,
    QDateTimeEdit,
    QFormLayout,
    QVBoxLayout,
    QHBoxLayout,
)

from PySide6.QtCore import QDateTime


class NewTransactionDialogView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Finance Tracker | New Transaction")
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        # Widgets
        self.date_time_edit = QDateTimeEdit()
        self.date_time_edit.setDateTime(QDateTime.currentDateTime())
        self.spin_box_amount = QDoubleSpinBox(
            decimals=2, minimum=0.01, singleStep=1.0, maximum=10000000
        )
        self.combo_box_type = QComboBox()
        self.combo_box_type.addItems(["Expense", "Income"])
        self.combo_box_category = QComboBox()
        self.combo_box_category.addItems(["Need", "Want", "Saving", "Other"])
        self.line_edit_details = QLineEdit()

        self.button_ok = QPushButton("Ok")
        self.button_cancel = QPushButton("Cancel")

        # Layout
        f_layout_transaction = QFormLayout()
        f_layout_transaction.addRow("Amount", self.spin_box_amount)
        f_layout_transaction.addRow("Date", self.date_time_edit)
        f_layout_transaction.addRow("Type", self.combo_box_type)
        f_layout_transaction.addRow("Category", self.combo_box_category)
        f_layout_transaction.addRow("Details", self.line_edit_details)

        h_layout_buttons = QHBoxLayout()
        h_layout_buttons.addWidget(self.button_ok)
        h_layout_buttons.addWidget(self.button_cancel)

        v_layout_main = QVBoxLayout()
        v_layout_main.addLayout(f_layout_transaction)
        v_layout_main.addLayout(h_layout_buttons)

        self.setLayout(v_layout_main)
