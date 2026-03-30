from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code" 
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False 
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        url_str = self.url if self.url else "None"
        return f"TextNode({self.text}, {self.text_type.value}, {url_str})"

def text_node_to_html_node(text_node):
    type_map = {
        TextType.TEXT: lambda n: LeafNode(None, n.text),
        TextType.BOLD: lambda n: LeafNode("b", n.text),
        TextType.ITALIC: lambda n: LeafNode("i", n.text),
        TextType.CODE: lambda n: LeafNode("code", n.text),
        TextType.LINK: lambda n: LeafNode("a", n.text, {"href": n.url}),
        TextType.IMAGE: lambda n: LeafNode("img", "", {"src": n.url, "alt": n.text}),
    }

    if text_node.text_type not in type_map:
        raise Exception(f"Invalid TextType: {text_node.text_type}")
    
    if text_node.text_type in (TextType.LINK, TextType.IMAGE) and text_node.url is None:
        raise ValueError(f"{text_node.text_type.value} requires a URL")

    return type_map[text_node.text_type](text_node)