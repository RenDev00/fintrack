from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QComboBox,
    QTableWidget,
    QAbstractItemView,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
)


class FinanceTrackerView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finance Tracker")
        self.setMinimumSize(560, 440)
        self.init_ui()

    def init_ui(self):
        # Widgets
        central_widget = QWidget()

        self.status_bar = self.statusBar()

        group_box_control = QGroupBox("Transaction Control")
        self.button_new = QPushButton("New")
        self.button_edit = QPushButton("Edit")
        self.button_delete = QPushButton("Delete")

        group_box_search = QGroupBox("Search")
        self.line_edit_search_term = QLineEdit(placeholderText="Enter a search term")
        self.combo_box_type = QComboBox()
        self.combo_box_type.addItems(["All", "Expense", "Income"])
        self.combo_box_category = QComboBox()
        self.combo_box_category.addItems(["All", "Need", "Want", "Other"])

        group_box_transactions = QGroupBox("Transactions")
        self.table_transactions = QTableWidget(0, 6)
        self.table_transactions.setHorizontalHeaderLabels(
            ["UUID", "Date", "Type", "Category", "Amount", "Details"]
        )
        self.table_transactions.hideColumn(0)
        self.table_transactions.horizontalHeader().setStretchLastSection(True)
        self.table_transactions.verticalHeader().setVisible(False)
        self.table_transactions.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        # Layout
        h_layout_control = QHBoxLayout()
        h_layout_control.addWidget(self.button_new)
        h_layout_control.addWidget(self.button_edit)
        h_layout_control.addWidget(self.button_delete)
        group_box_control.setLayout(h_layout_control)

        h_layout_search = QHBoxLayout()
        h_layout_search.addWidget(self.line_edit_search_term)
        h_layout_search.addWidget(self.combo_box_type)
        h_layout_search.addWidget(self.combo_box_category)
        group_box_search.setLayout(h_layout_search)

        h_layout_control_search = QHBoxLayout()
        h_layout_control_search.addWidget(group_box_control)
        h_layout_control_search.addWidget(group_box_search)

        v_layout_transactions = QVBoxLayout()
        v_layout_transactions.addWidget(self.table_transactions)
        group_box_transactions.setLayout(v_layout_transactions)

        v_layout_main = QVBoxLayout()
        v_layout_main.addLayout(h_layout_control_search)
        v_layout_main.addWidget(group_box_transactions)

        central_widget.setLayout(v_layout_main)
        self.setCentralWidget(central_widget)
