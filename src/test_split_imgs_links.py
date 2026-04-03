import unittest

from textnode import TextNode, TextType
from split_imgs_links import split_nodes_image, split_nodes_link


class TestSplitNodesImage(unittest.TestCase):
    
    # ===== Basic Image Splitting =====
    
    def test_split_images_single_image(self):
        """Test basic image splitting"""
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_images_image_at_start(self):
        """Test image at the start of text"""
        node = TextNode(
            "![image](https://example.com/img.png) at the start",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" at the start", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_images_image_at_end(self):
        """Test image at the end of text"""
        node = TextNode(
            "ends with ![image](https://example.com/img.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("ends with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            ],
            new_nodes,
        )
    
    def test_split_images_only_image(self):
        """Test text that is only an image"""
        node = TextNode(
            "![image](https://example.com/img.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            ],
            new_nodes,
        )
    
    def test_split_images_consecutive_images(self):
        """Test consecutive images without text between"""
        node = TextNode(
            "![img1](url1.png)![img2](url2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "url1.png"),
                TextNode("img2", TextType.IMAGE, "url2.png"),
            ],
            new_nodes,
        )
    
    def test_split_images_many_images(self):
        """Test text with many images"""
        node = TextNode(
            "![1](url1)text![2](url2)more![3](url3)end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("1", TextType.IMAGE, "url1"),
                TextNode("text", TextType.TEXT),
                TextNode("2", TextType.IMAGE, "url2"),
                TextNode("more", TextType.TEXT),
                TextNode("3", TextType.IMAGE, "url3"),
                TextNode("end", TextType.TEXT),
            ],
            new_nodes,
        )
    
    # ===== Image Alt Text Variations =====
    
    def test_split_images_empty_alt_text(self):
        """Test image with empty alt text"""
        node = TextNode(
            "Text ![](https://example.com/img.png) more",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" more", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_images_alt_text_with_spaces(self):
        """Test image alt text with multiple spaces"""
        node = TextNode(
            "![my image alt text](url.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("my image alt text", TextType.IMAGE, "url.png"),
            ],
            new_nodes,
        )
    
    def test_split_images_alt_text_with_special_chars(self):
        """Test image alt text with special characters"""
        node = TextNode(
            "![my-image_2](url.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("my-image_2", TextType.IMAGE, "url.png"),
            ],
            new_nodes,
        )
    
    # ===== URL Variations =====
    
    def test_split_images_url_with_query_params(self):
        """Test image URL with query parameters"""
        node = TextNode(
            "![img](https://example.com/img.png?size=large)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img", TextType.IMAGE, "https://example.com/img.png?size=large"),
            ],
            new_nodes,
        )
    
    def test_split_images_relative_url(self):
        """Test image with relative URL"""
        node = TextNode(
            "![image](../assets/image.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "../assets/image.png"),
            ],
            new_nodes,
        )
    
    # ===== Non-TEXT Node Handling =====
    
    def test_split_images_non_text_nodes_pass_through(self):
        """Test that non-TEXT nodes pass through unchanged"""
        bold_node = TextNode("already bold", TextType.BOLD)
        text_node = TextNode("text with ![img](url.png)", TextType.TEXT)
        
        new_nodes = split_nodes_image([bold_node, text_node])
        self.assertListEqual(
            [
                TextNode("already bold", TextType.BOLD),
                TextNode("text with ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "url.png"),
            ],
            new_nodes,
        )
    
    def test_split_images_multiple_node_types(self):
        """Test with multiple different node types"""
        nodes = [
            TextNode("bold text", TextType.BOLD),
            TextNode("text with ![img](url.png)", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode("![img2](url2.png)", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("bold text", TextType.BOLD),
                TextNode("text with ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "url.png"),
                TextNode("italic text", TextType.ITALIC),
                TextNode("img2", TextType.IMAGE, "url2.png"),
                TextNode("code", TextType.CODE),
            ],
            new_nodes,
        )
    
    # ===== Edge Cases =====
    
    def test_split_images_no_images(self):
        """Test text with no images"""
        node = TextNode("This is plain text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)
    
    def test_split_images_empty_list(self):
        """Test empty input list"""
        new_nodes = split_nodes_image([])
        self.assertListEqual([], new_nodes)
    
    def test_split_images_only_non_text_nodes(self):
        """Test list with only non-TEXT nodes"""
        bold_node = TextNode("bold", TextType.BOLD)
        code_node = TextNode("code", TextType.CODE)
        new_nodes = split_nodes_image([bold_node, code_node])
        self.assertListEqual([bold_node, code_node], new_nodes)


class TestSplitNodesLink(unittest.TestCase):
    
    # ===== Basic Link Splitting =====
    
    def test_split_links_single_link(self):
        """Test basic link splitting"""
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )
    
    def test_split_links_link_at_start(self):
        """Test link at the start of text"""
        node = TextNode(
            "[example](https://example.com) is a great site",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("example", TextType.LINK, "https://example.com"),
                TextNode(" is a great site", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_links_link_at_end(self):
        """Test link at the end of text"""
        node = TextNode(
            "Check out [this site](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check out ", TextType.TEXT),
                TextNode("this site", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )
    
    def test_split_links_only_link(self):
        """Test text that is only a link"""
        node = TextNode(
            "[link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )
    
    def test_split_links_consecutive_links(self):
        """Test consecutive links without text between"""
        node = TextNode(
            "[link1](url1)[link2](url2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "url1"),
                TextNode("link2", TextType.LINK, "url2"),
            ],
            new_nodes,
        )
    
    def test_split_links_many_links(self):
        """Test text with many links"""
        node = TextNode(
            "[1](url1)text[2](url2)more[3](url3)end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("1", TextType.LINK, "url1"),
                TextNode("text", TextType.TEXT),
                TextNode("2", TextType.LINK, "url2"),
                TextNode("more", TextType.TEXT),
                TextNode("3", TextType.LINK, "url3"),
                TextNode("end", TextType.TEXT),
            ],
            new_nodes,
        )
    
    # ===== Link Anchor Text Variations =====
    
    def test_split_links_empty_anchor_text(self):
        """Test link with empty anchor text"""
        node = TextNode(
            "Text [](https://example.com) more",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://example.com"),
                TextNode(" more", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_links_anchor_with_spaces(self):
        """Test link anchor text with multiple spaces"""
        node = TextNode(
            "[click here for more info](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("click here for more info", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )
    
    def test_split_links_anchor_with_special_chars(self):
        """Test link anchor text with special characters"""
        node = TextNode(
            "[my-link_text](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("my-link_text", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )
    
    # ===== URL Variations =====
    
    def test_split_links_url_with_path(self):
        """Test link URL with path"""
        node = TextNode(
            "[docs](https://example.com/docs/guide)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("docs", TextType.LINK, "https://example.com/docs/guide"),
            ],
            new_nodes,
        )
    
    def test_split_links_url_with_query_params(self):
        """Test link URL with query parameters"""
        node = TextNode(
            "[search](https://example.com/search?q=test&sort=date)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("search", TextType.LINK, "https://example.com/search?q=test&sort=date"),
            ],
            new_nodes,
        )
    
    def test_split_links_url_with_fragment(self):
        """Test link URL with fragment identifier"""
        node = TextNode(
            "[section](https://example.com/docs#introduction)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("section", TextType.LINK, "https://example.com/docs#introduction"),
            ],
            new_nodes,
        )
    
    def test_split_links_relative_url(self):
        """Test link with relative URL"""
        node = TextNode(
            "[docs](../docs/README.md)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("docs", TextType.LINK, "../docs/README.md"),
            ],
            new_nodes,
        )
    
    # ===== Non-TEXT Node Handling =====
    
    def test_split_links_non_text_nodes_pass_through(self):
        """Test that non-TEXT nodes pass through unchanged"""
        bold_node = TextNode("already bold", TextType.BOLD)
        text_node = TextNode("text with [link](url.com)", TextType.TEXT)
        
        new_nodes = split_nodes_link([bold_node, text_node])
        self.assertListEqual(
            [
                TextNode("already bold", TextType.BOLD),
                TextNode("text with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url.com"),
            ],
            new_nodes,
        )
    
    def test_split_links_multiple_node_types(self):
        """Test with multiple different node types"""
        nodes = [
            TextNode("bold text", TextType.BOLD),
            TextNode("text with [link](url.com)", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode("[link2](url2.com)", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("bold text", TextType.BOLD),
                TextNode("text with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url.com"),
                TextNode("italic text", TextType.ITALIC),
                TextNode("link2", TextType.LINK, "url2.com"),
                TextNode("code", TextType.CODE),
            ],
            new_nodes,
        )
    
    # ===== Edge Cases =====
    
    def test_split_links_no_links(self):
        """Test text with no links"""
        node = TextNode("This is plain text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)
    
    def test_split_links_empty_list(self):
        """Test empty input list"""
        new_nodes = split_nodes_link([])
        self.assertListEqual([], new_nodes)
    
    def test_split_links_only_non_text_nodes(self):
        """Test list with only non-TEXT nodes"""
        bold_node = TextNode("bold", TextType.BOLD)
        code_node = TextNode("code", TextType.CODE)
        new_nodes = split_nodes_link([bold_node, code_node])
        self.assertListEqual([bold_node, code_node], new_nodes)
    
    # ===== Image vs Link Distinction =====
    
    def test_split_links_does_not_match_images(self):
        """Test that images are not matched as links"""
        node = TextNode(
            "Here is an ![image](https://example.com/img.png) not a link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Here is an ![image](https://example.com/img.png) not a link", TextType.TEXT),
            ],
            new_nodes,
        )


class TestSplitNodesImageAndLink(unittest.TestCase):
    """Tests combining image and link splitting"""
    
    def test_split_images_and_links_separately(self):
        """Test that we can split images and links on the same text (separately)"""
        text_with_both = "Check ![img](url.png) and [link](url.com)"
        node = TextNode(text_with_both, TextType.TEXT)
        
        # Split images first
        after_images = split_nodes_image([node])
        # Then split links on TEXT nodes
        after_links = split_nodes_link(after_images)
        
        expected = [
            TextNode("Check ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
        ]
        self.assertListEqual(expected, after_links)
    
    def test_complex_document_split(self):
        """Test splitting a complex document with multiple images and links"""
        text = "Start with ![logo](logo.png), then [github](github.com) link, and ![screenshot](screen.jpg)"
        node = TextNode(text, TextType.TEXT)
        
        # Split images first, then links
        after_images = split_nodes_image([node])
        after_links = split_nodes_link(after_images)
        
        expected = [
            TextNode("Start with ", TextType.TEXT),
            TextNode("logo", TextType.IMAGE, "logo.png"),
            TextNode(", then ", TextType.TEXT),
            TextNode("github", TextType.LINK, "github.com"),
            TextNode(" link, and ", TextType.TEXT),
            TextNode("screenshot", TextType.IMAGE, "screen.jpg"),
        ]
        self.assertListEqual(expected, after_links)
    
    def test_split_mixed_content_with_multiple_nodes(self):
        """Test splitting mixed content across multiple input nodes"""
        nodes = [
            TextNode("First ![img1](url1.png)", TextType.TEXT),
            TextNode("Already BOLD", TextType.BOLD),
            TextNode("Text [link1](url1) more", TextType.TEXT),
        ]
        
        after_images = split_nodes_image(nodes)
        after_links = split_nodes_link(after_images)
        
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url1.png"),
            TextNode("Already BOLD", TextType.BOLD),
            TextNode("Text ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" more", TextType.TEXT),
        ]
        self.assertListEqual(expected, after_links)


if __name__ == "__main__":
    unittest.main()
