from migration.filters.base import Filter

class DebugFilter(Filter):
    def process_node(self, node):
        print(node)
        return node
