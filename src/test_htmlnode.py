import unittest

from htmlnode import HTMLNode


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

if __name__ == "__main__":
    unittest.main()