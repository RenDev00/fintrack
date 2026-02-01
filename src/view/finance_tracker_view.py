from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QComboBox,
    QTableWidget,
    QAbstractItemView,
    QLineEdit,
    QToolBar,
    QStackedWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
import pyqtgraph as pg

from utility import svg_icon_loader


class FinanceTrackerView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finance Tracker")
        self.setMinimumSize(560, 440)
        self.init_ui()

    def init_ui(self) -> None:
        # Actions
        self.action_home = QAction(
            svg_icon_loader.get_icon("./data/svg/home_24dp.svg", "#8ab4f7"),
            "Home",
        )
        self.action_graph = QAction(
            svg_icon_loader.get_icon("./data/svg/graph_24dp.svg", "#8ab4f7"),
            "Graph",
        )

        self.actions_side_bar = (
            self.action_home,
            self.action_graph,
        )

        # Widgets
        self.stacked_widget = QStackedWidget()

        self.home_widget = self.build_home_ui()
        self.graph_widget = self.build_graph_ui()

        side_bar = QToolBar()
        side_bar.setObjectName("side_bar")
        side_bar.addActions(self.actions_side_bar)

        # Layout
        self.stacked_widget.addWidget(self.home_widget)
        self.stacked_widget.addWidget(self.graph_widget)
        self.setCentralWidget(self.stacked_widget)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, side_bar)

    def build_home_ui(self) -> QWidget:
        # Widgets
        central_widget = QWidget()

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
        return central_widget

    def build_graph_ui(self) -> QWidget:
        central_widget = QWidget()
        self.graph = pg.PlotWidget()
        self.graph.setBackground(None)
        self.graph.getPlotItem().setContentsMargins(10, 10, 10, 10)
        self.graph.getPlotItem().setLabel("left", "Money")
        self.graph.getPlotItem().showGrid(False, True)
        self.graph.getPlotItem().addLegend()
        for axis in ["left", "right", "top", "bottom"]:
            ax = self.graph.getPlotItem().getAxis(axis)
            ax.setZValue(-1)

        self.bar_width = 0.2

        self.income_bar = pg.BarGraphItem(
            x=[],
            height=[],
            width=self.bar_width,
            brush="#2ecc71",
            pen=pg.mkPen("#27ae60", width=1.2),
            name="Income",
        )
        self.graph.addItem(self.income_bar)

        self.savings_bar = pg.BarGraphItem(
            x=[],
            height=[],
            width=self.bar_width,
            brush="#3498db",
            pen=pg.mkPen("#2980b9", width=1),
            name="Savings",
        )
        self.graph.addItem(self.savings_bar)

        self.needs_bar = pg.BarGraphItem(
            x=[],
            height=[],
            width=self.bar_width,
            brush="#f39c12",
            pen=pg.mkPen("#d35400", width=1),
            name="Needs",
        )
        self.graph.addItem(self.needs_bar)

        self.wants_bar = pg.BarGraphItem(
            x=[],
            height=[],
            width=self.bar_width,
            brush="#e74c3c",
            pen=pg.mkPen("#c0392b", width=1),
            name="Wants",
        )
        self.graph.addItem(self.wants_bar)

        v_layout_main = QVBoxLayout()
        v_layout_main.addWidget(self.graph)

        central_widget.setLayout(v_layout_main)
        return central_widget
