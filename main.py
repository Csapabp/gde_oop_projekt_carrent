import tkinter as tk
from tkinter import messagebox, ttk
from cardbhandler import CarDBHandler
from carrental import CarRental
from car import Car
from truck import Truck
from gui_rental import rental_screen, rent_vehicle
from gui_list_rentals import list_screen
from gui_maintenance import maintenance_screen
from gui_cancel import cancel_screen

#- Csernák Ádám SPMFF2

class RentalApp:
    def __init__(self, master):
        self.master = master
        master.title("SPMFF2 Autókölcsönző Rendszer")
        master.geometry("600x400")

        self.db = CarDBHandler("carrentdb.pkl")
        self.rental = self.db.load()

        self.main_menu()

        self.master.protocol("WM_DELETE_WINDOW", self.on_exit)

    def on_exit(self):
        self.db.save(self.rental)
        self.master.destroy()

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def main_menu(self):
        self.clear_window()

        frame = tk.Frame(self.master)
        frame.pack(expand=True)

        title = tk.Label(frame, text="Üdvözöljük az SPMFF2 Autókölcsönző Rendszerben!", font=("Arial", 14))
        title.pack(pady=20)

        rent_btn = tk.Button(frame, text="Bérlés", command=lambda: rental_screen(self), width=30)
        rent_btn.pack(pady=5)

        cancel_btn = tk.Button(frame, text="Bérlés lemondása", command=lambda: cancel_screen(self), width=30)
        cancel_btn.pack(pady=5)

        list_btn = tk.Button(frame, text="Aktuális bérlések megtekintése", command=lambda: list_screen(self), width=30)
        list_btn.pack(pady=5)

        maintenance_btn = tk.Button(frame, text="Járművek karbantartása", command=lambda: maintenance_screen(self), width=30)
        maintenance_btn.pack(pady=5)

        exit_btn = tk.Button(frame, text="Kilépés", command=self.on_exit, width=30)
        exit_btn.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = RentalApp(root)
    root.mainloop()
