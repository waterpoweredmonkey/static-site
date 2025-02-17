from conversion import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType
import unittest

class TestConversion(unittest.TestCase):

    def test_split_nodes_delimiter_bold_single(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_bold_single_at_start(self):
        node = TextNode("**This** is text with a bold block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This", TextType.BOLD),
            TextNode(" is text with a bold block word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_bold_multiple(self):
        node = TextNode("This is text with a **bold block** some non bold **bold block 2** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" some non bold ", TextType.TEXT),
            TextNode("bold block 2", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_bold_multiple_no_gap(self):
        node = TextNode("This is text with a **bold block****bold block 2** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode("bold block 2", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_italic_single(self):
        node = TextNode("This is text with a *italic block* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_italic_multiple(self):
        node = TextNode("This is text with a *italic block* some non italic *italic block 2* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" some non italic ", TextType.TEXT),
            TextNode("italic block 2", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_italic_multiple_no_gap(self):
        node = TextNode("This is text with a *italic block**italic block 2* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode("italic block 2", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_code_single(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_bold_multiple(self):
        node = TextNode("This is text with a `code block` some non code `code block 2` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" some non code ", TextType.TEXT),
            TextNode("code block 2", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_code_multiple_no_gap(self):
        node = TextNode("This is text with a `code block``code block 2` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode("code block 2", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_all_splits_bold(self):
        node = TextNode("This is **text** with *all* types of `block` in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with *all* types of `block` in it", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_all_but_bold_splits_italic(self):
        node = TextNode("This is text with *all* types of `block` in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("all", TextType.ITALIC),
            TextNode(" types of `block` in it", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_all_splits_code(self):
        node = TextNode("This is **text** with *all* types of `block` in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is **text** with *all* types of ", TextType.TEXT),
            TextNode("block", TextType.CODE),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_all_used_recursively(self):
        node = TextNode("This is **text** with *all* types of `block` in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_delimiter([node], "`", TextType.CODE),
                "**", TextType.BOLD,
            ),
            "*", TextType.ITALIC
        )
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with ", TextType.TEXT),
            TextNode("all", TextType.ITALIC),
            TextNode(" types of ", TextType.TEXT),
            TextNode("block", TextType.CODE),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_all_used_reversed(self):
        new_nodes = [TextNode("This is `text` with *all* types of **block** in it", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE),
        new_nodes = split_nodes_delimiter(new_nodes[0], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.CODE),
            TextNode(" with ", TextType.TEXT),
            TextNode("all", TextType.ITALIC),
            TextNode(" types of ", TextType.TEXT),
            TextNode("block", TextType.BOLD),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_extract_markdown_images(self):
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        actual = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [to boot dev](https://www.boot.dev)")
        self.assertEqual(expected, actual)

    def test_extract_markdown_images_on_mixed_text(self):
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        actual = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(expected, actual)

    def test_extract_markdown_links(self):
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        actual = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(expected, actual)
    
    def test_extract_markdown_links_mixed(self):
        expected = [("to boot dev", "https://www.boot.dev")]
        actual = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and ![rick roll](https://i.imgur.com/aKaOqIh.gif)")
        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()