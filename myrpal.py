import argparse 
import re
from lex import Lex
from queue_ import Queue
from parser_ import Parser
from st import Standard_tree
from node import Node
from CSE import CSE


class FileParser:

    def __init__(self) -> None:
        self.file = None
        self.file_name = None

    def get_filename(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("filename", help="Enter the filename")
        parser.add_argument("-ast", action="store_true",help="Generate the Abstract syntax Tree" )
        args = parser.parse_args()
        return args
    
    def open_file(self):
        self.file =  open(self.file_name, "r")

    def get_file_content(self):
        content = self.file.read()
        # Replace '\n' with actual newline character
        content = content.replace('\\n', '\n')
        content = content.replace('\\t', '\t')

        return content
    
    def lex(self):
        l = Lex(self.get_file_content())
        l.tokenize()
        new_token_list = list(filter(lambda x: x.type != "DELETE", l.tokens))
        input_stream = Queue(new_token_list)
        return input_stream

    def parse_file(self):

        p = Parser(self.lex(), debug=False)
        p.parse()

        st_tree = Standard_tree(p.stack.pop())
        st_tree = st_tree.parse_tree()
        cse_machine = CSE(st_tree, debug=False)
        cse_machine.print_deltas()
        cse_machine.operate()

    def get_ast(self):
        p = Parser(self.lex())
        p.parse()
        p.print_stack()
        
    
    def run(self):
        args = self.get_filename()
        if args.filename:
            self.file_name = args.filename
            self.open_file()

            if args.ast:
                self.get_ast()
            
            else:
                self.parse_file()
            
        else:
            print("Enter a filename")



def main():
    fileParser = FileParser()

    fileParser.run()

if __name__ == "__main__":
    main()