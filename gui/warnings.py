def handle_warnings(gui):
    """Obsługuje ostrzeżenia wizualne w GUI."""
    if gui.drive_time_game > 4.5 * 3600:
        gui.warning_label.config(text="Ostrzeżenie: Przekroczono 4,5 godziny jazdy bez przerwy!")
        gui.drive_time_label.config(fg="red")
    else:
        gui.drive_time_label.config(fg="black")

    if gui.work_time_game > 9 * 3600:
        gui.warning_label.config(text="Ostrzeżenie: Przekroczono 9 godzin pracy!")
        gui.work_time_label.config(fg="red")
    else:
        gui.work_time_label.config(fg="black")
