import unittest
from db import Db

class DbTest(unittest.TestCase):
    def setUp(self):
        self.conn = StubConn()
        self.sql = StubSql()
    
    def test_correct_sql_run_when_object_created(self):
        Db(3, self.conn, self.sql)
        execute_args = self.conn.stub_cursor.execute_args
        self.assertEqual(len(execute_args), 2)
        self.assertEqual(execute_args[0], ('create_table_sql',))
        self.assertEqual(execute_args[1], ('create_index_sql',))
        
    def test_error_when_add_word_count_wrong(self):
        db = Db(3, self.conn, self.sql)
        self.assertRaises(ValueError, db.add_word, ['one','two'])
        
    def test_insert_row_when_add_new_word_list(self):
        db = Db(3, self.conn, self.sql)
        word_list = ['one', 'two', 'three']
        db.add_word(word_list)
        
        execute_args = self.conn.stub_cursor.execute_args
        self.assertEqual(len(execute_args), 4)
        self.assertEqual(execute_args[2], ('select_count_for_words_sql', word_list))
        self.assertEqual(execute_args[3], ('insert_row_for_words_sql', word_list + [1]))
        
    def test_update_row_when_add_repeated_word_list(self):
        db = Db(3, self.conn, self.sql)
        row_count = 10
        word_list = ['one', 'two', 'three']
        self.conn.stub_cursor.fetchone_results.append([row_count])

        db.add_word(word_list)
        
        execute_args = self.conn.stub_cursor.execute_args
        self.assertEqual(len(execute_args), 4)
        self.assertEqual(execute_args[2], ('select_count_for_words_sql', word_list))
        self.assertEqual(execute_args[3], ('update_count_for_words_sql', [row_count + 1] + word_list))

    def test_db_commit_performed_correctly(self):
        db = Db(3, self.conn, self.sql)
        self.assertEqual(self.conn.commit_count, 0)
        db.commit()
        self.assertEqual(self.conn.commit_count, 1)
        
    def test_get_word_counts_works_correctly(self):
        db = Db(3, self.conn, self.sql)
        word_list = ['i', 'like']
        self.conn.stub_cursor.execute_results = [[['dogs',  1], ['cats',  2], ['frogs', 3]]]
        
        word_counts = db.get_word_count(word_list)
        
        self.assertEqual(word_counts, {'dogs' : 1, 'cats' : 2, 'frogs' : 3})
        execute_args = self.conn.stub_cursor.execute_args
        self.assertEqual(len(execute_args), 3)
        self.assertEqual(execute_args[2], ('select_words_and_counts_sql', word_list))

class StubCursor:
    def __init__(self):
        self.execute_results = []
        self.execute_args = []
        self.fetchone_results = []
        self.fetchone_count = 0
        
    def fetchone(self):
        self.fetchone_count += 1
        
        if len(self.fetchone_results):
            return self.fetchone_results.pop(0)
        
        return None
    
    def execute(self, *args):
        self.execute_args.append(args)
        
        if len(self.execute_results):
            return self.execute_results.pop(0)
        
        return None
    
    def get_execute_count(self):
        return self.execute_count
    
class StubConn:
    def __init__(self):
        self.commit_count = 0
        self.stub_cursor = StubCursor()
        
    def commit(self):
        self.commit_count += 1
        
    def cursor(self):
        return self.stub_cursor

class StubSql:
    def create_table_sql(self):
        return 'create_table_sql'
    
    def create_index_sql(self):
        return 'create_index_sql'
    
    def select_count_for_words_sql(self):
        return 'select_count_for_words_sql' 
    
    def update_count_for_words_sql(self):
        return 'update_count_for_words_sql' 
    
    def insert_row_for_words_sql(self):
        return 'insert_row_for_words_sql' 
    
    def select_words_and_counts_sql(self):
        return 'select_words_and_counts_sql'
    
    def delete_words_sql(self):
        return 'delete_words_sql'            
    
if __name__ == '__main__':
    unittest.main()