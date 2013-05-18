
class Db:
	def __init__(self, depth, conn, sql):
		self.depth  = depth
		self.conn   = conn 
		self.cursor = conn.cursor()
		self.sql    = sql

		self.cursor.execute(self.sql.create_table_sql())
		self.cursor.execute(self.sql.create_index_sql())

	def _get_word_list_count(self, word_list):
		if len(word_list) != self.depth:
			raise ValueError('Expected %s words in list but found %s' % (self.depth, len(word_list)))

		self.cursor.execute(self.sql.select_count_for_words_sql(), word_list)
		r = self.cursor.fetchone()
		if r:
			return r[0]
		else:
			return 0

	def add_word(self, word_list):
		count = self._get_word_list_count(word_list)
		if count:
			self.cursor.execute(self.sql.update_count_for_words_sql(), [count + 1] + word_list)
		else:
			self.cursor.execute(self.sql.insert_row_for_words_sql(), word_list + [1])

	def commit(self):
		self.conn.commit()

	def get_word_count(self, word_list):
		counts = {}
		sql = self.sql.select_words_and_counts_sql()
		for row in self.cursor.execute(sql, word_list):
			counts[row[0]] = row[1]

		return counts
