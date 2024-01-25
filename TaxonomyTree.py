import numpy as np
from utils import tree_utils
from bigtree import Node, levelordergroup_iter, get_subtree


class TaxonomyTree:
    def __init__(self, rows, config, rootName):
        self.rows = rows
        self.config = config
        self.branchPrefix = "Any "
        self.rootName = rootName
        self.tree = self.buildTree()
        self.branches = self.getBranches()

    def getBranch(self, branchName):
        return self.branches[branchName]

    def getTree(self):
        return self.tree

    # Build the taxonomy tree
    def buildTree(self):
        root = Node(self.rootName)
        # Generalise for each column (age, sex, ...)
        for column in self.config["generalization"]["fields"]:
            values = np.unique(self.rows[column].values)
            dataType = self.config["generalization"]["fields"][column]
            generalisedNode = tree_utils.generaliseValues(values, self.branchPrefix + column, dataType)
            generalisedNode.parent = root
        return root

    def printTree(self, maxDepth=0, direction="horizontal", style="rounded"):
        if direction not in ["horizontal", "vertical"]:
            raise Exception("Not implemented tree display direction")

        if direction == "horizontal":
            return self.tree.hshow(style=style, max_depth=maxDepth)

        return self.tree.show(style=style, max_depth=maxDepth)

    def getSubTree(self, root, name=None, maxDepth=0):
        return get_subtree(root, name, max_depth=maxDepth)

    def getBranches(self):
        ret = {}
        for column in self.config["generalization"]["fields"]:
            ret[column] = self.getSubTree(self.tree, self.branchPrefix + column)
        return ret

    def getTreeLevel(self, root, level):
        levels = [[node.node_name for node in group] for group in levelordergroup_iter(root, max_depth=level)]
        return levels[len(levels) - 1]
