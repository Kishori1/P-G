from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class WelcomeScreen(QWidget):
    def __init__(self, start_callback):
        super().__init__()

        # Outer wrapper layout for screen
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 40, 0, 40)

        # White card container
        white_card = QFrame()
        white_card.setFixedSize(1200, 700)
        white_card.setStyleSheet("""
            background-color: white;
            border-radius: 16px;
        """)

        # Content inside white card
        card_layout = QVBoxLayout(white_card)
        card_layout.setContentsMargins(100, 100, 100, 100)
        card_layout.setSpacing(40)
        card_layout.setAlignment(Qt.AlignCenter)

        prompt = QLabel("Flip the Pad and click on Start Button")
        prompt.setFont(QFont("Arial", 20, QFont.Bold))
        prompt.setStyleSheet("color: #2c3e50;")
        prompt.setAlignment(Qt.AlignCenter)

        start_button = QPushButton("START")
        start_button.setFixedSize(220, 65)
        start_button.setFont(QFont("Arial", 18, QFont.Bold))
        start_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border-radius: 32px;
            }
            QPushButton:hover {
                background-color: #219150;
            }
        """)
        start_button.clicked.connect(start_callback)

        card_layout.addWidget(prompt)
        card_layout.addWidget(start_button, alignment=Qt.AlignCenter)

        # Center the card itself on the page
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(white_card)
        center_layout.addStretch()

        outer_layout.addLayout(center_layout)
