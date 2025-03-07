from enum import Enum
from src.htmlnode import LeafNode


class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):

        if not isinstance(text_type, TextType):
            raise ValueError(f"Invalid text_type: {text_type}")

        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        return isinstance(value, TextNode) and vars(self) == vars(value)

    def __repr__(self):
        return f"TextNode({self.text!r}, {self.text_type.value!r}, {self.url!r})"


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
