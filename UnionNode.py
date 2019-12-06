class UnionNode(object):

    def __init__(self, label):
        self.vertices = {}  # current num of elements
        self.edges = {} # the number of disjoint sets or components
        self.label = label

    def get_edges(self):
        return self.edges
    def get_vertices(self):
        return self.vertices
    def __iter__(self):
        return iter(self.label)
