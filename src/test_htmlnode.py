import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_none(self):
        node = HTMLNode(tag="div", value="text", props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_property(self):
        node = HTMLNode(tag="img", props={"src": "image.png"})
        self.assertEqual(node.props_to_html(), ' src="image.png"')

    def test_props_to_html_multiple_properties(self):
        node = HTMLNode(tag="a", props={"href": "https://example.com", "target": "_blank"})
        output = node.props_to_html()
        self.assertIn(output, [
            ' href="https://example.com" target="_blank"',
            ' target="_blank" href="https://example.com"'
        ])
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()