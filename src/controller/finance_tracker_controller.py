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


class NumericTableWidgetItem(QTableWidgetItem):
    def __init__(self, value: float, text: str):
        super().__init__(text)
        self._numeric_value = value

    def __lt__(self, other):
        return self._numeric_value < other._numeric_value


class FinanceTrackerController:
    def __init__(self, view: FinanceTrackerView, model: FinanceTracker):
        self.view = view
        self.model = model
        self.populate_transaction_table()
        self.update_graph()

        # Signals
        self.view.button_new.clicked.connect(self.handle_new)
        self.view.button_edit.clicked.connect(self.handle_edit)
        self.view.button_delete.clicked.connect(self.handle_delete)
        self.view.line_edit_search_term.textChanged.connect(self.handle_search)
        self.view.combo_box_type.currentTextChanged.connect(self.handle_search)
        self.view.combo_box_category.currentTextChanged.connect(self.handle_search)
        self.view.combo_box_month.currentTextChanged.connect(self.handle_search)
        self.view.action_home.triggered.connect(self.show_home_tab)
        self.view.action_graph.triggered.connect(self.show_graph_tab)

        self.populate_month_dropdown()

    def show_home_tab(self):
        self.view.stacked_widget.setCurrentIndex(0)

    def show_graph_tab(self):
        self.view.stacked_widget.setCurrentIndex(1)

    def populate_month_dropdown(self):
        months = sorted(set(t.transaction_date[:7] for t in self.model.transactions))
        self.view.combo_box_month.clear()
        self.view.combo_box_month.addItem("All Months")
        for month in months:
            year, m = month.split("-")
            month_names = [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ]
            display_text = f"{month_names[int(m) - 1]} {year}"
            self.view.combo_box_month.addItem(display_text, month)

    def populate_transaction_table(self, transactions: list[Transaction] | None = None):
        if transactions == None:
            transactions = self.model.transactions

        transactions = sorted(
            transactions, key=lambda t: t.transaction_date, reverse=True
        )

        self.view.table_transactions.setSortingEnabled(False)

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
                    t.amount,
                    t.transaction_details,
                ]
            ):
                if col == 4:
                    item = NumericTableWidgetItem(t.amount, f"{round(t.amount, 2):.2f}")
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )
                else:
                    item = QTableWidgetItem(data)
                    if col not in [5]:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.view.table_transactions.setItem(row, col, item)

        self.view.table_transactions.resizeColumnToContents(1)
        self.view.table_transactions.setSortingEnabled(True)
        self.view.table_transactions.sortByColumn(1, Qt.SortOrder.DescendingOrder)
        self.view.table_transactions.horizontalHeader().setSortIndicator(
            1, Qt.SortOrder.DescendingOrder
        )

    def handle_new(self):
        dialog_view = NewTransactionDialogView(self.view)
        dialog_controller = NewTransactionDialogController(dialog_view, self.model)
        if dialog_controller.execute():
            self.populate_month_dropdown()
            self.handle_search()
            self.update_graph()

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
            self.populate_month_dropdown()
            self.handle_search()
            self.update_graph()

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
            self.populate_month_dropdown()
            self.handle_search()
            self.update_graph()

    def handle_search(self):
        search_term = self.view.line_edit_search_term.text().lower()
        type_filter = self.view.combo_box_type.currentText().strip().upper()
        category_filter = self.view.combo_box_category.currentText().strip().upper()
        month_filter = self.view.combo_box_month.currentData()

        transactions = self.model.transactions

        if search_term:
            transactions = [
                t for t in transactions if search_term in t.transaction_details.lower()
            ]
        if type_filter != "ALL TYPES":
            transactions = [
                t
                for t in transactions
                if t.transaction_type == TransactionType[type_filter]
            ]
        if category_filter != "ALL CATEGORIES":
            transactions = [
                t
                for t in transactions
                if t.transaction_category == TransactionCategory[category_filter]
            ]
        if month_filter:
            transactions = [
                t for t in transactions if t.transaction_date[:7] == month_filter
            ]

        self.populate_transaction_table(transactions)

    def update_graph(self) -> None:
        monthly_data: dict[str, dict[str, float]] = {}

        for t in self.model.transactions:
            month = t.transaction_date[:7]
            if month not in monthly_data:
                monthly_data[month] = {
                    "income": 0,
                    "needs": 0,
                    "wants": 0,
                    "savings": 0,
                }

            if t.transaction_type == TransactionType.INCOME:
                monthly_data[month]["income"] += t.amount
            elif t.transaction_type == TransactionType.EXPENSE:
                if t.transaction_category == TransactionCategory.NEED:
                    monthly_data[month]["needs"] += t.amount
                elif t.transaction_category == TransactionCategory.WANT:
                    monthly_data[month]["wants"] += t.amount
                elif t.transaction_category == TransactionCategory.SAVING:
                    monthly_data[month]["savings"] += t.amount

        sorted_months = sorted(monthly_data.keys())

        x_positions = list(range(len(sorted_months)))
        bar_width = self.view.bar_width

        income_heights = [monthly_data[m]["income"] for m in sorted_months]
        needs_heights = [monthly_data[m]["needs"] for m in sorted_months]
        wants_heights = [monthly_data[m]["wants"] for m in sorted_months]
        savings_heights = [monthly_data[m]["savings"] for m in sorted_months]

        self.view.income_bar.setOpts(
            x=[x - bar_width / 2 for x in x_positions],
            height=income_heights,
        )
        self.view.savings_bar.setOpts(
            x=[x + bar_width / 2 for x in x_positions],
            height=savings_heights,
        )
        self.view.needs_bar.setOpts(
            x=[x + bar_width / 2 for x in x_positions],
            height=needs_heights,
            y0=savings_heights,
        )
        self.view.wants_bar.setOpts(
            x=[x + bar_width / 2 for x in x_positions],
            height=wants_heights,
            y0=[s + n for s, n in zip(savings_heights, needs_heights)],
        )

        if sorted_months:
            self.view.graph.getPlotItem().getAxis("bottom").setTicks(
                [[(i, m) for i, m in enumerate(sorted_months)]]
            )
            self.view.graph.getPlotItem().showAxis("bottom")
            x_min = -0.5 - bar_width
            x_max = len(sorted_months) - 0.5 + bar_width
            self.view.graph.getPlotItem().setXRange(x_min, x_max, padding=0)
        else:
            self.view.graph.getPlotItem().hideAxis("bottom")
