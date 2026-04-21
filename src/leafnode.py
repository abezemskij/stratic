from htmlnode import HTMLNode

class LeafNode(HTMLNode):
	def __init__(self, tag=None, value=None, properties=None):
		super().__init__(tag, value, None, properties)

	def to_html(self):
		if not self.value or self.value == "":
			raise ValueError()
		if not self.tag:
			return self.value
		if not self.properties:
			return f"<{self.tag}>{self.value}</{self.tag}>"
		return f"<{self.tag} {self.properties_to_html()}>{self.value}</{self.tag}>"

	def __repr__(self):
		return f"LeafNode({self.tag}, {self.value}, {self.properties})"
