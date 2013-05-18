from db import Db
from gen import Generator
from parse import Parser
from sql import Sql
from rnd import Rnd
import sys
import sqlite3
import codecs

SENTENCE_SEPARATOR = '\n'
WORD_SEPARATOR = ''

if __name__ == '__main__':
	args = sys.argv
	usage = 'Usage: %s (parse <name> <depth> <path to txt file>|gen <name> <depth> <count>)' % (args[0], )

	if (len(args) != 5):
		raise ValueError(usage)

	mode  = args[1]
	name  = args[2]
	depth = int(args[3])
	sql   = Sql(depth)
	db    = Db(depth, sqlite3.connect(name + '.db'), sql)
	
	if mode == 'parse':
		file_name = args[4]
		txt = codecs.open(file_name, 'r', 'utf-8').read()
		Parser(name, db, SENTENCE_SEPARATOR, WORD_SEPARATOR).parse(depth, txt)
	
	elif mode == 'gen':
		count = int(args[4])
		generator = Generator(name, db, Rnd())
		for i in range(0, count):
			print generator.generate(depth, WORD_SEPARATOR)
	
	else:
		raise ValueError(usage)