import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):

    # Test equality of two TextNode instances with the same text, type, and URL
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    # Test equality with different text types
    def test_eq_different_text_type(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    # Test equality with a different URL
    def test_eq_no_url(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT, "https://archlinux.org")
        self.assertNotEqual(node, node2)

    # Test inequality when the URL differs
    def test_eq_different_url(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://url1.com")
        node2 = TextNode("This is a text node", TextType.TEXT, "https://url2.com")
        self.assertNotEqual(node, node2)

    # Test a TextNode with no URL (URL should default to None)
    def test_text_node_without_url(self):
        node = TextNode("No URL here", TextType.BOLD)
        self.assertEqual(node.url, None)

    # Test a TextNode with a URL
    def test_text_node_with_url(self):
        node = TextNode("This is a link", TextType.LINK, "https://example.com")
        self.assertEqual(node.url, "https://example.com")

    # Test two different TextNode instances with the same URL
    def test_eq_same_url_different_type(self):
        node = TextNode("Link to example", TextType.LINK, "https://example.com")
        node2 = TextNode("Another example", TextType.LINK, "https://example.com")
        self.assertNotEqual(node, node2)

    # Test invalid text_type (should raise an error)
    def test_invalid_text_type(self):
        with self.assertRaises(ValueError):
            TextNode("Invalid type", "invalid")

    # Test the string representation of a TextNode
    def test_repr(self):
        node = TextNode("Some code here", TextType.CODE)
        self.assertEqual(repr(node), "TextNode('Some code here', 'code', None)")

    # Test to ensure that an empty string as text is allowed
    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        self.assertEqual(node.text, "")

    # Test that the `text_type` is correctly handled
    def test_text_type_enum(self):
        node = TextNode("Italic text", TextType.ITALIC)
        self.assertEqual(node.text_type, TextType.ITALIC)


if __name__ == "__main__":
    unittest.main()
