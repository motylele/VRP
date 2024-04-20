from WarehouseVertex import WarehouseVertex
from ClientVertex import ClientVertex
from Vehicle import Vehicle
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random


class Graph:
    ############
    # __INIT__()
    ############
    # Graph class constructor
    # Input: num_vertices::INT                    - number of vertices
    #        num_warehouses::INT                  - number of warehouses
    #        vehicles_and_capacities::[[Int,Int]] - list of pairs [vehicles count, their capacity]
    #                                               *Assuming all warehouse vertices have the same fleet of vehicles*
    #                                               Ex. vehicles_and_capacities = [
    #                                                   (10, 12),  # 10 vehicles with capacity 12
    #                                                   (5, 8)     # 5 vehicles with capacity 8
    #                                               ]
    #        generate_new_edges::BOOL             - flag, if generate new edges
    #        filename_edges::STRING               - file name for writing/reading edges and their weights
    #                                               (default='graph-edges.txt')
    #        generate_new_vertices::BOOL          - flag, if generate new vertices
    #        filename_vertices::STRING            - file name for writing/reading vertices
    #                                               (default='graph-vertices.txt')
    def __init__(self,
                 num_vertices,
                 num_warehouses,
                 vehicles_and_capacities,
                 generate_new_edges=False,
                 edges_range=(1.0, 10.0),
                 filename_edges="graph-edges.txt",
                 generate_new_vertices=False,
                 vertices_range=(0, 10),
                 filename_vertices="graph-vertices.txt"):

        if num_vertices < 2:
            raise ValueError("Graph must have at least two vertices.")

        if num_warehouses < 1:
            raise ValueError("Graph must have at least one warehouse.")

        if num_warehouses > num_vertices - 1:
            raise ValueError("At least one client vertex is required.")

        # todo: 'vehicles_and_capacities' validation

        self.num_vertices = num_vertices
        self.num_warehouses = num_warehouses

        self.edges_range= edges_range
        self.vertices_range = vertices_range

        self.filename_edges = filename_edges
        self.filename_vertices = filename_vertices

        self.list_client_vertices = [ClientVertex(i, 0, 0)
                                     for i in range(1, self.num_vertices - self.num_warehouses + 1)]
        self.list_warehouse_vertices = [WarehouseVertex(i, vehicles_and_capacities)
                                        for i in range(-self.num_warehouses + 1, 1)]

        if generate_new_edges:
            self.generate_and_write_edges_to_file(
                min_weight=self.edges_range[0],
                max_weight=self.edges_range[1]
            )

        if generate_new_vertices:
            self.generate_and_write_vertices_to_file(
                min_vert=self.vertices_range[0],
                max_vert=self.vertices_range[1]
            )

        if self.check_if_can_read():
            raise ValueError("Incorrect parameters. Generate new valid graph or provide valid parameters.")

        self.graph = nx.complete_graph(self.num_vertices - self.num_warehouses + 1)
        self.adj_matrix = np.zeros((self.num_vertices, self.num_vertices))

        self.read_edges_from_file()
        self.read_vertices_from_file()

    #####################
    # CHECK_IF_CAN_READ()
    #####################
    # File readability conditions check:
    # 1. Checking if edge parameters match number of vertices, edges = (vertices * vertices - 1) / 2
    # 2. Checking if edges generated for proper number of warehouses
    # 3. Checking if vertices parameters match number of vertices
    def check_if_can_read(self):
        return (sum(1 for _ in open(self.filename_edges, 'r')) != self.num_vertices * (self.num_vertices - 1) / 2) \
            or (int(open(self.filename_edges, 'r').readline().split(',')[0]) != -self.num_warehouses + 1) \
            or (sum(1 for _ in open(self.filename_vertices, 'r')) != self.num_vertices - self.num_warehouses)

    ############
    # ADD_EDGE()
    ############
    # Adding edge to graph and adjacency matrix
    # Input: u::INT        - vertex u of {u, v} edge
    #        v::INT        - vertex v of {u, v} edge
    #        weight::FLOAT - weight of {u, v} edge
    def add_edge(self, u, v, weight):
        if u == v:
            raise ValueError("Attempting to add self-loop edge.")
        else:
            if self.adj_matrix[u + self.num_warehouses - 1][v + self.num_warehouses - 1] != 0:
                raise ValueError("Attempting to add the existing edge.")

        self.graph.add_edge(u, v, weight=weight)
        self.adj_matrix[u + self.num_warehouses - 1][v + self.num_warehouses - 1] = weight
        self.adj_matrix[v + self.num_warehouses - 1][u + self.num_warehouses - 1] = weight

    ###############
    # REMOVE_EDGE()
    ###############
    # Removing edge from graph and adjacency matrix
    # Edge does not exist if adj_matrix is 0 on [u][v] (and [v][u])
    # Input: u::INT - vertex u of {u, v} edge
    #        v::INT - vertex v of {u, v} edge
    def remove_edge(self, u, v):
        if u == v or not (self.graph.has_edge(u, v)):
            raise ValueError("No edge is found for removal.")

        self.graph.remove_edge(u, v)
        self.adj_matrix[u + self.num_warehouses - 1][v + self.num_warehouses - 1] = 0
        self.adj_matrix[v + self.num_warehouses - 1][u + self.num_warehouses - 1] = 0

    ####################################
    # GENERATE_AND_WRITE_EDGES_TO_FILE()
    ####################################
    # Generating new graph edges and writing them to file
    # Each line contains edge in the form of [u, v, weight],
    # Where u::Int, v::Int, weight::Float.random(), and u < v
    # Input: min_weight::Float - minimum edge weight (default: 1.0)
    #        max_weight::Float - maximum edge weight (default: 10.0)
    def generate_and_write_edges_to_file(self, min_weight=1.0, max_weight=10.0):
        with open(self.filename_edges, 'w') as file:
            for u in range(self.num_vertices):
                for v in range(u + 1, self.num_vertices):
                    file.write(f"{u - self.num_warehouses + 1}, "
                               f"{v - self.num_warehouses + 1}, "
                               f"{round(random.uniform(min_weight, max_weight), 2)}\n")

    #######################################
    # GENERATE_AND_WRITE_VERTICES_TO_FILE()
    #######################################
    # Generating new graph vertices and writing them to file
    # Each line contains vertex in the form of [c, s]
    # Where c::Int (max. capacity), s::Int (items stored)
    # Input: min_vert::Int - minimum vertex weight (default: 0)
    #        max_vert::Int - maximum vertex weight (default: 10)
    def generate_and_write_vertices_to_file(self, min_vert=0, max_vert=10):
        with open(self.filename_vertices, 'w') as file:
            for _ in range(self.num_vertices - self.num_warehouses):
                file.write(f"{random.randint(min_vert, max_vert)}, {random.randint(min_vert, max_vert)}\n")

    ########################
    # READ_EDGES_FROM_FILE()
    ########################
    # Reading graph edges from file
    # Each line contains edge and its weight in the form of [u, v, weight]
    # Where u::Int, v::Int, weight::Float
    def read_edges_from_file(self):
        with open(self.filename_edges, 'r') as file:
            for line in file:
                u, v, weight = map(float, line.strip().split(','))
                self.add_edge(int(u), int(v), weight)

    ###########################
    # READ_VERTICES_FROM_FILE()
    ###########################
    # Reading graph vertices from file
    # Each line contains vertex in the form of [capacity, stored]
    # Where capacity::Int (max. capacity), stored::Int (items stored)
    def read_vertices_from_file(self):
        with open(self.filename_vertices, 'r') as file:
            for idx, line in enumerate(file):
                capacity, stored = map(int, line.strip().split(','))
                self.list_client_vertices[idx].capacity = capacity
                self.list_client_vertices[idx].stored = stored

    ##############
    # GET_WEIGHT()
    ##############
    # Getting edge weight
    # Input:  u::INT                  - vertex 'u' of {u, v} edge
    #         v::INT                  - vertex 'v' of {u, v} edge
    # Output: adj_matrix[u][v]::FLOAT - weight of {u, v} edge
    def get_weight(self, u, v):
        if self.adj_matrix[u + self.num_warehouses - 1][v + self.num_warehouses - 1] == 0:
            raise ValueError("No edge found to get weight.")

        return self.adj_matrix[u + self.num_warehouses - 1][v + self.num_warehouses - 1]

    ############################
    # GET_VERTICES_PERMUTATION()
    ############################
    # Generating random permutation of client vertices
    # Output: permutation::[INT] - list of client vertices (vertices > 0)
    def get_vertices_permutation(self):
        permutation = list(range(1, self.num_vertices - self.num_warehouses + 1))
        random.shuffle(permutation)
        return permutation

    ##############
    # GET_VERTEX()
    ##############
    # Getting vertex parameters by given index
    # Input: vertex_idx::INT        - vertex index
    # Output: vertex::class::Vertex - vertex with its max. capacity and stored items
    def get_vertex(self, vertex_idx):
        return self.list_client_vertices[vertex_idx - 1]

    def get_client_vertices_len(self):
        return len(self.list_client_vertices)

    #########################
    # GET_CLOSEST_WAREHOUSE()
    #########################
    # Getting closest warehouse
    # Input: vertex::Int                                - vertex index
    # Output: closest_warehouse::class::WarehouseVertex - closest warehouse
    def get_closest_warehouse(self, vertex):
        closest_warehouse = None
        warehouse_weight = float('inf')

        for warehouse in self.list_warehouse_vertices:
            weight = self.get_weight(warehouse.index, vertex)
            if weight < warehouse_weight:
                closest_warehouse = warehouse
                warehouse_weight = weight
        return closest_warehouse

    ###########################
    # CHECK_GRAPH_CORRECTNESS()
    ###########################
    # Checking if the graph is complete (no edge with weight 0)
    # And if all edges have positive weights
    def check_graph_correctness(self):
        for u, v in self.graph.edges():
            if self.adj_matrix[u][v] == 0:
                raise ValueError("Graph not complete (edge with weight 0).")

            if self.adj_matrix[u][v] < 0:
                raise ValueError("Edge with non-positive weight.")

    ####################
    # PRINT_ADJ_MATRIX()
    ####################
    # Displaying adjacency matrix
    def print_adj_matrix(self):
        print("\nAdjacency matrix:")

        print("     ", end="")
        for vert in range(-self.num_warehouses + 1, self.num_vertices - self.num_warehouses + 1):
            print(f"{vert:5}", end=" ")
        print()

        for idx, row in enumerate(self.adj_matrix):
            print(f"{idx - self.num_warehouses + 1:5}  {' '.join(f'{val:5}' for val in row)}")
        print("\n")

    def print_client_vertices_params(self):
        print("VERTEX:   ", end="")
        for vertex in self.list_client_vertices:
            print(f"{vertex.index: 3}", end="")
        print()

        print("DEMAND:   ", end="")
        for vertex in self.list_client_vertices:
            print(f"{vertex.get_vertex_demand(): 3}", end="")
        print()

        print("CAPACITY: ", end="")
        for vertex in self.list_client_vertices:
            print(f"{vertex.capacity: 3}", end="")
        print()

        print("STORED:   ", end="")
        for vertex in self.list_client_vertices:
            print(f"{vertex.stored: 3}", end="")
        print()

    def print_warehouse_vertices_params(self):
        for vertex in self.list_warehouse_vertices:
            print(f"---VERTEX [{vertex.index: 3}]---")
            print(*vertex.list_vehicles, sep="\n")
            print()

    ###############
    # PRINT_GRAPH()
    ###############
    # Displaying graph as plot
    def print_graph(self):
        warehouses = [warehouse.index for warehouse in self.list_warehouse_vertices]

        pos = nx.spring_layout(self.graph, seed=42)
        nx.draw(self.graph, pos, with_labels=True)
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        nx.draw_networkx_nodes(self.graph, pos, nodelist=warehouses, node_color='r')
        plt.show()

    def print_graph_and_routes(self, descent_instance):
        routes = descent_instance[2]
        warehouses = [warehouse.index for warehouse in self.list_warehouse_vertices]

        pos = nx.spring_layout(self.graph, seed=42)
        nx.draw(self.graph, pos, with_labels=True, node_color='b')
        colors = ['g', 'b', 'c', 'm', 'y', 'k']  # Add more colors if needed

        for idx, route in enumerate(routes, start=1):
            edges = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
            color = colors[(idx - 1) % len(colors)]  # Use modulo to cycle through the list of colors
            nx.draw_networkx_edges(self.graph, pos, edgelist=edges, edge_color=color, width=3.0, label=f'Route {idx}')

        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        nx.draw_networkx_nodes(self.graph, pos, nodelist=warehouses, node_color='r', node_size=300)

        plt.legend(fontsize=15)
        plt.show()

        ''' max_cap = [8, 8]
                3  1  2  4 
       d        1  2 -1  8
        '''