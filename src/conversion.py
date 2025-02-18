import re
from textnode import TextNode, TextType

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
    new_nodes = split_nodes_image(new_nodes)
    return split_nodes_link(new_nodes)
