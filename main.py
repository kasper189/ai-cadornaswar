import sys
import random
import operator


class NodeData(object):
    def __init__(self):
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

        self.average_grade = 0

    def add_edge(self, u, w):
        self.adj[u].append(w)
        self.adj[w].append(u)

    def set_node_data(self, node, my_units, my_tolerance,
                      other_units, other_tolerance, can_assign):
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
            if len(self.near(i)) >= 4:
                self.spreadables.append(i)
                print >> sys.stderr, "i spreadable"

    def near(self, v):
        return self.adj[v]

    def __str__(self):
        as_text = str(self.adj) + "/n"
        for data in self.node_data:
            as_text += "mu {0} mt{1} ou{2} ot{3} ca{4} |".format(
                data.my_units, data.my_tolerance, data.other_units, data.other_tolerance, data.can_assign
            )
        return as_text

    def search_reachable_empty(self, start):
        frontier = [start]
        seen = []

        while len(frontier) > 0:
            candidate = frontier.pop()
            candidate_data = self.get_node_data(candidate)

            if candidate_data.my_units == 0 and candidate_data.other_units == 0 and candidate not in seen:
                for i in self.near(candidate):
                    frontier.append(i)

                seen.append(candidate)
        return len(seen)

    def get_average_grade(self):
        if self.average_grade ==0:
            for i in xrange(0, self.vertex_count):
                self.average_grade += len(self.near(i))
        self.average_grade /= self.vertex_count
        return self.average_grade


class General:
    def __init__(self, graph):
        self.graph = graph
        self.turn_count = 0

        self.forced_spread = None

    def safe_attack(self):
        node_power = {}

        for i in xrange(0, self.graph.vertex_count):
            node = self.graph.get_node_data(i)
            value_of_node = 0

            if not node.can_assign:
                value_of_node -= 10000

            value_of_node += 5 - node.other_tolerance

            if node.my_units == 0 and node.other_units == 0:
                value_of_node += 25

            relative_strength = node.my_units - node.other_units
            if relative_strength == 0:
                value_of_node += 15

            value_of_node += len(self.graph.near(i))
            value_of_node += self.graph.search_reachable_empty(i) * self.turn_count * 9
            node_power[i] = value_of_node

        best_attacks_tuples = sorted(node_power.items(), key=operator.itemgetter(1), reverse=True)

        print >> sys.stderr, "after weight " + str(best_attacks_tuples)

        best_attacks = []
        best_attacks_weight = []
        for x in best_attacks_tuples:
            best_attacks.append(x[0])
            best_attacks_weight.append(x[1])

        targets = []

        self.turn_count += 1
        if self.turn_count == 1:
            start = self.starting_node()
            best_weight = -1
            best_weight_node = 0
            for near in self.graph.near(start):
                weight = 0
                neigh_data = self.graph.get_node_data(near)

                if neigh_data.my_units == 0 and neigh_data.other_units == 0:
                    weight += 2
                elif -2 < (neigh_data.my_units - neigh_data.other_units) < 0:
                    weight += 1

                if weight > best_weight:
                    best_weight = weight
                    best_weight_node = near

            if self.graph.get_node_data(best_weight_node).can_assign and len(self.graph.near(best_weight_node)) > 4:
                targets.append(near)
                targets.append(near)
                targets.append(near)
                targets.append(near)
                targets.append(near)
                self.forced_spread = near

        for node_to_attack in best_attacks:
            print >> sys.stderr, "decision for " + str(node_to_attack)
            target_data = self.graph.get_node_data(node_to_attack)
            relative_strength = target_data.my_units - target_data.other_units
            assignable = target_data.can_assign
            if target_data.other_units == 0 and target_data.my_units == 0 and assignable:
                targets.append(node_to_attack)
                print >> sys.stderr, "A"
            elif relative_strength == 0 and assignable:
                targets.append(node_to_attack)
                targets.append(node_to_attack)
                targets.append(node_to_attack)
                targets.append(node_to_attack)
                print >> sys.stderr, "B"
            elif relative_strength > 0:
                print >> sys.stderr, "C"
            elif -5 < relative_strength < 0 and assignable:
                for i in xrange(0, abs(relative_strength - 5)):
                    targets.append(node_to_attack)
                print >> sys.stderr, "D"
            elif target_data.other_tolerance == 0 and assignable:
                targets.append(node_to_attack)
                print >> sys.stderr, "E"

        print >> sys.stderr, "Targets after decision " + str(targets)

        return targets

    def attack(self):
        node_power = {}

        for i in xrange(0, self.graph.vertex_count):
            node = self.graph.get_node_data(i)
            value_of_node = 0

            if not node.can_assign:
                value_of_node -= 10000

            value_of_node += 5 - node.other_tolerance

            if node.my_units == 0 and node.other_units == 0:
                value_of_node += 25

            relative_strength = node.my_units - node.other_units
            if relative_strength == 0:
                value_of_node += 15

            value_of_node += len(self.graph.near(i))
            value_of_node += self.graph.search_reachable_empty(i) * self.turn_count * 9

            near_enemy = 0
            for n in self.graph.near(i):
                near_enemy += self.graph.get_node_data(n).other_units
            value_of_node -= near_enemy * 2

            node_power[i] = value_of_node

        best_attacks_tuples = sorted(node_power.items(), key=operator.itemgetter(1), reverse=True)

        print >> sys.stderr, "after weight " + str(best_attacks_tuples)

        best_attacks = []
        best_attacks_weight = []
        for x in best_attacks_tuples:
            best_attacks.append(x[0])
            best_attacks_weight.append(x[1])

        targets = []

        self.turn_count += 1
        quarter_turn = graph.vertex_count / 2
        if self.turn_count <= quarter_turn and self.graph.get_average_grade() > 3:
            possible_spread_node = best_attacks[0]
            near = self.graph.near(possible_spread_node)
            free_nears = 0
            for n in near:
                near_data = self.graph.get_node_data(n)
                if near_data.other_units == 0 and near_data.my_units == 0:
                    free_nears += 1
            if free_nears >=4:
                spread_data = self.graph.get_node_data(possible_spread_node)
                for i in xrange(0, 5 - spread_data.my_units):
                    targets.append(possible_spread_node)
                self.forced_spread = possible_spread_node

        for node_to_attack in best_attacks:
            print >> sys.stderr, "decision for " + str(node_to_attack)
            target_data = self.graph.get_node_data(node_to_attack)
            relative_strength = target_data.my_units - target_data.other_units
            assignable = target_data.can_assign
            if target_data.other_units == 0 and target_data.my_units == 0 and assignable:
                targets.append(node_to_attack)
                print >> sys.stderr, "A"
            elif relative_strength == 0 and assignable:
                targets.append(node_to_attack)
                targets.append(node_to_attack)
                targets.append(node_to_attack)
                targets.append(node_to_attack)
                print >> sys.stderr, "B"
            elif relative_strength > 0:
                print >> sys.stderr, "C"
            elif -5 < relative_strength > 0 and assignable:
                for i in xrange(0, abs(relative_strength - 5)):
                    targets.append(node_to_attack)
                print >> sys.stderr, "D"
            elif target_data.other_tolerance == 0 and assignable:
                targets.append(node_to_attack)
                print >> sys.stderr, "E"

        print >> sys.stderr, "Targets after decision " + str(targets)

        return targets

    def starting_node(self):
        for i in xrange(0, self.graph.vertex_count):
            if self.graph.get_node_data(i).my_units == 5:
                return i
        raise Exception ("Funziona solo al primo turno")

    def pad_targets(self, targets):
        if len(targets) == 0:
            return [0,0,0,0,0]

        while len(targets) < 5:
            targets.append(targets[0])

        print >> sys.stderr, "Targets after padding " + str(targets)
        return targets

    def spread(self):
        if self.forced_spread is not None:
            s = self.forced_spread
            self.forced_spread = None
            return str(s)

        possible_spreaders = []
        # for i in xrange(0, self.graph.vertex_count):
        #     if self.graph.get_node_data(i).my_units >= 5:
        #         adj = self.graph.near(i)
        #         weight = 0
        #         for node in adj:
        #             if node not in bombed_targets:
        #                 neigh_data = self.graph.get_node_data(node)
        #                 if neigh_data.my_units == 0 and neigh_data.other_units == 0:
        #                     weight += 2
        #                 elif -2 < (neigh_data.my_units - neigh_data.other_units) < 0:
        #                     weight += 1
        #         possible_spreaders.append((i, weight))

        # for i in xrange(0, self.graph.vertex_count):
        #     if self.graph.get_node_data(i).my_units >= 5:
        #         adj = self.graph.near(i)
        #         weight = 0
        #         for node in adj:
        #             neigh_data = self.graph.get_node_data(node)
        #             if neigh_data.my_tolerance == 0:
        #                 return i
        #         #possible_spreaders.append((i, weight))
        sorted_list = sorted(possible_spreaders, key=lambda id_weight : id_weight[1])
        #return sorted_list[0][0] if len(sorted_list) and sorted_list[0][0] > 0 else "NONE"

        return "NONE"

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

    targets = cadorna.pad_targets(cadorna.safe_attack())

    for target in targets[0:5]:
        print str(target)
    print cadorna.spread(targets[0:5])
