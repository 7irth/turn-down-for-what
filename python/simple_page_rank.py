__author__ = 'Tirth'

# Simple implementation of PageRank algorithm
#
# Nodes containing values are ranked according to their weight
# and the nodes they link to.

from fractions import Fraction


class Node:
    def __init__(self, name, value, weight=1):
        self.name = name
        self.value = value
        self.out_links, self.in_links = [], []
        self.score = 0
        self.weight = weight
        self.in_this_time = 0

    def links_to(self, nodes_to_add):
        for node in nodes_to_add:
            self.out_links.append(node)
            node.in_links.append(self)

    def num_in(self):
        return len(self.in_links)

    def num_out(self):
        return len(self.out_links)

    def calculate_init_score(self):
        self.score = self.num_in()

    def calculate_score_out(self):
        self.score = 0
        for j in self.in_links:
            self.score += j.score * j.value

    def calculate_score_in(self):
        self.score = 0
        for j in self.out_links:
            self.score += j.score * j.value

    def calc_rank_out(self):
        if self.num_out() != 0:
            out_score = self.score / self.num_out()
            for node in self.out_links:
                node.in_this_time += out_score
        else:
            self.in_this_time = self.score

    def get_out_links(self):
        s = self.name + ' links to '

        for j in [node.name for node in self.out_links]:
            s += j + ', '

        if len(s) > (len(self.name) + 12):
            s = s[:-2]

        return s

    def get_in_links(self):
        s = self.name + ' is linked to from '

        for j in [node.name for node in self.in_links]:
            s += j + ', '

        if len(s) > (len(self.name) + 21):
            s = s[:-2]

        return s


def print_all(side, round_to=3):
    total = calculate_total_score(side)
    for node in side.values():
        print(node.name, '=', str(round((node.score / total), round_to)),
              end='| ')
    print()


def print_ranks(network, max_d=1000, round_to=3):
    for node in network.keys():
        network[node] = network[node].score

    for node in sorted(network, key=network.get, reverse=True):
        print(node, '=', str(Fraction(network[node]).limit_denominator(max_d)),
              '(' + str(round(network[node], round_to)) + ')')


def calc_cycle(uno, dos, cycles=10000):
    for _ in range(cycles):
        for node in uno.values():
            node.calculate_score_in()

        for node in dos.values():
            node.calculate_score_out()


def initialize_page_rank(network):
    init_rank = 1 / len(network.keys())

    for node in network.values():
        node.score = init_rank


def calculate_page_rank(network, cycles=10000, s=0.9):
    """ Scaled PageRank Update Rule

    :param network: dict of nodes comprising the network
    :param cycles: amount of times to apply update
    :param s: scaling factor
    """
    for _ in range(cycles):
        for node in network.values():
            node.calc_rank_out()

        for node in network.values():
            node.score = (
                node.in_this_time * s + ((1 - s) / len(network.values())))
            node.in_this_time = 0


def calculate_total_score(side):
    total = 0
    for node in side.values():
        total += node.score

    return total


if __name__ == '__main__':
    nodes = {}  # dict of - name: node(name)

    for char in range(65, 73):
        nodes[chr(char)] = Node(chr(char), 'Value')

    # currently just nodes of letters, but could contain anything
    nodes['A'].links_to((nodes['B'], nodes['C'], nodes['D']))
    nodes['B'].links_to((nodes['D'], nodes['E']))
    nodes['C'].links_to((nodes['F'], nodes['G']))
    nodes['D'].links_to((nodes['H'], nodes['A']))
    nodes['E'].links_to((nodes['H'], nodes['A']))
    nodes['F'].links_to([nodes['A']])
    nodes['G'].links_to([nodes['A']])
    nodes['H'].links_to([nodes['A']])

    initialize_page_rank(nodes)
    calculate_page_rank(nodes, s=0.85)
    print_ranks(nodes)