import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html_no_props(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>") 

    def test_link_to_html(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_to_html_value_none(self):
        node = LeafNode("a", props= {"href": "https://www.google.com"})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag(self):
        node = LeafNode(value="Click me!", props={"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "Click me!")

if __name__ == "__main__":
    unittest.main()