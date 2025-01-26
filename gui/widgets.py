import tkinter as tk

def create_break_buttons(gui):
    """Tworzy przyciski dla różnych typów przerw."""
    gui.short_break_button = tk.Button(gui.root, text="Przerwa 15 minut", command=lambda: gui.start_break(15), width=25)
    gui.short_break_button.pack(pady=5)

    gui.medium_break_button = tk.Button(gui.root, text="Przerwa 30 minut", command=lambda: gui.start_break(30), width=25)
    gui.medium_break_button.pack(pady=5)

    gui.long_break_button = tk.Button(gui.root, text="Przerwa 45 minut", command=lambda: gui.start_break(45), width=25)
    gui.long_break_button.pack(pady=5)

    gui.nine_hour_break_button = tk.Button(gui.root, text="Przerwa 9 godzin", command=lambda: gui.start_break(540), width=25)
    gui.nine_hour_break_button.pack(pady=5)


from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class TachographWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Ustawienia okna
        self.setWindowTitle("Tachograph")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: black;")

        # Załaduj obraz
        self.image_label = QLabel(self)
        self.pixmap = QPixmap(r"C:\Users\pablo\Documents\RITT_Tachograf\gui\tachograph_image.png")  # Poprawiona ścieżka
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

        # Tworzenie przycisków
        self.button1 = QPushButton("Start")
        self.button1.setStyleSheet("background-color: gold; color: black; font-size: 20px;")
        self.button1.setFixedSize(200, 60)
        self.button1.clicked.connect(self.on_button_click)

        # Tworzenie nakładki
        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.5);  /* Półprzezroczysta czarna nakładka */
            border: 2px solid gold;                  /* Złoty obrys */
            border-radius: 10px;                     /* Zaokrąglone rogi */
        """)
        self.overlay.setGeometry(0, 0, self.width(), self.height())  # Nakładka na całe okno

        # Upewnienie się, że nakładka jest widoczna
        self.overlay.show()

        # Układ przycisków

