
class Db:
	DEPTH_PARAM_NAME = 'depth'
	
	def __init__(self, conn, sql):
		self.conn   = conn 
		self.cursor = conn.cursor()
		self.sql    = sql
		self.depth  = None

	def setup(self, depth):
		self.depth = depth
		self.cursor.execute(self.sql.create_word_table_sql(depth))
		self.cursor.execute(self.sql.create_index_sql(depth))
		self.cursor.execute(self.sql.create_param_table_sql())
		self.cursor.execute(self.sql.set_param_sql(), (self.DEPTH_PARAM_NAME, depth))

	def _get_word_list_count(self, word_list):
		if len(word_list) != self.get_depth():
			raise ValueError('Expected %s words in list but found %s' % (self.get_depth(), len(word_list)))

		self.cursor.execute(self.sql.select_count_for_words_sql(self.get_depth()), word_list)
		r = self.cursor.fetchone()
		if r:
			return r[0]
		else:
			return 0

	def get_depth(self):
		if self.depth == None:
			self.cursor.execute(self.sql.get_param_sql(), (self.DEPTH_PARAM_NAME,))
			r = self.cursor.fetchone()
			if r:
				self.depth = int(r[0])
			else:
				raise ValueError('No depth value found in database, db does not seem to have been created by this utility')
			
		return self.depth
		
	def add_word(self, word_list):
		count = self._get_word_list_count(word_list)
		if count:
			self.cursor.execute(self.sql.update_count_for_words_sql(self.get_depth()), [count + 1] + word_list)
		else:
			self.cursor.execute(self.sql.insert_row_for_words_sql(self.get_depth()), word_list + [1])

	def commit(self):
		self.conn.commit()

	def get_word_count(self, word_list):
		counts = {}
		sql = self.sql.select_words_and_counts_sql(self.get_depth())
		for row in self.cursor.execute(sql, word_list):
			counts[row[0]] = row[1]

		return counts
