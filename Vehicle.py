class Vehicle:
    ############
    # __INIT__()
    ############
    # Vehicle class constructor
    # Input: capacity::INT - vehicle capacity, also described as 'q'
    def __init__(self, capacity):
        self.capacity = capacity

    def __str__(self):
        return f"    VEHICLE CAPACITY = {self.capacity}"
