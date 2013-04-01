from db import Db
from gen import Generator
from parse import Parser
import sys


if __name__ == '__main__':
	args = sys.argv
	usage = 'Usage: %s (parse <name> <path to txt file>|gen <name> <count>)' % (args[0], )

	if (len(args) != 4):
		raise ValueError(usage)

	mode = args[1]
	name = args[2]
	db = Db(name)
	if mode == 'parse':
		file_name = args[3]
		Parser(name, db).parse(file_name)
	elif mode == 'gen':
		count = int(args[3])
		Generator(name, db).generate(count)
	else:
		raise ValueError(usage)