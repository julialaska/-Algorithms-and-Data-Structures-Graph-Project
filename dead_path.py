from enum import Enum
from typing import Optional, Callable
from typing import Dict, List, Any
import graphviz
from graphviz import Digraph
from queue import Queue
from stack import Stack


class EdgeType(Enum):
    directed = 1
    undirected = 2


class Vertex:
    data: Any
    index: int

    def __init__(self, data1, index1=None):
        self.data = data1
        self.index = index1

    def __repr__(self):
        # return str(self.index) + ': ' + str(self.data)
        return str(self.data)


class Edge:
    source: Vertex
    destination: Vertex
    weight: Optional[float]

    def __init__(self, source, destination, weight=None):
        self.source = source
        self.destination = destination
        self.weight = weight

    def __repr__(self):
        return str(self.destination.index) + ': ' + str(self.destination.data)
        # return str(self.destination.index) + ': ' + str(self.destination.data) + ' ' + str(self.weight)
        # return str(self.destination.data)


class Graph:
    adjacencies: Dict[Vertex, List[Edge]]

    def __init__(self):
        self.adjacencies = {}

    def create_vertex(self, data: Any) -> Vertex:
        newVertex = Vertex(data, len(self.adjacencies))
        self.adjacencies[newVertex] = []
        return newVertex

    def add_directed_edge(self, source: Vertex, destination: Vertex, weight: Optional[float] = None) -> None:
        if source not in self.adjacencies:
            self.create_vertex(source.data)
        if destination not in self.adjacencies:
            self.create_vertex(destination.data)
        self.adjacencies[source].append(Edge(source, destination, weight))

    def add_undirected_edge(self, source: Vertex, destination: Vertex, weight: Optional[float] = None) -> None:
        if source not in self.adjacencies:
            self.create_vertex(source.data)
        if destination not in self.adjacencies:
            self.create_vertex(destination.data)
        self.adjacencies[source].append(Edge(source, destination, weight))
        self.adjacencies[destination].append(Edge(destination, source, weight))

    def add(self, edge: EdgeType, source: Vertex, destination: Vertex, weight: Optional[float] = None):
        if edge.value == 1:
            self.add_directed_edge(source, destination, weight)
        else:
            self.add_undirected_edge(source, destination, weight)

    def traverse_breadth_first(self, vertex: Vertex, visit: Callable[[Any], None]):
        visited = []
        queue = Queue()
        visited.append(vertex)
        queue.enqueue(vertex)
        while queue:
            v = queue.dequeue()
            visit(v)
            for neighbour in self.adjacencies:
                if neighbour not in visited:
                    visited.append(neighbour)
                    queue.enqueue(neighbour)
        return visited

    def traverse_depth_first(self, vertex: Vertex, visited: List[Vertex], visit: Callable[[Any], None]):
        visit(vertex)
        visited.append(vertex)
        for x in self.adjacencies[vertex]:
            if x.destination not in visited:
                self.traverse_depth_first(x.destination, visited, visit)

    def show(self):
        graph = Digraph()
        visited = []
        for vertex in self.adjacencies.keys():
            if vertex not in visited:
                graph.node(str(vertex.index), str(vertex.data))
                visited.append(vertex)
                for neighbour in self.adjacencies[vertex]:
                    graph.edge(str(neighbour.source.index), str(neighbour.destination.index))
                    # label=str(neighbour.weight))
        graph.view()

    def __repr__(self):
        tmp = ''
        for vertex, neighbour in self.adjacencies.items():
            tmp += str(vertex.data) + "  ---->  " + str(neighbour) + '\n'
            # tmp += str(vertex.index) + ": " + str(vertex.data) + "  ---->  " + str(neighbour) + '\n'
        return tmp


def dead_path(g: Graph, cross_id: Any):
    visit = []
    for vertex, adj in g.adjacencies.items():
        for neighbour in adj:
            if neighbour.destination == cross_id:
                visit.append(vertex)

    for i in visit:
        vertexes = list(g.adjacencies.keys())
        parents = {}
        vertexes.append(cross_id)
        parents[cross_id] = None
        path = Stack()

        while vertexes:
            v = vertexes.pop()

            for x in g.adjacencies[v]:
                if x.source != i:
                    parents[x.destination] = x.source
        print(parents)

        current_node = i
        path.push(cross_id)
        while parents[current_node]:
            path.push(current_node)
            current_node = parents[current_node]
        path.push(current_node)

        if len(path) != 0:
            return path
        return None


graph = Graph()
v0 = graph.create_vertex("v0")
v1 = graph.create_vertex("v1")
v2 = graph.create_vertex("v2")
v3 = graph.create_vertex("v3")
v4 = graph.create_vertex("v4")
v5 = graph.create_vertex("v5")

graph.add(EdgeType(1), v0, v1, 1)
graph.add(EdgeType(1), v0, v5, 5)
graph.add(EdgeType(1), v2, v1, 4)
graph.add(EdgeType(1), v2, v3, 3)
graph.add(EdgeType(1), v3, v4, 2)
graph.add(EdgeType(1), v4, v1, 6)
graph.add(EdgeType(1), v4, v5, 3)
graph.add(EdgeType(1), v5, v1, 3)
graph.add(EdgeType(1), v5, v2, 1)

# graph.traverse_breadth_first(v0, print)
# graph.traverse_depth_first(v0,[], print)

# print(graph)
# graph.show()

g = Graph()

a = g.create_vertex("A")
b = g.create_vertex("B")
c = g.create_vertex("C")
d = g.create_vertex("D")

g.add(EdgeType(1), a, b)
g.add(EdgeType(1), b, c)
g.add(EdgeType(1), c, d)
g.add(EdgeType(1), d, b)
g.add(EdgeType(1), c, a)

# g.show()
# print(g)
print(dead_path(g, c))

g1 = Graph()

a = g1.create_vertex("A")
b = g1.create_vertex("B")
c = g1.create_vertex("C")
d = g1.create_vertex("D")
e = g1.create_vertex("E")

g1.add(EdgeType(1), a, b)
g1.add(EdgeType(1), b, c)
g1.add(EdgeType(1), c, d)
g1.add(EdgeType(1), c, e)
g1.add(EdgeType(1), d, e)
g1.add(EdgeType(1), e, a)

# g1.show()

print(dead_path(g1, a))

g2 = Graph()

a = g2.create_vertex("A")
b = g2.create_vertex("B")
c = g2.create_vertex("C")
d = g2.create_vertex("D")
e = g2.create_vertex("E")

g2.add(EdgeType(1), b, c)
g2.add(EdgeType(1), d, c)
g2.add(EdgeType(1), a, c)
g2.add(EdgeType(1), e, c)
g2.add(EdgeType(1), b, e)
g2.add(EdgeType(1), e, a)

# g2.show()

print(dead_path(g2, b))
