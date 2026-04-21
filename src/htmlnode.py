from textnode import TextNode, TextType

class HTMLNode:
	def __init__(self, tag=None, value=None, children=None, properties=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.properties = properties

	def to_html(self):
		raise NotImplementedError()

	def properties_to_html(self):
		out_string = ""
		if self.properties:
			for item_key, item_value in self.properties.items():
				out_string += f"{item_key}=\"{item_value}\" "
		return out_string

	def __repr__(self):
		return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.properties})"

class LeafNode(HTMLNode):
	def __init__(self, tag=None, value=None, properties=None):
		super().__init__(tag, value, None, properties)

	def to_html(self):
		#if self.value is None:
		#	raise ValueError("invalid HTML: no value")
		#if self.tag is None:
		#	return self.value
		#return f"<{self.tag}{self.properties_to_html()}>{self.value}</{self.tag}>"
		if self.value is None:
			raise ValueError()
		if not self.tag:
			return self.value
		if not self.properties:
			return f"<{self.tag}>{self.value}</{self.tag}>"
		return f"<{self.tag} {self.properties_to_html()}>{self.value}</{self.tag}>"

	def __repr__(self):
		return f"LeafNode({self.tag}, {self.value}, {self.properties})"

class ParentNode(HTMLNode):
	def __init__(self, tag=None, children=None, properties=None):
		super().__init__(tag, None, children, properties)

	def to_html(self):
		if not self.tag:
			print("no tag specified")
			raise ValueError("No tag specified!")
		if not self.children or len(self.children) == 0:
			print("no children")
			raise ValueError("No children nodes provided")
		#print(f"I'm here! {self.children} | {len(self.children)}")
		out_string = f"<{self.tag}>"
		if not self.children:
			out_string += f"{self.value}"
		else:
			for chil in self.children:
				out_string += chil.to_html()
		out_string += f"</{self.tag}>"
		return out_string

def text_node_to_html_node(text_node):
	if not isinstance(text_node, TextNode):
		raise Exception("Invalid TextNode for conversion")
		#__init__(self, tag=None, value=None, properties=None):
	match text_node.text_type:
		case TextType.TEXT_PLAIN:
			return LeafNode(None, text_node.text)
		case TextType.TEXT_BOLD:
			return LeafNode('b', text_node.text)
		case TextType.TEXT_ITALIC:
			return LeafNode('i', text_node.text)
		case TextType.TEXT_CODE:
			return LeafNode("code", text_node.text)
		case TextType.TEXT_LINK:
			return LeafNode('a', text_node.text, {"href": text_node.url})
		case TextType.TEXT_IMAGE:
			return LeafNode('img', '', {"src": text_node.url, "alt": text_node.text})
		case _:
			raise NotImplementedError("No known conversion exists")
