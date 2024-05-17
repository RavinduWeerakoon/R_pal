import unittest
from lex import Lex
from queue_ import Queue
from parser_ import Parser
from st import Standard_tree
from node import Node
from CSE import CSE


def print_tree(root):
    if root:

        print(root.name)
        print_tree(root.left)
        print_tree(root.right)

class TestStringMethods(unittest.TestCase):

    def test_lex(self):

        ##### Testing
        l = Lex("""let Sum(A) = Psum (A,5)
                where rec Psum (T,N) = N eq 0 -> 0
                | Psum(T,N-1)+T N
                in Print ( Sum (1,2,3,4,5) )""")


        ##### WORKING on CSE!
        #l = Lex("""let x=5 in let y=3 in x+y""")
        #l = Lex("""let c = 3 within f x = x + c in f 2""")
        #l = Lex("""let f x = x eq 2 -> 3 | 4 in f 2""")
        #l = Lex("""let f x y = x eq 2 -> 3 | 4 in f 2 3""")
        #l = Lex("""let f x y = x eq y -> 3 | 4 in f "abc" "abc" """)
        #l = Lex("""let f(x,y) = x eq 2 -> 3 | 4 in f "sdfsd""sfsdf" """)
        #l = Lex("""let x = -6 in let y = 3 in let z = 2 in not -x + y / 3 > z""")
        #l = Lex("""Print(1,2,3)""")
        # l = Lex("(x+y where x=3) where y = 45")
        # l = Lex("""let rec f n = n eq 1 -> 1 | n * f (n - 1) in f 5""")
        # l = Lex("(fn (x,y,z). x+y+z)(5,6,7)")
        # l = Lex("let Sum(A) = Psum(A,2) where Psum (A,B) = A+B in Print Sum(2)")
        #########################################################################
                # l = Lex("""let Sum(A) = Psum (A,5)
        #         where rec Psum (T,N) = N eq 0 -> 0
        #         | Psum(T,N-1)+T N
        #         in Print ( Sum (1,2,3,4,5) )""")
        #########################################################################
        # l = Lex("""let rec f n = n eq 1 -> 1 | n * f (n - 1) in f 5""")
        # l = Lex("""let x = "abc" in Stern x""")
        # l = Lex("""let x = Conc "abc" "def" in x""")
        # l = Lex("""let x = Stem "abc" in x""")
        # l = Lex("""let rec f n = n eq 1 -> 0 | n eq 2 -> 1 | f (n-1) + f (n-2) in
        #         let rec fib n = n eq 0 -> nil | (fib (n-1) aug f (n)) in
        #         Print ( fib 5 )""")


        ##### NOT WORKING on CSE :(
        # rec not yet implemented :/
        


        l.tokenize()    
        new_token_list = list(filter(lambda x: x.type != "DELETE", l.tokens))
        input_stream = Queue(new_token_list)
        
        p = Parser(input_stream)
        p.parse()
        p.print_stack()
        st_tree = Standard_tree(p.stack.pop())
        st_tree = st_tree.parse_tree()
        st_tree.print_tree()

        cse_machine = CSE(st_tree, debug=False)
        cse_machine.operate()
        
        

if __name__ == '__main__':
    unittest.main()