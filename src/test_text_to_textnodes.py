import unittest

from textnode import TextNode, TextType
from split_imgs_links import text_to_textnodes


class TestTextToTextnodes(unittest.TestCase):
    
    # ===== Basic Examples =====
    
    def test_text_to_textnodes_plain_text(self):
        """Test plain text with no formatting"""
        text = "This is plain text"
        result = text_to_textnodes(text)
        expected = [TextNode("This is plain text", TextType.TEXT)]
        self.assertListEqual(result, expected)
    
    def test_text_to_textnodes_empty_string(self):
        """Test empty string"""
        result = text_to_textnodes("")
        # Empty input produces empty output after processing
        expected = []
        self.assertListEqual(result, expected)
    
    # ===== Code Blocks =====
    
    def test_text_to_textnodes_code_only(self):
        """Test text with only code block"""
        text = "`code`"
        result = text_to_textnodes(text)
        expected = [TextNode("code", TextType.CODE)]
        self.assertListEqual(result, expected)
    
    def test_text_to_textnodes_code_in_text(self):
        """Test code block in text"""
        text = "This has `code` inside"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" inside", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)
    
    def test_text_to_textnodes_multiple_code(self):
        """Test multiple code blocks"""
        text = "`first` and `second`"
        result = text_to_textnodes(text)
        expected = [
            TextNode("first", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.CODE),
        ]
        self.assertListEqual(result, expected)
    
    # ===== Bold =====
    
    def test_text_to_textnodes_bold_only(self):
        """Test text with only bold"""
        text = "**bold**"
        result = text_to_textnodes(text)
        expected = [TextNode("bold", TextType.BOLD)]
        self.assertListEqual(result, expected)
    
    def test_text_to_textnodes_bold_in_text(self):
        """Test bold in text"""
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)
    
    def test_text_to_textnodes_multiple_bold(self):
        """Test multiple bold sections"""
        text = "**first** and **second**"
        result = text_to_textnodes(text)
        expected = [
            TextNode("first", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.BOLD),
        ]
        self.assertListEqual(result, expected)
    
    # ===== Italic =====
    
    def test_text_to_textnodes_italic_only(self):
        """Test text with only italic"""
        text = "_italic_"
        result = text_to_textnodes(text)
        expected = [TextNode("italic", TextType.ITALIC)]
        self.assertListEqual(result, expected)
    
    def test_text_to_textnodes_italic_in_text(self):
        """Test italic in text"""
        text = "This is _italic_ text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)
    
    def test_text_to_textnodes_multiple_italic(self):
        """Test multiple italic sections"""
        text = "_first_ and _second_"
        result = text_to_textnodes(text)
        expected = [
            TextNode("first", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.ITALIC),
        ]
        self.assertListEqual(result, expected)
    
    # ===== Images =====
    
    def test_text_to_textnodes_image_only(self):
        """Test text with only image"""
        text = "![alt](url.png)"
        result = text_to_textnodes(text)
        expected = [TextNode("alt", TextType.IMAGE, "url.png")]
        self.assertListEqual(result, expected)
    
    def test_text_to_textnodes_image_in_text(self):
        """Test image in text"""
        text = "Text with ![image](url.png) inside"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url.png"),
            TextNode(" inside", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)
    
    def test_text_to_textnodes_multiple_images(self):
        """Test multiple images"""
        text = "![img1](url1.png) and ![img2](url2.png)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("img1", TextType.IMAGE, "url1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2.png"),
        ]
        self.assertListEqual(result, expected)
    
    # ===== Links =====
    
    def test_text_to_textnodes_link_only(self):
        """Test text with only link"""
        text = "[link](url.com)"
        result = text_to_textnodes(text)
        expected = [TextNode("link", TextType.LINK, "url.com")]
        self.assertListEqual(result, expected)
    
    def test_text_to_textnodes_link_in_text(self):
        """Test link in text"""
        text = "Text with [link](url.com) inside"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
            TextNode(" inside", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)
    
    def test_text_to_textnodes_multiple_links(self):
        """Test multiple links"""
        text = "[link1](url1.com) and [link2](url2.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("link1", TextType.LINK, "url1.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2.com"),
        ]
        self.assertListEqual(result, expected)
    
    # ===== Combined Simple =====
    
    def test_text_to_textnodes_bold_and_italic(self):
        """Test bold and italic together"""
        text = "**bold** and _italic_"
        result = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertListEqual(result, expected)
    
    def test_text_to_textnodes_code_and_bold(self):
        """Test code and bold together"""
        text = "`code` and **bold**"
        result = text_to_textnodes(text)
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertListEqual(result, expected)
    
    def test_text_to_textnodes_image_and_link(self):
        """Test image and link together"""
        text = "![image](img.png) and [link](url.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("image", TextType.IMAGE, "img.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
        ]
        self.assertListEqual(result, expected)
    
    # ===== Complex Combined Examples =====
    
    def test_text_to_textnodes_complex_example_from_assignment(self):
        """Test the example from the assignment"""
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(result, expected)
    
    def test_text_to_textnodes_all_features(self):
        """Test all features combined"""
        text = "Start with **bold**, _italic_, `code`, ![img](url.png), and [link](url.com) end"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Start with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url.png"),
            TextNode(", and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)
    
    def test_text_to_textnodes_mixed_formatting(self):
        """Test mixed formatting in separate locations"""
        text = "Here's a **bold** and some `code` and _italic_ in the text"
        result = text_to_textnodes(text)
        # This tests that all formats can coexist in the same text
        expected = [
            TextNode("Here's a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and some ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" in the text", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)
    
    def test_text_to_textnodes_markdown_document(self):
        """Test a section of a markdown document"""
        text = "Check out [our docs](https://docs.example.com) and ![screenshot](screen.jpg). Also see **important** info."
        result = text_to_textnodes(text)
        expected = [
            TextNode("Check out ", TextType.TEXT),
            TextNode("our docs", TextType.LINK, "https://docs.example.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("screenshot", TextType.IMAGE, "screen.jpg"),
            TextNode(". Also see ", TextType.TEXT),
            TextNode("important", TextType.BOLD),
            TextNode(" info.", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)
    
    # ===== Edge Cases =====
    
    def test_text_to_textnodes_nested_style_formatting(self):
        """Test that processing order is: code, bold, italic, images, links"""
        text = "Start **bold** middle `code` end"
        result = text_to_textnodes(text)
        # This verifies the processing order works correctly
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" middle ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)
    
    def test_text_to_textnodes_consecutive_different_types(self):
        """Test consecutive different formatting types"""
        text = "**bold**_italic_`code`"
        result = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]
        self.assertListEqual(result, expected)
    
    def test_text_to_textnodes_whitespace_preservation(self):
        """Test that whitespace is preserved correctly"""
        text = "  **bold**  and  _italic_  "
        result = text_to_textnodes(text)
        expected = [
            TextNode("  ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("  and  ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("  ", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)
    
    def test_text_to_textnodes_special_characters_in_content(self):
        """Test special characters in various types"""
        text = "**text-with-dashes** and _italic-text_ and `code += 1` and ![alt-text](url-with-dashes.png)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("text-with-dashes", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic-text", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code += 1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("alt-text", TextType.IMAGE, "url-with-dashes.png"),
        ]
        self.assertListEqual(result, expected)
    
    def test_text_to_textnodes_urls_with_special_chars(self):
        """Test URLs with query parameters and fragments"""
        text = "[link](https://example.com/path?q=test&sort=1#section) and ![img](https://example.com/img.png?w=200&h=300)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("link", TextType.LINK, "https://example.com/path?q=test&sort=1#section"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://example.com/img.png?w=200&h=300"),
        ]
        self.assertListEqual(result, expected)
    
    # ===== Order and Processing Tests =====
    
    def test_text_to_textnodes_processing_order_matters(self):
        """Test that processing order is code first, then bold, italic, images, links"""
        # Code backticks are processed first, so any ** inside code blocks are literal
        text = "Has `code here` and **bold** separately"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Has ", TextType.TEXT),
            TextNode("code here", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" separately", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)
    
    def test_text_to_textnodes_long_text(self):
        """Test processing of longer text"""
        text = "This is a long text with **multiple bold** sections, _several italic_ words, `some code blocks`, ![images](img.png), and [many links](url.com). It should all work **correctly**."
        result = text_to_textnodes(text)
        # Verify it produces the right number of nodes
        self.assertTrue(len(result) > 5)
        # Verify all types are present
        types = set(node.text_type for node in result)
        self.assertIn(TextType.TEXT, types)
        self.assertIn(TextType.BOLD, types)
        self.assertIn(TextType.ITALIC, types)
        self.assertIn(TextType.CODE, types)
        self.assertIn(TextType.IMAGE, types)
        self.assertIn(TextType.LINK, types)


if __name__ == "__main__":
    unittest.main()
