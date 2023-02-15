import re
from migration.filters.base import Filter
import shlex

class ShortcodeFilter(Filter):
    """Translates hugo's shortcode syntax to zola's, optionally stripping
    or deleting named shortcodes. Optional arguments to constructor:
    - strip: names of shortcodes to strip, leaving their bodies as content
    - delete: names of shortcodes to delete entirely
    - arg_names: dict like {shortcode_name: [arg_names]} specifying names
      of args to override
    """
    def __init__(self, strip=None, delete=None, arg_names=None):
        self.strip = strip or []
        self.delete = delete or []
        self.arg_names = arg_names or {}

    def process_node(self, node):
        self.filter_shortcodes_with_bodies(node)
        self.filter_shortcodes_without_bodies(node)
        return node

    def filter_shortcodes_with_bodies(self, node):
        pattern_a = "{{< *(?P<name>\w+)(?P<args>.*?) *>}}(?P<body>.*?){{< */(?P=name) *>}}"
        pattern_b = "{{% *(?P<name>\w+)(?P<args>.*?) *%}}(?P<body>.*?){{% */(?P=name) *%}}"
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
                    "{% " + name + self.convert_args(name, argstr) + " %}" + 
                    body + 
                    "{% end %}"
                )
        node.markdown_content = re.sub(pattern_a, sub, node.markdown_content, flags=re.DOTALL)
        node.markdown_content = re.sub(pattern_b, sub, node.markdown_content, flags=re.DOTALL)

    def filter_shortcodes_without_bodies(self, node):
        pattern_a = "{{< *(\w+)(.*?) *>}}"
        pattern_b = "{{% *(\w+)(.*?) *%}}"
        def sub(match):
            name = match.group(1)
            argstr = match.group(2)
            if name in self.strip or name in self.delete:
                return ""
            else:
                return "{{ " + name + self.convert_args(name, argstr) + " }}" 
        node.markdown_content = re.sub(pattern_a, sub, node.markdown_content)
        node.markdown_content = re.sub(pattern_b, sub, node.markdown_content)

    def convert_args(self, name, args):
        if not args:
            return "()"

        arglist = shlex.split(args.strip(), posix=False)
        named_args = []
        for arg in arglist:
            if m := re.match("(?P<key>\w+)=(?P<val>.*)", arg):
                named_args.append([m.group('key'), m.group('val')])
            else:
                named_args.append([f"arg{len(named_args)}", arg])
        if name in self.arg_names:
            given_names = self.arg_names[name]
            if len(given_names) < len(named_args):
                msg = f"{len(given_names)} args named for shortcode {name}, but "
                msg += f"found {len(named_args)} args: {named_args}"
                raise ValueError(msg)
            named_args = [[given, val] for given, (key, val) in zip(given_names, named_args)]
        return "(" + ", ".join([key + '=' + val for key, val in named_args]) + ")"
