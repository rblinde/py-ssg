from textnode import TextNode, TextType
import re

REGEX_IMAGE = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
REGEX_LINK = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"


def extract_markdown_images(text):
    return re.findall(REGEX_IMAGE, text)


def extract_markdown_links(text):
    return re.findall(REGEX_LINK, text)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        count = node.text.count(delimiter)
        if count % 2 != 0:
            raise ValueError("invalid markdown format")

        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.PLAIN))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def _split_nodes_image_link_helper(old_nodes, extract_fn, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        images = extract_fn(node.text)
        if not images:
            new_nodes.append(node)
            continue

        text = node.text
        for alt, url in images:
            splitter = (
                f"![{alt}]({url})" if text_type == TextType.IMAGE else f"[{alt}]({url})"
            )
            parts = text.split(splitter, 1)
            nodes = [
                TextNode(parts[0], TextType.PLAIN),
                TextNode(alt, text_type, url),
            ]
            for node in nodes:
                if node.text == "":
                    continue
                new_nodes.append(node)
            text = parts[1]

        if text != "":
            new_nodes.append(TextNode(text, TextType.PLAIN))

    return new_nodes


def split_nodes_image(old_nodes):
    return _split_nodes_image_link_helper(
        old_nodes, extract_markdown_images, TextType.IMAGE
    )


def split_nodes_link(old_nodes):
    return _split_nodes_image_link_helper(
        old_nodes, extract_markdown_links, TextType.LINK
    )


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes
