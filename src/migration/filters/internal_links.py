import re
from migration.filters.base import Filter

class InternalLinksFilter(Filter):
    """Translates hugo's internal link syntax to zola's.
    """

    def process_node(self, node):
        pattern_a = '{{< +((rel)?ref) +"(?P<link>.*)" +>}}'
        pattern_b = '{{% +((rel)?ref) +"(?P<link>.*)" +>%}}'
        def sub(m):
            link = m.group("link")
            return f'@/{link}'
        node.markdown_content = re.sub(pattern_a, sub, node.markdown_content)
        node.markdown_content = re.sub(pattern_b, sub, node.markdown_content)
        return node
