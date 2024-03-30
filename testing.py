import unittest
from lex import Lex
class TestStringMethods(unittest.TestCase):

    def test_lex(self):
        l = Lex("""MY 12344 name is 
                Ravind""")
        l.tokenize()

        for z in zip(l.token, l.lexword):
            print(z)

if __name__ == '__main__':
    unittest.main()