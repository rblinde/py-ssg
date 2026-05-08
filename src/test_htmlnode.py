import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode("p")
        want = ""
        self.assertEqual(node.props_to_html(), want)

    def test_props_to_html_single_item(self):
        node = HTMLNode("a", "click here", props={"href": "https://example.com"})
        want = ' href="https://example.com"'
        self.assertEqual(node.props_to_html(), want)

    def test_props_to_html_multiple_items(self):
        node = HTMLNode(
            "a", "click here", props={"href": "https://example.com", "target": "_blank"}
        )
        want = ' href="https://example.com" target="_blank"'
        self.assertEqual(node.props_to_html(), want)

    def test_repr(self):
        node = HTMLNode("p", None, "text here")
        want = "HTMLNode(p, None, text here, None)"
        self.assertEqual(repr(node), want)

    def test_repr_full(self):
        node = HTMLNode("p", "value", "text here", {"href": "https://example.com"})
        want = "HTMLNode(p, value, text here, {'href': 'https://example.com'})"
        self.assertEqual(repr(node), want)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        want = "<p>Hello, world!</p>"
        self.assertEqual(node.to_html(), want)

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        want = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), want)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        want = "Hello, world!"
        self.assertEqual(node.to_html(), want)

    def test_leaf_to_html_no_val(self):
        node = LeafNode("p", "")
        self.failureException(node)


class TestParentNode(unittest.TestCase):
    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        want = "<div><span>child</span></div>"
        self.assertEqual(parent_node.to_html(), want)

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        want = "<div><span><b>grandchild</b></span></div>"
        self.assertEqual(parent_node.to_html(), want)

    def test_parent_to_html_with_multiple_children(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node, grandchild_node])
        want = "<div><span><b>grandchild</b></span><b>grandchild</b></div>"
        self.assertEqual(parent_node.to_html(), want)

    def test_parent_to_html_ultra_nested(self):
        great_grandchild_node = LeafNode("div", "nested")
        grandchild_node = ParentNode("div", [great_grandchild_node])
        child_node = ParentNode("div", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        want = "<div><div><div><div>nested</div></div></div></div>"
        self.assertEqual(parent_node.to_html(), want)

    def test_parent_to_html_no_children(self):
        node = ParentNode("p", [])
        self.failureException(node)


if __name__ == "__main__":
    unittest.main()
