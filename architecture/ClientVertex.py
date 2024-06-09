class ClientVertex:
    # ClientVertex constructor
    def __init__(self, index, discharged, capacity, stored):
        self.index = index
        self.discharged = discharged
        self.capacity = capacity
        self.stored = stored

    # Getting client vertex demand
    def get_vertex_demand(self):
        return self.capacity - self.stored
