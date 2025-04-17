import re

from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type
from htmlnode import ParentNode
from textnode import TextNode, TextType, HeadingNode, text_node_to_html_node


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Found opening delimiter without matching closing delimiter")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_link(nodes):
    return split_node_for_link_type(nodes, extract_markdown_links, TextType.LINK, format_markdown_link)

def format_markdown_link(link):
    return f"[{link[0]}]({link[1]})"

def split_nodes_image(nodes):
    return split_node_for_link_type(nodes, extract_markdown_images, TextType.IMAGE, format_markdown_image)

def format_markdown_image(link):
    return f"![{link[0]}]({link[1]})"

def split_node_for_link_type(nodes, extract, link_type, format_markdown):
    new_nodes = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract(text)

        if not links:
            new_nodes.append(node)
            continue

        for link in links:
            if not text: # check text is not empty, raise error
                raise ValueError("ran out of text to process")
            formatted_link = format_markdown(link)
            link_start = text.find(formatted_link)
            if link_start > 0:
                new_nodes.append(TextNode(text[:link_start], TextType.TEXT))
            
            new_nodes.append(TextNode(link[0], link_type, link[1]))

            link_len = len(formatted_link)
            text = text[link_start + link_len:]
        
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_image(new_nodes)
    return split_nodes_link(new_nodes)

def heading_to_headingnode(heading):
    heading_parts = heading.split(" ", 1)
    heading_type = heading_parts[0]
    heading_text = heading_parts[1]
    return HeadingNode(heading_text, len(heading_type))

def block_to_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_htmlnode(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_htmlnode(block)
    if block_type == BlockType.QUOTE:
        return quote_to_htmlnode(block)
    if block_type == BlockType.ULIST:
        return ulist_to_htmlnode(block)
    if block_type == BlockType.OLIST:
        return olist_to_htmlnode(block)
    raise ValueError(f"Unknown block type: {block_type}")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_htmlnode(paragraph):
    lines = paragraph.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(heading):
    level = 0
    for char in heading:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(heading):
        raise ValueError(f"invalid heading level: {level}")
    text = heading[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_htmlnode(code):
    if not code.startswith("```") or not code.endswith("```"):
        raise ValueError("invalid code block")
    text = code[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def quote_to_htmlnode(quote):
    lines = quote.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def ulist_to_htmlnode(ulist):
    items = ulist.split("\n")
    html_nodes = []
    for item in items:
        text = item[2:]  # strip the "- " from the front of the item
        children = text_to_children(text)
        html_nodes.append(ParentNode("li", children))
    return ParentNode("ul", html_nodes)

def olist_to_htmlnode(olist):
    items = olist.split("\n")
    html_nodes = []
    for item in items:
        text = item[3:]  # strip the "\d. " from the front of the item
        children = text_to_children(text)
        html_nodes.append(ParentNode("li", children))
    return ParentNode("ol", html_nodes)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        node = block_to_node(block)
        nodes.append(node)
    return ParentNode("div", nodes, None)