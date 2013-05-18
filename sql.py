class Sql:
    WORD_COL_NAME_PREFIX = 'word'
    COUNT_COL_NAME       = 'count'
    WORD_TABLE_NAME      = 'word'
    INDEX_NAME           = 'i_word'
    PARAM_TABLE_NAME     = 'param'
    KEY_COL_NAME         = 'name'
    VAL_COL_NAME         = 'value'
    
    def _check_column_count(self, count):
        if count < 2:
            raise ValueError('Invalid column_count value, must be >= 2')
        
    def _make_column_name_list(self, column_count):
        return ', '.join([self.WORD_COL_NAME_PREFIX + str(n) for n in range(1, column_count + 1)])
        
    def _make_column_names_and_placeholders(self, column_count):
        return ' AND '.join(['%s%s=?' % (self.WORD_COL_NAME_PREFIX, n) for n in range(1, column_count + 1)])

    def create_word_table_sql(self, column_count):
        return 'CREATE TABLE IF NOT EXISTS %s (%s, %s)' % (self.WORD_TABLE_NAME, self._make_column_name_list(column_count), self.COUNT_COL_NAME)
    
    def create_param_table_sql(self):
        return 'CREATE TABLE IF NOT EXISTS %s (%s, %s)' % (self.PARAM_TABLE_NAME, self.KEY_COL_NAME, self.VAL_COL_NAME)
    
    def set_param_sql(self):
        return 'INSERT INTO %s (%s, %s) VALUES (?, ?)' % (self.PARAM_TABLE_NAME, self.KEY_COL_NAME, self.VAL_COL_NAME)
    
    def get_param_sql(self):
        return 'SELECT %s FROM %s WHERE %s=?' % (self.VAL_COL_NAME, self.PARAM_TABLE_NAME, self.KEY_COL_NAME)

    def create_index_sql(self, column_count):
        return 'CREATE INDEX IF NOT EXISTS %s ON %s (%s)' % (self.INDEX_NAME, self.WORD_TABLE_NAME, self._make_column_name_list(column_count))
    
    def select_count_for_words_sql(self, column_count):
        return 'SELECT %s FROM %s WHERE %s' % (self.COUNT_COL_NAME, self.WORD_TABLE_NAME, self._make_column_names_and_placeholders(column_count)) 
    
    def update_count_for_words_sql(self, column_count):
        return 'UPDATE %s SET %s=? WHERE %s' % (self.WORD_TABLE_NAME, self.COUNT_COL_NAME, self._make_column_names_and_placeholders(column_count)) 
    
    def insert_row_for_words_sql(self, column_count):
        columns = self._make_column_name_list(column_count) + ', ' + self.COUNT_COL_NAME
        values  = ', '.join(['?'] * (column_count + 1))
        
        return 'INSERT INTO %s (%s) VALUES (%s)' % (self.WORD_TABLE_NAME, columns, values) 
    
    def select_words_and_counts_sql(self, column_count):
        last_word_col_name = self.WORD_COL_NAME_PREFIX + str(column_count)
        
        return 'SELECT %s, %s FROM %s WHERE %s' % (last_word_col_name, self.COUNT_COL_NAME, self.WORD_TABLE_NAME, self._make_column_names_and_placeholders(column_count - 1))
    
    def delete_words_sql(self):
        return 'DELETE FROM ' + self.WORD_TABLE_NAME
        