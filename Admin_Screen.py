import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame, QPushButton, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QSizePolicy, QHeaderView, QLineEdit, QDialog, QTableWidget, QTableWidgetItem, QStyle, QStyleOptionButton, QStylePainter, QHBoxLayout, QToolButton
)
from PyQt5.QtGui import QFont, QColor, QIcon
from PyQt5.QtCore import Qt


class EditDialog(QDialog):
    def __init__(self, row_data, row_index, table):
        super().__init__()
        self.row_data = row_data
        self.row_index = row_index
        self.table = table

        self.setWindowTitle("Edit Row")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.name_input = QLineEdit(self.row_data[0])
        self.status_input = QLineEdit(self.row_data[1])

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_changes)

        layout.addWidget(QLabel("Name"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Status"))
        layout.addWidget(self.status_input)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.setStyleSheet("""
            background-color: white;
            border-radius: 8px;
        """)

        self.name_input.setStyleSheet("""
            padding: 6px;
            border: 1px solid #ddd;
            border-radius: 5px;
        """)
        self.status_input.setStyleSheet("""
            padding: 6px;
            border: 1px solid #ddd;
            border-radius: 5px;
        """)
        self.save_button.setStyleSheet("""
            background-color: blue;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        """)

    def save_changes(self):
        self.table.setItem(self.row_index, 0, QTableWidgetItem(self.name_input.text()))
        self.table.setItem(self.row_index, 1, QTableWidgetItem(self.status_input.text()))
        self.accept()


def create_action_buttons(table, row_index):
    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    layout.setAlignment(Qt.AlignCenter)

    edit_button = QToolButton()
    edit_button.setText("📝")
    edit_button.clicked.connect(lambda: show_edit_dialog(table, row_index))
    edit_button.setStyleSheet("font-size: 16px;")

    delete_button = QToolButton()
    delete_button.setText("🗑️")
    delete_button.clicked.connect(lambda: table.removeRow(row_index))
    delete_button.setStyleSheet("font-size: 16px;")

    layout.addWidget(edit_button)
    layout.addWidget(delete_button)

    return container


def show_edit_dialog(table, row_index):
    row_data = (
        table.item(row_index, 0).text(),
        table.item(row_index, 1).text()
    )
    dialog = EditDialog(row_data, row_index, table)
    dialog.exec_()


def create_quality_control_table(table_type, add_button_container):
    table = QTableWidget()
    table.setColumnCount(3)
    table.setRowCount(5)
    table.setHorizontalHeaderLabels(["Name", "Status", "Action"])
    table.verticalHeader().setVisible(False)
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table.setSelectionMode(QAbstractItemView.NoSelection)
    table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    table.horizontalHeader().setStretchLastSection(True)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    table.setStyleSheet("""
    QTableWidget {
        background-color: #FAFAFA;
        font-size: 14px;
        border: none;
    }
    QHeaderView::section {
        background-color: #3F51B5;
        color: white;
        font-size: 14px;
        font-weight: bold;
        border: none;
    }
    QTableWidget::item {
        border: none;
    }
    QTableWidget::item:hover {
        background-color: #E3F2FD;
    }
    """)

    if table_type == "Operators":
        data = [("John", "Active"), ("Amit", "Inactive"), ("Priya", "Active"), ("Lee", "Active"), ("Sara", "Inactive")]
    elif table_type == "Models":
        data = [("Model A", "Enabled"), ("Model B", "Disabled"), ("Model C", "Enabled"), ("Model D", "Disabled"), ("Model E", "Enabled")]
    else:
        data = [("Embossed Channel", "Pass"), ("Crimp Seal", "Pass"), ("PFA", "Fail"), ("SFA", "Fail"), ("Visual Signal", "Pass")]

    for i, (col1, col2) in enumerate(data):
        for j, text in enumerate([col1, col2]):
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignCenter)
            if table_type == "Inspection Stages" and j == 1:
                item.setBackground(QColor("#C8E6C9") if text.lower() == "pass" else QColor("#FFCDD2"))
                item.setForeground(QColor("#2E7D32") if text.lower() == "pass" else QColor("#C62828"))
            table.setItem(i, j, item)

        action_widget = create_action_buttons(table, i)
        table.setCellWidget(i, 2, action_widget)

    for i in reversed(range(add_button_container.count())):
        add_button_container.itemAt(i).widget().deleteLater()

    add_button = QPushButton("✚ Add")
    add_button.setFixedSize(80, 30)
    add_button.setStyleSheet("""
        QPushButton {
            background-color: blue;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 6px;
        }
        QPushButton:hover {
            background-color: #43A047;
        }
    """)
    add_button.clicked.connect(lambda: add_new_row(table))
    add_button_container.addWidget(add_button, alignment=Qt.AlignRight)

    return table


def add_new_row(table):
    row_position = table.rowCount()
    table.insertRow(row_position)

    for col in range(3):
        if col == 2:
            action_widget = create_action_buttons(table, row_position)
            table.setCellWidget(row_position, col, action_widget)
        else:
            item = QTableWidgetItem("")
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row_position, col, item)


class AIQualityControlUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Quality Control Box")
        self.resize(1000, 650)
        self.setStyleSheet("background-color: #F0F3F7;")
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        top_bar = QFrame()
        top_bar.setFixedHeight(50)
        top_bar.setStyleSheet("background-color: #1F3B61;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(10, 0, 10, 0)

        logo = QLabel()
        logo.setFixedSize(25, 25)
        logo.setStyleSheet("background-color: #4A90E2; border-radius: 4px;")

        title = QLabel("AI Quality Control Box")
        title.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
        title.setFont(QFont("Arial", 12))

        status = QLabel("System Ready")
        status.setStyleSheet("color: white; font-size: 12px;")
        status_dot = QLabel()
        status_dot.setFixedSize(12, 12)
        status_dot.setStyleSheet("background-color: #00C853; border-radius: 6px;")

        top_layout.addWidget(logo)
        top_layout.addSpacing(10)
        top_layout.addWidget(title)
        top_layout.addStretch()
        top_layout.addWidget(status)
        top_layout.addSpacing(5)
        top_layout.addWidget(status_dot)

        admin_title = QLabel("Admin Screen")
        admin_title.setFont(QFont("Arial", 14, QFont.Bold))
        admin_title.setAlignment(Qt.AlignCenter)
        admin_title.setStyleSheet("color: #1F3B61; margin-top: 10px;")

        square_panel = QFrame()
        square_panel.setFixedSize(1300, 550)
        square_panel.setStyleSheet("background-color: white; border-radius: 12px; border: 1px solid #CCCCCC;")
        self.square_layout = QVBoxLayout(square_panel)
        self.square_layout.setContentsMargins(30, 30, 30, 30)
        self.square_layout.setSpacing(25)

        buttons_layout = QHBoxLayout()
        button_names = ["Operators", "Models", "Inspection Stages"]
        for name in button_names:
            button = QPushButton(name)
            button.setFixedSize(140, 40)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #42A5F5;
                    color: white;
                    font-weight: bold;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #1E88E5;
                }
            """)
            button.clicked.connect(lambda _, t=name: self.load_table(t))
            buttons_layout.addWidget(button, alignment=Qt.AlignCenter)

        self.add_button_container = QHBoxLayout()
        self.table_container = QVBoxLayout()

        self.square_layout.addLayout(buttons_layout)
        self.square_layout.addLayout(self.add_button_container)
        self.square_layout.addLayout(self.table_container)
        self.square_layout.addStretch()

        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 20, 0, 20)

        middle_layout = QVBoxLayout()
        middle_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        middle_layout.addWidget(admin_title, alignment=Qt.AlignCenter)
        middle_layout.addSpacing(10)
        middle_layout.addWidget(square_panel, alignment=Qt.AlignCenter)

        center_layout.addStretch()
        center_layout.addLayout(middle_layout)
        center_layout.addStretch()

        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(30)
        bottom_bar.setStyleSheet("background-color: #1F3B61;")
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setContentsMargins(10, 0, 10, 0)
        bottom_layout.setAlignment(Qt.AlignCenter)

        version = QLabel("AI Quality Control System v1.0")
        version.setStyleSheet("color: white; font-size: 10px;")
        bottom_layout.addWidget(version)

        main_layout.addWidget(top_bar)
        main_layout.addWidget(center_widget, stretch=1)
        main_layout.addWidget(bottom_bar)

    def load_table(self, table_type):
        for i in reversed(range(self.table_container.count())):
            widget = self.table_container.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        table = create_quality_control_table(table_type, self.add_button_container)
        self.table_container.addWidget(table)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = AIQualityControlUI()
    ui.show()
    sys.exit(app.exec_())