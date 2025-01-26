import tkinter as tk
import json
import os


class OverlayGUI:
    CONFIG_FILE = os.path.join(os.getcwd(), "overlay_config.json")  # Ścieżka pliku JSON

    def __init__(self, telemetry_manager):
        self.telemetry_manager = telemetry_manager

        # Konfiguracja okna nakładki
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # Usuwa ramkę okna
        self.root.attributes("-topmost", True)  # Okno zawsze na wierzchu
        self.root.attributes("-transparentcolor", "black")  # Czarny kolor jako przezroczysty
        self.root.configure(bg="black")  # Czarny kolor tła

        print(f"Plik konfiguracji: {self.CONFIG_FILE}")

        # Wczytaj poprzednie ustawienia
        self.load_geometry()

        self.offset_x = 0
        self.offset_y = 0

        # Ramka
        self.frame = tk.Frame(self.root, bg="gold", bd=2)  # Złote obramowanie
        self.frame.pack(fill="both", expand=True)

        # Obszar przeciągania
        self.drag_area = tk.Label(self.frame, bg="gold", height=1, text="RITT", font=("Arial", 10))
        self.drag_area.pack(fill="x", side="top")
        self.drag_area.bind("<ButtonPress-1>", self.start_drag)
        self.drag_area.bind("<B1-Motion>", self.do_drag)

        # Canvas
        self.canvas = tk.Canvas(self.frame, highlightthickness=0, bg="black")
        self.canvas.pack(fill="both", expand=True)

        # Dodanie etykiet
        self.speed_label = self.canvas.create_text(400, 25, text="Prędkość: brak danych", font=("Arial", 16), fill="white")
        self.time_label = self.canvas.create_text(400, 75, text="Czas gry: brak danych", font=("Arial", 16), fill="white")

        # Obsługa zmiany rozmiaru
        self.add_resize_support()

        # Obsługa zamknięcia okna
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def save_geometry(self):
        """Zapisuje pozycję i rozmiar okna do pliku konfiguracyjnego."""
        try:
            geometry = self.root.geometry()
            config = {"geometry": geometry}
            print(f"Próba zapisu geometrii: {geometry}")
            with open(self.CONFIG_FILE, "w") as file:
                json.dump(config, file)
            print(f"Zapisano geometrię: {geometry}")
        except Exception as e:
            print(f"Błąd podczas zapisywania geometrii: {e}")

    def load_geometry(self):
        """Wczytuje pozycję i rozmiar okna."""
        try:
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, "r") as file:
                    config = json.load(file)
                    geometry = config.get("geometry", "800x100+100+100")
                    self.root.geometry(geometry)
                    print(f"Wczytano geometrię: {geometry}")
            else:
                self.root.geometry("800x100+100+100")
                print("Plik konfiguracji nie istnieje. Ustawiono domyślną geometrię.")
        except Exception as e:
            print(f"Błąd podczas wczytywania geometrii: {e}")

    def add_resize_support(self):
        """Dodaje obsługę zmiany rozmiaru za pomocą myszki."""
        self.frame.bind("<Enter>", self.change_cursor_on_border)
        self.frame.bind("<Leave>", self.reset_cursor)
        self.frame.bind("<ButtonPress-1>", self.start_resize)
        self.frame.bind("<B1-Motion>", self.do_resize)

    def change_cursor_on_border(self, event):
        """Zmienia kursor na strzałki przy krawędziach."""
        x, y = event.x, event.y
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        if x > width - 10 and y > height - 10:
            self.root.config(cursor="size_nw_se")  # Dolny prawy róg
        elif x > width - 10:
            self.root.config(cursor="size_we")  # Prawa krawędź
        elif y > height - 10:
            self.root.config(cursor="size_ns")  # Dolna krawędź
        else:
            self.root.config(cursor="arrow")  # Zwykły kursor

    def reset_cursor(self, event):
        """Przywraca domyślny kursor."""
        self.root.config(cursor="arrow")

    def start_resize(self, event):
        """Zapisuje początkowe wartości rozmiaru okna."""
        self.start_width = self.root.winfo_width()
        self.start_height = self.root.winfo_height()
        self.start_mouse_x = event.x_root
        self.start_mouse_y = event.y_root

    def do_resize(self, event):
        """Zmienia rozmiar okna na podstawie ruchu myszy."""
        dx = event.x_root - self.start_mouse_x
        dy = event.y_root - self.start_mouse_y

        new_width = max(200, self.start_width + dx)  # Minimalna szerokość
        new_height = max(50, self.start_height + dy)  # Minimalna wysokość

        self.root.geometry(f"{new_width}x{new_height}")
        self.canvas.config(width=new_width, height=new_height)

        # Przeliczanie pozycji i rozmiaru tekstów
        self.scale_canvas(new_width, new_height)
        self.save_geometry()  # Zapisz rozmiar okna po zmianie

    def scale_canvas(self, new_width, new_height):
        """Przelicza pozycje i rozmiary elementów na Canvas."""
        scale_x = new_width / 800  # Domyślna szerokość
        scale_y = new_height / 100  # Domyślna wysokość

        # Skalowanie tekstów
        self.canvas.coords(self.speed_label, new_width * 0.5, new_height * 0.25)
        self.canvas.coords(self.time_label, new_width * 0.5, new_height * 0.5)

        # Skalowanie czcionek
        new_font_size = int(16 * min(scale_x, scale_y))
        self.canvas.itemconfig(self.speed_label, font=("Arial", new_font_size))
        self.canvas.itemconfig(self.time_label, font=("Arial", new_font_size))

    def start_drag(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def do_drag(self, event):
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f"+{x}+{y}")
        self.save_geometry()  # Natychmiastowy zapis pozycji

    def on_close(self):
        self.save_geometry()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
