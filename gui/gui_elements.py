import tkinter as tk

def create_label(root, text, font=("Arial", 12), fg=None):
    label = tk.Label(root, text=text, font=font, fg=fg)
    label.pack(pady=10)
    return label

def create_quit_button(root, command):
    return tk.Button(root, text="Zamknij", command=command, width=25)

def create_warning_label(root):
    return tk.Label(root, text="", font=("Arial", 12), fg="red")

def create_time_and_violation_row(root, time_text, violation_text, time_font=("Arial", 12), violation_font=("Arial", 12), violation_fg="red"):
    """
    Tworzy ramkę zawierającą etykietę czasu i przekroczeń w jednej linii.
    """
    frame = tk.Frame(root)
    frame.pack(pady=10)

    time_label = tk.Label(frame, text=time_text, font=time_font)
    time_label.grid(row=0, column=0, padx=10)

    violation_label = tk.Label(frame, text=violation_text, font=violation_font, fg=violation_fg)
    violation_label.grid(row=0, column=1, padx=10)

    return time_label, violation_label
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class TachographGUI(QWidget):
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
        self.overlay.setVisible(True)  # Upewnij się, że nakładka jest widoczna

        # Układ przycisków
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)  # Dodanie obrazu
        layout.addWidget(self.button1)      # Dodanie przycisku
        self.setLayout(layout)

    def on_button_click(self):
        print("Przycisk kliknięty!")
        self.overlay.setVisible(False)  # Ukryj nakładkę po kliknięciu przycisku
