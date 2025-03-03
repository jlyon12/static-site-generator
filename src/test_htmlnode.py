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


if __name__ == "__main__":
    unittest.main()
