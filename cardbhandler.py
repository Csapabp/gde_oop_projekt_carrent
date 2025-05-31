import os
import pickle
import random
from carrental import CarRental
from car import Car
from truck import Truck
from rental import Rental
from datetime import datetime, timedelta
#- Csernák Ádám SPMFF2
class CarDBHandler:
    def __init__(self, filename):
        self.filename = os.path.join("CarRentSystem", filename)
        os.makedirs("CarRentSystem", exist_ok=True)

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "rb") as f:
                return pickle.load(f)
        else:
            rental = CarRental("BestRent")
            car1 = Car("ABC123", "Toyota Corolla", 8000, 4)
            car2 = Car("XYZ789", "Opel Astra", 7500, 5)
            truck1 = Truck("TRK111", "Ford Transit", 12000, 2000)
            truck2 = Truck("TRK222", "Mercedes Sprinter", 13000, 2500)

            rental.add_vehicle(car1)
            rental.add_vehicle(car2)
            rental.add_vehicle(truck1)
            rental.add_vehicle(truck2)

            today = datetime.today().date()
            attempts = 0
            added = 0
            while added < 4 and attempts < 20:
                vehicle = random.choice(rental.vehicles)
                start_offset = random.randint(0, 5)
                duration = random.randint(2, 4)
                start_date = today + timedelta(days=start_offset)
                end_date = start_date + timedelta(days=duration)
                if rental.rent_vehicle(vehicle.license_plate, str(start_date), str(end_date)):
                    added += 1
                attempts += 1

            return rental

    def save(self, rental):
        with open(self.filename, "wb") as f:
            pickle.dump(rental, f)