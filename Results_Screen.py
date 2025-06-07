from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QGridLayout, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCursor(Qt.PointingHandCursor)  # Show hand icon

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)


class ResultScreen(QWidget):
    detail_requested = pyqtSignal(str)

    def __init__(self, back_callback, repeat_callback, back1_callback):
        super().__init__()

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 40, 0, 40)

        # White card container
        white_card = QFrame()
        white_card.setFixedSize(1000, 550)
        white_card.setStyleSheet("""
            background-color: white;
            border-radius: 16px;
        """)

        card_layout = QVBoxLayout(white_card)
        card_layout.setContentsMargins(50, 50, 50, 50)
        card_layout.setSpacing(30)

        # Title
        title = QLabel("Results")
        title.setFont(QFont("Arial", 26, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        # Grid Table for results
        grid = QGridLayout()
        grid.setHorizontalSpacing(40)
        grid.setVerticalSpacing(20)

        headers = ["Category", "Threshold", "Status"]
        for i, text in enumerate(headers):
            label = QLabel(text)
            label.setFont(QFont("Arial", 16, QFont.Bold))
            label.setStyleSheet("""
                background-color: #2c3e50;
                color: white;
                border-radius: 8px;
                padding: 8px 20px;
            """)
            label.setAlignment(Qt.AlignCenter)
            grid.addWidget(label, 0, i)

        rows = [
            ("Embossed Channel", "Under threshold", "PASS"),
            ("Crimp Seal", "Under threshold", "PASS"),
            ("Visual Signal", "Under threshold(Color match)", "PASS"),
        ]

        for r, (cat, thres, stat) in enumerate(rows, start=1):
            cat_lbl = ClickableLabel(cat)
            cat_lbl.setFont(QFont("Arial", 14))
            cat_lbl.setStyleSheet("""
                QLabel {
                    color: #2c3e50;
                    font-weight: bold;
                    padding: 4px 6px;
                    border-bottom: 2px solid transparent;
                }
                QLabel:hover {
                    color: #2c3e50;
                    border-bottom: 2px solid #1a5276;
                    background-color: #f4f6f7;
                }
            """)

            cat_lbl.setAlignment(Qt.AlignCenter)
            cat_lbl.clicked.connect(lambda c=cat: self.detail_requested.emit(c))

            thres_lbl = QLabel(thres)
            thres_lbl.setFont(QFont("Arial", 14))
            thres_lbl.setStyleSheet("color: #2c3e50;")
            thres_lbl.setAlignment(Qt.AlignCenter)

            stat_lbl = QLabel(stat)
            stat_lbl.setFont(QFont("Arial", 14, QFont.Bold))
            stat_lbl.setAlignment(Qt.AlignCenter)
            stat_lbl.setStyleSheet("""
                background-color: #27ae60;
                color: white;
                border-radius: 8px;
                padding: 6px 20px;
            """)

            grid.addWidget(cat_lbl, r, 0)
            grid.addWidget(thres_lbl, r, 1)
            grid.addWidget(stat_lbl, r, 2)

        card_layout.addLayout(grid)

        # Overall status
        overall_status = QLabel("OVERALL STATUS: PASS")
        overall_status.setFont(QFont("Arial", 16, QFont.Bold))
        overall_status.setAlignment(Qt.AlignCenter)
        overall_status.setStyleSheet("""
            background-color: #27ae60;
            color: white;
            border-radius: 8px;
            padding: 12px 30px;
        """)
        card_layout.addWidget(overall_status, alignment=Qt.AlignCenter)

        # Footer buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(30)

        continue_btn = QPushButton("Continue")
        repeat_btn = QPushButton("Repeat")
        back_btn = QPushButton("Back")

        for btn in [continue_btn, repeat_btn, back_btn]:
            btn.setFixedSize(160, 50)
            btn.setFont(QFont("Arial", 14, QFont.Bold))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #b0bec5;
                    color: white;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #90a4ae;
                }
            """)

        continue_btn.clicked.connect(back_callback)
        repeat_btn.clicked.connect(repeat_callback)
        back_btn.clicked.connect(back1_callback)

        btn_row.addWidget(continue_btn)
        btn_row.addWidget(repeat_btn)
        btn_row.addWidget(back_btn)
        card_layout.addLayout(btn_row)

        # Center the card in layout
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(white_card)
        center_layout.addStretch()

        outer_layout.addLayout(center_layout)
