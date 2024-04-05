
import re
from token_ import Token

# Keywords for the language
keywords = ["let", "in", "fn", "aug", "or", "not", "gr", "ge", "ls", "le", "eq", "ne", "where", "rec", "within", "and", "true", "false", "nil", "dummy", "list"]

# Lexcal rules for the language
rules = [
             ('IDENTIFIER', r'[a-zA-Z]\w*'),
             ('INTEGER', r'\d(\d)*'),
             ('STRING', r'\"(?:\\[t]|\\[n]|\\\\|\\["]|\(|\)|\;|\,|\,|\s|[a-zA-Z0-9\+\-\*\<\>\&\.\@\/\:\=\~\|\$\!\#\%\^\_\[\]\{\}\"\'\?])*?\"'),
             ('DELETE', r"[\n\t\s]+|\/\/(?:\"|\(|\)|\;|\,|\\|\s|\t|\w|[\+\-\*\<\>\&\.\@\/\:\=\~\|\$\!\#\%\^\[\]\{\}\"\'\?])*?(?:\n|$)"),
             ('OPERATOR', r'[\+\-\*\<\>\&\.\@\/\:\=\~\|\$\!\#\%\^\_\[\]\{\}\"\'\?]+'),

             # Punctuations
             # Note: Using ) ( ; , for group names will cause an error in the regex match. 
             # left_bracket, right_bracket, semi_colon, comma used instead and later mapped to expected values
             ('left_bracket', r'\('),
             ('right_bracket', r'\)'),
             ("semi_colon", r'\;'),
             ("comma", r'\,'),

             ('MISMATCH', r'.')
             
        ]

# Mapping of the token types to their respective lex words
lex_map = {
            'IDENTIFIER': '<IDENTIFIER>',
            'INTEGER': '<INTEGER>',
            'DELETE': '<DELETE>',
            'STRING': '<STRING>',
            'OPERATOR': '<OPERATOR>',
            'left_bracket': '(',
            'right_bracket': ')',
            'semi_colon': ';',
            'comma': ',',
            'MISMATCH': 'MISMATCH'
        }


class Lex:
    def __init__(self, code, rules=rules)->None:
        self.code = code
        self.tokens_join = '|'.join('(?P<%s>%s)' % x for x in rules)
        self.lin_start = 0

        # Lists of output for the program
        # self.token = []
        # self.lexword = []
        self.tokens = []
       

    def tokenize(self):
        # It analyzes the code to find the lex words and their respective Tokens
        for m in re.finditer(self.tokens_join, self.code):
            token_type = m.lastgroup
            token_lexword = m.group(token_type)

            if token_type == 'MISMATCH':
                raise RuntimeError('%r unexpected on line %d' % (token_lexword, self.lin_num))
            elif token_lexword in keywords:
                # Create a new token object and append it to the list of tokens
                token = Token("KEYWORD", token_lexword)
                self.tokens.append(token)
            else:
                # Create a new token object and append it to the list of tokens
                token = Token(token_type, token_lexword)
                self.tokens.append(token)