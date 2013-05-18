from db import Db
from gen import Generator
from parse import Parser
from sql import Sql
from rnd import Rnd
import sys
import sqlite3
import codecs

SENTENCE_SEPARATOR = '.'
WORD_SEPARATOR = ' '

if __name__ == '__main__':
	args = sys.argv
	usage = 'Usage: %s (parse <name> <depth> <path to txt file>|gen <name> <count>)' % (args[0], )

	if (len(args) < 3):
		raise ValueError(usage)

	mode  = args[1]
	name  = args[2]
	
	if mode == 'parse':
		if (len(args) != 5):
			raise ValueError(usage)
		
		depth = int(args[3])
		file_name = args[4]
		
		db = Db(sqlite3.connect(name + '.db'), Sql())
		db.setup(depth)
		
		txt = codecs.open(file_name, 'r', 'utf-8').read()
		Parser(name, db, SENTENCE_SEPARATOR, WORD_SEPARATOR).parse(txt)
	
	elif mode == 'gen':
		count = int(args[3])
		db = Db(sqlite3.connect(name + '.db'), Sql())
		generator = Generator(name, db, Rnd())
		for i in range(0, count):
			print generator.generate(WORD_SEPARATOR)
	
	else:
		raise ValueError(usage)