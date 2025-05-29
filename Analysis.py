import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame, QSizePolicy, QTableWidget, QTableWidgetItem, QAbstractItemView,
    QHeaderView, QPushButton
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

from DetailView import DetailView  

class AIQualityControlUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Quality Control Box")
        self.resize(1280, 750)
        self.setStyleSheet("background-color: #EEF2F7; font-family: 'Segoe UI';")
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Top bar
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

        # Center Area
        center_wrapper = QFrame()
        center_wrapper_layout = QVBoxLayout(center_wrapper)
        center_wrapper_layout.setContentsMargins(30, 30, 30, 30)

        white_panel = QFrame()
        white_panel.setStyleSheet("""
            background-color: white;
            border-radius: 15px;
            border: 1px solid #d0d0d0;
        """)
        white_panel_layout = QHBoxLayout(white_panel)
        white_panel_layout.setContentsMargins(30, 30, 30, 30)
        white_panel_layout.setSpacing(30)

        # Left Panel
        left_panel = QVBoxLayout()
        info_box = QLabel("Operator: John Doe\nModel: X100-Scan\nLast Update: 2025-05-01")
        info_box.setAlignment(Qt.AlignCenter)
        info_box.setStyleSheet("""
            background-color: #E8F5FE;
            border-radius: 10px;
            padding: 20px;
            font-size: 14px;
            font-weight: 500;
            color: #1A237E;
        """)
        left_panel.addWidget(info_box)

        start_btn = QPushButton("▶ Start")
        start_btn.setFixedSize(140, 45)
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: #1E88E5;
                color: white;
                border-radius: 8px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
        """)

        save_btn = QPushButton("🖫 Save / End")
        save_btn.setFixedSize(140, 45)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #E53935;
                color: white;
                border-radius: 8px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #C62828;
            }
        """)

        button_row = QHBoxLayout()
        button_row.setSpacing(20)
        button_row.setAlignment(Qt.AlignCenter)
        button_row.addWidget(start_btn)
        button_row.addWidget(save_btn)

        left_panel.addSpacing(20)
        left_panel.addLayout(button_row)

        left_frame = QFrame()
        left_frame.setFixedWidth(420)
        left_frame.setLayout(left_panel)

        # Right Panel
        right_frame = QFrame()
        right_panel_layout = QVBoxLayout(right_frame)
        right_panel_layout.setContentsMargins(10, 10, 10, 10)

        table = QTableWidget()
        table.setColumnCount(3)
        table.setRowCount(5)
        table.setHorizontalHeaderLabels(["Category", "Status", "Action"])
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
                padding: 10px;
                border: none;
            }
            QTableWidget::item {
                padding: 12px;
                border: none;
            }
            QTableWidget::item:hover {
                background-color: #E3F2FD;
            }
        """)

        data = [
            ("Embossed Channel", "Pass"),
            ("Crimp Seal", "Pass"),
            ("PFA", "Fail"),
            ("SFA", "Fail"),
            ("Visual Signal", "Pass")
        ]

        for i, (category, status) in enumerate(data):
            item1 = QTableWidgetItem(category)
            item1.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 0, item1)

            item2 = QTableWidgetItem(status)
            item2.setTextAlignment(Qt.AlignCenter)
            if status.lower() == "pass":
                item2.setBackground(QColor("#C8E6C9"))
                item2.setForeground(QColor("#2E7D32"))
            else:
                item2.setBackground(QColor("#FFCDD2"))
                item2.setForeground(QColor("#C62828"))
            table.setItem(i, 1, item2)

            view_btn = QPushButton("View")
            view_btn.setStyleSheet("""
                QPushButton {
                    background-color: #BBDEFB;
                    color: #0D47A1;
                    border-radius: 6px;
                    font-weight: bold;
                    padding: 6px 10px;
                }
                QPushButton:hover {
                    background-color: #90CAF9;
                }
            """)
            view_btn.clicked.connect(self.make_view_callback(category))
            table.setCellWidget(i, 2, view_btn)
            table.setRowHeight(i, 50)

        overall = QLabel("Overall Status: FAIL")
        overall.setAlignment(Qt.AlignCenter)
        overall.setFixedHeight(45)
        overall.setStyleSheet("""
            background-color: #D32F2F;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
        """)

        right_panel_layout.addWidget(table)
        right_panel_layout.addSpacing(12)
        right_panel_layout.addWidget(overall)

        white_panel_layout.addWidget(left_frame)
        white_panel_layout.addWidget(right_frame)
        center_wrapper_layout.addWidget(white_panel)

        # Bottom bar
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(30)
        bottom_bar.setStyleSheet("background-color: #1F3B61;")
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setContentsMargins(10, 0, 10, 0)
        bottom_layout.setAlignment(Qt.AlignCenter)

        version = QLabel("AI Quality Control System v1.0")
        version.setStyleSheet("color: white; font-size: 10px;")
        bottom_layout.addWidget(version)

        # Add everything to main layout
        main_layout.addWidget(top_bar)
        main_layout.addWidget(center_wrapper)
        main_layout.addWidget(bottom_bar)

    def make_view_callback(self, category_name):
        return lambda: self.open_detail_view(category_name)

    def open_detail_view(self, category_name):
        self.detail_window = DetailView(category_name)
        self.detail_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AIQualityControlUI()
    window.show()
    sys.exit(app.exec_())