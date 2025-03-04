import unittest
from src.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    # Test for basic leaf node HTML generation
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    # Test with properties added to the tag
    def test_leaf_to_html_p_with_props(self):
        node = LeafNode("p", "Hello, world!", {"id": "unique"})
        self.assertEqual(node.to_html(), '<p id="unique">Hello, world!</p>')

    # Test with no tag provided
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    # Test with no tag and properties provided
    def test_leaf_to_html_no_tag_with_props(self):
        node = LeafNode(None, "Hello, world!", {"id": "unique"})
        self.assertEqual(node.to_html(), "Hello, world!")

    # Test for empty string as value
    def test_leaf_to_html_empty_string(self):
        node = LeafNode("p", "")
        self.assertEqual(node.to_html(), "<p></p>")

    # Test for long value
    def test_leaf_to_html_long_value(self):
        long_string = "a" * 1000  # A very long string
        node = LeafNode("p", long_string)
        self.assertEqual(node.to_html(), f"<p>{long_string}</p>")

    # Test for invalid tag type (not a string)
    def test_invalid_tag_type(self):
        with self.assertRaises(ValueError):
            LeafNode(123, "Invalid tag type")

    # Test for multiple properties
    def test_leaf_to_html_multiple_props(self):
        node = LeafNode(
            "a", "Click here", {"href": "https://example.com", "target": "_blank"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://example.com" target="_blank">Click here</a>',
        )

    # Test for nested tags
    def test_leaf_to_html_nested(self):
        child_node = LeafNode("span", "Nested Text")
        node = LeafNode("div", "Parent Text", {"class": "parent"})
        node_with_child = (
            f'<div class="parent">Parent Text<span>Nested Text</span></div>'
        )
        self.assertEqual(node.to_html(), '<div class="parent">Parent Text</div>')
        self.assertEqual(child_node.to_html(), "<span>Nested Text</span>")

    # Test for invalid value type (not a string)
    def test_invalid_value_type(self):
        with self.assertRaises(ValueError):
            LeafNode("p", 123)


if __name__ == "__main__":
    unittest.main()
