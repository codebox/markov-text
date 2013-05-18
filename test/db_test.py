import unittest
from db import Db

class DbTest(unittest.TestCase):
    def setUp(self):
        self.conn = StubConn()
        self.sql = StubSql()
    
    def test_correct_sql_run_when_setup_called(self):
        Db(self.conn, self.sql).setup(3)
        execute_args = self.conn.stub_cursor.execute_args
        self.assertEqual(len(execute_args), 4)
        self.assertEqual(execute_args[0], ('create_word_table_sql 3',))
        self.assertEqual(execute_args[1], ('create_index_sql 3',))
        self.assertEqual(execute_args[2], ('create_param_table_sql',))
        self.assertEqual(execute_args[3], ('set_param_sql', ('depth', 3)))
        
    def test_error_when_add_word_count_wrong(self):
        db = Db(self.conn, self.sql)
        db.setup(3)
        self.assertRaises(ValueError, db.add_word, ['one','two'])
        
    def test_insert_row_when_add_new_word_list(self):
        db = Db(self.conn, self.sql)
        db.setup(3)
        word_list = ['one', 'two', 'three']
        db.add_word(word_list)
        
        execute_args = self.conn.stub_cursor.execute_args
        self.assertEqual(len(execute_args), 6)
        self.assertEqual(execute_args[4], ('select_count_for_words_sql 3', word_list))
        self.assertEqual(execute_args[5], ('insert_row_for_words_sql 3', word_list + [1]))
        
    def test_update_row_when_add_repeated_word_list(self):
        db = Db(self.conn, self.sql)
        db.setup(3)
        row_count = 10
        word_list = ['one', 'two', 'three']
        self.conn.stub_cursor.fetchone_results.append([row_count])

        db.add_word(word_list)
        
        execute_args = self.conn.stub_cursor.execute_args
        self.assertEqual(len(execute_args), 6)
        self.assertEqual(execute_args[4], ('select_count_for_words_sql 3', word_list))
        self.assertEqual(execute_args[5], ('update_count_for_words_sql 3', [row_count + 1] + word_list))

    def test_db_commit_performed_correctly(self):
        db = Db(self.conn, self.sql)
        db.setup(3)
        self.assertEqual(self.conn.commit_count, 0)
        db.commit()
        self.assertEqual(self.conn.commit_count, 1)
        
    def test_get_word_counts_works_correctly(self):
        db = Db(self.conn, self.sql)
        db.setup(3)
        word_list = ['i', 'like']
        self.conn.stub_cursor.execute_results = [[['dogs',  1], ['cats',  2], ['frogs', 3]]]
        
        word_counts = db.get_word_count(word_list)
        
        self.assertEqual(word_counts, {'dogs' : 1, 'cats' : 2, 'frogs' : 3})
        execute_args = self.conn.stub_cursor.execute_args
        self.assertEqual(len(execute_args), 5)
        self.assertEqual(execute_args[4], ('select_words_and_counts_sql 3', word_list))

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
    def create_word_table_sql(self, column_count):
        return 'create_word_table_sql' + ' ' + str(column_count)
    
    def create_index_sql(self, column_count):
        return 'create_index_sql' + ' ' + str(column_count)
    
    def create_param_table_sql(self):
        return 'create_param_table_sql'
    
    def set_param_sql(self):
        return 'set_param_sql'
    
    def get_param_sql(self):
        return 'get_param_sql'
    
    def select_count_for_words_sql(self, column_count):
        return 'select_count_for_words_sql' + ' ' + str(column_count)
    
    def update_count_for_words_sql(self, column_count):
        return 'update_count_for_words_sql'  + ' ' + str(column_count)
    
    def insert_row_for_words_sql(self, column_count):
        return 'insert_row_for_words_sql' + ' ' + str(column_count)
    
    def select_words_and_counts_sql(self, column_count):
        return 'select_words_and_counts_sql' + ' ' + str(column_count)
    
    def delete_words_sql(self):
        return 'delete_words_sql'            
    
if __name__ == '__main__':
    unittest.main()