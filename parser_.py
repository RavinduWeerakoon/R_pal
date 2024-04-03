from token_ import Token
from queue_ import Queue
from stack import Stack

s = Stack()
class Node:
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right
    
    def __repr__(self) -> str:
        return self.value

def build_tree(item, N):
    p = None
    for i in range(N):
        c = s.pop()
        c.right = p
        p = c
    s.push(Node(item, p, None))


class Parser():

    def __init__(self, input_stream: Queue):
        self.input_stream = input_stream
        self.stack = Stack()


    def read(self, value=None, type_check=False, type_=None):
        # Remove the token from the input stream
        if value == self.input_stream.peek().value:
            self.input_stream.dequeue()
        elif type_check:
                if self.input_stream.peek().type == type_:
                    self.input_stream.dequeue()
                else:
                    raise Exception(f"Expected {value} but got {self.input_stream.peek().value}")
        else:
            if value == self.input_stream.peek().type:
                print("Removing", self.input_stream.peek())
                self.input_stream.dequeue()
            else:
                raise Exception(f"Expected {value} but got {self.input_stream.peek().value}")
        return
    
    def parse(self):
        self.E()

    def E(self):

        next = self.input_stream.peek()
        if self.input_stream.peek() is not None:
            if next.value == "let":
                self.read("let")
                self.D()
                self.read("in")
                self.E()
                build_tree("let", 2)
            elif next.value == "fn":
                self.read("fn")
                n = 1
                self.Vb()
                while self.input_stream.peek().type == "left_bracket" or self.input_stream.peek().type == "IDENTIFIER":
                    self.Vb()
                    n += 1
                build_tree("lambda", n)
            
            else:
                self.Ew()


    def Ew(self):
        
        self.T()
        if self.input_stream.peek() is not None and self.input_stream.peek().value == "where":
            self.read("where")
            self.Dr()
            build_tree("where", 2)


    def T(self):
        
        self.Ta()
        if self.input_stream.peek() is not None and self.input_stream.peek().value == ",":
            self.read(",")
            self.Ta()
            n = 1
            while self.input_stream.peek().value == ",":
                self.read(",")
                self.Ta()
                n+=1
            build_tree("tau", n)


    def Ta(self):
        
        self.Tc()
        if self.input_stream.peek() is not None and self.input_stream.peek().value == "aug":
            self.read("aug")
            self.Tc()
            while self.input_stream.peek() is not None and self.input_stream.peek().value == "aug":
                self.read("aug")
                self.Tc()
                build_tree("aug", 2)

    def Tc(self):
        
        self.B()
        if self.input_stream.peek() is not None and self.input_stream.peek().value == "->":
            self.read("->")
            self.Tc()
            self.read("|")
            self.Tc()
            build_tree("->", 3)
    


    def B(self):
        self.Bt()
        while self.input_stream.peek() is not None and self.input_stream.peek().value == "or":
            self.read("or")
            self.Bt()    
            build_tree("or", 2)
    def Bt(self):
        self.Bs()
        while self.input_stream.peek() is not None and self.input_stream.peek().value == "&":
            self.read("&")
            self.Bs()
            build_tree("&", 2)

    def Bs(self):
        
        if self.input_stream.peek() is not None:
            if self.input_stream.peek().value == "not":
                self.read("not")
                self.Bp()
                build_tree("not", 1)
            else:
                self.Bp()
#Think Should check the other conditions as well
    def Bp(self):
        self.A()
        if self.input_stream.peek() is not None:
            if self.input_stream.peek().value == "gr":
                self.read("gr")
                self.A()
                build_tree("gr", 2)
            elif self.input_stream.peek().value == ">":
                self.read(">")
                self.A()
                build_tree("gr", 2)
            elif self.input_stream.peek().value == ">=":
                self.read(">=")
                self.A()
                build_tree("le", 2)
            elif self.input_stream.peek().value == "<":
                self.read("<")
                self.A()
                build_tree("ls", 2)
            elif self.input_stream.peek().value == "<=":
                self.read("<=")
                self.A()
                build_tree("le", 2)
            elif self.input_stream.peek().value == "eq":
                self.read("eq")
                self.A()
                build_tree("eq", 2)
            elif self.input_stream.peek().value == "ne":
                self.read("ne")
                self.A()
                build_tree("ne", 2)

    def A(self):
        if self.input_stream.peek() is not None:
            if self.input_stream.peek().value == "+":
                self.read("+")
                self.At()
                build_tree("+", 2)

            elif self.input_stream.peek().value == "-":
                self.read("-")
                self.At()
                build_tree("-", 2)

            else:
                self.At()
                if self.input_stream.peek() is not None:
                    if self.input_stream.peek().value == "+":
                        self.read("+")
                        self.At()

                    elif self.input_stream.peek().value == "-":
                        self.read("-")
                        self.At()
                        build_tree("neg", 1)


    def At(self):
        self.Af()
        if self.input_stream.peek() is not None:
            if self.input_stream.peek().value == "*":
                self.read("*")
                self.Af()
                build_tree("*", 2)
            elif self.input_stream.peek().value == "/":
                self.read("/")
                self.Af()
                build_tree("/", 2)


    def Af(self):
        self.Ap()
        if self.input_stream.peek() is not None and self.input_stream.peek().value == "**":
            self.read("**")
            self.Af()
            build_tree("**", 2)

    def Ap(self):
        self.R()
       
        while self.input_stream.peek() is not None and self.input_stream.peek().value == "@":
            self.read("@")
            self.read(type_check=True, type_="IDENTIFIER")
            self.R()
            build_tree("@", 3)

    def R(self):
        
        self.Rn()
        while self.input_stream.peek() is not None and (self.input_stream.peek().type == "IDENTIFIER" or self.input_stream.peek().type == "INTEGER" or self.input_stream.peek().type == "STRING" or self.input_stream.peek().value == "nil" or self.input_stream.peek().value == "dummy" or self.input_stream.peek().value == "true" or self.input_stream.peek().value == "false" or self.input_stream.peek().type == "left_bracket"):
            self.Rn()
            build_tree("gamma", 2)

#do we have to add the identifier as the leafs of the tree
    def Rn(self):
        if self.input_stream.peek().type == "IDENTIFIER":
            self.read(type_check=True, type_="IDENTIFIER")
            build_tree("<IDENTIFIER>", 0)

        elif self.input_stream.peek().type == "INTEGER":
            self.read(type_check=True, type_="INTEGER")
            build_tree("<INTEGER>", 0)

        elif self.input_stream.peek().type == "STRING":
            self.read(type_check=True, type_="STRING")
            build_tree("<STRING>", 0)
        
        elif self.input_stream.peek().value == "true":
            self.read("true")
            build_tree("true", 0)
        
        elif self.input_stream.peek().value == "false":
            self.read("false")
            build_tree("false", 0)

        elif self.input_stream.peek().value == "nil":
            self.read("nil")
            build_tree("nil", 0)
            
        elif self.input_stream.peek().value == "(":
            self.read("(")
            self.E()
            self.read(")")
        
        elif self.input_stream.peek().value == "dummy":
            self.read("dummy")
            build_tree("dummy", 0)

        else:
            raise Exception(f"Expected an identifier, integer, string, nil, dummy, true, false or an expression but got {self.input_stream.peek()}")


    def D(self):
        
        self.Da()

        if self.input_stream.peek().value == "within":
            self.read("within")
           
            self.D()
            build_tree("within", 2)
        

    def Da(self):
        self.Dr()
        if self.input_stream.peek().value == "and":
            self.read("and")
            self.Dr()
            build_tree("and", 2)
            
            while self.input_stream.peek().value == "and":
                self.read("and")
                self.Dr()
        
    def Dr(self):
        if self.input_stream.peek().value =="rec":
            self.read("rec")
            self.Db()
            build_tree("rec", 1)
        elif self.input_stream.peek().type == "IDENTIFIER" or self.input_stream.peek().type == "left_bracket":
            self.Db()
        else:
            raise Exception(f"Expected rec or IDENTIFIER or left_bracket but got {self.input_stream.peek().value}")

    def Db(self):
        if self.input_stream.peek().type == "IDENTIFIER":
            if self.input_stream.peek(index=1).type == "IDENTIFIER" or self.input_stream.peek(index=1).value == "(":
                self.read(type_check=True, type_="IDENTIFIER")
                self.Vb()
                n = 1
                while self.input_stream.peek().type == "IDENTIFIER" or self.input_stream.peek().value == "(":
                    self.Vb()
                    n+=1
                
                self.read("=")
                self.E()
                build_tree("function_form", n)
            elif self.input_stream.peek(index=1).value == "=":
                self.read(type_check=True, type_="IDENTIFIER")
                self.Vl()
                self.read("=")
                self.E()
                build_tree("=", 2)
        elif self.input_stream.peek().value == "(":
            self.read("(")
            self.D()
            self.read(")")
           
        
        else:
            raise Exception("Expected IDENTIFIER or ( but got {self.input_stream.peek().value}")
        
#should add the () case
    def Vb(self):
        if self.input_stream.peek().type == "IDENTIFIER":
            self.read(type_check=True, type_="IDENTIFIER")
        elif self.input_stream.peek().value == "(":
            self.read("(")
            self.Vl()
            self.read(")")
        else:
            raise Exception(f"Expected IDENTIFIER or ( but got {self.input_stream.peek().value}")
        
    def Vl(self):
        print("Vl", self.input_stream.peek().value)
        if self.input_stream.peek().type == "IDENTIFIER":
            self.read(type_check=True, type_="IDENTIFIER")
            n = 0
            while self.input_stream.peek().value == ",":
                self.read(",")
                self.read(type_check=True, type_="IDENTIFIER")
                n += 1
            build_tree(",", n)
        else:
            raise Exception(f"Expected IDENTIFIER but got {self.input_stream.peek().value}")
        

