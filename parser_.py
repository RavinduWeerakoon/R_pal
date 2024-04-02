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


def T():
    Ta()
    if input_stream.peek().value == ",":
        read(",")
        Ta()
        while input_stream.peek().value == ",":
            read(",")
            Ta()


def Ta():
    Tc()
    if input_stream.peek().value == "aug":
        read("aug")
        Tc()
        while input_stream.peek().value == "aug":
            read("aug")
            Tc()

def Tc():
    B()
    if input_stream.peak.value == ";":
        read(";")
    else:
        read("->")
        Tc()
        read("|")
        Tc()


def B():
    Bt()
    while input_stream.peek().value == "or":
        read("or")
        Bt()    

def Bt():
    Bs()
    while input_stream.peek().value == "&":
        read("&")
        Bs()

def Bs():
    if input_stream.peek().value == "not":
        read("not")
        Bp()
    else:
        Bp()

def Bp():
    A()
    if input_stream.peek().value == "gr":
        read("gr")
        A()
    elif input_stream.peek().value == ">":
        read(">")
        A()
    elif input_stream.peek().value == ">=":
        read(">=")
        A()
    elif input_stream.peek().value == "<":
        read("<")
        A()
    elif input_stream.peek().value == "<=":
        read("<=")
        A()
    elif input_stream.peek().value == "eq":
        read("eq")
        A()
    elif input_stream.peek().value == "ne":
        read("ne")
        A()

def A():
    if input_stream.peek().value == "+":
        read("+")
        At()

    elif input_stream.peek().value == "-":
        read("-")
        At()

    else:
        At()
        if input_stream.peek().value == "+":
            read("+")
            At()
        elif input_stream.peek().value == "-":
            read("-")
            At()


def At():
    Af()
    if input_stream.peek().value == "*":
        read("*")
        Af()
    elif input_stream.peek().value == "/":
        read("/")
        Af()


def Af():
    Ap()
    if input_stream.peek().value == "**":
        read("**")
        Af()

def Ap():
    R()
    while input_stream.peek().value == "@":
        read("@")
        read(type_check=True, type_="IDENTIFIER")
        R()

def R():
    Rn()
    while input_stream.peek().type == "IDENTIFIER" or input_stream.peek().type == "INTEGER" or input_stream.peek().type == "STRING" or input_stream.peek().value == "nil" or input_stream.peek().value == "dummy" or input_stream.peek().value == "true" or input_stream.peek().value == "false" or input_stream.peek().type == "left_bracket":
        Rn()


def Rn():
    if input_stream.peek().type == "IDENTIFIER":
        read(type_check=True, type_="IDENTIFIER")

    elif input_stream.peek().type == "INTEGER":
        read(type_check=True, type_="INTEGER")

    elif input_stream.peek().type == "STRING":
        read(type_check=True, type_="STRING")
    
    elif input_stream.peek().value == "true":
        read("true")
    
    elif input_stream.peek().value == "false":
        read("false")

    elif input_stream.peek().value == "nil":
        read("nil")
        
    elif input_stream.peek().value == "(":
            read("(")
            E()
            read(")")
    
    elif input_stream.peek().value == "dummy":
        read("dummy")

    else:
        raise Exception(f"Expected an identifier, integer, string, nil, dummy, true, false or an expression but got {input_stream.peek()}")


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




        
