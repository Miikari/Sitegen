from enum import Enum
import re
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import text_node_to_html_node, text_to_textnodes, TextNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"

def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED
    if all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED
    
    return BlockType.PARAGRAPH
        
def markdown_to_blocks(markdown):
    new_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        stripped = block.strip()
        if stripped:
            new_blocks.append(stripped)
    return new_blocks
    
def markdown_to_html_node(markdown):
    new_blocks = markdown_to_blocks(markdown)
    childNodes = []
    for block in new_blocks:
        block_type = block_to_block_type(block)
        tag = ""
        if block_type == BlockType.CODE:
            block = block[4:len(block)-3]
            tn = LeafNode("code", block, None)
            pn = ParentNode("pre", [tn], None)
            childNodes.append(pn)
            continue
        if block_type == BlockType.HEADING:
            first_line = block.strip().split("\n")[0]
            match = re.match(r"^(#+)", first_line)
            count = len(match.group(1))
            block = block[count+1:]
            tag =f"h{count}"
        if block_type == BlockType.PARAGRAPH:
            block = block.replace("\n", " ")
            tag = "p"
        if block_type == BlockType.QUOTE:
            blocks = block.split("\n")
            new_blocks = []
            for b in blocks:
                b = b[2:]
                new_blocks.append(b)
            block = " ".join(new_blocks)
            tag = "blockquote"
        if block_type == BlockType.UNORDERED:
            blocks = block.split("\n")
            new_blocks = []
            childs = []
            for b in blocks:
                b = b[2:]
                childs.append(ParentNode("li", text_to_children(b), None))
            
            pn = ParentNode("ul", childs, None)
            childNodes.append(pn)
            continue
        if block_type == BlockType.ORDERED:
            blocks = block.split("\n")
            new_blocks = []
            childs = []
            for b in blocks:
                b = b[3:]
                childs.append(ParentNode("li", text_to_children(b), None))
            
            pn = ParentNode("ol", childs, None)
            childNodes.append(pn)
            continue

        children = text_to_children(block)
        childNodes.append(ParentNode(tag, children, None))

    parNode = ParentNode("div", childNodes, None)

    return parNode

def text_to_children(block):
    blocks = text_to_textnodes(block)
    new_blocks = []
    for block in blocks:
        new_blocks.append(text_node_to_html_node(block))

    return new_blocks

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            line = line[1:]
            return line.strip(" ")
    raise Exception("No title found")

