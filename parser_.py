from token_ import Token
from queue_ import Queue

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


def D():
    Da()

    if input_stream.peek().value == "within":
        read("within")
        print("D -> Da within D")
        D()
    

def Da():
    Dr()
    if input_stream.peek().value == "and":
        read("and")
        Dr()
        
        while input_stream.peek().value == "and":
            read("and")
            Dr()
    
def Dr():
    if input_stream.peek().value =="rec":
        read("rec")
        Db()
    elif input_stream.peek().value == "IDENTIFIER" or input_stream.peek().type == "left_bracket":
        Db()
    else:
        raise Exception("Expected rec or IDENTIFIER or left_bracket but got {input_stream.peek().value}")

def Db():
    if input_stream.peek().type == "IDENTIFIER":
        if input_stream.peek(index=1).value == "IDENTIFIER":
            read("IDENTIFIER")
            Vb()
            while input_stream.peek().value == "IDENTIFIER":
                Vb()
            read("=")
            E()
            print("Db -> Vb+ = E")
        elif input_stream.peek().value == "=":
            Vl()
            read("=")
            E()
    elif input_stream.peek().value == "(":
        read("(")
        D()
        read(")")
        print("Db -> (D)")
    
    else:
        raise Exception("Expected IDENTIFIER or ( but got {input_stream.peek().value}")
    

def Vb():
    if input_stream.peek().type == "IDENTIFIER":
        read("IDENTIFIER")
    elif input_stream.peek().value == "(":
        read("(")
        Vl()
        read(")")
    else:
        raise Exception("Expected IDENTIFIER or ( but got {input_stream.peek().value}")
    
def Vl():
    if input_stream.peek().type == "IDENTIFIER":
        read("IDENTIFIER")
        read("list")
    else:
        raise Exception("Expected IDENTIFIER but got {input_stream.peek().value}")




        
