import unittest
from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
