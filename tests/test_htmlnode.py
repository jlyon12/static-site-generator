import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        node = HTMLNode(
            None,
            None,
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_single_prop(self):
        node = HTMLNode(
            None,
            None,
            None,
            {"href": "https://www.google.com"},
        )
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://www.google.com"')

    def test_props_to_html_multi_prop(self):
        node = HTMLNode(
            None,
            None,
            None,
            {
                "href": "https://www.example.com",
                "target": "_blank",
                "class": "btn btn-primary",
                "id": "unique-element",
            },
        )
        result = node.props_to_html()
        self.assertEqual(
            result,
            ' href="https://www.example.com" target="_blank" class="btn btn-primary" id="unique-element"',
        )

    def test_props_to_html_props_is_None(self):
        node = HTMLNode(None, None, None, None)
        result = node.props_to_html()
        self.assertEqual(result, "")

    # Test when props contains an empty dictionary (edge case)
    def test_props_to_html_empty_dict(self):
        node = HTMLNode(None, None, None, {})
        result = node.props_to_html()
        self.assertEqual(result, "")

    # Test when props contains an empty string as a value
    def test_props_to_html_empty_string_value(self):
        node = HTMLNode(None, None, None, {"href": ""})
        result = node.props_to_html()
        self.assertEqual(result, ' href=""')

    # Test when props contains numeric values as strings
    def test_props_to_html_numeric_value(self):
        node = HTMLNode(None, None, None, {"value": "123"})
        result = node.props_to_html()
        self.assertEqual(result, ' value="123"')

    # Test when props contains boolean attributes (e.g., checked, disabled)
    def test_props_to_html_boolean_attributes(self):
        node = HTMLNode(None, None, None, {"checked": "true", "disabled": "false"})
        result = node.props_to_html()
        self.assertEqual(result, ' checked="true" disabled="false"')

    # Test props with special characters (quotes, spaces, etc.)
    def test_props_to_html_special_characters(self):
        node = HTMLNode(
            None, None, None, {"title": 'An "example" title', "class": "special class"}
        )
        result = node.props_to_html()
        self.assertEqual(
            result,
            ' title="An &quot;example&quot; title" class="special class"',
        )


class TestParentNode(unittest.TestCase):

    # Test case for a parent node with one child
    def test_to_html_with_single_child(self):
        child_node = LeafNode("p", "single child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><p>single child</p></div>")

    # Test case for a parent node with multiple children
    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("p", "child 1")
        child_node2 = LeafNode("span", "child 2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(), "<div><p>child 1</p><span>child 2</span></div>"
        )

    # Test case for a parent node with nested children (grandchildren)
    def test_to_html_with_nested_children(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(), "<div><span><b>grandchild</b></span></div>"
        )

    # Test case for an empty children list (should raise ValueError)
    def test_empty_children_list(self):
        with self.assertRaises(ValueError):
            ParentNode("div", [])

    # Test case for children being None (should raise ValueError)
    def test_none_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None)

    # Test case for invalid children type (should raise TypeError)
    def test_invalid_children_type(self):
        with self.assertRaises(TypeError):
            ParentNode("div", "invalid children")

    # Test case where a child is not an instance of HTMLNode (should raise TypeError)
    def test_invalid_child_type(self):
        with self.assertRaises(TypeError):
            ParentNode("div", [LeafNode("p", "valid child"), "invalid child"])

    # Test case for a ParentNode with props
    def test_to_html_with_props(self):
        child_node = LeafNode("p", "child with props")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><p>child with props</p></div>',
        )

    # Test case for ParentNode with no props
    def test_to_html_without_props(self):
        child_node = LeafNode("p", "child without props")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><p>child without props</p></div>")

    # Test case for nested ParentNode with props
    def test_to_html_with_nested_and_props(self):
        child_node = ParentNode(
            "span", [LeafNode("b", "grandchild")], {"class": "child-class"}
        )
        parent_node = ParentNode("div", [child_node], {"id": "parent-id"})
        self.assertEqual(
            parent_node.to_html(),
            '<div id="parent-id"><span class="child-class"><b>grandchild</b></span></div>',
        )


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
