import unittest
from parse import Parser

class ParserTest(unittest.TestCase):
    def setUp(self):
        self.db = StubDb()
        
    def test_db_updated_correctly_from_input_with_depth_2_and_extra_whitespace(self):
        Parser('name', self.db, '\n', ' ').parse(' the   cat  sat  on the  mat \n good    cat ')
        self.assertEqual(self.db.commit_count, 2)
        self.assertEqual(self.db.added_word_list, [['^', 'the'], ['the', 'cat'], ['cat', 'sat'], ['sat', 'on'], ['on', 'the'], ['the', 'mat'], ['mat', '$'], ['^', 'good'], ['good', 'cat'], ['cat', '$']])
        
    def test_db_updated_correctly_from_input_with_depth_4(self):
        self.db.depth = 4
        Parser('name', self.db, '\n', ' ').parse('the cat sat on the mat')
        self.assertEqual(self.db.commit_count, 1)
        self.assertEqual(self.db.added_word_list, [['^', '^', '^', 'the'], ['^', '^', 'the', 'cat'], ['^', 'the', 'cat', 'sat'], ['the', 'cat', 'sat', 'on'], ['cat', 'sat', 'on', 'the'], ['sat', 'on', 'the', 'mat'], ['on', 'the', 'mat', '$'], ['the', 'mat', '$', '$'], ['mat', '$', '$', '$']])

class StubDb:
    def __init__(self):
        self.commit_count = 0
        self.added_word_list = []
        self.depth = 2
        
    def get_depth(self):
        return self.depth
        
    def add_word(self, word_list):
        self.added_word_list.append(word_list)

    def commit(self):
        self.commit_count += 1

if __name__ == '__main__':
    unittest.main()