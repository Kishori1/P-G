import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame, QPushButton
)
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap, QPainter, QPen, QColor

class ScanningAnimation(QWidget):
    def __init__(self):
        super().__init__()
        original = QPixmap("pads.png")
        self.image = original.scaled(500, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.line_y = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_line)
        self.timer.start(30)
        self.setFixedSize(self.image.size())

    def update_line(self):
        self.line_y += 3
        if self.line_y > self.height():
            self.line_y = 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.image)
        pen = QPen(QColor("#00FF00"), 4)
        painter.setPen(pen)
        painter.drawLine(0, self.line_y, self.width(), self.line_y)


class CapturingScreen(QWidget):
    next_screen_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(30)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        arrow_btn = QPushButton("→")
        arrow_btn.setFixedSize(60, 60)
        arrow_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 26px;
                border: none;
                border-radius: 30px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        arrow_btn.clicked.connect(self.next_screen_requested.emit)
        button_layout.addWidget(arrow_btn)

        layout.addLayout(button_layout)

        header = QLabel("Capturing Images")
        header.setFont(QFont("Arial", 24, QFont.Bold))
        header.setStyleSheet("color: #2c3e50;")
        header.setAlignment(Qt.AlignCenter)

        scanning_widget = ScanningAnimation()

        layout.addWidget(header)
        layout.addStretch()
        layout.addWidget(scanning_widget, alignment=Qt.AlignCenter)
        layout.addStretch()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Outer window container
    window = QWidget()
    window.setWindowTitle("AI Quality Control Box")
    window.resize(1900, 1000)
    window.setStyleSheet("background-color: #f0f2f5;")

    main_layout = QVBoxLayout(window)
    main_layout.setSpacing(0)
    main_layout.setContentsMargins(0, 0, 0, 0)

    # Top bar
    top_bar = QFrame()
    top_bar.setFixedHeight(70)
    top_bar.setStyleSheet("background-color: #2c3e50;")
    top_layout = QHBoxLayout(top_bar)
    top_layout.setContentsMargins(20, 0, 20, 0)

    logo = QLabel()
    logo.setFixedSize(40, 40)
    logo.setStyleSheet("background-color: #3498db; border-radius: 5px;")

    title = QLabel("AI Quality Control Box")
    title.setStyleSheet("color: white; font-weight: bold; font-size: 22px; font-family: Arial;")

    top_layout.addWidget(logo)
    top_layout.addSpacing(15)
    top_layout.addWidget(title)
    top_layout.addStretch()

    status_label = QLabel("System Ready")
    status_label.setStyleSheet("color: white; font-size: 14px;")
    status_dot = QLabel()
    status_dot.setFixedSize(14, 14)
    status_dot.setStyleSheet("background-color: #27ae60; border-radius: 7px;")

    top_layout.addWidget(status_label)
    top_layout.addSpacing(5)
    top_layout.addWidget(status_dot)

    # Create capturing screen inside white card
    white_card = QFrame()
    white_card.setFixedSize(700, 500)
    white_card.setStyleSheet("""
        background-color: white;
        border-radius: 16px;
    """)

    card_layout = QVBoxLayout(white_card)
    card_layout.setContentsMargins(50, 50, 50, 50)

    center_card = CapturingScreen()
    center_card.setStyleSheet("background-color: transparent;")  # inherit white background
    card_layout.addWidget(center_card)

    # Wrap white card inside center container
    middle_container = QWidget()
    middle_layout = QVBoxLayout(middle_container)
    middle_layout.setContentsMargins(0, 40, 0, 40)

    center_wrapper = QHBoxLayout()
    center_wrapper.addStretch()
    center_wrapper.addWidget(white_card)
    center_wrapper.addStretch()

    middle_layout.addLayout(center_wrapper)

    # Footer
    bottom_bar = QFrame()
    bottom_bar.setFixedHeight(30)
    bottom_bar.setStyleSheet("background-color: #2c3e50;")
    bottom_layout = QHBoxLayout(bottom_bar)
    bottom_layout.setContentsMargins(0, 0, 0, 0)
    bottom_layout.setAlignment(Qt.AlignCenter)

    version_label = QLabel("AI Quality Control System v1.0")
    version_label.setStyleSheet("color: #aaa; font-size: 12px; font-family: Arial;")
    bottom_layout.addWidget(version_label)

    # Combine all
    main_layout.addWidget(top_bar)
    main_layout.addWidget(middle_container)
    main_layout.addWidget(bottom_bar)

    window.show()
    sys.exit(app.exec_())
