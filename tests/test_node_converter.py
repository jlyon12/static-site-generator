import unittest
from src.textnode import TextNode, TextType
from src.node_converter import text_node_to_html_node


class TestTextToHtmlNode(unittest.TestCase):
    # Test conversion of a normal text node without formatting
    def test_text(self):
        text_node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    # Test conversion of a bold text node
    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>bold text</b>")

    # Test conversion of an italic text node
    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<i>italic text</i>")

    # Test conversion of a code text node
    def test_text_node_to_html_node_code(self):
        text_node = TextNode("print('Hello')", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<code>print('Hello')</code>")

    # Test conversion of a hyperlink text node
    def test_text_node_to_html_node_link(self):
        text_node = TextNode("Arch Linux", TextType.LINK, "http://archlinux.org")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(
            html_node.to_html(), '<a href="http://archlinux.org">Arch Linux</a>'
        )

    # Test conversion of an image text node with alt text
    def test_text_node_to_html_node_image(self):
        text_node = TextNode(
            "Arch Linux Logo", TextType.IMAGE, "http://archlinux.org/logo.png"
        )
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(
            html_node.to_html(),
            '<img src="http://archlinux.org/logo.png" alt="Arch Linux Logo"></img>',
        )

    # Test handling of an invalid text type
    def test_text_node_to_html_node_invalid_type(self):
        with self.assertRaises(Exception):
            text_node = TextNode("Invalid", "invalid_type")
            text_node_to_html_node(text_node)


if __name__ == "__main__":
    unittest.main()
