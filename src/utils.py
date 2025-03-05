import re
from src.textnode import TextType, TextNode
from src.leafnode import LeafNode


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": f"{text_node.url}"})
        case TextType.IMAGE:
            return LeafNode(
                "img", "", {"src": f"{text_node.url}", "alt": f"{text_node.text}"}
            )
        case _:
            raise Exception("Invalid Type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            segments = node.text.split(delimiter)
            if len(segments) == 1:
                new_nodes.append(node)
            else:
                if len(segments) % 2 == 0:
                    raise ValueError(
                        f"Invalid markdown: Unpaired delimiter {delimiter}"
                    )
                for i, segment in enumerate(segments):
                    if i % 2 == 0:
                        if segment:
                            new_nodes.append(TextNode(segment, TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(segment, text_type))
    return new_nodes


def extract_markdown_images(text):
    alt_url_pairs = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return alt_url_pairs


def extract_markdown_links(text):
    link_url_pairs = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return link_url_pairs
