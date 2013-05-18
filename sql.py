class Sql:
    WORD_COL_NAME_PREFIX = 'word'
    COUNT_COL_NAME       = 'count'
    TABLE_NAME           = 'word'
    INDEX_NAME           = 'i_word'
    
    def __init__(self, column_count):
        self.column_count = int(column_count)
        if self.column_count < 2:
            raise ValueError('Invalid column_count value, must be >= 2')
        
    def _make_column_name_list(self):
        return ', '.join([self.WORD_COL_NAME_PREFIX + str(n) for n in range(1, self.column_count + 1)])
        
    def _make_column_names_and_placeholders(self, col_count):
        return ' AND '.join(['%s%s=?' % (self.WORD_COL_NAME_PREFIX, n) for n in range(1, col_count + 1)])

    def create_table_sql(self):
        return 'CREATE TABLE IF NOT EXISTS %s (%s, %s)' % (self.TABLE_NAME, self._make_column_name_list(), self.COUNT_COL_NAME)
    
    def create_index_sql(self):
        return 'CREATE INDEX IF NOT EXISTS %s ON %s (%s)' % (self.INDEX_NAME, self.TABLE_NAME, self._make_column_name_list())
    
    def select_count_for_words_sql(self):
        return 'SELECT %s FROM %s WHERE %s' % (self.COUNT_COL_NAME, self.TABLE_NAME, self._make_column_names_and_placeholders(self.column_count)) 
    
    def update_count_for_words_sql(self):
        return 'UPDATE %s SET %s=? WHERE %s' % (self.TABLE_NAME, self.COUNT_COL_NAME, self._make_column_names_and_placeholders(self.column_count)) 
    
    def insert_row_for_words_sql(self):
        columns = self._make_column_name_list() + ', ' + self.COUNT_COL_NAME
        values  = ', '.join(['?'] * (self.column_count + 1))
        
        return 'INSERT INTO %s (%s) VALUES (%s)' % (self.TABLE_NAME, columns, values) 
    
    def select_words_and_counts_sql(self):
        last_word_col_name = self.WORD_COL_NAME_PREFIX + str(self.column_count)
        
        return 'SELECT %s, %s FROM %s WHERE %s' % (last_word_col_name, self.COUNT_COL_NAME, self.TABLE_NAME, self._make_column_names_and_placeholders(self.column_count - 1))
    
    def delete_words_sql(self):
        return 'DELETE FROM ' + self.TABLE_NAME
        