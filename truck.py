from vehicle import Vehicle

class Truck(Vehicle):
    def __init__(self, license_plate: str, model: str, rental_price: int, capacity: int):
        super().__init__(license_plate, model, rental_price)
        self.capacity = capacity

    def description(self):
        return f"Truck - {self.license_plate}, {self.model}, {self.capacity} kg capacity, {self.rental_price} HUF/day"
