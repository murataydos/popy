from .po_exceptions import InvalidMessageEntry


class MessageEntry(object):

    TRANSLATOR_COMMENT_PREFIX = '# '
    EXTRACTED_COMMENT_PREFIX = '#. '
    REFERENCE_PREFIX = '#: '
    FLAG_PREFIX = '#, '
    FUZZY_PREFIX = '#~ '

    def __init__(self, msgid, msgstr, msgid_plural=None, msgctxt=None,
                 translator_comments=None, extracted_comments=None, references=None, 
                 flags=None, is_fuzzy=False):
        self.msgid = msgid
        self.msgstr = msgstr if isinstance(msgstr, list) else [msgstr]
        self.msgid_plural = msgid_plural
        self.msgctxt = msgctxt
        self.translator_comments = translator_comments
        self.extracted_comments = extracted_comments
        self.references = references
        self.flags = flags
        self.is_fuzzy = is_fuzzy

    @property
    def translator_comments_text(self):
        return '{}\n'.format('\n'.join([self.TRANSLATOR_COMMENT_PREFIX + comment for comment in self.translator_comments])) \
            if self.translator_comments else ''

    @property
    def extracted_comments_text(self):
        return '{}\n'.format('\n'.join([self.EXTRACTED_COMMENT_PREFIX + comment for comment in self.extracted_comments])) \
            if self.extracted_comments else ''

    @property
    def references_text(self):
        return '{}\n'.format('\n'.join([self.REFERENCE_PREFIX + reference for reference in self.references])) \
            if self.references else ''

    @property
    def flags_text(self):
        return '{}\n'.format('\n'.join([self.FLAG_PREFIX + flag for flag in self.flags])) \
            if self.flags else ''

    @property
    def msgstr_text(self):
        if not self.msgstr:
            if self.msgid_plural:
                return 'msgstr[0] ""\n'
            return 'msgstr ""\n'
        elif len(self.msgstr) == 1 and not self.msgid_plural:
            if len(self.msgid):
                return 'msgstr "{}"\n'.format(self.msgstr[0])
            return 'msgstr ""\n' + '{}\n'.format('\n'.join(['"{}\\n"'.format(header) \
                for header in self.msgstr[0].split('\\n') if header]))
        return '{}\n'.format('\n'.join(['msgstr[{}] "{}"'.format(index, value) \
            for index, value in enumerate(self.msgstr)]))

    @property
    def msgid_text(self):
        return 'msgid "{}"\n'.format(self.msgid)

    @property
    def msgid_plural_text(self):
        return 'msgid_plural "{}"\n'.format(self.msgid_plural) if self.msgid_plural else ''

    @property
    def msgctxt_text(self):
        return 'msgctxt "{}"\n'.format(self.msgctxt) if self.msgctxt else ''

    def fix_newline_matching(self):
        if not len(self.msgid) or not len(self.msgstr) or not len(self.msgstr[0]):
            return
        num_beginning_newlines, num_ending_newlines, _ = self.count_newlines_and_strip(self.msgid)
        self.msgstr[0] = self.add_newlines(self.msgstr[0], num_beginning_newlines, num_ending_newlines)

        if self.msgid_plural and len(self.msgstr) > 1:
            num_beginning_newlines, num_ending_newlines, _ = self.count_newlines_and_strip(self.msgid_plural)
            for index, msg in enumerate(self.msgstr[1:]):
                self.msgstr[index + 1] = self.add_newlines(msg, num_beginning_newlines, num_ending_newlines)

    def count_newlines_and_strip(self, msg):
        num_beginning_newlines = 0
        num_ending_newlines = 0
        while msg.startswith('\\n'):
            num_beginning_newlines += 1
            msg = msg[2:]
        while msg.endswith('\\n'):
            num_ending_newlines += 1
            msg = msg[:-2]
        return num_beginning_newlines, num_ending_newlines, msg

    def add_newlines(self, msg, num_beginning_newlines, num_ending_newlines):
        _, _, msg = self.count_newlines_and_strip(msg)
        return ''.join(['\\n' for i in range(0, num_beginning_newlines)]) + msg + \
            ''.join(['\\n' for i in range(0, num_ending_newlines)])

    def __str__(self):
        return self.translator_comments_text + self.extracted_comments_text + \
            self.references_text + self.flags_text + self.msgctxt_text + self.msgid_text + \
            self.msgid_plural_text + self.msgstr_text

    @classmethod
    def remove_fuzzy_prefix(cls, fuzzy_lines):
        lines = []
        is_fuzzy = False
        for line in fuzzy_lines:
            if line.startswith(cls.FUZZY_PREFIX):
                is_fuzzy = True
                lines.append(line[len(cls.FUZZY_PREFIX):])
            else:
                lines.append(line)
        return lines, is_fuzzy

    @classmethod
    def from_lines(cls, lines):
        if len(lines) < 2:
            raise InvalidMessageEntry()
        msgid = None
        msgid_plural = None
        msgctxt = None
        msgstr = []
        translator_comments = []
        extracted_comments = []
        references = []
        flags = []
        previous_line_type = None
        last_msgstr_index = -1
        lines, is_fuzzy = cls.remove_fuzzy_prefix(lines)
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                if line.startswith(cls.TRANSLATOR_COMMENT_PREFIX):
                    translator_comments.append(line[2:])
                elif line.startswith(cls.EXTRACTED_COMMENT_PREFIX):
                    extracted_comments.append(line[3:])
                elif line.startswith(cls.REFERENCE_PREFIX):
                    references.append(line[3:])
                elif line.startswith(cls.FLAG_PREFIX):
                    flags.append(line[3:])
            else:
                if line.startswith('msgid '):
                    previous_line_type = 'msgid'
                    msgid = line[7:-1] if len(line[7:]) > 1 else ''
                elif line.startswith('msgid_plural'):
                    previous_line_type = 'msgid_plural'
                    msgid_plural = line[14:-1] if len(line[14:]) > 1 else ''
                elif line.startswith('msgstr'):
                    last_msgstr_index += 1
                    previous_line_type = 'msgstr'
                    msgstr.append(line[line.index('"') + 1:-1] if len(line[line.index('"'):]) > 1 else '')
                elif line.startswith('msgctxt'):
                    previous_line_type = 'msgctxt'
                    msgid = line[9:-1] if len(line[9:]) > 1 else ''
                elif line.startswith('"'):
                    if previous_line_type == 'msgid':
                        msgid += line[1:-1] if len(line) > 2 else ''
                    elif previous_line_type == 'msgid_plural':
                        msgid_plural += line[1:-1] if len(line) > 2 else ''
                    elif previous_line_type == 'msgctxt':
                        msgctxt += line[1:-1] if len(line) > 2 else ''
                    elif previous_line_type == 'msgstr':
                        msgstr[last_msgstr_index] += line[1:-1] if len(line) > 2 else ''
                    else:
                        raise InvalidMessageEntry()
                else:
                    raise InvalidMessageEntry()

        return cls(msgid, msgstr, msgid_plural, msgctxt, translator_comments,
                   extracted_comments, references, flags, is_fuzzy)
