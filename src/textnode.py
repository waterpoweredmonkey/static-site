from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    HEADING = "heading"

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (
            isinstance(other, TextNode)
            and self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def text_node_to_html_node(text_node):
    type = text_node.text_type.value
    match type:
        case TextType.TEXT.value:
            return LeafNode(None, text_node.text)
        case TextType.BOLD.value:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC.value:
            return LeafNode("i", text_node.text)
        case TextType.CODE.value:
            return LeafNode("code", text_node.text)
        case TextType.LINK.value:
            return LeafNode("a", text_node.text, { "href": text_node.url })
        case TextType.IMAGE.value:
            return LeafNode("img", "", { "src": text_node.url, "alt": text_node.text })
        case _:
            print(text_node.text_type)
            raise NotImplementedError

def text_nodes_to_html_nodes(nodes):
    html_nodes = []
    for text_node in nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes

class HeadingNode:
    def __init__(self, text, level):
        self.text = text
        self.level = level

    def __eq__(self, other):
        return (
                isinstance(other, TextNode)
                and self.text == other.text
                and self.level == other.level
        )

    def __repr__(self):
        return f"HeadingNode({self.text}, {self.level})"

def heading_node_to_html_node(heading_node):
    return LeafNode(f"h{heading_node.level}", heading_node.text)


# todo
#  add node for the following & convert blocks to node
#   - code node
#   - quote node
#   - ulist node
#   - olist node