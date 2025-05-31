from rental import Rental
from datetime import datetime
#- Csernák Ádám SPMFF2
class CarRental:
    def __init__(self, name: str):
        self.name = name
        self.vehicles = []
        self.rentals = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def rent_vehicle(self, license_plate: str, start_date: str, end_date: str):
        today = datetime.today().strftime("%Y-%m-%d")
        if start_date < today:
            return None  

        for vehicle in self.vehicles:
            if vehicle.license_plate == license_plate:
                for rental in self.rentals:
                    if rental.vehicle.license_plate == license_plate:
                        if not (end_date < rental.start_date or start_date > rental.end_date):
                            return None  
                rental = Rental(vehicle, start_date, end_date)
                self.rentals.append(rental)
                return rental
        return None

    def cancel_rental(self, license_plate: str):
        return False 

    def cancel_exact_rental(self, license_plate: str, start_date: str, end_date: str):
        for rental in self.rentals:
            if (rental.vehicle.license_plate == license_plate and
                rental.start_date == start_date and
                rental.end_date == end_date):
                self.rentals.remove(rental)
                return True
        return False

    def list_rentals(self):
        return [str(rental) for rental in self.rentals]

    def has_active_rental(self, license_plate: str):
        for rental in self.rentals:
            if rental.vehicle.license_plate == license_plate:
                return True
        return False
    
    def calculate_profit(self, license_plate: str):
        return sum(r.price() for r in self.rentals if r.vehicle.license_plate == license_plate)