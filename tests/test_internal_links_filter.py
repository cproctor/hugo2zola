import sys
sys.path.insert(0, 'src')

from tests.stub_node import StubContentNode
from migration.filters.internal_links import InternalLinksFilter
from unittest import TestCase, main

class TestInternalLinksFilter(TestCase):
    def setUp(self):
        self.f = InternalLinksFilter()
        self.ref_node = StubContentNode({}, '{{< ref "blog/neat.md" >}}')
        self.relref_node = StubContentNode({}, '{{< relref "blog/neat.md" >}}')

    def test_formats_internal_links(self):
        self.f.process_node(self.ref_node)
        self.assertEqual(self.ref_node.markdown_content, "@/blog/neat.md")
        self.f.process_node(self.relref_node)
        self.assertEqual(self.relref_node.markdown_content, "@/blog/neat.md")

if __name__ == '__main__':
    main()

