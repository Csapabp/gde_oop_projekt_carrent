import tkinter as tk
from tkinter import messagebox, ttk
from car import Car
from truck import Truck
#- Csernák Ádám SPMFF2
def maintenance_screen(app):
  import tkinter as tk
from tkinter import messagebox, ttk
from car import Car
from truck import Truck

def maintenance_screen(app):
    app.master.geometry("1100x500")
    app.clear_window()

    frame = tk.Frame(app.master)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="Járművek listája", font=("Arial", 12)).pack(pady=10)

    columns = ("rendszám", "típus", "modell", "bérlés ára", "ajtók száma", "kapacitás", "összes haszon")
    tree_frame = tk.Frame(frame)
    tree_frame.pack(expand=True, fill="both", padx=10, pady=10)

    scrollbar_x = tk.Scrollbar(tree_frame, orient="horizontal")
    scrollbar_x.pack(side="bottom", fill="x")

    app.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", xscrollcommand=scrollbar_x.set)
    scrollbar_x.config(command=app.tree.xview)

    for col in columns:
        app.tree.heading(col, text=col)
        app.tree.column(col, width=120, anchor="center")

    for v in app.rental.vehicles:
        tipus = "Személyautó" if isinstance(v, Car) else "Teherautó"
        ajtok = v.doors if isinstance(v, Car) else "N/A"
        kapacitas = v.capacity if isinstance(v, Truck) else "N/A"
        profit = app.rental.calculate_profit(v.license_plate)

        app.tree.insert("", tk.END, values=(v.license_plate, tipus, v.model, v.rental_price, ajtok, kapacitas, f"{profit} Ft"))

    app.tree.pack(expand=True, fill="both")

    btn_frame = tk.Frame(app.master)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Új jármű hozzáadása", command=lambda: add_vehicle_screen(app), width=25).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Kiválasztott jármű törlése", command=lambda: delete_vehicle(app), width=25).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Kiválasztott jármű módosítása", command=lambda: modify_vehicle_screen(app), width=25).pack(side="left", padx=5)

    tk.Button(app.master, text="Vissza a főmenübe", command=app.main_menu).pack(side="bottom", pady=10)

def delete_vehicle(app):
    selected = app.tree.selection()
    if not selected:
        messagebox.showwarning("Nincs kiválasztva", "Előbb válassz ki egy járművet a listából!")
        return

    values = app.tree.item(selected[0], 'values')
    plate = values[0]

    if app.rental.has_active_rental(plate):
        messagebox.showerror("Hiba", "A kiválasztott járműhöz tartozik aktív foglalás, ezért nem törölhető.")
        return

    confirm = messagebox.askyesno("Megerősítés", f"Biztosan törölni szeretnéd a(z) {plate} rendszámú járművet?")
    if not confirm:
        return

    app.rental.vehicles = [v for v in app.rental.vehicles if v.license_plate != plate]
    app.db.save(app.rental)
    maintenance_screen(app)

def add_vehicle_screen(app):
    app.clear_window()

    frame = tk.Frame(app.master)
    frame.pack(pady=20)

    tk.Label(frame, text="Új jármű hozzáadása", font=("Arial", 12)).pack(pady=10)

    tk.Button(frame, text="Mégse", command=lambda: maintenance_screen(app)).pack(pady=(0, 10))

    type_var = tk.StringVar()
    tk.Label(frame, text="Típus kiválasztása:").pack()
    type_combo = ttk.Combobox(frame, textvariable=type_var, values=["Személyautó", "Teherautó"])
    type_combo.pack(pady=5)

    details_frame = tk.Frame(frame)
    details_frame.pack(pady=10)

    def show_fields(*args):
        for widget in details_frame.winfo_children():
            widget.destroy()

        tk.Label(details_frame, text="Rendszám:").pack()
        plate_entry = tk.Entry(details_frame)
        plate_entry.pack(pady=5)

        tk.Label(details_frame, text="Modell:").pack()
        model_entry = tk.Entry(details_frame)
        model_entry.pack(pady=5)

        tk.Label(details_frame, text="Bérlés ára (Ft/nap):").pack()
        price_entry = tk.Entry(details_frame)
        price_entry.pack(pady=5)

        if type_var.get() == "Személyautó":
            tk.Label(details_frame, text="Ajtók száma:").pack()
            extra_entry = tk.Entry(details_frame)
            extra_entry.pack(pady=5)
        else:
            tk.Label(details_frame, text="Kapacitás (kg):").pack()
            extra_entry = tk.Entry(details_frame)
            extra_entry.pack(pady=5)

        def add_vehicle():
            plate = plate_entry.get()
            model = model_entry.get()
            price = price_entry.get()
            extra = extra_entry.get()

            if not plate or not model or not price or not extra:
                messagebox.showerror("Hiba", "Minden mező kitöltése kötelező!")
                return
            try:
                price = int(price)
                extra_val = int(extra)
            except ValueError:
                messagebox.showerror("Hiba", "Az ár és a kiegészítő mező csak szám lehet!")
                return
            if any(v.license_plate == plate for v in app.rental.vehicles):
                messagebox.showerror("Hiba", "Ez a rendszám már létezik!")
                return
            if type_var.get() == "Személyautó":
                new_vehicle = Car(plate, model, price, extra_val)
            else:
                new_vehicle = Truck(plate, model, price, extra_val)

            app.rental.vehicles.append(new_vehicle)
            app.db.save(app.rental)
            maintenance_screen(app)

        tk.Button(details_frame, text="Hozzáadás", command=add_vehicle).pack(pady=10)
        tk.Button(details_frame, text="Mégse", command=lambda: maintenance_screen(app)).pack()

    type_combo.bind("<<ComboboxSelected>>", show_fields)

def modify_vehicle_screen(app):
    selected = app.tree.selection()
    if not selected:
        messagebox.showwarning("Nincs kiválasztva", "Előbb válassz ki egy járművet a listából!")
        return
    values = app.tree.item(selected[0], 'values')
    plate = values[0]

    vehicle = next((v for v in app.rental.vehicles if v.license_plate == plate), None)
    if not vehicle:
        messagebox.showerror("Hiba", "Nem található a kiválasztott jármű.")
        return

    app.clear_window()

    frame = tk.Frame(app.master)
    frame.pack(pady=20)

    tk.Label(frame, text="Jármű módosítása", font=("Arial", 12)).pack(pady=10)

    tk.Label(frame, text="Rendszám:").pack()
    plate_entry = tk.Entry(frame)
    plate_entry.insert(0, vehicle.license_plate)
    plate_entry.pack(pady=5)

    tk.Label(frame, text="Modell:").pack()
    model_entry = tk.Entry(frame)
    model_entry.insert(0, vehicle.model)
    model_entry.pack(pady=5)

    tk.Label(frame, text="Bérlés ára (Ft/nap):").pack()
    price_entry = tk.Entry(frame)
    price_entry.insert(0, str(vehicle.rental_price))
    price_entry.pack(pady=5)

    if isinstance(vehicle, Car):
        tk.Label(frame, text="Ajtók száma:").pack()
        extra_entry = tk.Entry(frame)
        extra_entry.insert(0, str(vehicle.doors))
        extra_entry.pack(pady=5)
    else:
        tk.Label(frame, text="Kapacitás (kg):").pack()
        extra_entry = tk.Entry(frame)
        extra_entry.insert(0, str(vehicle.capacity))
        extra_entry.pack(pady=5)

    def modify_vehicle():
        new_plate = plate_entry.get()
        new_model = model_entry.get()
        new_price = price_entry.get()
        new_extra = extra_entry.get()

        if not new_plate or not new_model or not new_price or not new_extra:
            messagebox.showerror("Hiba", "Minden mező kitöltése kötelező!")
            return

        if new_plate != vehicle.license_plate and any(v.license_plate == new_plate for v in app.rental.vehicles):
            messagebox.showerror("Hiba", "Ez a rendszám már létezik!")
            return

        try:
            vehicle.license_plate = new_plate
            vehicle.model = new_model
            vehicle.rental_price = int(new_price)
            if isinstance(vehicle, Car):
                vehicle.doors = int(new_extra)
            else:
                vehicle.capacity = int(new_extra)
        except ValueError:
            messagebox.showerror("Hiba", "Az ár és a kiegészítő mező csak szám lehet!")
            return

        app.db.save(app.rental)
        maintenance_screen(app)

    tk.Button(frame, text="Mentés", command=modify_vehicle).pack(pady=10)
    tk.Button(frame, text="Mégse", command=lambda: maintenance_screen(app)).pack()
