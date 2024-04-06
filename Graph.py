import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random


class Graph:

    # Graph class constructor
    # Input: num_vertices::[INT] - number of vertices
    def __init__(self, num_vertices):
        if num_vertices < 2:
            raise ValueError("Graph must have at least two vertices")
        self.num_vertices = num_vertices
        self.graph = nx.complete_graph(num_vertices)
        self.adj_matrix = np.zeros((num_vertices, num_vertices))

    # Adding edges to graph and adjacency matrix
    # Input: u::[INT]        - vertex 'u' of {u, v} edge
    #        v::[INT]        - vertex 'v' of {u, v} edge
    #        weight::[FLOAT] - weight of {u, v} edge
    def add_edge(self, u, v, weight):
        if u == v:
            raise ValueError("Self-loop edge")
        else:
            if self.adj_matrix[u][v] != 0:
                raise ValueError("Edge already exists")
        self.graph.add_edge(u, v, weight=weight)
        self.adj_matrix[u][v] = weight
        self.adj_matrix[v][u] = weight

    # Removing edges from graph and adjacency matrix
    # Edge does not exist if adj_matrix is 0 on [u][v] and [v][u]
    # Input: u::[INT]        - vertex 'u' of {u, v} edge
    #        v::[INT]        - vertex 'v' of {u, v} edge
    def remove_edge(self, u, v):
        if u == v or not (self.graph.has_edge(u, v)):
            raise ValueError("No edge found")
        self.graph.remove_edge(u, v)
        self.adj_matrix[u][v] = 0
        self.adj_matrix[v][u] = 0

    # Generating new graph edges and writing them to file
    # Each line contains edge in the form of [u, v, weight],
    # Where u::[Int], v::[Int], weight::[Float].random(), and u < v
    # Input: num_edges::[Int]   - number of edges to be generated
    #        filename::[String] - file name for writing (default: 'graph-edges.txt')
    #        min_weight[Float]  - minimum edge weight (default: 1.0)
    #        max_weight[Float]  - maximum edge weight (default: 10.0)
    @staticmethod
    def generate_and_write_edges_to_file(num_edges, filename="graph-edges.txt", min_weight=1.0, max_weight=10.0):
        with open(filename, 'w') as file:
            for u in range(num_edges):
                for v in range(u + 1, num_edges):
                    file.write(f"{u}, {v}, {round(random.uniform(min_weight, max_weight), 2)}\n")

    # Reading graph edges from file
    # Each line contains edge in the form of [u, v, weight]
    # Where u::[Int], v::[Int], weight::[Float]
    # Input: filename::[String] - file name for reading (default: 'graph-edges.txt')
    def read_edges_from_file(self, filename="graph-edges.txt"):
        # Assert that no more lines are read than are present in file
        if sum(1 for line in open(filename)) < self.num_vertices * (self.num_vertices - 1) / 2:
            raise ValueError("Trying to read non-existent records")

        with open(filename, 'r') as file:
            for line in file:
                u, v, weight = map(float, line.strip().split(','))
                if int(u) >= self.num_vertices or int(v) >= self.num_vertices:
                    continue
                self.add_edge(int(u), int(v), weight)

    # Getting edge weight
    # Input:  u::[INT]         - vertex 'u' of {u, v} edge
    #         v::[INT]         - vertex 'v' of {u, v} edge
    # Output: adj_matrix[u][v] - weight of {u, v} edge
    def get_weight(self, u, v):
        if self.adj_matrix[u][v] == 0:
            raise ValueError("No edge found")
        return self.adj_matrix[u][v]

    # Checking if the graph is complete (no edge with weight 0)
    # And if all edges have positive weights
    def check_graph_correctness(self):
        for u, v in self.graph.edges():
            if self.graph[u][v]['weight'] == 0:
                raise ValueError("Graph not complete (edge with weight 0)")
            if self.graph[u][v]['weight'] < 0:
                raise ValueError("Edge with non-positive weight")

    # Displaying adjacency matrix
    def print_adj_matrix(self):
        print("Adjacency matrix:")
        for row in self.adj_matrix:
            print(" ".join(f"{val:5}" for val in row))

    # Displaying graph as plot
    def print_graph(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True)
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        plt.show()

    # Sample complete graph
    @staticmethod
    def get_sample():
        graph = Graph(4)

        graph.add_edge(0, 1, 1)
        graph.add_edge(0, 2, 10)
        graph.add_edge(0, 3, 4)
        graph.add_edge(1, 2, 7)
        graph.add_edge(1, 3, 4)
        graph.add_edge(2, 3, 8)

        return graph
