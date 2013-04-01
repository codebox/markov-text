import sqlite3
import codecs
import sys

class Parser:
	SENTENCE_START_SYMBOL = '^'
	SENTENCE_END_SYMBOL = '$'

	def __init__(self, name, db):
		self.name = name
		self.db   = db

	def save_word_pair(self, word1, word2):
		self.db.add_word(word1, word2)

	def parse(self, file_name):
		txt = codecs.open(file_name, 'r', 'utf-8').read()
		sentences = txt.split('\n')
		i = 0

		for sentence in sentences:
			words = sentence.split()
			prev_word = Parser.SENTENCE_START_SYMBOL

			for word in words:
				self.save_word_pair(prev_word, word)
				prev_word = word

			self.save_word_pair(prev_word, Parser.SENTENCE_END_SYMBOL)
			self.db.commit()
			i += 1
			if i % 1000 == 0:
				print i
				sys.stdout.flush()


