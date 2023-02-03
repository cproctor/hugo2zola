import re
from migration.filters.base import Filter

class ShortcodeFilter(Filter):
    """Translates hugo's shortcode syntax to zola's, optionally stripping
    or deleting named shortcodes.
    """
    def __init__(self, strip=None, delete=None):
        self.strip = strip or []
        self.delete = delete or []

    def process_node(self, node):
        self.filter_shortcodes_with_bodies(node)
        self.filter_shortcodes_without_bodies(node)
        return node

    def filter_shortcodes_with_bodies(self, node):
        pattern_a = "{{< +(?P<name>\w+)(?P<args>.*) +>}}(?P<body>.*){{< +/(?P=name) +>}}"
        pattern_b = "{{% +(?P<name>\w+)(?P<args>.*) +%}}(?P<body>.*){{% +/(?P=name) +%}}"
        def sub(match):
            name = match.group("name")
            argstr = match.group("args")
            body = match.group("body")
            if name in self.strip:
                return body
            elif name in self.delete:
                return ""
            else:
                return (
                    "{% " + name + self.convert_args(argstr) + " %}" + 
                    body + 
                    "{% end %}"
                )
        node.markdown_content = re.sub(pattern_a, sub, node.markdown_content, flags=re.DOTALL)
        node.markdown_content = re.sub(pattern_b, sub, node.markdown_content, flags=re.DOTALL)

    def filter_shortcodes_without_bodies(self, node):
        pattern_a = "{{< +(\w+)(.*) +>}}"
        pattern_b = "{{% +(\w+)(.*) +%}}"
        def sub(match):
            name = match.group(1)
            argstr = match.group(2)
            if name in self.strip or name in self.delete:
                return ""
            else:
                return "{% " + name + self.convert_args(argstr) + " %}" 
        node.markdown_content = re.sub(pattern_a, sub, node.markdown_content)
        node.markdown_content = re.sub(pattern_b, sub, node.markdown_content)

    def convert_args(self, args):
        return "()"
