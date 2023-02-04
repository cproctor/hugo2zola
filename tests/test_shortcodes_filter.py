import sys
sys.path.insert(0, 'src')

from tests.stub_node import StubContentNode
from migration.filters.shortcodes import ShortcodeFilter
from unittest import TestCase, main

class TestShortcodesFilter(TestCase):
    def setUp(self):
        self.f = ShortcodeFilter()
        self.node = StubContentNode(
            {}, 
            "{{< aside >}}"
        )
        self.node_args = StubContentNode(
            {}, 
            '{{< aside 1 "two" >}}'
        )
        self.node_kwargs = StubContentNode(
            {}, 
            '{{< aside one=1 two="two" >}}'
        )
        self.node_body = StubContentNode(
            {}, 
            "{{< aside >}} content {{< /aside >}}"
        )
        self.node_body_args = StubContentNode(
            {}, 
            '{{< aside 1 "two" >}} content {{< /aside >}}'
        )
        self.node_body_kwargs = StubContentNode(
            {}, 
            '{{< aside one=1 two="two" >}} content {{< /aside >}}'
        )

    def test_formats_zola_shortcode(self):
        self.f.process_node(self.node)
        self.assertEqual(self.node.markdown_content, "{{ aside() }}")
        self.f.process_node(self.node_body)
        self.assertEqual(self.node_body.markdown_content, "{% aside() %} content {% end %}")

    def test_parses_arguments(self):
        self.f.process_node(self.node_args)
        self.assertEqual(self.node_args.markdown_content, '{{ aside(arg0=1, arg1="two") }}')
        self.f.process_node(self.node_kwargs)
        self.assertEqual(self.node_kwargs.markdown_content, '{{ aside(one=1, two="two") }}')

if __name__ == '__main__':
    main()
