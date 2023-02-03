import shutil
from pathlib import Path
import toml
from migration.content_node import ContentNode

class Migrator:
    """Migrates a hugo source directory to zola.
    """
    CONTENT_DIR = "content"
    HUGO_SECTION_STEM = "_index"
    MARKDOWN_SUFFIX = ".md"
    ZOLA_CONFIG_FILE = "config.toml"

    def __init__(self, filters):
        self.filters = filters

    def migrate(self, hugo_root, zola_root, theme=None, clean=False, config=False):
        self.hugo_root = hugo_root
        zola_root = Path(zola_root)
        self.prepare_zola_dir(zola_root, theme, clean, config)
        for node in self.iter_dir(Path(hugo_root) / self.CONTENT_DIR):
            for f in self.filters:
                node = f.process_node(node)
            node.write_zola(zola_root)

    def prepare_zola_dir(self, zola_root, theme=None, clean=False, config=False):
        if zola_root.exists():
            if clean:
                shutil.rmtree(zola_root)
            else:
                raise FileExistsError("zola_root exists and --clean not set")
        zola_root.mkdir(parents=True)
        if theme:
            theme_path = Path(theme)
            (zola_root / "themes").mkdir()
            shutil.copytree(theme_path, zola_root / "themes" / theme_path.name)
        if config:
            with open(zola_root / self.ZOLA_CONFIG_FILE, 'w') as fh:
                config = {
                    "base_url": "https://test.com",
                    "link_checker": {
                        "internal_level": "warn",
                        "external_level": "warn",
                    }
                }
                if theme:
                    config['theme'] = theme_path.name
                toml.dump(config, fh)

    
    def iter_dir(self, path, parent_section=None):
        subdirs = []
        page_paths = []
        resource_paths = []
        section = None
        section_path = None
        for p in path.iterdir():
            if p.is_dir():
                subdirs.append(p)
            elif p.stem == self.HUGO_SECTION_STEM:
                section_path = p
            elif p.suffix == self.MARKDOWN_SUFFIX:
                page_paths.append(p)
            else:
                resource_paths.append(p)
        if section_path:
            section = ContentNode(
                section_path, 
                self.hugo_root,
                content_type="section",
                resource_paths=resource_paths, 
                section=parent_section,
            )
            yield section
        for page_path in page_paths:
            yield ContentNode(page_path, self.hugo_root)
        for subdir in subdirs:
            for node in self.iter_dir(subdir, parent_section=section):
                yield node

    def read_node(self, path):
        node = frontmatter.load(path)
        return fm
