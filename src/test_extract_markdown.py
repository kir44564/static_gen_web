import unittest

from extract_markdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):
    
    # ===== Basic Image Extraction =====
    
    def test_extract_markdown_images_single_image(self):
        """Test extracting a single image"""
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_multiple_images(self):
        """Test extracting multiple images"""
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(expected, matches)
    
    def test_extract_markdown_images_at_start(self):
        """Test image at the start of text"""
        text = "![image](https://example.com/img.png) is here"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://example.com/img.png")], matches)
    
    def test_extract_markdown_images_at_end(self):
        """Test image at the end of text"""
        text = "Here is an ![image](https://example.com/img.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://example.com/img.png")], matches)
    
    # ===== Image Alt Text Variations =====
    
    def test_extract_markdown_images_empty_alt_text(self):
        """Test image with empty alt text"""
        text = "![](https://example.com/image.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "https://example.com/image.png")], matches)
    
    def test_extract_markdown_images_alt_text_with_spaces(self):
        """Test image alt text with multiple spaces"""
        text = "![alt text with spaces](https://example.com/img.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("alt text with spaces", "https://example.com/img.png")], matches)
    
    def test_extract_markdown_images_alt_text_with_numbers(self):
        """Test image alt text with numbers"""
        text = "![image 2024](https://example.com/img.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image 2024", "https://example.com/img.png")], matches)
    
    def test_extract_markdown_images_alt_text_with_special_chars(self):
        """Test image alt text with special characters"""
        text = "![my-image_1](https://example.com/img.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("my-image_1", "https://example.com/img.png")], matches)
    
    # ===== URL Variations =====
    
    def test_extract_markdown_images_url_with_query_params(self):
        """Test image URL with query parameters"""
        text = "![image](https://example.com/img.png?size=large&format=png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://example.com/img.png?size=large&format=png")], matches)
    
    def test_extract_markdown_images_url_with_fragment(self):
        """Test image URL with fragment identifier"""
        text = "![image](https://example.com/img.png#section1)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://example.com/img.png#section1")], matches)
    
    def test_extract_markdown_images_relative_url(self):
        """Test image with relative URL"""
        text = "![image](../assets/image.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "../assets/image.png")], matches)
    
    def test_extract_markdown_images_local_file_url(self):
        """Test image with local file URL"""
        text = "![image](./images/pic.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "./images/pic.jpg")], matches)
    
    # ===== Edge Cases =====
    
    def test_extract_markdown_images_no_images(self):
        """Test text with no images"""
        text = "This is plain text with no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)
    
    def test_extract_markdown_images_empty_string(self):
        """Test empty string"""
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)
    
    def test_extract_markdown_images_text_with_brackets(self):
        """Test that regular text with brackets is not matched"""
        text = "Text with [brackets] but no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)
    
    def test_extract_markdown_images_consecutive_images(self):
        """Test consecutive images without text between"""
        text = "![img1](https://example.com/1.png)![img2](https://example.com/2.png)"
        matches = extract_markdown_images(text)
        expected = [
            ("img1", "https://example.com/1.png"),
            ("img2", "https://example.com/2.png")
        ]
        self.assertListEqual(expected, matches)
    
    def test_extract_markdown_images_many_images(self):
        """Test extracting many images"""
        text = "".join([
            "![img1](url1.png)",
            " text ",
            "![img2](url2.png)",
            " more ",
            "![img3](url3.png)",
            " and ",
            "![img4](url4.png)"
        ])
        matches = extract_markdown_images(text)
        expected = [
            ("img1", "url1.png"),
            ("img2", "url2.png"),
            ("img3", "url3.png"),
            ("img4", "url4.png")
        ]
        self.assertListEqual(expected, matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    
    # ===== Basic Link Extraction =====
    
    def test_extract_markdown_links_single_link(self):
        """Test extracting a single link"""
        text = "This is text with a [link](https://www.example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://www.example.com")], matches)
    
    def test_extract_markdown_links_multiple_links(self):
        """Test extracting multiple links"""
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(expected, matches)
    
    def test_extract_markdown_links_at_start(self):
        """Test link at the start of text"""
        text = "[example](https://example.com) is a great site"
        matches = extract_markdown_links(text)
        self.assertListEqual([("example", "https://example.com")], matches)
    
    def test_extract_markdown_links_at_end(self):
        """Test link at the end of text"""
        text = "Check out [this site](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("this site", "https://example.com")], matches)
    
    # ===== Link Text Variations =====
    
    def test_extract_markdown_links_empty_anchor_text(self):
        """Test link with empty anchor text"""
        text = "[](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("", "https://example.com")], matches)
    
    def test_extract_markdown_links_anchor_with_spaces(self):
        """Test link anchor text with multiple spaces"""
        text = "[click here for more info](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("click here for more info", "https://example.com")], matches)
    
    def test_extract_markdown_links_anchor_with_numbers(self):
        """Test link anchor text with numbers"""
        text = "[link 123](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link 123", "https://example.com")], matches)
    
    def test_extract_markdown_links_anchor_with_special_chars(self):
        """Test link anchor text with special characters"""
        text = "[my-link_text](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("my-link_text", "https://example.com")], matches)
    
    # ===== URL Variations =====
    
    def test_extract_markdown_links_url_with_path(self):
        """Test link URL with path"""
        text = "[docs](https://example.com/docs/guide)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("docs", "https://example.com/docs/guide")], matches)
    
    def test_extract_markdown_links_url_with_query_params(self):
        """Test link URL with query parameters"""
        text = "[search](https://example.com/search?q=test&sort=date)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("search", "https://example.com/search?q=test&sort=date")], matches)
    
    def test_extract_markdown_links_url_with_fragment(self):
        """Test link URL with fragment identifier"""
        text = "[section](https://example.com/docs#introduction)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("section", "https://example.com/docs#introduction")], matches)
    
    def test_extract_markdown_links_relative_url(self):
        """Test link with relative URL"""
        text = "[docs](../docs/README.md)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("docs", "../docs/README.md")], matches)
    
    def test_extract_markdown_links_email_url(self):
        """Test link with email URL"""
        text = "[contact](mailto:test@example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("contact", "mailto:test@example.com")], matches)
    
    # ===== Image vs Link Distinction =====
    
    def test_extract_markdown_links_does_not_match_images(self):
        """Test that images are not matched as links"""
        text = "Here is an ![image](https://example.com/img.png) not a link"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links_mixed_images_and_links(self):
        """Test text with both images and links"""
        text = "![img](url.png) and [link](url.com) in text"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "url.com")], matches)
    
    # ===== Edge Cases =====
    
    def test_extract_markdown_links_no_links(self):
        """Test text with no links"""
        text = "This is plain text with no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links_empty_string(self):
        """Test empty string"""
        matches = extract_markdown_links("")
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links_text_with_brackets(self):
        """Test that unmatched brackets don't create false matches"""
        text = "Text with (parentheses) but no [complete] links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links_consecutive_links(self):
        """Test consecutive links without text between"""
        text = "[link1](url1.com)[link2](url2.com)"
        matches = extract_markdown_links(text)
        expected = [
            ("link1", "url1.com"),
            ("link2", "url2.com")
        ]
        self.assertListEqual(expected, matches)
    
    def test_extract_markdown_links_many_links(self):
        """Test extracting many links"""
        text = "".join([
            "[link1](url1.com)",
            " text ",
            "[link2](url2.com)",
            " more ",
            "[link3](url3.com)",
            " and ",
            "[link4](url4.com)"
        ])
        matches = extract_markdown_links(text)
        expected = [
            ("link1", "url1.com"),
            ("link2", "url2.com"),
            ("link3", "url3.com"),
            ("link4", "url4.com")
        ]
        self.assertListEqual(expected, matches)
    
    # ===== Complex Real-World Cases =====
    
    def test_extract_markdown_links_real_markdown_document(self):
        """Test extraction from a more realistic markdown snippet"""
        text = """
# Welcome

Check out [our documentation](https://docs.example.com) for more info.

You can also visit [our blog](https://blog.example.com) or 
[contact us](mailto:support@example.com) for questions.
        """
        matches = extract_markdown_links(text)
        expected = [
            ("our documentation", "https://docs.example.com"),
            ("our blog", "https://blog.example.com"),
            ("contact us", "mailto:support@example.com")
        ]
        self.assertListEqual(expected, matches)


class TestExtractMarkdownCombined(unittest.TestCase):
    """Tests for both functions working together"""
    
    def test_extract_both_in_same_text(self):
        """Test extracting both images and links from same text"""
        text = "Check ![image](img.png) and [link](url.com)"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        self.assertListEqual([("image", "img.png")], images)
        self.assertListEqual([("link", "url.com")], links)
    
    def test_extract_complex_document(self):
        """Test extracting from a complex markdown document"""
        text = """
# Title

Here's an ![logo](logo.png).

Links: [google](https://google.com) and [github](https://github.com)

Another image: ![screenshot](screen.jpg)

Final link: [docs](README.md)
        """
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        expected_images = [
            ("logo", "logo.png"),
            ("screenshot", "screen.jpg")
        ]
        expected_links = [
            ("google", "https://google.com"),
            ("github", "https://github.com"),
            ("docs", "README.md")
        ]
        
        self.assertListEqual(expected_images, images)
        self.assertListEqual(expected_links, links)


if __name__ == "__main__":
    unittest.main()
