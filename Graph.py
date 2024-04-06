import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random


class Graph:

    # Graph class constructor
    # Input: num_vertices::[INT]       - number of vertices
    #        num_warehouses::[INT]     - number of warehouses
    #        generate_new_data::[BOOL] - flag, if generate new data
    #        filename::[STRING]        - file name for writing/reading data (default='graph-edges.txt')
    def __init__(self, num_vertices, num_warehouses, generate_new_data=False, filename="graph-edges.txt"):
        if num_vertices < 2:
            raise ValueError("Graph must have at least two vertices.")

        if num_warehouses < 1:
            raise ValueError("Graph must have at least one warehouse.")

        if num_warehouses > num_vertices - 1:
            raise ValueError("At least one client vertex is required.")

        self.num_vertices = num_vertices
        self.num_warehouses = num_warehouses
        self.filename = filename

        if generate_new_data:
            self.generate_and_write_edges_to_file(
                min_weight=1.0,
                max_weight=10.0
            )

        if self.check_if_can_read():
            raise ValueError("Incorrect parameters.Generate new valid graph or provide valid parameters.")

        self.graph = nx.complete_graph(self.num_vertices - self.num_warehouses + 1)
        self.adj_matrix = np.zeros((self.num_vertices, self.num_vertices))

        self.read_edges_from_file()

    # Checking if parameters match number of vertices and warehouses provided in file
    def check_if_can_read(self):
        return (sum(1 for line in open(self.filename, 'r')) != self.num_vertices * (self.num_vertices - 1) / 2) \
            or (int(open(self.filename, 'r').readline().split(',')[0]) != -self.num_warehouses + 1)

    # Adding edges to graph and adjacency matrix
    # Input: u::[INT]        - vertex u of {u, v} edge
    #        v::[INT]        - vertex v of {u, v} edge
    #        weight::[FLOAT] - weight of {u, v} edge
    def add_edge(self, u, v, weight):
        if u == v:
            raise ValueError("Self-loop edge.")
        else:
            if self.adj_matrix[u + self.num_warehouses - 1][v + self.num_warehouses - 1] != 0:
                raise ValueError("Attempting to add the same edge.")

        self.graph.add_edge(u, v, weight=weight)
        self.adj_matrix[u + self.num_warehouses - 1][v + self.num_warehouses - 1] = weight
        self.adj_matrix[v + self.num_warehouses - 1][u + self.num_warehouses - 1] = weight

    # Removing edges from graph and adjacency matrix
    # Edge does not exist if adj_matrix is 0 on [u][v] and [v][u]
    # Input: u::[INT]        - vertex u of {u, v} edge
    #        v::[INT]        - vertex v of {u, v} edge
    def remove_edge(self, u, v):
        if u == v or not (self.graph.has_edge(u, v)):
            raise ValueError("No edge is found for removal.")

        self.graph.remove_edge(u, v)
        self.adj_matrix[u][v] = 0
        self.adj_matrix[v][u] = 0

    # Generating new graph edges and writing them to file
    # Each line contains edge in the form of [u, v, weight],
    # Where u::[Int], v::[Int], weight::[Float].random(), and u < v
    # Input: min_weight[Float]  - minimum edge weight (default: 1.0)
    #        max_weight[Float]  - maximum edge weight (default: 10.0)
    def generate_and_write_edges_to_file(self, min_weight=1.0, max_weight=10.0):
        with open(self.filename, 'w') as file:
            for u in range(self.num_vertices):
                for v in range(u + 1, self.num_vertices):
                    file.write(f"{u - self.num_warehouses + 1}, "
                               f"{v - self.num_warehouses + 1}, "
                               f"{round(random.uniform(min_weight, max_weight), 2)}\n")

    # Reading graph edges from file
    # Each line contains edge in the form of [u, v, weight]
    # Where u::[Int], v::[Int], weight::[Float]
    def read_edges_from_file(self):
        with open(self.filename, 'r') as file:
            for line in file:
                u, v, weight = map(float, line.strip().split(','))
                self.add_edge(int(u), int(v), weight)

    # Getting edge weight
    # Input:  u::[INT]         - vertex 'u' of {u, v} edge
    #         v::[INT]         - vertex 'v' of {u, v} edge
    # Output: adj_matrix[u][v] - weight of {u, v} edge
    def get_weight(self, u, v):
        if self.adj_matrix[u + self.num_warehouses - 1][v + self.num_warehouses - 1] == 0:
            raise ValueError("No edge found to get weight.")

        return self.adj_matrix[u + self.num_warehouses - 1][v + self.num_warehouses - 1]

    # Checking if the graph is complete (no edge with weight 0)
    # And if all edges have positive weights
    def check_graph_correctness(self):
        for u, v in self.graph.edges():
            if self.adj_matrix[u][v] == 0:
                print(u, v)
                raise ValueError("Graph not complete (edge with weight 0).")

            if self.adj_matrix[u][v] < 0:
                print(u, v)
                raise ValueError("Edge with non-positive weight.")

    # Displaying adjacency matrix
    def print_adj_matrix(self):
        print("Adjacency matrix:")

        print("     ", end="")
        for vert in range(-self.num_warehouses + 1, self.num_vertices - self.num_warehouses + 1):
            print(f"{vert:5}", end=" ")
        print()

        for idx, row in enumerate(self.adj_matrix):
            print(f"{idx - self.num_warehouses + 1:5}  {' '.join(f'{val:5}' for val in row)}")

    # Displaying graph as plot
    def print_graph(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True)
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        plt.show()
