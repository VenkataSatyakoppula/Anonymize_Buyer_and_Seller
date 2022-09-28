import csv
from io import StringIO
from tree import Node, Tree


class _DGH:
    # Represents multiple hierarchies as a dictionary of trees.
    def __init__(self, dgh_path):

        # Dictionary where the values are trees and the keys are the values of the corresponding roots.
        self.hierarchies = dict()
        # Dictionary whose keys are the hierarchies root values and whose values are the hierarchies depths (number of generalization levels).
        self.gen_levels = dict()

    # Returns the upper lever generalization of a value in the domain.
    def generalize(self, value, gen_level=None):

        # Search across all hierarchies (slow if there are a lot of hierarchies):
        for hierarchy in self.hierarchies:

            # Try to find the node:
            if gen_level is None:
                node = self.hierarchies[hierarchy].bfs_search(value)
            else:
                node = self.hierarchies[hierarchy].bfs_search(
                    value,
                    # Depth.
                    self.gen_levels[hierarchy] - gen_level) 

            if node is None:
                continue
            elif node.parent is None:
                # The value is a hierarchy root:
                return None
            else:
                return node.parent.data

        # The value is not found:
        raise KeyError(value)


class CsvDGH(_DGH):
    def __init__(self, dgh_path):
        super().__init__(dgh_path)
        try:
            with open(dgh_path, 'r') as file:
                for line in file:

                    try:
                        csv_reader = csv.reader(StringIO(line))
                    except IOError:
                        raise
                    values = next(csv_reader)
                    # If it doesn't exist a hierarchy with this root, add one:
                    if values[-1] not in self.hierarchies:
                        self.hierarchies[values[-1]] = Tree(Node(values[-1]))
                        # Add the number of generalization levels:
                        self.gen_levels[values[-1]] = len(values) - 1
                    # Populate hierarchy with the other values:
                    self._insert_hierarchy(values[:-1], self.hierarchies[values[-1]])

        except FileNotFoundError:
            raise
        except IOError:
            raise
    
    # Inserts values, ordered from child to parent, to a tree.
    @staticmethod
    def _insert_hierarchy(values, tree):
        current_node = tree.root

        for i, value in enumerate(reversed(values)):

            if value in current_node.children:
                current_node = current_node.children[value]
                continue
            else:
                # Insert the hierarchy from this node:
                for v in list(reversed(values))[i:]:
                    current_node.add_child(Node(v))
                    current_node = current_node.children[v]
                return True

        return False
