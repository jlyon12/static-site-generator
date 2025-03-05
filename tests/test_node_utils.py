import unittest
from src.textnode import TextNode, TextType
from src.node_utils import text_node_to_html_node, split_nodes_delimiter


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


class TestSplitDelimiter(unittest.TestCase):

    # Test basic bold splitting (**)
    def test_basic_bold_split(self):
        old_nodes = [
            TextNode(
                "This is text with a **bolded phrase** in the middle", TextType.TEXT
            )
        ]
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD), expected
        )

    # Test basic italic splitting (_)
    def test_basic_italic_split(self):
        old_nodes = [TextNode("This is _italic_ text", TextType.TEXT)]
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, "_", TextType.ITALIC), expected
        )

    # Test basic code splitting (`code`)
    def test_basic_code_split(self):
        old_nodes = [TextNode("This is `inline code` inside text", TextType.TEXT)]
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("inline code", TextType.CODE),
            TextNode(" inside text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(old_nodes, "`", TextType.CODE), expected)

    # Test multiple occurrences of bold, italic, and code

    def test_multiple_delimiter_splits(self):
        old_nodes = [TextNode("**Bold1** normal _Italic1_ `Code1`", TextType.TEXT)]

        # First, split bold (**)
        after_bold_split = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(
            after_bold_split,
            [
                TextNode("Bold1", TextType.BOLD),
                TextNode(" normal _Italic1_ `Code1`", TextType.TEXT),
            ],
        )

        # Then, split italic (_)
        after_italic_split = split_nodes_delimiter(
            after_bold_split, "_", TextType.ITALIC
        )
        self.assertEqual(
            after_italic_split,
            [
                TextNode("Bold1", TextType.BOLD),
                TextNode(" normal ", TextType.TEXT),
                TextNode("Italic1", TextType.ITALIC),
                TextNode(" `Code1`", TextType.TEXT),
            ],
        )

        # Finally, split code (`)
        after_code_split = split_nodes_delimiter(after_italic_split, "`", TextType.CODE)
        self.assertEqual(
            after_code_split,
            [
                TextNode("Bold1", TextType.BOLD),
                TextNode(" normal ", TextType.TEXT),
                TextNode("Italic1", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("Code1", TextType.CODE),
            ],
        )

    # Test handling of unmatched delimiters
    def test_unmatched_delimiters(self):
        for delimiter, text_type in [
            ("**", TextType.BOLD),
            ("_", TextType.ITALIC),
            ("`", TextType.CODE),
        ]:
            with self.assertRaises(ValueError):
                split_nodes_delimiter(
                    [TextNode(f"This {delimiter}is not closed", TextType.TEXT)],
                    delimiter,
                    text_type,
                )

    # Test string with no delimiters
    def test_no_delimiters(self):
        old_nodes = [TextNode("No special formatting here", TextType.TEXT)]
        expected = [TextNode("No special formatting here", TextType.TEXT)]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD), expected
        )

    # Test empty input
    def test_empty_string(self):
        old_nodes = [TextNode("", TextType.TEXT)]
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD), expected
        )

    # Test only delimiters (edge case)
    def test_only_delimiters(self):
        for delimiter in ["**", "_", "`"]:
            with self.assertRaises(ValueError):
                split_nodes_delimiter(
                    [TextNode(delimiter, TextType.TEXT)], delimiter, TextType.BOLD
                )

    # Test multiple nodes where only some contain the delimiter
    def test_mixed_nodes(self):
        old_nodes = [
            TextNode("This is normal text. ", TextType.TEXT),
            TextNode("**Bolded Text**", TextType.TEXT),
            TextNode(" More normal text.", TextType.TEXT),
            TextNode("_Italic_", TextType.TEXT),
        ]
        expected = [
            TextNode("This is normal text. ", TextType.TEXT),
            TextNode("Bolded Text", TextType.BOLD),
            TextNode(" More normal text.", TextType.TEXT),
            TextNode("Italic", TextType.ITALIC),
        ]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD),
            [
                TextNode("This is normal text. ", TextType.TEXT),
                TextNode("Bolded Text", TextType.BOLD),
                TextNode(" More normal text.", TextType.TEXT),
                TextNode("_Italic_", TextType.TEXT),
            ],
        )
        self.assertEqual(
            split_nodes_delimiter(expected, "_", TextType.ITALIC), expected
        )

    # Test input with non-text type nodes (should be ignored)
    def test_non_text_nodes_ignored(self):
        old_nodes = [
            TextNode("This is normal text. ", TextType.TEXT),
            TextNode("**Bolded Text**", TextType.TEXT),
            TextNode("https://example.com", TextType.LINK, "https://example.com"),
        ]
        expected = [
            TextNode("This is normal text. ", TextType.TEXT),
            TextNode("Bolded Text", TextType.BOLD),
            TextNode("https://example.com", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD), expected
        )


if __name__ == "__main__":
    unittest.main()
