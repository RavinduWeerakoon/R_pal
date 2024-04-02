from token_ import Token
from queue import Queue

class Parser():

    def __init__(self, input_stream):
        self.input_stream = input_stream

    def parse(self):
        E(self.input_stream)

    def read(self, token: Token):
        print(token.value)


input_stream = Queue()


def read(value):
    # Remove the token from the input stream
    if value == input_stream.peek().value:
        input_stream.dequeue()
    else:
        raise Exception(f"Expected {value} but got {input_stream.peek().value}")
    return


def D():
    pass

def E():
    next = input_stream.peek()
    if next.value == "let":
        read("let")
        D()
        read("in")
        E()

    elif next.value == "fn":
        read("fn")
        Vb()
        while input_stream.peek().type == "left_bracket" or input_stream.peek().type == "IDENTIFIER":
            Vb()
    
    else:
        Ew(input_stream)


def Ew():
    T()
    if input_stream.peek().value == "where":
        read("where")
        Dr()

    else:
        read(";")

def Vb():
    pass

def T():
    pass

def Dr():
    pass