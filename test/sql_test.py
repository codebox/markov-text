import unittest
from sql import Sql

class SqlTest(unittest.TestCase):
    def test_create_word_table_sql_correct(self):
        self.assertEqual(Sql().create_word_table_sql(3), 'CREATE TABLE IF NOT EXISTS word (word1, word2, word3, count)')
    
    def test_create_param_table_sql_correct(self):
        self.assertEqual(Sql().create_param_table_sql(), 'CREATE TABLE IF NOT EXISTS param (name, value)')
    
    def test_set_param_sql_correct(self):
        self.assertEqual(Sql().set_param_sql(), 'INSERT INTO param (name, value) VALUES (?, ?)')
    
    def test_create_index_sql_correct(self):
        self.assertEqual(Sql().create_index_sql(3), 'CREATE INDEX IF NOT EXISTS i_word ON word (word1, word2, word3)')
    
    def test_select_count_for_words_sql_correct(self):
        self.assertEqual(Sql().select_count_for_words_sql(3), 'SELECT count FROM word WHERE word1=? AND word2=? AND word3=?')
     
    def test_update_count_for_words_sql_correct(self):
        self.assertEqual(Sql().update_count_for_words_sql(3), 'UPDATE word SET count=? WHERE word1=? AND word2=? AND word3=?')

    def test_insert_row_for_words_sql_correct(self):
        self.assertEqual(Sql().insert_row_for_words_sql(3), 'INSERT INTO word (word1, word2, word3, count) VALUES (?, ?, ?, ?)')

    def test_select_words_and_counts_sql_correct(self):
        self.assertEqual(Sql().select_words_and_counts_sql(3), 'SELECT word3, count FROM word WHERE word1=? AND word2=?')

    def test_delete_words_sql_correct(self):
        self.assertEqual(Sql().delete_words_sql(), 'DELETE FROM word')

if __name__ == '__main__':
    unittest.main()