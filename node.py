class Node:
    label = ""
    leaf = False
    children = {}

    def __init__(self, label, leaf=False, instances=0):
        self.label = label
        self.children = {}
        self.leaf = leaf
        self.instances = instances

    def getChildren(self):
        return self.children
