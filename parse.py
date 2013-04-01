from __future__ import division
import sqlite3
import codecs
import sys

class Parser:
	SENTENCE_START_SYMBOL = '^'
	SENTENCE_END_SYMBOL = '$'

	def __init__(self, name, db, split_char = '.'):
		self.name = name
		self.db   = db
		self.split_char = split_char

	def save_word_pair(self, word1, word2):
		self.db.add_word(word1, word2)

	def parse(self, file_name):
		txt = codecs.open(file_name, 'r', 'utf-8').read()
		sentences = txt.split(self.split_char)
		i = 0
		l = len(sentences)

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
				print '%d%% complete' % (100 * i / l,)
				sys.stdout.flush()


