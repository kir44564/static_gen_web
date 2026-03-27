import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_same_properties(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url_none_vs_non_none(self):
        node_none_url = TextNode("Link text", TextType.LINK, None)
        node_with_url = TextNode("Link text", TextType.LINK, "https://example.com")
        self.assertNotEqual(node_none_url, node_with_url)

    def test_eq_different_text_type(self):
        node_plain = TextNode("Same text", TextType.PLAIN)
        node_bold = TextNode("Same text", TextType.BOLD)
        self.assertNotEqual(node_plain, node_bold)

    def test_eq_different_text(self):
        node1 = TextNode("Text A", TextType.ITALIC)
        node2 = TextNode("Text B", TextType.ITALIC)
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()