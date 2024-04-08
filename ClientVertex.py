class ClientVertex:
    ############
    # __INIT__()
    ############
    # ClientVertex class constructor
    # Input: index::Int    - vertex index
    #        capacity::INT - vertex capacity
    #        stored::INT   - number of items stored
    def __init__(self, index, capacity, stored):
        self.index = index
        self.capacity = capacity
        self.stored = stored

    ####################
    # GET_VERTEX_DEMAND()
    ####################
    # Getting vertex demand for items
    # Output: demand::INT - vertex demand
    def get_vertex_demand(self):
        return self.capacity - self.stored

