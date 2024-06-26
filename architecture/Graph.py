from architecture.WarehouseVertex import WarehouseVertex
from architecture.ClientVertex import ClientVertex
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random


class Graph:

    # Graph class constructor
    def __init__(self,
                 num_vertices,
                 num_warehouses,
                 vehicles_and_capacities,
                 discharged_percent=30,
                 generate_new_edges=False,
                 edges_range=(1.0, 10.0),
                 filename_edges="data/graph-edges.txt",
                 generate_new_vertices=False,
                 vertices_range=(0, 10),
                 filename_vertices="data/graph-vertices.txt",
                 real_data=False):

        if num_vertices < 2:
            raise ValueError("Graph must have at least two vertices.")

        if num_warehouses < 1:
            raise ValueError("Graph must have at least one warehouse.")

        if num_warehouses > num_vertices - 1:
            raise ValueError("At least one client vertex is required.")

        self.num_vertices = num_vertices
        self.num_warehouses = num_warehouses
        self.discharged_percent = discharged_percent
        self.real_data = real_data

        self.edges_range = edges_range
        self.vertices_range = vertices_range

        self.filename_edges = filename_edges
        self.filename_vertices = filename_vertices

        self.list_client_vertices = [ClientVertex(i, 0, 0, 0)
                                     for i in range(1, self.num_vertices - self.num_warehouses + 1)]
        self.list_warehouse_vertices = [WarehouseVertex(i, vehicles_and_capacities)
                                        for i in range(-self.num_warehouses + 1, 1)]

        if generate_new_edges and not self.real_data:
            self.generate_and_write_edges_to_file(
                min_weight=self.edges_range[0],
                max_weight=self.edges_range[1]
            )

        if generate_new_vertices and not self.real_data:
            self.generate_and_write_vertices_to_file(
                min_vert=self.vertices_range[0],
                max_vert=self.vertices_range[1]
            )

        if not self.real_data and self.check_if_can_read():
            raise ValueError("Incorrect parameters. Generate new valid graph or provide valid parameters.")

        self.graph = nx.complete_graph(self.num_vertices - self.num_warehouses + 1)
        self.adj_matrix = np.zeros((self.num_vertices, self.num_vertices))

        self.read_edges_from_file()
        self.read_vertices_from_file()

    # File readability conditions check:
    # 1. Checking if edge parameters match number of vertices, edges = (vertices * vertices - 1) / 2
    # 2. Checking if edges generated for proper number of warehouses
    # 3. Checking if vertices parameters match number of vertices
    def check_if_can_read(self):
        return (sum(1 for _ in open(self.filename_edges, 'r')) != self.num_vertices * (self.num_vertices - 1) / 2) \
            or (int(open(self.filename_edges, 'r').readline().split(',')[0]) != -self.num_warehouses + 1) \
            or (sum(1 for _ in open(self.filename_vertices, 'r')) != self.num_vertices - self.num_warehouses)

    # Adding edge to graph and adjacency matrix
    def add_edge(self, u, v, weight):
        if u == v:
            raise ValueError("Attempting to add self-loop edge.")
        else:
            if not self.real_data and self.adj_matrix[u + self.num_warehouses - 1][v + self.num_warehouses - 1] != 0:
                raise ValueError("Attempting to add the existing edge.")

        self.graph.add_edge(u, v, weight=weight)
        self.adj_matrix[u + self.num_warehouses - 1][v + self.num_warehouses - 1] = weight
        if not self.real_data:
            self.adj_matrix[v + self.num_warehouses - 1][u + self.num_warehouses - 1] = weight

    # Removing edge from graph and adjacency matrix
    def remove_edge(self, u, v):
        if u == v or not (self.graph.has_edge(u, v)):
            raise ValueError("No edge is found for removal.")

        self.graph.remove_edge(u, v)
        self.adj_matrix[u + self.num_warehouses - 1][v + self.num_warehouses - 1] = 0
        self.adj_matrix[v + self.num_warehouses - 1][u + self.num_warehouses - 1] = 0

    # Generating new edges parameters and writing them into a file
    def generate_and_write_edges_to_file(self, min_weight=1.0, max_weight=10.0):
        with open(self.filename_edges, 'w') as file:
            for u in range(self.num_vertices):
                for v in range(u + 1, self.num_vertices):
                    file.write(f"{u - self.num_warehouses + 1}, "
                               f"{v - self.num_warehouses + 1}, "
                               f"{round(random.uniform(min_weight, max_weight), 2)}\n")

    # Generating new vertices params and writing them into a file
    def generate_and_write_vertices_to_file(self, min_vert=0, max_vert=10):
        with open(self.filename_vertices, 'w') as file:
            for _ in range(self.num_vertices - self.num_warehouses):
                capacity = random.randint(2, max_vert)
                stored = random.randint(min_vert, max_vert)
                while stored == capacity:
                    stored = random.randint(min_vert, max_vert)

                if random.randint(1, 100) <= self.discharged_percent:
                    discharged = random.randint(0, stored)
                else:
                    discharged = 0

                file.write(f"{discharged}, {capacity}, {stored}\n")

    # Reading edges from file
    def read_edges_from_file(self):
        with open(self.filename_edges, 'r') as file:
            for line in file:
                u, v, weight = map(float, line.strip().split(','))
                self.add_edge(int(u), int(v), weight)

    # Reading vertices from file
    def read_vertices_from_file(self):
        with open(self.filename_vertices, 'r') as file:
            for idx, line in enumerate(file):
                discharged, capacity, stored = map(int, line.strip().split(','))
                self.list_client_vertices[idx].discharged = discharged
                self.list_client_vertices[idx].capacity = capacity
                self.list_client_vertices[idx].stored = stored

    # Getting edge weight
    def get_weight(self, u, v):
        if self.adj_matrix[u + self.num_warehouses - 1][v + self.num_warehouses - 1] == 0:
            raise ValueError("No edge found to get weight.")

        return self.adj_matrix[u + self.num_warehouses - 1][v + self.num_warehouses - 1]

    # Creating vertices random permutation
    def get_vertices_permutation(self):
        permutation = list(range(1, self.num_vertices - self.num_warehouses + 1))
        random.shuffle(permutation)
        return permutation

    # Getting vertex object by given index
    def get_vertex(self, vertex_idx):
        return self.list_client_vertices[vertex_idx - 1]

    def get_client_vertices_len(self):
        return len(self.list_client_vertices)

    # Getting the closest warehouse to given vertex
    def get_closest_warehouse(self, vertex):
        closest_warehouse = None
        warehouse_weight = float('inf')

        for warehouse in self.list_warehouse_vertices:
            weight = self.get_weight(warehouse.index, vertex)
            if weight < warehouse_weight:
                closest_warehouse = warehouse
                warehouse_weight = weight
        return closest_warehouse

    # Graph validation
    def check_graph_correctness(self):
        for u, v in self.graph.edges():
            if self.adj_matrix[u][v] == 0:
                raise ValueError("Graph not complete (edge with weight 0).")

            if self.adj_matrix[u][v] < 0:
                raise ValueError("Edge with non-positive weight.")

    # Displaying adjacency matrix
    def print_adj_matrix(self):
        print("\nAdjacency matrix:")

        print("     ", end="")
        for vert in range(-self.num_warehouses + 1, self.num_vertices - self.num_warehouses + 1):
            print(f"{vert:7}", end=" ")
        print()

        for idx, row in enumerate(self.adj_matrix):
            print(f"{idx - self.num_warehouses + 1:7}  {' '.join(f'{val:7}' for val in row)}")
        print("\n")

    # Displaying client vertices params
    def print_client_vertices_params(self):
        print("VERTEX:       ", end="")
        for vertex in self.list_client_vertices:
            print(f"{vertex.index: 3}", end="")
        print()

        print("DISCHARGED:   ", end="")
        for vertex in self.list_client_vertices:
            print(f"{vertex.discharged: 3}", end="")
        print()

        print("DEMAND:       ", end="")
        for vertex in self.list_client_vertices:
            print(f"{vertex.get_vertex_demand(): 3}", end="")
        print()

        print("CAPACITY:     ", end="")
        for vertex in self.list_client_vertices:
            print(f"{vertex.capacity: 3}", end="")
        print()

        print("STORED:       ", end="")
        for vertex in self.list_client_vertices:
            print(f"{vertex.stored: 3}", end="")
        print()

    # Displaying warehouse vertices params
    def print_warehouse_vertices_params(self):
        for vertex in self.list_warehouse_vertices:
            print(f"---VERTEX [{vertex.index: 3}]---")
            print(*vertex.list_vehicles, sep="\n")
            print()

    # Displaying graph as plot
    def print_graph(self):
        warehouses = [warehouse.index for warehouse in self.list_warehouse_vertices]

        pos = nx.spring_layout(self.graph, seed=42)
        nx.draw(self.graph, pos, with_labels=True)
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        nx.draw_networkx_nodes(self.graph, pos, nodelist=warehouses, node_color='r')
        plt.show()

    # Displaying graph as a plot and determined paths
    def print_graph_and_routes(self, alg_instance):
        routes = alg_instance[2]
        warehouses = [warehouse.index for warehouse in self.list_warehouse_vertices]

        pos = nx.spring_layout(self.graph, seed=42)
        nx.draw(self.graph, pos, with_labels=True, node_color='black', edge_color='gray', font_color='w')
        colors = ['g', 'b', 'c', 'm', 'y', 'k']  # Add more colors if needed

        for idx, route in enumerate(routes, start=1):
            edges = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
            color = colors[(idx - 1) % len(colors)]
            nx.draw_networkx_edges(self.graph, pos, edgelist=edges, edge_color=color, width=4.0, label=f'Route {idx}')

        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels, font_color='black', font_size=8)
        nx.draw_networkx_nodes(self.graph, pos, nodelist=warehouses, node_color='r', node_size=300)

        plt.legend(fontsize=15)
        plt.show()
