from htmlnode import *
from textnode import * 
import re

def split_nodes_delimiter(nodes, delimiter, text_type):
	if not nodes:
		raise ValueError("Invalid nodes input")
	ret_list = []

	for text_node in nodes:
		#check for for start and end
		#print(f"Debug: {text_node.text.find(delimiter)} and {text_node.text[text_node.text.find(delimiter)+1:].find(delimiter)}")
		#Experiment Implementation
		if text_node.text.find(delimiter) != -1 and text_node.text[text_node.text.find(delimiter)+1:].find(delimiter) != -1:
			#means we have normal delimited block
			#temp = text_node.text.split(delimiter, maxsplit=3)
			#ret_list.append(TextNode(temp[0], text_node.text_type, text_node.url if text_node.url else None))
			#ret_list.append(TextNode(temp[1], text_type, text_node.url if text_node.url else None))
			#ret_list.append(TextNode(temp[2], text_node.text_type, text_node.url if text_node.url else None))
		
		# Working Implementation
			if text_node.text_type != TextType.TEXT_PLAIN:
				ret_list.append(text_node)
				continue

			split_nodes = []
			node_sections = text_node.text.split(delimiter)
			if len(node_sections) % 2 == 0:
				raise ValueError("Should never happen")

			for i in range(len(node_sections)):
				if node_sections[i] == '':
					continue
				if i % 2 == 0:
					split_nodes.append(TextNode(node_sections[i], TextType.TEXT_PLAIN))
				else:
					split_nodes.append(TextNode(node_sections[i], text_type))
			ret_list.extend(split_nodes)
		else:
			raise Exception("Match for delimiter not found")

		return ret_list

def extract_markdown_images(text):
	matches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
	return matches

def extract_markdown_links(text):
	matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
	return matches

def split_nodes_image(nodes):
	if not nodes:
		raise ValueError("Unable to split image, incorrect input provided")
	ret_list = []
	local_copy_nodes = nodes.copy()

	for node in local_copy_nodes:
		# Each node is TextNode
		split_nodes = []
		image_data_extracted = extract_markdown_images(node.text)
		if not image_data_extracted:
			split_nodes.append(node)
			continue

		for image in image_data_extracted:
			split_string = node.text.split(f"![{image[0]}]({image[1]})", maxsplit=1)
			if split_string[0] == "":
				continue
			node.text = node.text.replace(f"![{image[0]}]({image[1]})", "").replace(f"{split_string[0]}", "")
			split_nodes.append(TextNode(split_string[0], TextType.TEXT_PLAIN))
			split_nodes.append(TextNode(f"{image[0]}", TextType.TEXT_IMAGE, f"{image[1]}"))
			#print(split_nodes)
		
		ret_list.extend(split_nodes)		
		
		
	return ret_list



def split_nodes_link(nodes):
	if not nodes:
		raise ValueError("Unable to split image, incorrect input provided")
	ret_list = []
	local_copy_nodes = nodes.copy()

	for node in local_copy_nodes:
		# Each node is TextNode
		split_nodes = []
		image_data_extracted = extract_markdown_links(node.text)
		if not image_data_extracted:
			split_nodes.append(node)
			continue

		for image in image_data_extracted:
			split_string = node.text.split(f"[{image[0]}]({image[1]})", maxsplit=1)
			if split_string[0] == "":
				continue
			node.text = node.text.replace(f"[{image[0]}]({image[1]})", "").replace(f"{split_string[0]}", "")
			split_nodes.append(TextNode(split_string[0], TextType.TEXT_PLAIN))
			split_nodes.append(TextNode(f"{image[0]}", TextType.TEXT_LINK, f"{image[1]}"))
			#print(split_nodes)
		
		ret_list.extend(split_nodes)		
		
		
	return ret_list

def text_to_textnodes(text):
	ret_list = [TextNode(text, TextType.TEXT_PLAIN)]
	ret_list = split_nodes_delimiter(ret_list, "**", TextType.TEXT_BOLD)
	ret_list = split_nodes_delimiter(ret_list, "`", TextType.TEXT_ITALIC)

	return ret_list

test_str = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
print(f"Processed: {text_to_textnodes(test_str)}")
#
#node = TextNode(
#    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
#    TextType.TEXT_PLAIN,
#)
#new_nodes = split_nodes_image([node])
#print(f"Images: {new_nodes}")

#node = TextNode(
#    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
#    TextType.TEXT_PLAIN,
#)
#new_nodes = split_nodes_link([node])
#print(f"Links: {new_nodes}")