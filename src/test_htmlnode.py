import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):

    def test_fields(self):
        expected_tag = "expectedTag"
        expected_value = "expectedValue"
        node = HTMLNode(expected_tag, expected_value)

        self.assertEqual(node.tag, expected_tag)
        self.assertEqual(node.value, expected_value)

    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        props_in = {
            "a": "b",
            "c": "d"
        }
        node = HTMLNode(props=props_in)
        self.assertEqual(
            node.props_to_html(),
            " a=\"b\" c=\"d\""
        )

    def test_props_to_html_when_not_set(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

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

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)


    def test_to_html_parent_w_n_nested_parents(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "p",
                    [ 
                        ParentNode("p", [ LeafNode(None, "Normal text") ]),
                    ]
                ),
                ParentNode("p", [ LeafNode(None, "Normal text") ]),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = "<p><p><p>Normal text</p></p><p>Normal text</p>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_parent_w_empty_children(self):
        node = ParentNode("p",[])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_parent_w_none_children(self):
        node = ParentNode("p",None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_parent_w_nested_parents_w_o_children(self):
        node = ParentNode("p",[ParentNode("p", [])])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_tag_none(self):
        node = ParentNode(None, [ LeafNode(None, "Normal text") ])
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()