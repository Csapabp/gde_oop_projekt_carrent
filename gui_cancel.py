import tkinter as tk
from tkinter import messagebox, ttk
#- Csernák Ádám SPMFF2
def cancel_screen(app):
    app.clear_window()

    frame = tk.Frame(app.master)
    frame.pack(expand=True)

    active_rentals = [f"{r.vehicle.license_plate} | {r.start_date} → {r.end_date}" for r in app.rental.rentals]

    if not active_rentals:
        tk.Label(frame, text="Jelenleg nincs egy autó sem lefoglalva.").pack(pady=10)
    else:
        tk.Label(frame, text="Válassz egy lemondandó foglalást:").pack(pady=5)
        app.cancel_var = tk.StringVar()
        app.cancel_combo = ttk.Combobox(frame, textvariable=app.cancel_var)
        app.cancel_combo['values'] = active_rentals
        app.cancel_combo.pack(pady=5)

        tk.Button(frame, text="Lemondás", command=lambda: cancel_rental(app)).pack(pady=5)

    tk.Button(app.master, text="Vissza a főmenübe", command=app.main_menu).pack(side="bottom", pady=10)

def cancel_rental(app):
    selected = app.cancel_var.get()
    if not selected:
        messagebox.showerror("Hiba", "Válassz egy foglalást a lemondáshoz.")
        return
    try:
        plate, date_range = selected.split(" | ")
        start, end = date_range.strip().split(" → ")
    except ValueError:
        messagebox.showerror("Hiba", "Hibás formátum a kiválasztásnál.")
        return

    if app.rental.cancel_exact_rental(plate, start, end):
        messagebox.showinfo("Siker", "A bérlés le lett mondva.")
        cancel_screen(app)
    else:
        messagebox.showerror("Hiba", "Nem található ilyen bérlés.")