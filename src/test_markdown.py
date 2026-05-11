import unittest

from markdown import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_heading_only(self):
        result = markdown_to_html_node("### heading").to_html()
        want = "<div><h3>heading</h3></div>"
        self.assertEqual(result, want)

    def test_italic_heading(self):
        result = markdown_to_html_node("## _italic_ heading").to_html()
        want = "<div><h2><i>italic</i> heading</h2></div>"
        self.assertEqual(result, want)

    def test_paragraph_only(self):
        result = markdown_to_html_node("_italic_ and **bold** text").to_html()
        want = "<div><p><i>italic</i> and <b>bold</b> text</p></div>"
        self.assertEqual(result, want)

    def test_heading_and_paragraph(self):
        result = markdown_to_html_node(
            "# heading\n\n_italic_ and **bold** text"
        ).to_html()
        want = "<div><h1>heading</h1><p><i>italic</i> and <b>bold</b> text</p></div>"
        self.assertEqual(result, want)

    def test_quote(self):
        result = markdown_to_html_node(
            "> first line of quote\n> _italic_ and **bold** text"
        ).to_html()
        want = (
            "<div><blockquote>first line of quote "
            "<i>italic</i> and <b>bold</b> text</blockquote></div>"
        )
        self.assertEqual(result, want)

    def test_ordered_list(self):
        result = markdown_to_html_node(
            "1. first line of quote\n2. _italic_ and **bold** text"
        ).to_html()
        want = (
            "<div><ol><li>first line of quote</li>"
            "<li><i>italic</i> and <b>bold</b> text</li></ol></div>"
        )
        self.assertEqual(result, want)

    def test_unordered_list(self):
        result = markdown_to_html_node(
            "- first line of quote\n- _italic_ and **bold** text"
        ).to_html()
        want = (
            "<div><ul><li>first line of quote</li>"
            "<li><i>italic</i> and <b>bold</b> text</li></ul></div>"
        )
        self.assertEqual(result, want)

    def test_codeblock(self):
        result = markdown_to_html_node(
            "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"
        ).to_html()

        want = (
            "<div><pre><code>This is text that _should_ remain\n"
            "the **same** even with inline stuff</code></pre></div>"
        )
        self.assertEqual(result, want)
