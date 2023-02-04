import re
from migration.filters.base import Filter

class ReplaceContentFilter(Filter):
    """Uses re.sub to replace matching patterns. 
    Replacements should be a list of (pattern, replacement)
    """
    def __init__(self, replacements):
        self.replacements = replacements

    def process_node(self, node):
        for pattern, replacement in self.replacements:
            node.markdown_content = re.sub(pattern, replacement, node.markdown_content)
        return node
