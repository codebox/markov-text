import sqlite3

class Db:
	def __init__(self, name):
		self.name = name
		self.conn = sqlite3.connect(name + '.db')
		c = self.conn.cursor()
		c.execute('CREATE TABLE IF NOT EXISTS words (word, next_word, count)')
		c.execute('CREATE INDEX IF NOT EXISTS i_word ON words (word,next_word)')

	def get_word_pair_count(self, word, next_word):
		c = self.conn.cursor()
		c.execute('select count from words where word=? and next_word=?' , (word, next_word))
		r = c.fetchone()
		if r:
			return r[0]
		else:
			return 0

	def add_word(self, word, next_word):
		count = self.get_word_pair_count(word, next_word)
		c = self.conn.cursor()
		if count:
			c.execute('UPDATE words SET count=? WHERE word=? AND next_word=?', (count + 1, word, next_word))
		else:
			c.execute('INSERT INTO words (word, next_word, count) VALUES (?,?,?)', (word, next_word, 1))

	def commit(self):
		self.conn.commit()

	def get_word_count(self, word):
		c = self.conn.cursor()
		counts = {}
		for row in c.execute('SELECT next_word, count FROM words WHERE word=?', (word,)):
			counts[row[0]] = row[1]

		return counts

	def reset(self):
		c = self.conn.cursor()
		c.execute('delete from words')
		self.conn.commit()
