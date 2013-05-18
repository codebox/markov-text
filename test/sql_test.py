import unittest
from sql import Sql

class SqlTest(unittest.TestCase):
    def test_non_numeric_colcount_value_causes_error(self):
        self.assertRaises(ValueError, Sql, 'bork')

    def test_too_small_colcount_value_causes_error(self):
        self.assertRaises(ValueError, Sql, 1)

    def test_create_table_sql_correct(self):
        self.assertEqual(Sql(3).create_table_sql(), 'CREATE TABLE IF NOT EXISTS word (word1, word2, word3, count)')
    
    def test_create_index_sql_correct(self):
        self.assertEqual(Sql(3).create_index_sql(), 'CREATE INDEX IF NOT EXISTS i_word ON word (word1, word2, word3)')
    
    def test_select_count_for_words_sql_correct(self):
        self.assertEqual(Sql(3).select_count_for_words_sql(), 'SELECT count FROM word WHERE word1=? AND word2=? AND word3=?')
     
    def test_update_count_for_words_sql_correct(self):
        self.assertEqual(Sql(3).update_count_for_words_sql(), 'UPDATE word SET count=? WHERE word1=? AND word2=? AND word3=?')

    def test_insert_row_for_words_sql_correct(self):
        self.assertEqual(Sql(3).insert_row_for_words_sql(), 'INSERT INTO word (word1, word2, word3, count) VALUES (?, ?, ?, ?)')

    def test_select_words_and_counts_sql_correct(self):
        self.assertEqual(Sql(3).select_words_and_counts_sql(), 'SELECT word3, count FROM word WHERE word1=? AND word2=?')

    def test_delete_words_sql_correct(self):
        self.assertEqual(Sql(3).delete_words_sql(), 'DELETE FROM word')

if __name__ == '__main__':
    unittest.main()