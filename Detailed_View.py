from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QFont
from PyQt5.QtCore import Qt, QRectF, pyqtSignal

DEFECT_IMG_PATH = "pads.png"
PRODUCT_IMG_PATH = "pads.png"


class DetailView(QWidget):
    back_requested = pyqtSignal()

    def __init__(self, category_name: str):
        super().__init__()

        self.setStyleSheet("background-color: #f0f2f5;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(700, 550)

        # ─── OUTER LAYOUT ───────────────────────────────────────────────
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 40, 0, 40)
        outer_layout.setSpacing(30)

        # ─── TITLE + BACK BUTTON ────────────────────────────────────────
        title = QLabel(category_name)
        title.setFont(QFont("Arial", 28, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; border: none;")
        title.setAlignment(Qt.AlignLeft)

        back_btn = QPushButton("Back")
        back_btn.setFixedSize(100, 45)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e90ff; color: white;
                border: none; border-radius: 10px; font-weight: bold;
            }
            QPushButton:hover { background-color: #166ebf; }
        """)
        back_btn.clicked.connect(self.back_requested.emit)

        # ─── HEADER SECTION: Left-aligned title + back button ──────────────
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(30, 0, 0, 0)
        header_layout.setSpacing(10)

        title = QLabel(category_name)
        title.setFont(QFont("Arial", 28, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; border: none;")
        title.setAlignment(Qt.AlignLeft)

        back_btn = QPushButton("Back")
        back_btn.setFixedSize(100, 45)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e90ff; color: white;
                border: none; border-radius: 10px; font-weight: bold;
            }
            QPushButton:hover { background-color: #166ebf; }
        """)
        back_btn.clicked.connect(self.back_requested.emit)

        header_layout.addWidget(title, alignment=Qt.AlignLeft)
        header_layout.addWidget(back_btn, alignment=Qt.AlignLeft)

        outer_layout.addLayout(header_layout)

        # ─── DEFECT BOX ─────────────────────────────────────────────────
        defect_box = QFrame()
        defect_box.setStyleSheet("""
            background-color: white;
            border: 2px solid #ccc;
            border-radius: 12px;
        """)
        defect_box.setFixedSize(500, 390)

        defect_layout = QVBoxLayout(defect_box)
        defect_layout.setContentsMargins(30, 30, 30, 30)
        defect_layout.setSpacing(20)

        defect_title = QLabel("Defects")
        defect_title.setFont(QFont("Arial", 20, QFont.Bold))
        defect_title.setStyleSheet("color: #2c3e50; border: none;")
        defect_layout.addWidget(defect_title)

        defect_img_row = QHBoxLayout()
        img_label = QLabel()
        img_label.setPixmap(
            QPixmap(DEFECT_IMG_PATH).scaled(240, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        img_label.setStyleSheet("border: none; background: none;")
        defect_img_row.addWidget(img_label)

        defect_labels = QVBoxLayout()
        for txt in ["Defect01 : 0.3 mm", "Defect02 : 0.2 mm", "Defect03 : 0.5 mm"]:
            lbl = QLabel(txt)
            lbl.setFont(QFont("Arial", 15))
            lbl.setStyleSheet("color: #2c3e50; border: none;")
            defect_labels.addWidget(lbl)

        defect_img_row.addLayout(defect_labels)
        defect_img_row.addStretch()
        defect_layout.addLayout(defect_img_row)
        defect_layout.addStretch()

        status = QLabel("Status : Pass")
        status.setFont(QFont("Arial", 24, QFont.Bold))
        status.setAlignment(Qt.AlignCenter)
        status.setStyleSheet("color: #2c3e50; border: none;")
        defect_layout.addWidget(status)

        # ─── PRODUCT BOX ────────────────────────────────────────────────
        product_box = QFrame()
        product_box.setStyleSheet("""
            background-color: white;
            border: 2px solid #ccc;
            border-radius: 12px;
        """)
        product_box.setFixedSize(500, 390)

        product_layout = QVBoxLayout(product_box)
        product_layout.setContentsMargins(30, 30, 30, 30)
        product_layout.setSpacing(20)

        product_title = QLabel("Product Visual")
        product_title.setFont(QFont("Arial", 20, QFont.Bold))
        product_title.setStyleSheet("color: #2c3e50; border: none;")
        product_layout.addWidget(product_title)

        prod_pix = QPixmap(PRODUCT_IMG_PATH).scaled(
            600, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        annotated = QPixmap(prod_pix.size())
        annotated.fill(Qt.transparent)

        painter = QPainter(annotated)
        painter.drawPixmap(0, 0, prod_pix)
        painter.setPen(QPen(Qt.red, 5))
        painter.drawRect(
            QRectF(
                prod_pix.width() * 0.25,
                prod_pix.height() * 0.10,
                prod_pix.width() * 0.50,
                prod_pix.height() * 0.80,
            )
        )
        painter.end()

        annotated_label = QLabel()
        annotated_label.setPixmap(annotated)
        annotated_label.setAlignment(Qt.AlignCenter)
        annotated_label.setStyleSheet("border: none; background: none;")
        product_layout.addWidget(annotated_label)

        # ─── HORIZONTAL ROW FOR DEFECT + PRODUCT ───────────────────────
        row_layout = QHBoxLayout()
        row_layout.setSpacing(40)
        row_layout.setAlignment(Qt.AlignCenter)
        row_layout.addWidget(defect_box)
        row_layout.addWidget(product_box)

        outer_layout.addLayout(row_layout)
        outer_layout.addStretch()
