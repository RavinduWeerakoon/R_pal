import unittest
from lex import Lex
from queue_ import Queue
from parser_ import Parser
from st import Standard_tree
def print_tree(root):
    if root:
        print(root.name)
        print_tree(root.left)
        print_tree(root.right)

class TestStringMethods(unittest.TestCase):

    def test_lex(self):
        l = Lex("""Print(1,2,3)""")


        l.tokenize()

        # for z in zip(l.token, l.lexword):
        #     print(z)
        # for token in l.tokens:
        #     print(token)

    
        new_token_list = list(filter(lambda x: x.type != "DELETE", l.tokens))

        input_stream = Queue(new_token_list)
        
        p = Parser(input_stream)
        p.parse()
        # p.print_stack()
        root = Standard_tree(p.stack.pop())
        x = root.parse_tree()
        print("......", type(x))
        
        


if __name__ == '__main__':
    unittest.main()