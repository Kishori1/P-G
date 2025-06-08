import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QFrame, QPushButton, QStackedWidget, QSizePolicy
)
from PyQt5.QtGui import QFont, QPainter, QPen, QColor, QPixmap
from PyQt5.QtCore import Qt, QRect

from Capturing_Images import CapturingScreen
from Results_Screen import ResultScreen
from welcome_screen import WelcomeScreen
from Processing import ProcessingScreen
from Detailed_View import DetailView
from PyQt5.QtCore import pyqtSignal

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()

class DashedBox(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor('#3498db'), 2, Qt.DashLine)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawRoundedRect(QRect(0, 0, self.width() - 1, self.height() - 1), 5, 5)

        radius = 10
        positions = [
            (20, 20),
            (self.width() - 40, 20),
            (20, self.height() - 40),
            (self.width() - 40, self.height() - 40)
        ]

        for x, y in positions:
            painter.setBrush(QColor('#3498db'))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(x, y, radius * 2, radius * 2)


class AIQualityControlUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Quality Control Box")
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        self.resize(int(screen_geometry.width() * 0.9), int(screen_geometry.height() * 0.9))
        self.setStyleSheet("background-color: #f0f2f5;")
        self.detail_view = None  # Keep track of DetailView instance
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Top Header
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
        
        
       
        
        icon_label = ClickableLabel()
        icon_label.clicked.connect(self.go_to_main_card)
        icon_pixmap = QPixmap("C:/Augle_AI(kishori)/P-G_SW-main/P-G_SW-main/home.png")
        icon_pixmap = icon_pixmap.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setFixedSize(30, 30)
    

        status_label = QLabel("System Ready")
        status_label.setStyleSheet("color: white; font-size: 14px;")
        status_dot = QLabel()
        status_dot.setFixedSize(14, 14)
        status_dot.setStyleSheet("background-color: #27ae60; border-radius: 7px;")
        
        top_layout.addWidget(icon_label)
        top_layout.addSpacing(10)
        top_layout.addWidget(status_label)
        top_layout.addSpacing(5)
        top_layout.addWidget(status_dot)

        # Central Switch Area
        self.middle_switch = QStackedWidget()

        # ----- MAIN CARD -----
        self.main_card_container = QWidget()
        main_layout_main_card = QVBoxLayout(self.main_card_container)
        main_layout_main_card.setContentsMargins(0, 40, 0, 40)

        white_card = QFrame()
        white_card.setMinimumSize(800, 450)  # Reasonable min size
        white_card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        white_card.setStyleSheet("""
            background-color: white;
            border-radius: 16px;
        """)

        card_layout = QVBoxLayout(white_card)
        card_layout.setContentsMargins(50, 50, 50, 50)
        card_layout.setSpacing(30)

        header = QLabel("AI Quality Control Box")
        header.setFont(QFont("Arial", 28, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; background: none;")
        header.setAlignment(Qt.AlignCenter)

        subtext = QLabel("Welcome to the automated quality inspection system")
        subtext.setFont(QFont("Arial", 18))
        subtext.setStyleSheet("color: #555; background: none;")
        subtext.setAlignment(Qt.AlignCenter)

        prompt = QLabel("Press Start Button to continue")
        prompt.setFont(QFont("Arial", 14))
        prompt.setStyleSheet("color: #777; background: none;")
        prompt.setAlignment(Qt.AlignCenter)

        dashed_box = DashedBox()
        dashed_box.setFixedSize(200, 120)

        start_button = QPushButton("START")
        start_button.setFixedSize(220, 65)
        start_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-size: 24px;
                font-weight: bold;
                border-radius: 32px;
            }
            QPushButton:hover {
                background-color: #219150;
            }
        """)
        start_button.clicked.connect(self.open_capturing_screen)

        result_button = QPushButton("RESULT")
        result_button.setFixedSize(220, 65)
        result_button.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                color: white;
                font-size: 24px;
                font-weight: bold;
                border-radius: 32px;
            }
            QPushButton:hover {
                background-color: #1a2d45;
            }
        """)
        result_button.clicked.connect(self.open_result_screen)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(40)
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.addWidget(start_button)
        btn_layout.addWidget(result_button)

        card_layout.addWidget(header)
        card_layout.addWidget(subtext)
        card_layout.addWidget(prompt)
        card_layout.addWidget(dashed_box, alignment=Qt.AlignCenter)
        card_layout.addLayout(btn_layout)

        center = QHBoxLayout()
        center.addStretch()
        center.addWidget(white_card)
        center.addStretch()

        main_layout_main_card.addLayout(center)

        # ----- WORKFLOW STACK -----
        self.workflow_stack = QStackedWidget()
        self.workflow_stack.setStyleSheet("background-color: #f0f2f5;")

        # Capture screen inside white card container
        self.capture_card = CapturingScreen()
        self.capture_card.setStyleSheet("background-color: transparent;")
        self.capture_card.next_screen_requested.connect(self.open_processing_screen)

        capture_card_frame = QFrame()
        capture_card_frame.setMinimumSize(800, 600)
        capture_card_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        capture_card_frame.setStyleSheet("""
            background-color: white;
            border-radius: 16px;
        """)

        capture_card_layout = QVBoxLayout(capture_card_frame)
        capture_card_layout.setContentsMargins(50, 50, 50, 50)
        capture_card_layout.addWidget(self.capture_card)

        self.capture_card_container = QWidget()
        capture_container_layout = QVBoxLayout(self.capture_card_container)
        capture_container_layout.setContentsMargins(0, 40, 0, 40)

        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(capture_card_frame)
        center_layout.addStretch()

        capture_container_layout.addLayout(center_layout)
        self.workflow_stack.addWidget(self.capture_card_container)

        # Other screens
        self.welcome_screen = WelcomeScreen(start_callback=self.open_capturing_screen)
        self.welcome_screen.setStyleSheet("background-color: #f0f2f5;")
        self.workflow_stack.addWidget(self.welcome_screen)

        self.result_card = ResultScreen(
            back_callback=self.open_welcome_screen,
            repeat_callback=self.open_capturing_screen,
            back1_callback= self.go_to_main_card
            
        )
        self.result_card.setStyleSheet("background-color: #f0f2f5;")
        self.result_card.detail_requested.connect(self.open_detail_view)
        self.workflow_stack.addWidget(self.result_card)

        # Wrap ProcessingScreen inside white card
        self.processing_card = ProcessingScreen()
        self.processing_card.setStyleSheet("background-color: transparent;")
        self.processing_card.next_screen_requested.connect(self.open_result_screen)

        processing_card_frame = QFrame()
        processing_card_frame.setMinimumSize(800, 600)
        processing_card_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        processing_card_frame.setStyleSheet("""
            background-color: white;
            border-radius: 16px;
        """)

        processing_card_layout = QVBoxLayout(processing_card_frame)
        processing_card_layout.setContentsMargins(50, 50, 50, 50)
        processing_card_layout.addWidget(self.processing_card)

        self.processing_card_container = QWidget()
        processing_container_layout = QVBoxLayout(self.processing_card_container)
        processing_container_layout.setContentsMargins(0, 40, 0, 40)

        processing_center_layout = QHBoxLayout()
        processing_center_layout.addStretch()
        processing_center_layout.addWidget(processing_card_frame)
        processing_center_layout.addStretch()

        processing_container_layout.addLayout(processing_center_layout)

        # Add wrapped version to workflow stack
        self.workflow_stack.addWidget(self.processing_card_container)

        # Add main card and workflow stack to middle_switch
        self.middle_switch.addWidget(self.main_card_container)
        self.middle_switch.addWidget(self.workflow_stack)

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

        # Layout Assembly
        main_layout.addWidget(top_bar)
        main_layout.addWidget(self.middle_switch)
        main_layout.addWidget(bottom_bar)

        # Show main card first
        self.middle_switch.setCurrentWidget(self.main_card_container)

    def open_capturing_screen(self):
        self.middle_switch.setCurrentWidget(self.workflow_stack)
        self.workflow_stack.setCurrentWidget(self.capture_card_container)

    def open_result_screen(self):
        self.middle_switch.setCurrentWidget(self.workflow_stack)
        self.workflow_stack.setCurrentWidget(self.result_card)

    def open_welcome_screen(self):
        self.middle_switch.setCurrentWidget(self.workflow_stack)
        self.workflow_stack.setCurrentWidget(self.welcome_screen)

    def open_processing_screen(self):
        self.middle_switch.setCurrentWidget(self.workflow_stack)
        self.workflow_stack.setCurrentWidget(self.processing_card_container)
        
    def go_to_main_card(self):
            self.middle_switch.setCurrentWidget(self.main_card_container)    

    def open_detail_view(self, category_name):
        # Remove existing detail_view to prevent duplicates
        if self.detail_view is not None:
            self.workflow_stack.removeWidget(self.detail_view)
            self.detail_view.deleteLater()
            self.detail_view = None

        self.detail_view = DetailView(category_name)
        self.detail_view.setStyleSheet("background-color: #f0f2f5;")
        self.detail_view.back_requested.connect(self.open_result_screen)
        self.workflow_stack.addWidget(self.detail_view)
        self.middle_switch.setCurrentWidget(self.workflow_stack)
        self.workflow_stack.setCurrentWidget(self.detail_view)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AIQualityControlUI()
    window.show()
    sys.exit(app.exec_())




