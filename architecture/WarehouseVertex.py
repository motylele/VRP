from architecture.Vehicle import Vehicle
import random


class WarehouseVertex:
    # WarehouseVertex class constructor
    def __init__(self, index, vehicles_and_capacities, latitude=0, longitude=0):
        self.index = index
        self.list_vehicles = [Vehicle(capacity * 5) for count, capacity in vehicles_and_capacities for _ in range(count)]
        self.latitude = latitude
        self.longitude = longitude

    # Probabilistic vehicle selection
    def select_vehicle(self):
        capacities = [vehicle.capacity for vehicle in self.list_vehicles]
        total_capacity = sum(capacities)
        probabilities = [capacity / total_capacity for capacity in capacities]
        chosen_vehicle = random.choices(self.list_vehicles, probabilities)[0]
        return chosen_vehicle
