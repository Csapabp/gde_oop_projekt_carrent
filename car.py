from vehicle import Vehicle
#- Csernák Ádám SPMFF2
class Car(Vehicle):
    def __init__(self, license_plate: str, model: str, rental_price: int, doors: int):
        super().__init__(license_plate, model, rental_price)
        self.doors = doors

    def description(self):
        return f"Car - {self.license_plate}, {self.model}, {self.doors} doors, {self.rental_price} HUF/day"
