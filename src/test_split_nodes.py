import unittest

from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    
    # ===== Basic Code Block Tests =====
    
    def test_split_nodes_delimiter_code_basic(self):
        """Test basic code block splitting with backticks"""
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_code_multiple(self):
        """Test splitting with multiple code blocks"""
        node = TextNode("This is `code1` and `code2` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_code_at_start(self):
        """Test code delimiter at the start of text"""
        node = TextNode("`code` at start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" at start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_code_at_end(self):
        """Test code delimiter at the end of text"""
        node = TextNode("ends with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("ends with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)
    
    # ===== Bold Delimiter Tests =====
    
    def test_split_nodes_delimiter_bold(self):
        """Test bold text splitting with ** delimiter"""
        node = TextNode("This is **bold text** here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_bold_multiple(self):
        """Test multiple bold sections"""
        node = TextNode("**bold1** and **bold2** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    # ===== Italic Delimiter Tests =====
    
    def test_split_nodes_delimiter_italic(self):
        """Test italic text splitting with _ delimiter"""
        node = TextNode("This is _italic text_ here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_italic_multiple(self):
        """Test multiple italic sections"""
        node = TextNode("_italic1_ text _italic2_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        
        expected = [
            TextNode("italic1", TextType.ITALIC),
            TextNode(" text ", TextType.TEXT),
            TextNode("italic2", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected)
    
    # ===== Non-TEXT Node Handling =====
    
    def test_split_nodes_delimiter_non_text_nodes_pass_through(self):
        """Test that non-TEXT nodes pass through unchanged"""
        bold_node = TextNode("already bold", TextType.BOLD)
        code_node = TextNode("already code", TextType.CODE)
        text_node = TextNode("this is `code`", TextType.TEXT)
        
        new_nodes = split_nodes_delimiter(
            [bold_node, code_node, text_node], "`", TextType.CODE
        )
        
        expected = [
            TextNode("already bold", TextType.BOLD),
            TextNode("already code", TextType.CODE),
            TextNode("this is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_only_non_text_nodes(self):
        """Test that list of only non-TEXT nodes passes through"""
        bold_node = TextNode("bold", TextType.BOLD)
        code_node = TextNode("code", TextType.CODE)
        
        new_nodes = split_nodes_delimiter(
            [bold_node, code_node], "`", TextType.CODE
        )
        
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)
    
    # ===== Edge Cases =====
    
    def test_split_nodes_delimiter_no_delimiters_in_text(self):
        """Test text with no delimiters present"""
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [TextNode("This is plain text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_empty_delimited_section(self):
        """Test empty section between delimiters"""
        node = TextNode("text `` more text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        # Empty code blocks should be skipped
        expected = [
            TextNode("text ", TextType.TEXT),
            TextNode(" more text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_empty_input_list(self):
        """Test empty input list"""
        new_nodes = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(new_nodes, [])
    
    def test_split_nodes_delimiter_only_delimiter(self):
        """Test text that is only the delimited content"""
        node = TextNode("`code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [TextNode("code", TextType.CODE)]
        self.assertEqual(new_nodes, expected)
    
    # ===== Error Handling =====
    
    def test_split_nodes_delimiter_unmatched_opening(self):
        """Test unmatched opening delimiter raises ValueError"""
        node = TextNode("This is `unmatched code", TextType.TEXT)
        
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertIn("unmatched", str(context.exception).lower())
        self.assertIn("`", str(context.exception))
    
    def test_split_nodes_delimiter_unmatched_bold(self):
        """Test unmatched bold delimiter raises ValueError"""
        node = TextNode("This is **unmatched bold", TextType.TEXT)
        
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertIn("unmatched", str(context.exception).lower())
    
    def test_split_nodes_delimiter_unmatched_at_start(self):
        """Test unmatched delimiter at start of text"""
        node = TextNode("`only opening delimiter", TextType.TEXT)
        
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertIn("unmatched", str(context.exception).lower())
    
    # ===== Chaining Multiple Delimiters =====
    
    def test_split_nodes_delimiter_chain_different_sections(self):
        """Test chaining multiple delimiters on different text sections"""
        # Each section gets its own delimiter
        node = TextNode("text `code` and _italic_ and **bold**", TextType.TEXT)
        
        after_code = split_nodes_delimiter([node], "`", TextType.CODE)
        after_italic = split_nodes_delimiter(after_code, "_", TextType.ITALIC)
        after_bold = split_nodes_delimiter(after_italic, "**", TextType.BOLD)
        
        expected = [
            TextNode("text ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(after_bold, expected)
    
    def test_split_nodes_delimiter_chain_multiple_nodes(self):
        """Test chaining delimiters on multiple input nodes"""
        node1 = TextNode("First `code` part", TextType.TEXT)
        node2 = TextNode("Second _italic_ part", TextType.TEXT)
        
        # First pass: split all by code
        after_code = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        
        # Second pass: split all by italic
        after_italic = split_nodes_delimiter(after_code, "_", TextType.ITALIC)
        
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" part", TextType.TEXT),
            TextNode("Second ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" part", TextType.TEXT),
        ]
        self.assertEqual(after_italic, expected)
    
    # ===== Multi-node Input Tests =====
    
    def test_split_nodes_delimiter_multiple_input_nodes(self):
        """Test processing multiple input nodes at once"""
        node1 = TextNode("First has `code1`", TextType.TEXT)
        node2 = TextNode("Second has `code2`", TextType.TEXT)
        node3 = TextNode("Already bold", TextType.BOLD)
        
        new_nodes = split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE)
        
        expected = [
            TextNode("First has ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode("Second has ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode("Already bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_preserves_order(self):
        """Test that order is preserved with mixed nodes"""
        nodes = [
            TextNode("plain text", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode("text with `code`", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        expected = [
            TextNode("plain text", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode("text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected)
    
    # ===== Special Characters and Content Tests =====
    
    def test_split_nodes_delimiter_with_special_characters(self):
        """Test delimited content with special characters"""
        node = TextNode("Code: `x += 1` in Python", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("Code: ", TextType.TEXT),
            TextNode("x += 1", TextType.CODE),
            TextNode(" in Python", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_with_numbers(self):
        """Test delimited content with numbers"""
        node = TextNode("Version `2.0.1` released", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("Version ", TextType.TEXT),
            TextNode("2.0.1", TextType.CODE),
            TextNode(" released", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_with_spaces_in_delimited_content(self):
        """Test that spaces inside delimited content are preserved"""
        node = TextNode("Text `with  spaces  inside` more", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("with  spaces  inside", TextType.CODE),
            TextNode(" more", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()
