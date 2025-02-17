import unittest

from leafnode import LeafNode
from parentnode import ParentNode

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