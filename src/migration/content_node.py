import frontmatter
import toml

class ContentNode:
    """Represents a node of content
    """

    TOML_DELIMITER = "+++"

    def __init__(self, hugo_path, hugo_root, content_type="page", section=None, 
            resource_paths=None):
        fm = frontmatter.load(hugo_path)
        self.relative_path = hugo_path.relative_to(hugo_root)
        self.content_type = content_type
        self.metadata = fm.metadata
        self.markdown_content = fm.content

    def get_output_path(self, root):
        return root / self.relative_path

    def __str__(self):
        return f"<ContentNode {self.content_type} {self.relative_path}>"

    def write_zola(self, zola_root):
        output_path = self.get_output_path(zola_root)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.get_output_path(zola_root), 'w') as fh:
            fh.write(self.TOML_DELIMITER + '\n')
            toml.dump(self.metadata, fh)
            fh.write(self.TOML_DELIMITER + '\n\n')
            fh.write(self.markdown_content)
