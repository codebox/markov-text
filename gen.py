from parse import Parser

class Generator:
	def __init__(self, name, db, rnd):
		self.name = name
		self.db   = db
		self.rnd  = rnd

	def _get_next_word(self, word_list):
		candidate_words = self.db.get_word_count(word_list)
		total_next_words = sum(candidate_words.values())
		i = self.rnd.randint(total_next_words)
		t=0
		for w in candidate_words.keys():
			t += candidate_words[w]
			if (i <= t):
				return w
		assert False

	def generate(self, word_separator):
		depth = self.db.get_depth()
		sentence = [Parser.SENTENCE_START_SYMBOL] * (depth - 1)
		end_symbol = [Parser.SENTENCE_END_SYMBOL] * (depth - 1)

		while True:
			tail = sentence[(-depth+1):]
			if tail == end_symbol:
				break
			word = self._get_next_word(tail)
			sentence.append(word)
		
		return word_separator.join(sentence[depth-1:][:1-depth])
