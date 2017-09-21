import sys
import math
import random


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
        self.spreadables  = []
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


    def compute_spreadable(self):
        for i in xrange(0, self.vertex_count):
            print >> sys.stderr, "i " + str(i) + " l " +str(len(self.near(i)))
            if len(self.near(i)) >= 5:
                self.spreadables.append(i)
                print >> sys.stderr, "i spreadable"


    def near(self, v):
        return self.adj[v]

    def __str__(self):
        as_text = str(self.adj) + "/n"
        for data in self.node_data:
            as_text += "mu {0} mt{1} ou{2} ot{3} ca{4} |".format(data.my_units, data.my_tolerance, data.other_units, data.other_tolerance, data.can_assign)
        return as_text


class General:
    def __init__(self, graph):
        self.graph = graph
        self.turn_count = 0

        self.forced_spread = None


    def attack(self):
        targets = []
        self.turn_count += 1

        if self.turn_count == 1:
            start = self.starting_node()

            if len(self.graph.near(start)) >= 5:
                self.forced_spread = start
                targets.append(start)
            else:
                most_connected_near = -1
                most_connected_grade = 0
                for near in self.graph.near(start):
                    if most_connected_grade < len(self.graph.near(near)):
                        most_connected_near = near
                        most_connected_grade = len(self.graph.near(near))

                if self.graph.get_node_data(most_connected_near).can_assign and most_connected_grade > 3:
                    targets.append(near)
                    targets.append(near)
                    targets.append(near)
                    targets.append(near)
                    targets.append(near)
                    self.forced_spread = near



        for i in xrange(0, self.graph.vertex_count):
            for near in self.graph.near(i):
                near_data = self.graph.get_node_data(near)
                #if near_data.my_units <= near_data.other_units and near_data.can_assign:
                relative_strength = near_data.my_units - near_data.other_units
                assignable = near_data.can_assign
                if near_data.other_tolerance == 0 and assignable:
                    targets.append(near)
                elif relative_strength == 0 and assignable:
                        targets.append(near)
                elif relative_strength > 0:
                    pass
                elif near_data.other_units == 0 and near_data.my_units == 0 and assignable:
                    targets.append(near)
                elif relative_strength < 0 and relative_strength > -5 and assignable:
                    for i in xrange(0, abs(relative_strength - 5)):
                        targets.append(near)

        #sorted(targets, key= lambda id : len(self.graph.near(id)))
        #sorted(targets,  reverse = True, key= lambda id : len(self.graph.near(id)))
        #sorted(targets, key= lambda id : self.graph.get_node_data(i).other_units)
        #sorted(targets, reverse = True, key= lambda id : self.graph.get_node_data(i).other_units)

        return targets

    def starting_node(self):
        for i in xrange(0, self.graph.vertex_count):
            if self.graph.get_node_data(i).my_units == 5:
                return i
        raise Exception ("Funziona solo al primo turno")


    def pad_targets(self, targets):
        while len(targets) < 5:
            random_node = random.randint(0, self.graph.vertex_count - 1)
            if random_node not in targets:
                targets.append(random_node)

        return targets

    def spread(self):
        if self.forced_spread is not None:
            s = self.forced_spread
            self.forced_spread = None
            return str(s)

        if len(self.graph.spreadables) == 0:
            return "NONE"
        return str(self.graph.spreadables[random.randint(0, len(self.graph.spreadables) - 1)])
        #for node in self.graph.spreadables:
        #    if self.graph.get_node_data(i).my_units >= 5:
        #        return str(node)
        # return "NONE"






# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.



planet_count, edge_count = [int(i) for i in raw_input().split()]
graph = Graph(planet_count)
cadorna = General(graph)

random.seed()

for i in xrange(edge_count):
    planet_a, planet_b = [int(j) for j in raw_input().split()]
    graph.add_edge(planet_a, planet_b)

graph.compute_spreadable()
print >> sys.stderr, graph.spreadables

# game loop
while True:
    for i in xrange(planet_count):
        my_units, my_tolerance, other_units, other_tolerance, can_assign = [int(j) for j in raw_input().split()]

        graph.set_node_data(i, my_units, my_tolerance, other_units, other_tolerance, can_assign)

    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."

    targets = cadorna.pad_targets(cadorna.attack())

    for target in targets[0:5]:
        print str(target)
    print cadorna.spread()




