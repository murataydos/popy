from .po_exceptions import InvalidFilePath
from .message_entry import MessageEntry


class PoFile(object):

	def __init__(self, path=None, messages=None):
		self.path = path
		self.messages = messages if messages else []

	def get_messages(self):
		lines = self._get_file_content()
		self.messages = self._parse_blocks(lines)
		return self.messages

	def write_messages(self):
		content = ""
		for message in self.messages:
			content += message.__str__() + '\n'
		self._write_file(content)

	def _parse_blocks(self, lines):
		message_blocks = []
		block = []
		for line in lines:
			if not len(line.strip()):
				message_blocks.append(MessageEntry.from_lines(block))
				block = []
			else:
				block.append(line)
		return message_blocks

	def _get_file_content(self):
		if not self.path:
			raise InvalidFilePath()
		f = open(self.path, 'r+')
		lines = f.readlines()
		f.close()
		return lines

	def _write_file(self, content):
		if not self.path:
			raise InvalidFilePath()
		f = open(self.path, 'w+')
		f.write(content)
		f.close()
