import os
import sys
import unittest

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(file_path))

from popy import message_entry


class TestMessageEntry(unittest.TestCase):

    def setUp(self):
        self.message_entry = message_entry.MessageEntry(
            msgid='Some msgid',
            msgstr=['Sample msgstr'])

    def test_translator_comments_text(self):
        self.message_entry.translator_comments = ['Comment 1', 'Comment 2']
        self.assertEqual(self.message_entry.translator_comments_text, '# Comment 1\n# Comment 2\n')

    def test_extracted_comments_text(self):
        self.message_entry.extracted_comments = ['Comment 1', 'Comment 2', 'Comment 3']
        self.assertEqual(
            self.message_entry.extracted_comments_text,
            '#. Comment 1\n#. Comment 2\n#. Comment 3\n')

    def test_references_text(self):
        self.message_entry.references = ['Reference 1', 'Reference 2']
        self.assertEqual(
            self.message_entry.references_text,
            '#: Reference 1\n#: Reference 2\n')

    def test_flags_text(self):
        self.message_entry.flags = ['Flag 1', 'Flag 2']
        self.assertEqual(
            self.message_entry.flags_text,
            '#, Flag 1\n#, Flag 2\n')

    def test_msgstr_text_empty(self):
        self.message_entry.msgstr = []
        self.assertEqual(self.message_entry.msgstr_text, 'msgstr ""\n')

    def test_msgstr_text_signular(self):
        self.assertEqual(self.message_entry.msgstr_text, 'msgstr "Sample msgstr"\n')
        self.message_entry.msgstr = ['Msgid hasn\'t been translated yet!']
        self.assertEqual(self.message_entry.msgstr_text,
                         'msgstr "Msgid hasn\'t been translated yet!"\n')

    def test_msgstr_text_plural(self):
        self.message_entry.msgstr = ['MSGSTR singular', 'MSGSTR plural']
        self.assertEqual(self.message_entry.msgstr_text,
                         'msgstr[0] "MSGSTR singular"\nmsgstr[1] "MSGSTR plural"\n')

    def test_msgstr_text_header(self):
        self.message_entry.msgid = ''
        self.message_entry.msgstr = [
            'Project-Id-Version: base\\nReport-Msgid-Bugs-To:\\n' + \
            'Language-Team: Spanish\\nLanguage: es\\nMIME-Version: 1.0\\n'
        ]
        self.assertEqual(
            self.message_entry.msgstr_text,
            'msgstr ""\n"Project-Id-Version: base\\n"\n"Report-Msgid-Bugs-To:\\n"\n' +
            '"Language-Team: Spanish\\n"\n"Language: es\\n"\n"MIME-Version: 1.0\\n"\n')

    def test_msgid_text(self):
        self.assertEqual(self.message_entry.msgid_text, 'msgid "Some msgid"\n')

    def test_msgid_plural_text(self):
        self.message_entry.msgid_plural = 'You have N notifications'
        self.assertEqual(self.message_entry.msgid_plural_text,
                         'msgid_plural "You have N notifications"\n')

    def test_msgctxt_text(self):
        self.message_entry.msgctxt = 'Sample message context'
        self.assertEqual(self.message_entry.msgctxt_text,
                         'msgctxt "Sample message context"\n')

    def test_fix_newline_matching_singular(self):
        self.message_entry.msgid = '\\nBegins with one newline'
        self.message_entry.msgstr = ['Ends with one newline\\n']
        self.message_entry.fix_newline_matching()
        self.assertEqual(self.message_entry.msgstr, ['\\nEnds with one newline'])

        self.message_entry.msgid = '\\nBegins and ends with one newline\\n'
        self.message_entry.msgstr = ['Ends with two newlines\\n\\n']
        self.message_entry.fix_newline_matching()
        self.assertEqual(self.message_entry.msgstr, ['\\nEnds with two newlines\\n'])

        self.message_entry.msgid = '\\n\\nBegins and ends with two newlines\\n\\n'
        self.message_entry.msgstr = ['\\nEnds with five newlines\\n\\n\\n\\n\\n']
        self.message_entry.fix_newline_matching()
        self.assertEqual(self.message_entry.msgstr, ['\\n\\nEnds with five newlines\\n\\n'])

    def test_fix_newline_matching_plural(self):
        self.message_entry.msgid = '\\nBegins with one newline'
        self.message_entry.msgid_plural = '\\n\\nBegins with two newlines'
        self.message_entry.msgstr = ['Ends with one newline\\n', 'Ends with two newlines\\n\\n']
        self.message_entry.fix_newline_matching()
        self.assertEqual(self.message_entry.msgstr,
                         ['\\nEnds with one newline', '\\n\\nEnds with two newlines'])

        self.message_entry.msgid = '\\nBegins and ends with one newline\\n'
        self.message_entry.msgid_plural = '\\n\\n\\nBegins and ends with three newlines\\n\\n\\n'
        self.message_entry.msgstr = ['Ends with two newline\\n\\n', 'Ends with two newlines\\n\\n']
        self.message_entry.fix_newline_matching()
        self.assertEqual(
            self.message_entry.msgstr,
            ['\\nEnds with two newline\\n', '\\n\\n\\nEnds with two newlines\\n\\n\\n'])

    def test_count_newlines_and_strip(self):
        self.assertEqual(
            self.message_entry.count_newlines_and_strip('\\n\\nSample Message\\n'),
            (2, 1, 'Sample Message'))

        self.assertEqual(
            self.message_entry.count_newlines_and_strip('\\n\\n\\nSample Message\\n\\n\\n\\n'),
            (3, 4, 'Sample Message'))

        self.assertEqual(
            self.message_entry.count_newlines_and_strip('Sample Message'),
            (0, 0, 'Sample Message'))

    def test_add_newlines(self):
        msg = 'No newline'
        self.assertEqual(self.message_entry.add_newlines(msg, 1, 3),
                         '\\nNo newline\\n\\n\\n')
        self.assertEqual(self.message_entry.add_newlines(msg, 2, 0),
                         '\\n\\nNo newline')
        self.assertEqual(self.message_entry.add_newlines(msg, 0, 2),
                         'No newline\\n\\n')

    def test_str_(self):
        self.message_entry.translator_comments = ['Translator comment']
        self.message_entry.extracted_comments = ['Extracted comment']
        self.message_entry.references = ['Reference']
        self.message_entry.flags = ['Flag 1', 'Flag 2']
        self.message_entry.msgctxt = 'Message context'
        self.message_entry.msgid = 'Sample message id'
        self.message_entry.msgid_plural = 'Sample plural message id'
        self.message_entry.msgstr = ['Singular translation', 'Plural translation']
        self.assertEqual(
            self.message_entry.__str__(),
            '# Translator comment\n#. Extracted comment\n#: Reference\n#, Flag 1\n#, Flag 2\n' +
            'msgctxt "Message context"\nmsgid "Sample message id"\n' + \
            'msgid_plural "Sample plural message id"\nmsgstr[0] "Singular translation"\n' +
            'msgstr[1] "Plural translation"\n')

    def test_from_lines_singular(self):
        lines = [
            '#: test.py:139',
            'msgid "Sample text"',
            'msgstr "Ornek yazi"'
        ]
        message = message_entry.MessageEntry.from_lines(lines)
        self.assertEqual(message.references, ['test.py:139'])
        self.assertEqual(message.msgid, 'Sample text')
        self.assertEqual(message.msgstr, ['Ornek yazi'])

        lines = [
            '# Translator comment',
            '#. Extracted comment',
            '#, Flag 1',
            '#, Flag 2',
            'msgctxt "Message context"',
            'msgid ""',
            '"Sample message id "',
            '"with multiple lines"',
            'msgstr ""',
            '"Sample message string "',
            '"with multiple lines"'
        ]
        message = message_entry.MessageEntry.from_lines(lines)
        self.assertEqual(message.references, [])
        self.assertEqual(message.flags, ['Flag 1', 'Flag 2'])
        self.assertEqual(message.translator_comments, ['Translator comment'])
        self.assertEqual(message.extracted_comments, ['Extracted comment'])
        self.assertEqual(message.msgid, 'Sample message id with multiple lines')
        self.assertEqual(message.msgstr, ['Sample message string with multiple lines'])

    def test_from_lines_plural(self):
        lines = [
            '#: test.py:171',
            'msgid "Sample text"',
            'msgid_plural "Sample plural text"',
            'msgstr[0] "Ornek yazi"',
            'msgstr[1] "Ornek cogul yazi"'
        ]
        message = message_entry.MessageEntry.from_lines(lines)
        self.assertEqual(message.references, ['test.py:171'])
        self.assertEqual(message.msgid, 'Sample text')
        self.assertEqual(message.msgid_plural, 'Sample plural text')
        self.assertEqual(message.msgstr, ['Ornek yazi', 'Ornek cogul yazi'])
        self.assertEqual(message.is_fuzzy, False)

    def test_from_lines_plural_fuzzy(self):
        lines = [
            '#~ #: test.py:171',
            '#~ msgid "Sample text"',
            '#~ msgid_plural "Sample plural text"',
            '#~ msgstr[0] "Ornek yazi"',
            '#~ msgstr[1] "Ornek cogul yazi"'
        ]
        message = message_entry.MessageEntry.from_lines(lines)
        self.assertEqual(message.references, ['test.py:171'])
        self.assertEqual(message.msgid, 'Sample text')
        self.assertEqual(message.msgid_plural, 'Sample plural text')
        self.assertEqual(message.msgstr, ['Ornek yazi', 'Ornek cogul yazi'])
        self.assertEqual(message.is_fuzzy, True)

    def test_remove_fuzzy_prefix(self):
        fuzzy_lines = [
            '#~ msgid "Test"',
            '#~ msgstr "Fuzzy"'
        ]
        lines, is_fuzzy = message_entry.MessageEntry.remove_fuzzy_prefix(fuzzy_lines)
        self.assertEqual(lines, ['msgid "Test"', 'msgstr "Fuzzy"'])
        self.assertEqual(is_fuzzy, True)


if __name__ == '__main__':
    unittest.main()
