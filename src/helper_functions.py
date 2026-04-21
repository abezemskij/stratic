from htmlnode import *
from textnode import * 
import re
import os
import shutil

def copy_directory_contents(src_dir, dest_dir):
    # Check if the destination directory exists; if so, delete it
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)  # Create an empty destination directory

    # Walk through the source directory recursively
    for root, dirs, files in os.walk(src_dir):
        # Calculate the relative path for each file or directory in the source
        relative_path = os.path.relpath(root, src_dir)
        # Determine the destination directory for the current folder
        current_dest_dir = os.path.join(dest_dir, relative_path)

        # Create directories in the destination
        if not os.path.exists(current_dest_dir):
            os.mkdir(current_dest_dir)
        
        # Loop through and copy each file
        for file_name in files:
            src_file_path = os.path.join(root, file_name)
            dest_file_path = os.path.join(current_dest_dir, file_name)
            
            # Log the copying process
            print(f"Copying {src_file_path} to {dest_file_path}")
            
            # Copy the file
            shutil.copy(src_file_path, dest_file_path)

def extract_title(markdown):
	out = ""
	list_lines = markdown.split('\n')
	for line in list_lines:
		if line.startswith('#'):
			return line[1:].strip()
		else:
			continue

	raise Exception("No title in markdown")

def generate_page(from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	MAX_FILE = 10000

	if not os.path.exists(from_path):
		raise Exception("From path doesn't exist")

	if not os.path.exists(template_path):
		raise Exception("Template path doesn't exist")

	markdown = ""
	template = ""
	with open(from_path) as f:
		markdown = f.read(MAX_FILE)

	with open(template_path) as f:
		template = f.read(MAX_FILE)

	html_string = markdown_to_html_node(markdown).to_html()
	#print(html_string)
	title = extract_title(markdown)
	template = template.replace("{{ Title }}", title)
	template = template.replace("{{ Content }}", html_string)

	dir_path = os.path.dirname(dest_path)
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

	with open(dest_path, 'w') as f:
		f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
	if not os.path.exists(dir_path_content):
		raise Exception("From path doesn't exist")

	for instance in os.listdir(dir_path_content):
		instance_path = os.path.join(dir_path_content, instance)
		#print(f"instance_path: {instance_path}")
		if os.path.isdir(instance_path):
			generate_pages_recursive(instance_path, template_path, dest_dir_path)
		elif os.path.isfile(instance_path) and instance.endswith(".md"):
			generate_page(instance_path, template_path, dest_dir_path + '/' + instance_path[instance_path.find('/')+1:].replace('.md', '.html'))
			#print(f"generate_page({instance_path}, {template_path}, {dest_dir_path + '/' + instance_path[instance_path.find('/')+1:].replace('.md', '.html')})")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT_PLAIN:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT_PLAIN))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
	matches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
	return matches

def extract_markdown_links(text):
	matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
	return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT_PLAIN:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT_PLAIN))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.TEXT_IMAGE,
                    image[1],
                )
            )
            #print(new_nodes)
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT_PLAIN))
    return new_nodes



def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT_PLAIN:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT_PLAIN))
            new_nodes.append(TextNode(link[0], TextType.TEXT_LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT_PLAIN))
    return new_nodes

def text_to_textnodes(text):
	ret_list = [TextNode(text, TextType.TEXT_PLAIN)]
	ret_list = split_nodes_delimiter(ret_list, "**", TextType.TEXT_BOLD)
	ret_list = split_nodes_delimiter(ret_list, "_", TextType.TEXT_ITALIC)
	ret_list = split_nodes_delimiter(ret_list, "`", TextType.TEXT_CODE)
	ret_list = split_nodes_image(ret_list)
	ret_list = split_nodes_link(ret_list)
	return ret_list


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]



def split_markdown_blocks(markdown):
    # Normalize newlines (convert all to \n)
    markdown = markdown.replace("\r\n", "\n").replace("\r", "\n")

    # Split by double newlines (Markdown convention for separating blocks)
    blocks = markdown.split("\n\n")

    # Trim surrounding whitespace for each block
    blocks = [block.strip() for block in blocks if block.strip()]

    return blocks

def block_to_block_type(block):
    # Heading (1-6 levels)
    if block.startswith("#"):
        return "heading"

    # Code block (triple backticks or indented code)
    elif block.startswith("```") or block.startswith("    "):  # Checking for indented code
        return "code"

    # Blockquote (lines starting with '>')
    elif block.startswith(">"):
        return "quote"

    # List (either ordered or unordered)
    elif block.startswith("-") or block[0].isdigit() and block[1] == ".":
        return "ul" if block.startswith("-") else "ol"

    # Paragraph (fallback, anything else)
    return "paragraph"

def markdown_to_html_node(markdown):
    blocks = split_markdown_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        # PARAGRAPH
        if block_type == "paragraph":
            # collapse newlines into spaces
            text = " ".join(block.splitlines()).strip()
            children.append(
                ParentNode("p", text_to_children(text))
            )

        # HEADING
        elif block_type == "heading":
            level = len(block) - len(block.lstrip("#"))
            text = block[level:].strip()
            children.append(
                ParentNode(f"h{level}", text_to_children(text))
            )

        # CODE BLOCK (special case)
        elif block_type == "code":
            # remove ``` wrapping
            lines = block.split("\n")
            code_text = "\n".join(lines[1:-1]) + "\n"

            code_node = text_node_to_html_node(
                TextNode(code_text, TextType.TEXT_CODE)
            )
            children.append(
                ParentNode("pre", [code_node])
            )

        # QUOTE
        elif block_type == "quote":
            lines = [line.lstrip("> ").strip() for line in block.splitlines()]
            text = " ".join(lines)
            children.append(
                ParentNode("blockquote", text_to_children(text))
            )

        # UNORDERED LIST
        elif block_type == "ul":
            items = []
            for line in block.splitlines():
                text = line.lstrip("- ").strip()
                items.append(ParentNode("li", text_to_children(text)))
            children.append(ParentNode("ul", items))

        # ORDERED LIST
        elif block_type == "ol":
            items = []
            for line in block.splitlines():
                # remove "1. ", "2. ", etc.
                text = line.split(".", 1)[1].strip()
                items.append(ParentNode("li", text_to_children(text)))
            children.append(ParentNode("ol", items))

        else:
            raise ValueError(f"Unknown block type: {block_type}")

    return ParentNode("div", children)

#def generate_page(from_path, template_path, dest_path):
#generate_page("../content/index.md", "template.html", "...")