import sys
import math


class NodeData:
    def __init_(self):
        self.my_units = 0
        self.my_tolerance = 0
        self.other_units = 0
        self.other_tolerance = 0
        self.can_assign = 0

    def __repr___(self):
        return self.__str__()

    def __str__(self):
        return str(self.__dict__)



class Graph(object):
    def __init__(self, vertex_count):
        self.vertex_count = vertex_count
        self.adj = {}
        self.node_data = []
        for i in xrange(0, self.vertex_count):
            self.adj[i] = []
            self.node_data.append(NodeData())



    def add_edge(self, u, w):
        self.adj[u].append(w)
        self.adj[w].append(u)


    def set_node_data(self, node, my_units, my_tolerance, other_units, other_tolerance, can_assign):
        self.node_data[node].my_units = my_units
        self.node_data[node].my_tolerance = my_tolerance
        self.node_data[node].other_units = other_units
        self.node_data[node].other_tolerance = other_tolerance
        self.node_data[node].can_assign = can_assign

    def get_node_data(self, v):
        return self.node_data[v]



    def near(self, v):
        return self.adj[v]

    def __str__(self):
        as_text = str(self.adj) + "/n"
        for data in self.node_data:
            as_text += "mu {0} mt{1} ou{2} ot{3} ca{4} |".format(data.my_units, data.my_tolerance, data.other_units, data.other_tolerance, data.can_assign)
        return as_text


class General:
    def attack(self, graph):
        targets = []
        for i in xrange(0, graph.vertex_count):
            for near in graph.near(i):
                near_data = graph.get_node_data(near)
                if near_data.my_units <= near_data.other_units and near_data.can_assign:
                    targets.append(near)
        return targets

    def pad_targets(self, targets):
        selected = len(targets)
        if selected < 5:
            for i in xrange(selected, 5):
                targets.append(0)

        return targets




# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.



planet_count, edge_count = [int(i) for i in raw_input().split()]
graph = Graph(planet_count)
cadorna = General()

for i in xrange(edge_count):
    planet_a, planet_b = [int(j) for j in raw_input().split()]
    graph.add_edge(planet_a, planet_b)

# game loop
while True:
    for i in xrange(planet_count):
        my_units, my_tolerance, other_units, other_tolerance, can_assign = [int(j) for j in raw_input().split()]
        graph.set_node_data(i, my_units, my_tolerance, other_units, other_tolerance, can_assign)

    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."

    targets = cadorna.pad_targets(cadorna.attack(graph))

    for target in targets[0:5]:
        print str(target)
    print "NONE"




