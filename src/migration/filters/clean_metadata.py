from migration.filters.base import Filter

class CleanMetadataFilter(Filter):
    ZOLA_FRONTMATTER_KEYS = [
        'title',
        'description', 
        'date',
        'updated', 
        'weight', 
        'draft', 
        'slug',
        'path', 
        'aliases',
        'template', 
        'taxonomies',
        'extra',
    ]

    def __init__(self, keys_to_keep=None):
        self.keys_to_keep = keys_to_keep or self.ZOLA_FRONTMATTER_KEYS

    def process_node(self, node):
        keys_to_remove = []
        for key in node.metadata.keys():
            if key not in self.keys_to_keep:
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del node.metadata[key]
        return node


