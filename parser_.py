from token_ import Token
from queue_ import Queue
from stack import Stack


class Parser():

    def __init__(self, input_stream):
        self.input_stream = input_stream
        self.stack = Stack()


    def read(self, value):
        # Remove the token from the input stream
        if value == self.input_stream.peek().value:
            self.input_stream.dequeue()
        else:
            raise Exception(f"Expected {value} but got {self.input_stream.peek().value}")
        return
    
    def parse(self):
        self.E()

    def E(self):
        next = self.input_stream.peek()
        if next.value == "let":
            self.read("let")
            self.D()
            self.read("in")
            self.E()

        elif next.value == "fn":
            self.read("fn")
            self.Vb()
            while self.input_stream.peek().type == "left_bracket" or self.input_stream.peek().type == "IDENTIFIER":
                self.Vb()
        
        else:
            self.Ew()


    def Ew(self):
        self.T()
        if self.input_stream.peek().value == "where":
            self.read("where")
            self.Dr()

        else:
            self.read(";")


    def T(self):
        self.Ta()
        if self.input_stream.peek().value == ",":
            self.read(",")
            self.Ta()
            while self.input_stream.peek().value == ",":
                self.read(",")
                self.Ta()


    def Ta(self):
        self.Tc()
        if self.input_stream.peek().value == "aug":
            self.read("aug")
            self.Tc()
            while self.input_stream.peek().value == "aug":
                self.read("aug")
                self.Tc()

    def Tc(self):
        self.B()
        if self.input_stream.peak.value == ";":
            self.read(";")
        else:
            self.read("->")
            self.Tc()
            self.read("|")
            self.Tc()


    def B(self):
        self.Bt()
        while self.input_stream.peek().value == "or":
            self.read("or")
            self.Bt()    

    def Bt(self):
        self.Bs()
        while self.input_stream.peek().value == "&":
            self.read("&")
            self.Bs()

    def Bs(self):
        if self.input_stream.peek().value == "not":
            self.read("not")
            self.Bp()
        else:
            self.Bp()

    def Bp(self):
        self.A()
        if self.input_stream.peek().value == "gr":
            self.read("gr")
            self.A()
        elif self.input_stream.peek().value == ">":
            self.read(">")
            self.A()
        elif self.input_stream.peek().value == ">=":
            self.read(">=")
            self.A()
        elif self.input_stream.peek().value == "<":
            self.read("<")
            self.A()
        elif self.input_stream.peek().value == "<=":
            self.read("<=")
            self.A()
        elif self.input_stream.peek().value == "eq":
            self.read("eq")
            self.A()
        elif self.input_stream.peek().value == "ne":
            self.read("ne")
            self.A()

    def A(self):
        if self.input_stream.peek().value == "+":
            self.read("+")
            self.At()

        elif self.input_stream.peek().value == "-":
            self.read("-")
            self.At()

        else:
            self.At()
            if self.input_stream.peek().value == "+":
                self.read("+")
                self.At()
            elif self.input_stream.peek().value == "-":
                self.read("-")
                self.At()


    def At(self):
        self.Af()
        if self.input_stream.peek().value == "*":
            self.read("*")
            self.Af()
        elif self.input_stream.peek().value == "/":
            self.read("/")
            self.Af()


    def Af(self):
        self.Ap()
        if self.input_stream.peek().value == "**":
            self.read("**")
            self.Af()

    def Ap(self):
        self.R()
        while self.input_stream.peek().value == "@":
            self.read("@")
            self.read(type_check=True, type_="IDENTIFIER")
            self.R()

    def R(self):
        self.Rn()
        while self.input_stream.peek().type == "IDENTIFIER" or self.input_stream.peek().type == "INTEGER" or self.input_stream.peek().type == "STRING" or self.input_stream.peek().value == "nil" or self.input_stream.peek().value == "dummy" or self.input_stream.peek().value == "true" or self.input_stream.peek().value == "false" or self.input_stream.peek().type == "left_bracket":
            self.Rn()


    def Rn(self):
        if self.input_stream.peek().type == "IDENTIFIER":
            self.read(type_check=True, type_="IDENTIFIER")

        elif self.input_stream.peek().type == "INTEGER":
            self.read(type_check=True, type_="INTEGER")

        elif self.input_stream.peek().type == "STRING":
            self.read(type_check=True, type_="STRING")
        
        elif self.input_stream.peek().value == "true":
            self.read("true")
        
        elif self.input_stream.peek().value == "false":
            self.read("false")

        elif self.input_stream.peek().value == "nil":
            self.read("nil")
            
        elif self.input_stream.peek().value == "(":
                self.read("(")
                self.E()
                self.read(")")
        
        elif self.input_stream.peek().value == "dummy":
            self.read("dummy")

        else:
            raise Exception(f"Expected an identifier, integer, string, nil, dummy, true, false or an expression but got {self.input_stream.peek()}")


    def D(self):
        self.Da()

        if self.input_stream.peek().value == "within":
            self.read("within")
            print("D -> Da within D")
            self.D()
        

    def Da(self):
        self.Dr()
        if self.input_stream.peek().value == "and":
            self.read("and")
            self.Dr()
            
            while self.input_stream.peek().value == "and":
                self.read("and")
                self.Dr()
        
    def Dr(self):
        if self.input_stream.peek().value =="rec":
            self.read("rec")
            self.Db()
        elif self.input_stream.peek().value == "IDENTIFIER" or self.input_stream.peek().type == "left_bracket":
            self.Db()
        else:
            raise Exception("Expected rec or IDENTIFIER or left_bracket but got {self.input_stream.peek().value}")

    def Db(self):
        if self.input_stream.peek().type == "IDENTIFIER":
            if self.input_stream.peek(index=1).value == "IDENTIFIER":
                self.read("IDENTIFIER")
                self.Vb()
                while self.input_stream.peek().value == "IDENTIFIER":
                    self.Vb()
                self.read("=")
                self.E()
                print("Db -> Vb+ = E")
            elif self.input_stream.peek().value == "=":
                self.Vl()
                self.read("=")
                self.E()
        elif self.input_stream.peek().value == "(":
            self.read("(")
            self.D()
            self.read(")")
            print("Db -> (D)")
        
        else:
            raise Exception("Expected IDENTIFIER or ( but got {self.input_stream.peek().value}")
        

    def Vb(self):
        if self.input_stream.peek().type == "IDENTIFIER":
            self.read("IDENTIFIER")
        elif self.input_stream.peek().value == "(":
            self.read("(")
            self.Vl()
            self.read(")")
        else:
            raise Exception("Expected IDENTIFIER or ( but got {self.input_stream.peek().value}")
        
    def Vl(self):
        if self.input_stream.peek().type == "IDENTIFIER":
            self.read("IDENTIFIER")
            self.read("list")
        else:
            raise Exception("Expected IDENTIFIER but got {self.input_stream.peek().value}")