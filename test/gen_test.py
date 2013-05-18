import unittest
from collections import OrderedDict
from gen import Generator

class GenTest(unittest.TestCase):
    def setUp(self):
        self.db = StubDb()
        self.rnd = StubRnd()
        
    def test_generated_sequence_is_correct(self):
        self.db.count_values = [
            OrderedDict([('the', 2), ('a', 1)]), 
            OrderedDict([('mat', 1), ('cat', 1)]), 
            OrderedDict([('sat', 2)]), 
            OrderedDict([('on', 1), ('under' , 4)]), 
            OrderedDict([('my', 2), ('the', 2)]), 
            OrderedDict([('mat', 1), ('cat', 1)]), 
            OrderedDict([('$', 1)])]
        
        self.rnd.vals = [1, 2, 2, 1, 4, 1, 1]
        
        self.assertEqual(Generator('name', self.db, self.rnd).generate(' '), 'the cat sat on the mat')
        self.assertEqual(self.db.get_word_count_args, [['^'], ['the'], ['cat'], ['sat'], ['on'], ['the'], ['mat']])
        self.assertEqual(self.rnd.maxints, [3, 2, 2, 5, 4, 2, 1])
    
class StubDb:
    def __init__(self):
        self.count_values = []
        self.get_word_count_args = []
        self.depth = 2
        
    def get_depth(self):
        return self.depth
    
    def get_word_count(self, word_list):   
        self.get_word_count_args.append(word_list)     
        return self.count_values.pop(0)
        
class StubRnd:
    def __init__(self):
        self.vals = []
        self.maxints = []
        
    def randint(self, maxint):
        self.maxints.append(maxint)
        return self.vals.pop(0)

if __name__ == '__main__':
    unittest.main()