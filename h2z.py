import sys
sys.path.insert(0, 'src')

from argparse import ArgumentParser
from migration.filters.debug import DebugFilter
from migration.filters.clean_metadata import CleanMetadataFilter
from migration.filters.replace_content import ReplaceContentFilter
from migration.filters.highlighting import HighlightingFilter
from migration.filters.internal_links import InternalLinksFilter
from migration.filters.shortcodes import ShortcodeFilter
from migration import Migrator

parser = ArgumentParser()
parser.add_argument('hugo_path')
parser.add_argument('zola_path')
parser.add_argument('-t', '--theme')
parser.add_argument('-x', '--clean', action='store_true')
parser.add_argument('-c', '--config', action='store_true')
args = parser.parse_args()

migrator = Migrator([
    DebugFilter(),
    CleanMetadataFilter(['title']),
    HighlightingFilter({'shell': 'bash', 'python3': 'py3'}),
    InternalLinksFilter(),
    ShortcodeFilter(
        arg_names={
            'youtube': ['id', 'autoplay'],
            'details': ['summary'],
            'aside': ['title'],
        }
    ),
])

migrator.migrate(
    args.hugo_path, 
    args.zola_path, 
    theme=args.theme,
    clean=args.clean,
    config=args.config,
)
