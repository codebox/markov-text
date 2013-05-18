import unittest
from db_test import DbTest
from gen_test import GenTest
from parse_test import ParserTest
from sql_test import SqlTest

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(DbTest))
    test_suite.addTest(unittest.makeSuite(GenTest))
    test_suite.addTest(unittest.makeSuite(ParserTest))
    test_suite.addTest(unittest.makeSuite(SqlTest))
    return test_suite

if __name__ == "__main__":
    #So you can run tests from this module individually.
    unittest.main() 