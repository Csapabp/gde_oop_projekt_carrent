import tkinter as tk
#- Csernák Ádám SPMFF2
def list_screen(app):
    app.clear_window()

    frame = tk.Frame(app.master)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="Aktuális bérlések:").pack(pady=5)
    rentals_box = tk.Text(frame, height=15)
    rentals_box.pack(fill="both", padx=10)

    rentals = app.rental.list_rentals()
    if rentals:
        for r in rentals:
            rentals_box.insert(tk.END, r + "\n")
    else:
        rentals_box.insert(tk.END, "Nincs aktív bérlés.")

    tk.Button(app.master, text="Vissza a főmenübe", command=app.main_menu).pack(side="bottom", pady=10)