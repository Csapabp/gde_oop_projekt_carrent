from abc import ABC, abstractmethod
#- Csernák Ádám SPMFF2
class Vehicle(ABC):
    def __init__(self, license_plate: str, model: str, rental_price: int):
        self.license_plate = license_plate
        self.model = model
        self.rental_price = rental_price
        self.available = True

    @abstractmethod
    def description(self):
        pass
