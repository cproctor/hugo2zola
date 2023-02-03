import re
from migration.filters.base import Filter

class HighlightingFilter(Filter):
    """Zola does highlighting differently. The following would be converted 
    from hugo-style highlighting:
        ```bash {hl_lines=["2"]}
        ```python3 {linenos=table}
        ```python3 {linenos=table, hl_lines=["1-3"],linenostart=170}
    """
    def __init__(self, language_mappings=None):
        self.language_mappings = language_mappings or {}

    def process_node(self, node):
        pattern = "``` *(\w+) *({(.*)})?"
        node.markdown_content = re.sub(pattern, self.convert_highlighting, 
                node.markdown_content)
        return node

    def convert_highlighting(self, m):
        language = self.language_mappings.get(m.group(1).strip(), m.group(1).strip())
        if m.group(2):
            hugo_annotations = [ann.strip() for ann in m.group(2).split(',')]
        else:
            hugo_annotations = []
        zola_annotations = [language]
        for ann in hugo_annotations:
            if ann.startswith("linenos"):
                zola_annotations.append("linenos")
            elif ann.startswith("linenostart"):
                zola_annotations.append(ann)
            elif ann.startswith("hl_lines"):
                if lm := re.search("\[(.*)\]", ann):
                    lines = lm.group(1)
                    lines = lines.replace('"', '')
                    zola_annotations.append(f"hl_lines={lines}")
        return "```" + ','.join(zola_annotations)

