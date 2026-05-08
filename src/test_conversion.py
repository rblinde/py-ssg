import unittest

from conversion import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestExtractMarkdownImages(unittest.TestCase):
    def test_empty(self):
        result = extract_markdown_images("")
        want = []
        self.assertEqual(result, want)

    def test_single(self):
        result = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        )
        want = [("rick roll", ("https://i.imgur.com/aKaOqIh.gif"))]
        self.assertEqual(result, want)

    def test_double(self):
        result = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
            + " and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        want = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(result, want)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_empty(self):
        result = extract_markdown_links("")
        want = []
        self.assertEqual(result, want)

    def test_single(self):
        result = extract_markdown_links(
            "This is text with an [example](https://example.com)"
        )
        want = [("example", ("https://example.com"))]
        self.assertEqual(result, want)

    def test_double(self):
        result = extract_markdown_links(
            "This is text with a [example](https://example.com) and [google](https://google.com)"
        )
        want = [("example", "https://example.com"), ("google", "https://google.com")]
        self.assertEqual(result, want)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_empty(self):
        new = split_nodes_delimiter([], "**", TextType.BOLD)
        want = []
        self.assertEqual(new, want)

    def test_no_text_nodes(self):
        node_bold = TextNode("lorem ipsum etcetera", TextType.BOLD)
        node_italic = TextNode("lorem ipsum etcetera", TextType.ITALIC)
        new = split_nodes_delimiter([node_bold, node_italic], "**", TextType.BOLD)
        want = [node_bold, node_italic]
        self.assertEqual(new, want)

    def test_invalid(self):
        node = TextNode("This is text with a `code block word", TextType.PLAIN)
        self.assertRaises(ValueError, split_nodes_delimiter, [node], "`", TextType.CODE)

    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        want = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertEqual(result, want)

    def test_bold(self):
        node = TextNode("This is some **bold text**", TextType.PLAIN)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        want = [
            TextNode("This is some ", TextType.PLAIN),
            TextNode("bold text", TextType.BOLD),
        ]
        self.assertEqual(result, want)

    def test_italic(self):
        node = TextNode("This is some _italic text_ yeah!", TextType.PLAIN)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        want = [
            TextNode("This is some ", TextType.PLAIN),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" yeah!", TextType.PLAIN),
        ]
        self.assertEqual(result, want)

    def test_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        want = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(want, new_nodes)

    def test_double_bold(self):
        node = TextNode("Text with a **bolded** word and **another**", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        want = [
            TextNode("Text with a ", TextType.PLAIN),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word and ", TextType.PLAIN),
            TextNode("another", TextType.BOLD),
        ]
        self.assertEqual(want, new_nodes)


class TestSplitNodesImages(unittest.TestCase):
    def test_empty(self):
        result = split_nodes_image([])
        want = []
        self.assertEqual(result, want)

    def test_no_images(self):
        node = TextNode("lorem ipsum etcetera", TextType.PLAIN)
        result = split_nodes_image([node])
        want = [node]
        self.assertEqual(result, want)

    def test_no_text_nodes(self):
        node_bold = TextNode("lorem ipsum etcetera", TextType.BOLD)
        node_italic = TextNode("lorem ipsum etcetera", TextType.ITALIC)
        result = split_nodes_image([node_bold, node_italic])
        want = [node_bold, node_italic]
        self.assertEqual(result, want)

    def test_single(self):
        node = TextNode(
            "Text with image ![example](https://example.com)",
            TextType.PLAIN,
        )
        result = split_nodes_image([node])
        want = [
            TextNode("Text with image ", TextType.PLAIN),
            TextNode("example", TextType.IMAGE, "https://example.com"),
        ]
        self.assertEqual(result, want)

    def test_multiple(self):
        node = TextNode(
            "Text with image ![example](https://example.com) and ![another](https://example.com).",
            TextType.PLAIN,
        )
        result = split_nodes_image([node])
        want = [
            TextNode("Text with image ", TextType.PLAIN),
            TextNode("example", TextType.IMAGE, "https://example.com"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("another", TextType.IMAGE, "https://example.com"),
            TextNode(".", TextType.PLAIN),
        ]
        self.assertEqual(result, want)

    def test_image_and_link(self):
        node = TextNode(
            "Text with image ![example](https://example.com) and [link](https://example.com)",
            TextType.PLAIN,
        )
        result = split_nodes_image([node])
        want = [
            TextNode("Text with image ", TextType.PLAIN),
            TextNode("example", TextType.IMAGE, "https://example.com"),
            TextNode(" and [link](https://example.com)", TextType.PLAIN),
        ]
        self.assertEqual(result, want)


class TestSplitNodesLinks(unittest.TestCase):
    def test_empty(self):
        result = split_nodes_link([])
        want = []
        self.assertEqual(result, want)

    def test_no_links(self):
        node = TextNode("lorem ipsum etcetera", TextType.PLAIN)
        result = split_nodes_link([node])
        want = [node]
        self.assertEqual(result, want)

    def test_no_text_nodes(self):
        node_bold = TextNode("lorem ipsum etcetera", TextType.BOLD)
        node_italic = TextNode("lorem ipsum etcetera", TextType.ITALIC)
        result = split_nodes_link([node_bold, node_italic])
        want = [node_bold, node_italic]
        self.assertEqual(result, want)

    def test_single(self):
        node = TextNode(
            "Text with [example](https://example.com)",
            TextType.PLAIN,
        )
        result = split_nodes_link([node])
        want = [
            TextNode("Text with ", TextType.PLAIN),
            TextNode("example", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(result, want)

    def test_multiple(self):
        node = TextNode(
            "Text with [example](https://example.com) and [another](https://example.com).",
            TextType.PLAIN,
        )
        result = split_nodes_link([node])
        want = [
            TextNode("Text with ", TextType.PLAIN),
            TextNode("example", TextType.LINK, "https://example.com"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("another", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.PLAIN),
        ]
        self.assertEqual(result, want)

    def test_image_and_link(self):
        node = TextNode(
            "Text with image ![example](https://example.com) and [link](https://example.com)",
            TextType.PLAIN,
        )
        result = split_nodes_link([node])
        want = [
            TextNode(
                "Text with image ![example](https://example.com) and ", TextType.PLAIN
            ),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(result, want)


class TestTextToTextNodes(unittest.TestCase):
    def test_empty(self):
        result = text_to_textnodes("")
        want = []
        self.assertEqual(result, want)

    def test_all(self):
        result = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` "
            + "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            + "and a [link](https://boot.dev)"
        )
        want = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, want)
