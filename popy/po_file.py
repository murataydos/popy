import codecs

from .po_exceptions import InvalidFilePath
from .message_entry import MessageEntry


class PoFile(object):

	def __init__(self, path=None, messages=None):
		self.path = path
		self.messages = messages if messages else []

	def get_messages(self):
		if not self.messages:
			self.messages = self.read_messages()
		return self.messages

	def read_messages(self):
		lines = self._get_file_content()
		return self._parse_blocks(lines)

	def write_messages(self):
		content = ""
		for message in self.messages:
			content += message.__str__() + '\n'
		self._write_file(content)

	def fix_newline_matching(self):
		self.get_messages()
		for message in self.messages:
			message.fix_newline_matching()

	def _parse_blocks(self, lines):
		message_blocks = []
		block = []
		found_header = False
		for line in lines:
			if not found_header:
				if line.startswith('msgid ""'):
					found_header = True
				else:
					continue
			if not len(line.strip()):
				message_blocks.append(MessageEntry.from_lines(block))
				block = []
			else:
				block.append(line)
		return message_blocks

	def _get_file_content(self):
		if not self.path:
			raise InvalidFilePath()
		f = codecs.open(self.path, 'r+', encoding='utf-8')
		lines = f.readlines()
		f.close()
		return lines

	def _write_file(self, content):
		if not self.path:
			raise InvalidFilePath()
		f = codecs.open(self.path, 'w+', encoding='utf-8')
		f.write(content)
		f.close()
