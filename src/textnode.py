from enum import Enum

class TextType(Enum):
	TEXT_PLAIN = 0
	TEXT_BOLD = 1
	TEXT_ITALIC = 2
	TEXT_CODE = 3
	TEXT_LINK = 4
	TEXT_IMAGE = 5

class TextNode():
	def __init__(self, text, text_type, url=None):
		self.text = text
		self.text_type = text_type
		self.url = url
		if url:
			self.url = url

	def __eq__(self, compare_to):
		if not self or not compare_to:
			return False
		if self.text != compare_to.text:
			return False
		if self.text_type != compare_to.text_type:
			return False
		if self.url:
			if self.url != compare_to.url:
				return False

		return True

	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type}, {self.url})"
