import sqlite3
from parse import Parser
from random import randint

class Generator:
	def __init__(self, name, db):
		self.name = name
		self.db = db

	def get_next_word(self, word):
		candidate_words = self.db.get_word_count(word)
		total_next_words = sum(candidate_words.values())
		i = randint(1, total_next_words)
		t=0
		for w in candidate_words.keys():
			t += candidate_words[w]
			if (i <= t):
				return w
		assert False

	def make_sentence(self):
		word = self.get_next_word(Parser.SENTENCE_START_SYMBOL)
		sentence = []

		while word != Parser.SENTENCE_END_SYMBOL:
			sentence.append(word)
			word = self.get_next_word(word)

		return ' '.join(sentence)

	def generate(self, count):
		for i in range(0, count):
			print self.make_sentence()