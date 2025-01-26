class Interface:
    def __init__(self, time_manager):
        self.time_manager = time_manager

    def run(self):
        print("Interfejs tachografu uruchomiony!")
        self.display_menu()

    def display_menu(self):
        while True:
            print("\nWybierz opcję:")
            print("1. Dodaj czas jazdy")
            print("2. Dodaj przerwę")
            print("3. Wyświetl status")
            print("4. Wyjdź")

            choice = input("Wybór: ")

            if choice == "1":
                minutes = int(input("Podaj czas jazdy (w minutach): "))
                self.time_manager.times["DRIVE"] += minutes
            elif choice == "2":
                minutes = int(input("Podaj czas przerwy (w minutach): "))
                self.time_manager.times["BREAK"] += minutes
            elif choice == "3":
                self.show_status()
            elif choice == "4":
                break
            else:
                print("Nieprawidłowy wybór!")

    def show_status(self):
        print("Status: ")
        for key, value in self.time_manager.times.items():
            print(f"{key.name}: {value} minut")
