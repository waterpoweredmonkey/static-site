import unittest

from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()