import unittest
from parentnode import ParentNode
from leafnode import LeafNode


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


if __name__ == "__main__":
    unittest.main()
