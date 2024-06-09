from Vehicle import Vehicle
import random


class WarehouseVertex:
    ############
    # __INIT__()
    ############
    # WarehouseVertex class constructor
    # Input: index::Int                           - vertex index
    #        vehicles_and_capacities::[[Int,Int]] - list of pairs [vehicles count, their capacity]
    #        Ex. vehicles_and_capacities = [
    #               (10, 12),  # 10 vehicles with capacity 12
    #               (5, 8)     # 5 vehicles with capacity 8
    #           ]
    def __init__(self, index, vehicles_and_capacities, latitude=0, longitude=0):
        self.index = index
        self.list_vehicles = [Vehicle(capacity * 5) for count, capacity in vehicles_and_capacities for _ in range(count)]
        self.latitude = latitude
        self.longitude = longitude

    '''
    POC:
    - deleting vehicle if chosen: warehouse may run out of vehicles, but every route is served by different vehicle
    - not deleting: every route may be served by the same vehicle <- current
    '''
    ##################
    # SELECT_VEHICLE()
    ##################
    # Selecting random vehicle with a probability advantage for cars with larger capacity
    # Output: chosen_vehicle::class::Vehicle - chosen vehicle
    def select_vehicle(self):
        capacities = [vehicle.capacity for vehicle in self.list_vehicles]
        total_capacity = sum(capacities)
        probabilities = [capacity / total_capacity for capacity in capacities]
        chosen_vehicle = random.choices(self.list_vehicles, probabilities)[0]
        return chosen_vehicle
