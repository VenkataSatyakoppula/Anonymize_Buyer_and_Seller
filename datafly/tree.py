from queue import Queue

# define a node in the tree
class Node:
    # constructor
    def __init__(self, data):
        self.data = data
        self.parent = None
        # Dictionary whose values are the node children and whose keys are the corresponding nodes data.
        self.children = dict()

    def add_child(self, child):
        child.parent = self
        self.children[child.data] = child

class Tree:
    # constructor
    def __init__(self, root: Node):
        self.root = root

    #  Searches for a node, given its data. The search starts from the root.
    # Given node data to find
    def bfs_search(self, data, depth=None):
        visited, queue = set(), Queue()
        # Each element of the queue is a couple (node, level):
        queue.put((self.root, 0))
        while not queue.empty():
            node, level = queue.get()
            if depth is not None and level > depth:
                break
            if depth is None:
                if node.data == data:
                    return node
            else:
                if level == depth and node.data == data:
                    return node
            for child in node.children.values():
                if child in visited:
                    continue
                queue.put((child, level + 1))
            visited.add(node)
        return None

    def _bfs_insert(self, child: Node, parent: Node) -> bool:
        node = self.bfs_search(parent.data)
        if node is not None:
            node.add_child(child)
            return True
        else:
            return False

    # Inserts a node given its parent. 
    # Note: insertion is done on the first node with the samedata as the given parent node.
    def insert(self, child: Node, parent: Node) -> bool:
        return self._bfs_insert(child, parent)

    # Gets the parent of a node, given the node data.
    def parent(self, data):
        node = self.bfs_search(data)
        if node is not None:
            return node.parent
        else:
            return None
