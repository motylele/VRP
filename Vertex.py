class Vertex:
    ############
    # __INIT__()
    ############
    # Vertex class constructor
    # Input: capacity::INT - vertex capacity
    #        stored::INT   - number of items stored
    def __init__(self, capacity, stored):
        self.capacity = capacity
        self.stored = stored

    ####################
    # GET_VERTEX_DEMAND()
    ####################
    # Getting vertex demand for items
    # Output: demand::INT - vertex demand
    def get_vertex_demand(self):
        return self.capacity - self.stored

