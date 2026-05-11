from blocks import BlockType, block_to_block_type, markdown_to_blocks
from conversion import text_to_textnodes
from htmlnode import LeafNode, ParentNode
from textnode import text_node_to_html_node


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return list(map(text_node_to_html_node, text_nodes))


def create_heading_node(block):
    heading, text = block.split(" ", 1)
    return ParentNode(f"h{len(heading)}", text_to_children(text))


def create_paragraph_node(block):
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))


def create_blockquote_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    return ParentNode("blockquote", text_to_children(content))


def create_ordered_list_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        parts = line.split(". ", 1)
        children.append(ParentNode("li", text_to_children(parts[1])))
    return ParentNode("ol", children)


def create_unordered_list_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        children.append(ParentNode("li", text_to_children(line[2:])))
    return ParentNode("ul", children)


def create_code_node(block):
    code_node = LeafNode("code", block.strip("`\n"))
    return ParentNode("pre", [code_node])


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return create_paragraph_node(block)
    if block_type == BlockType.HEADING:
        return create_heading_node(block)
    if block_type == BlockType.CODE:
        return create_code_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return create_ordered_list_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return create_unordered_list_node(block)
    if block_type == BlockType.QUOTE:
        return create_blockquote_node(block)
    raise ValueError("invalid block type")


def markdown_to_html_node(markdown):
    children = []

    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        node = block_to_html_node(block)
        children.append(node)

    return ParentNode("div", children)
