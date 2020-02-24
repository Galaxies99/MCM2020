# Calculating Page rank.
class Graph():
    def __init__(self):
        self.linked_node_map = {}
        self.PR_map = {}

    def add_node(self, node_id):
        if node_id not in self.linked_node_map:
            self.linked_node_map[node_id] = []
            self.PR_map[node_id] = 0

    def add_link(self, node1, node2, v):
        if node1 not in self.linked_node_map:
            self.add_node(node1)
        if node2 not in self.linked_node_map:
            self.add_node(node2)
        # When Inserting links, weights are already divided by sum.
        self.linked_node_map[node2].append([node1, v])

    # Compute Page Rank
    def get_PR(self, epoch_num=50, d=0.95):
        for i in range(epoch_num):
            for node in self.PR_map:
                self.PR_map[node] = (1 - d) + d * sum(
                    [self.PR_map[temp_node[0]] * temp_node[1] 
                     for temp_node in self.linked_node_map[node]])
        return self.PR_map
