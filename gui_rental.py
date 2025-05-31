import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime

def rental_screen(app):
    app.clear_window()

    frame = tk.Frame(app.master)
    frame.pack(expand=True)

    tk.Label(frame, text="Válassz járművet a bérléshez:").pack(pady=5)

    app.vehicle_var = tk.StringVar()
    app.vehicle_combo = ttk.Combobox(frame, textvariable=app.vehicle_var)
    app.vehicle_combo.pack(pady=5)
    app.vehicle_combo['values'] = [v.license_plate for v in app.rental.vehicles]

    tk.Label(frame, text="Bérlés kezdete:").pack()
    app.start_date = DateEntry(frame, date_pattern='yyyy-mm-dd')
    app.start_date.pack(pady=5)

    tk.Label(frame, text="Bérlés vége:").pack()
    app.end_date = DateEntry(frame, date_pattern='yyyy-mm-dd')
    app.end_date.pack(pady=5)

    tk.Button(frame, text="Gépjármű lefoglalása", command=lambda: rent_vehicle(app)).pack(pady=10)

    tk.Button(app.master, text="Vissza a főmenübe", command=app.main_menu).pack(side="bottom", pady=10)

def rent_vehicle(app):
    license_plate = app.vehicle_var.get()
    start_date = app.start_date.get_date().strftime("%Y-%m-%d")
    end_date = app.end_date.get_date().strftime("%Y-%m-%d")
    today = datetime.today().strftime("%Y-%m-%d")

    if not license_plate:
        messagebox.showerror("Hiba", "Válassz járművet!")
        return

    if start_date > end_date:
        messagebox.showerror("Hiba", "A kezdő dátum nem lehet későbbi, mint a végdátum.")
        return

    if start_date < today:
        messagebox.showerror("Hiba", "A kezdő dátum nem lehet korábbi a mai napnál.")
        return

    rental = app.rental.rent_vehicle(license_plate, start_date, end_date)
    if rental:
        messagebox.showinfo("Siker", f"Bérlés sikeres: {rental.price()} Ft")
        app.vehicle_combo.set("")
    else:
        messagebox.showerror("Hiba", "A jármű nem elérhető a megadott időszakban.")