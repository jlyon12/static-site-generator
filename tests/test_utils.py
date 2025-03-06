import unittest
from src.textnode import TextNode, TextType
from src.utils import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_link,
    split_nodes_image,
)


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


class TestExtractMarkdownImages(unittest.TestCase):
    # Test case with a single markdown image
    def test_single_image(self):
        text = "![Alt text](https://example.com/image.jpg)"
        expected = [("Alt text", "https://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    # Test case with multiple markdown images
    def test_multiple_images(self):
        text = "![First](https://example.com/1.jpg) and ![Second](https://example.com/2.png)"
        expected = [
            ("First", "https://example.com/1.jpg"),
            ("Second", "https://example.com/2.png"),
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    # Test case with no markdown images in the text
    def test_no_images(self):
        text = "This is just a normal text without any images."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    # Test case with mixed content: some text and one markdown image
    def test_mixed_content(self):
        text = "Some text ![Valid](https://example.com/image.jpg) and some more text."
        expected = [("Valid", "https://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    # Test case with markdown image containing special characters in the alt text
    def test_images_with_special_characters(self):
        text = "![Alt (with) special](https://example.com/image.jpg)"
        expected = [("Alt (with) special", "https://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    # Test case with markdown image containing spaces in the alt text or URL
    def test_images_with_spaces(self):
        text = "![Space Alt](https://example.com/my image.jpg)"
        expected = [("Space Alt", "https://example.com/my image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    # Test case with markdown image URL containing query parameters
    def test_images_with_query_params(self):
        text = "![Query](https://example.com/image.jpg?width=100&height=200)"
        expected = [("Query", "https://example.com/image.jpg?width=100&height=200")]
        self.assertEqual(extract_markdown_images(text), expected)

    # Test case with markdown image containing escaped characters in the alt text
    def test_images_with_escaped_characters(self):
        text = r"![Escaped \[bracket\]](https://example.com/escaped.jpg)"
        expected = [("Escaped \\[bracket\\]", "https://example.com/escaped.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)


class TestExtractMarkdownLinks(unittest.TestCase):

    # Test basic link extraction [anchor](url)
    def test_basic_link_extraction(self):
        text = "This is a [link](https://example.com)."
        expected = [("link", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    # Test multiple links extraction [anchor1](url1) and [anchor2](url2)
    def test_multiple_links_extraction(self):
        text = "Here is a [first link](https://example1.com) and a [second link](https://example2.com)."
        expected = [
            ("first link", "https://example1.com"),
            ("second link", "https://example2.com"),
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    # Test input with no links to ensure empty list is returned
    def test_no_links(self):
        text = "This text has no links."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    # Test mixed text and links to ensure only links are extracted
    def test_mixed_text_and_links(self):
        text = "Some text and a [link](https://example.com) and more text."
        expected = [("link", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    # Test links with special characters in the anchor text
    def test_links_with_special_characters_in_anchor(self):
        text = "This is a [link with (special)](https://example.com)."
        expected = [("link with (special)", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    # Test links with spaces in the URL
    def test_links_with_spaces_in_url(self):
        text = "This is a [link with spaces](https://example.com/my page)."
        expected = [("link with spaces", "https://example.com/my page")]
        self.assertEqual(extract_markdown_links(text), expected)

    # Test links with query parameters in the URL
    def test_links_with_query_params_in_url(self):
        text = "This is a [query link](https://example.com/search?q=test)."
        expected = [("query link", "https://example.com/search?q=test")]
        self.assertEqual(extract_markdown_links(text), expected)

    # Test links with escaped characters in the anchor text
    def test_links_with_escaped_characters_in_anchor(self):
        text = r"This is a [escaped \[bracket\]](https://example.com/escaped)."
        expected = [("escaped \\[bracket\\]", "https://example.com/escaped")]
        self.assertEqual(extract_markdown_links(text), expected)


class TestSplitNodesLink(unittest.TestCase):
    # Test case for when there are no links in the text
    def test_no_links(self):
        old_nodes = [TextNode("Just a normal text.", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(new_nodes, old_nodes)

    # Test case for a single link in the text
    def test_single_link(self):
        old_nodes = [TextNode("Check this [link](http://example.com).", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        expected = [
            TextNode("Check this ", TextType.TEXT),
            TextNode("link", TextType.LINK, "http://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    # Test case for multiple links in the text
    def test_multiple_links(self):
        old_nodes = [
            TextNode(
                "See [Google](http://google.com) and [Bing](http://bing.com).",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_link(old_nodes)
        expected = [
            TextNode("See ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "http://google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("Bing", TextType.LINK, "http://bing.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    # Test case for text only before a link
    def test_text_only_before_link(self):
        old_nodes = [TextNode("Before [link](http://example.com)", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        expected = [
            TextNode("Before ", TextType.TEXT),
            TextNode("link", TextType.LINK, "http://example.com"),
        ]
        self.assertEqual(new_nodes, expected)

    # Test case for text only after a link
    def test_text_only_after_link(self):
        old_nodes = [TextNode("[link](http://example.com) after", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        expected = [
            TextNode("link", TextType.LINK, "http://example.com"),
            TextNode(" after", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    # Test case for mixed nodes containing text and links separately
    def test_mixed_nodes(self):
        old_nodes = [
            TextNode("Some text before.", TextType.TEXT),
            TextNode("[link](http://example.com)", TextType.TEXT),
            TextNode("Some text after.", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(old_nodes)
        expected = [
            TextNode("Some text before.", TextType.TEXT),
            TextNode("link", TextType.LINK, "http://example.com"),
            TextNode("Some text after.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    # Test case for non-text nodes to ensure they are not modified
    def test_non_text_nodes(self):
        old_nodes = [
            TextNode("Some text.", TextType.TEXT),
            TextNode("Code snippet", TextType.CODE),
            TextNode("More text with [link](http://example.com).", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(old_nodes)
        expected = [
            TextNode("Some text.", TextType.TEXT),
            TextNode("Code snippet", TextType.CODE),
            TextNode("More text with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "http://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    # Test handling an empty text node
    def test_empty_text_node(self):
        old_nodes = [TextNode("", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    # Test multiple adjacent links in the same text node
    def test_multiple_adjacent_links(self):
        old_nodes = [
            TextNode(
                "[link1](http://example1.com)[link2](http://example2.com)",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_link(old_nodes)
        expected = [
            TextNode("link1", TextType.LINK, "http://example1.com"),
            TextNode("link2", TextType.LINK, "http://example2.com"),
        ]
        self.assertEqual(new_nodes, expected)

    # Test multiple adjacent links with surrounding text
    def test_multiple_adjacent_links_with_text(self):
        old_nodes = [
            TextNode(
                "Click [here](http://example.com) and [there](http://example.org)",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_link(old_nodes)
        expected = [
            TextNode("Click ", TextType.TEXT),
            TextNode("here", TextType.LINK, "http://example.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("there", TextType.LINK, "http://example.org"),
        ]
        self.assertEqual(new_nodes, expected)

    # Test handling an empty list of nodes
    def test_empty_list(self):
        old_nodes = []
        new_nodes = split_nodes_link(old_nodes)
        expected = []
        self.assertEqual(new_nodes, expected)


class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        # Test handling a single image within text
        old_nodes = [
            TextNode("An image: ![alt](http://example.com/img.jpg)", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(old_nodes)
        expected = [
            TextNode("An image: ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "http://example.com/img.jpg"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_adjacent_images(self):
        # Test handling multiple images appearing next to each other
        old_nodes = [
            TextNode(
                "![img1](http://example.com/1.jpg)![img2](http://example.com/2.jpg)",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_image(old_nodes)
        expected = [
            TextNode("img1", TextType.IMAGE, "http://example.com/1.jpg"),
            TextNode("img2", TextType.IMAGE, "http://example.com/2.jpg"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_image_with_surrounding_text(self):
        # Test handling an image with text before and after
        old_nodes = [
            TextNode("Before ![img](http://example.com/img.jpg) after", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(old_nodes)
        expected = [
            TextNode("Before ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "http://example.com/img.jpg"),
            TextNode(" after", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_images(self):
        # Test handling text with no images
        old_nodes = [TextNode("Just some text.", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(new_nodes, old_nodes)

    def test_non_text_nodes(self):
        # Test handling non-text nodes
        old_nodes = [
            TextNode("Some text.", TextType.TEXT),
            TextNode("Code block", TextType.CODE),
            TextNode("Another ![img](http://example.com/img.jpg) here.", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(old_nodes)
        expected = [
            TextNode("Some text.", TextType.TEXT),
            TextNode("Code block", TextType.CODE),
            TextNode("Another ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "http://example.com/img.jpg"),
            TextNode(" here.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_empty_text_node(self):
        # Test handling an empty text node
        old_nodes = [TextNode("", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(new_nodes, old_nodes)


if __name__ == "__main__":
    unittest.main()
