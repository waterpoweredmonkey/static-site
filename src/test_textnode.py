import unittest

from enum import Enum
from htmlnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "aUrl")
        node2 = TextNode("This is a text node", TextType.BOLD, "aUrl")
        self.assertEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.IMAGE, "differentUrl")
        node2 = TextNode("This is a text node", TextType.IMAGE, "aUrl")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://boot.dev")
        self.assertEqual("TextNode(This is a text node, TextType.BOLD, http://boot.dev)", repr(node))

class TestTextNodeToHtmlNode(unittest.TestCase):

    def test_text_type(self):
        text_node = TextNode("Some text", TextType.TEXT)
        expected_html_node = LeafNode(value="Some text")
        self.assertEqual(text_node_to_html_node(text_node), expected_html_node)

    def test_bold_type(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        expected_html_node = LeafNode("b", "Bold text")
        self.assertEqual(text_node_to_html_node(text_node), expected_html_node)

    def test_italic_type(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        expected_html_node = LeafNode("i", "Italic text")
        self.assertEqual(text_node_to_html_node(text_node), expected_html_node)

    def test_code_type(self):
        text_node = TextNode("print('Hello')", TextType.CODE)
        expected_html_node = LeafNode("code", "print('Hello')")
        self.assertEqual(text_node_to_html_node(text_node), expected_html_node)

    def test_link_type(self):
        text_node = TextNode("Click here", TextType.LINK, "https://example.com")
        expected_html_node = LeafNode("a", "Click here", {"href": "https://example.com"})
        self.assertEqual(text_node_to_html_node(text_node), expected_html_node)

    def test_image_type(self):
        text_node = TextNode("My Image", TextType.IMAGE, "https://example.com/image.jpg")
        expected_html_node = LeafNode("img", "", {"src": "https://example.com/image.jpg", "alt": "My Image"})
        self.assertEqual(text_node_to_html_node(text_node), expected_html_node)

    def test_text_type_empty_string(self):
        text_node = TextNode("", TextType.TEXT)
        expected_html_node = LeafNode(value="")
        self.assertEqual(text_node_to_html_node(text_node), expected_html_node)

    def test_link_type_no_url(self):
        # Test what happens if URL is None (should still work)
        text_node = TextNode("Click here", TextType.LINK, None)
        expected_html_node = LeafNode("a", "Click here", {"href": None})
        self.assertEqual(text_node_to_html_node(text_node), expected_html_node)

    def test_image_type_empty_text_and_url(self):
        #test what happens if both text and url are empty strings
        text_node = TextNode("", TextType.IMAGE, "")
        expected_html_node = LeafNode("img", "", {"src": "", "alt": ""})
        self.assertEqual(text_node_to_html_node(text_node), expected_html_node)

if __name__ == "__main__":
    unittest.main()