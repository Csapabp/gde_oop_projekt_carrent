from datetime import datetime

class Rental:
    def __init__(self, vehicle, start_date: str, end_date: str):
        self.vehicle = vehicle
        self.start_date = start_date  # formátum: 'YYYY-MM-DD'
        self.end_date = end_date

    def price(self):
        days = (datetime.strptime(self.end_date, "%Y-%m-%d") - datetime.strptime(self.start_date, "%Y-%m-%d")).days + 1
        return self.vehicle.rental_price * max(days, 0)

    def __str__(self):
        return f"{self.vehicle.license_plate} - {self.start_date} → {self.end_date} - {self.price()} HUF"
