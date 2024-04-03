import unittest
from lex import Lex
from queue_ import Queue
from parser_ import Parser
from parser_ import s



class TestStringMethods(unittest.TestCase):

    def test_lex(self):
        # l = Lex("""MY 12344 name
        #         // test
        #         // gesgsdgs
        #         my_variable == 56;
        #         // this is a comment

        #         testfun() {
        #             return 0;
        #         }
                
        #         Ravind;""")

        l = Lex(""" 
        let Sum(A) = Psum (A,Order A )
        where rec Psum (T,N) = N eq 0 -> 0
              | Psum(T,N-1)+T N
        in Print ( Sum (1,2,3,4,5) )
        """)


        l.tokenize()

        # for z in zip(l.token, l.lexword):
        #     print(z)
        # for token in l.tokens:
        #     print(token)

    
        new_token_list = list(filter(lambda x: x.type != "DELETE", l.tokens))

        input_stream = Queue(new_token_list)
        
        p = Parser(input_stream)
        p.parse()

        





if __name__ == '__main__':
    unittest.main()