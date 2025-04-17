from conversion import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_link,
    split_nodes_image,
    text_to_textnodes,
    markdown_to_html_node
)
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

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_returns_originals_when_no_links_present(self):
        expected = [
            TextNode("This is text without a link ", TextType.TEXT),
            TextNode("neither node has a link", TextType.TEXT),
            TextNode("neither does this bold text", TextType.BOLD),
        ]
        self.assertEqual(split_nodes_image(expected), expected)

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        actual = text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
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
        self.assertEqual(expected, actual)

    def test_text_to_textnodes_w_o_links(self):
        actual = text_to_textnodes("This is **text** with an *italic* word and a `code block`")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE)
        ]
        self.assertEqual(expected, actual)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )


if __name__ == "__main__":
    unittest.main()