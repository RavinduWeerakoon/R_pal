
import re
rules = [
             ('IDENTIFIER', r'[a-zA-Z]\w*'),
             ('INTEGER', r'\d(\d)*'),
             ('DELETE', r'[\n\t\s]+'),
             ('MISMATCH', r'.')
             
        ]


class Lex:
    def __init__(self, code, rules=rules)->None:
        self.code = code
        self.tokens_join = '|'.join('(?P<%s>%s)' % x for x in rules)
        self.lin_start = 0

        # Lists of output for the program
        self.token = []
        self.lexword = []
       

    def tokenize(self):
        # It analyzes the code to find the lex words and their respective Tokens
        for m in re.finditer(self.tokens_join, self.code):
            token_type = m.lastgroup
            token_lexword = m.group(token_type)

            

            if token_type == 'MISMATCH':
                raise RuntimeError('%r unexpected on line %d' % (token_lexword, self.lin_num))
            else:
                    
                   
                    self.token.append(token_type)
                    self.lexword.append(token_lexword)
                    
                    


