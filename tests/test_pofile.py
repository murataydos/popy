import os
import sys
import unittest

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(file_path))

from popy import po_file


class TestPoFile(unittest.TestCase):

    def setUp(self):
        self.static_path = os.path.join(file_path, 'tests', 'static')
        self.po_file = po_file.PoFile(path=os.path.join(self.static_path, 'sample.po'))

    def test_get_messages(self):
        messages = self.po_file.get_messages()
        self.assertEqual(len(messages), 7)
        self.assertEqual(messages[1].msgid,
                         'There are many strings in a po file\\nsome contain only one line\\n' + \
                         'and some contain many...')
        self.assertTrue(messages[5].is_fuzzy)
        self.assertEqual(messages[5].msgid, 'A fuzzy message.')


if __name__ == '__main__':
    unittest.main()
