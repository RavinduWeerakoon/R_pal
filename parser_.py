from token_ import Token
from queue_ import Queue
from stack import Stack
from node import Node


class Parser():

    def __init__(self, input_stream: Queue, debug=False):
        self.input_stream = input_stream
        self.stack = Stack()
        self.debug = debug


    def read(self, value=None, type_check=False, type_=None):
        # Remove the token from the input stream
        if value == self.input_stream.peek().value:
            self.input_stream.dequeue()
        elif type_check:
                if self.input_stream.peek().type == type_:
                    self.add_to_stack(self.input_stream.peek())
                    self.input_stream.dequeue()
                else:
                    raise Exception(f"Expected {value} but got {self.input_stream.peek().value}")
        else:
            if value == self.input_stream.peek().type:
                self.input_stream.dequeue()
            else:
                raise Exception(f"Expected {value} but got {self.input_stream.peek().value}")
        return
    

    def add_to_stack(self, token):
        self.stack.push(token)


    def pop_from_stack(self):
        return self.stack.pop()
    
    def print_stack(self):
        root = self.stack.stack[-1]
        root.print_node()
    

    def build_tree(self, name, n):
        print("Building tree", name, n)
        node = Node(name)
        for _ in range(n):
            node.add_child(self.pop_from_stack())
        self.add_to_stack(node)

    
    def parse(self):
        self.E()

    def E(self):
        if self.debug:
            print("E", self.input_stream.peek().value)

        next = self.input_stream.peek()
        if self.input_stream.peek() is not None:
            if next.value == "let":
                self.read("let")
                self.D()
                self.read("in")
                self.E()
                self.build_tree("let", 2)

            elif next.value == "fn":
                self.read("fn")
                n = 1
                self.Vb()
                while self.input_stream.peek().type == "left_bracket" or self.input_stream.peek().type == "IDENTIFIER":
                    self.Vb()
                    n+= 1
                
                self.read(".")
                self.E()
                self.build_tree("lambda", n+1)
            
            else:
                self.Ew()


    def Ew(self):
        if self.debug:
            print("Ew", self.input_stream.peek().value)

        self.T()
        if self.input_stream.peek() is not None and self.input_stream.peek().value == "where":
            self.read("where")
            self.Dr()
            self.build_tree("where", 2)


    def T(self):
        if self.debug:
            print("T", self.input_stream.peek().value)

        self.Ta()
        if self.input_stream.peek() is not None and self.input_stream.peek().value == ",":
            self.read(",")
            self.Ta()
            n = 2
            while self.input_stream.peek().value == ",":
                self.read(",")
                self.Ta()
                n+= 1
            self.build_tree("tau", n)


    def Ta(self):
        if self.debug:
            print("Ta", self.input_stream.peek().value)

        self.Tc()
        if self.input_stream.peek() is not None and self.input_stream.peek().value == "aug":
            self.read("aug")
            self.Tc()
            self.build_tree("aug", 2)
            while self.input_stream.peek() is not None and self.input_stream.peek().value == "aug":
                self.read("aug")
                self.Tc()
                self.build_tree("aug", 2)

    def Tc(self):
        if self.debug:
            print("Tc", self.input_stream.peek().value)

        self.B()
        if self.input_stream.peek() is not None and self.input_stream.peek().value == "->":
            self.read("->")
            self.Tc()
            self.read("|")
            self.Tc()
            self.build_tree("->", 3)


    def B(self):
        if self.debug:
            print("B", self.input_stream.peek().value)

        self.Bt()
        while self.input_stream.peek() is not None and self.input_stream.peek().value == "or":
            self.read("or")
            self.Bt()
            self.build_tree("or", 2)

    def Bt(self):
        if self.debug:
            print("Bt", self.input_stream.peek().value)

        self.Bs()
        while self.input_stream.peek() is not None and self.input_stream.peek().value == "&":
            self.read("&")
            self.Bs()
            self.build_tree("&", 2)

    def Bs(self):
        if self.debug:
            print("Bs", self.input_stream.peek().value)

        if self.input_stream.peek() is not None:
            if self.input_stream.peek().value == "not":
                self.read("not")
                self.Bp()
                self.build_tree("not", 1)
            else:
                self.Bp()

    def Bp(self):
        if self.debug:
            print("Bp", self.input_stream.peek().value)

        self.A()
        if self.input_stream.peek() is not None:
            if self.input_stream.peek().value == "gr":
                self.read("gr")
                self.A()
                self.build_tree("gr", 2)
            elif self.input_stream.peek().value == ">":
                self.read(">")
                self.A()
                self.build_tree("gr", 2)
            elif self.input_stream.peek().value == "ge":
                self.read("ge")
                self.A()
                self.build_tree("ge", 2)
            elif self.input_stream.peek().value == ">=":
                self.read(">=")
                self.A()
                self.build_tree("ge", 2)
            elif self.input_stream.peek().value == "ls":
                self.read("ls")
                self.A()
                self.build_tree("ls", 2)
            elif self.input_stream.peek().value == "<":
                self.read("<")
                self.A()
                self.build_tree("ls", 2)
            elif self.input_stream.peek().value == "le":
                self.read("le")
                self.A()
                self.build_tree("le", 2)
            elif self.input_stream.peek().value == "<=":
                self.read("<=")
                self.A()
                self.build_tree("le", 2)
            elif self.input_stream.peek().value == "eq":
                self.read("eq")
                self.A()
                self.build_tree("eq", 2)
            elif self.input_stream.peek().value == "ne":
                self.read("ne")
                self.A()
                self.build_tree("ne", 2)

    def A(self):
        if self.debug:
            print("A", self.input_stream.peek().value)

        if self.input_stream.peek() is not None:
            
            if self.input_stream.peek().value=="+" and self.input_stream.peek().value(index=2) not in ["+","-"]:
                self.read("+")
                self.At()

            elif self.input_stream.peek().value == "-":
                self.read("-")
                self.At()
                self.build_tree("neg", 1)
    
            else:
                self.At()
            
            while self.input_stream.peek() is not None and self.input_stream.peek().value in ["+", '-']:
                if self.input_stream.peek().value == "+":
                    self.read("+")
                    self.At()
                    self.build_tree("+", 2)
                elif self.input_stream.peek().value == "-":
                    self.read("-")
                    self.At()
                    self.build_tree("-", 2)


    def At(self):
        if self.debug:
            print("At", self.input_stream.peek().value)

        self.Af()
        while self.input_stream.peek() is not None and self.input_stream.peek().value in ["*", "/"]:
            if self.input_stream.peek().value == "*":
                self.read("*")
                self.Af()
                self.build_tree("*", 2)
            elif self.input_stream.peek().value == "/":
                self.read("/")
                self.Af()
                self.build_tree("/", 2)


    def Af(self):
        if self.debug:
            print("Af", self.input_stream.peek().value)

        self.Ap()
        if self.input_stream.peek() is not None and self.input_stream.peek().value == "**":
            self.read("**")
            self.Af()
            self.build_tree("**", 2)

    def Ap(self):
        if self.debug:
            print("Ap", self.input_stream.peek().value)

        self.R()
        while self.input_stream.peek() is not None and self.input_stream.peek().value == "@":
            self.read("@")
            self.read(type_check=True, type_="IDENTIFIER")
            self.R()
            self.build_tree("@", 3)

    def R(self):
        if self.debug:
            print("R", self.input_stream.peek().value)

        self.Rn()
        while self.input_stream.peek() is not None and (self.input_stream.peek().type == "IDENTIFIER" or self.input_stream.peek().type == "INTEGER" or self.input_stream.peek().type == "STRING" or self.input_stream.peek().value == "nil" or self.input_stream.peek().value == "dummy" or self.input_stream.peek().value == "true" or self.input_stream.peek().value == "false" or self.input_stream.peek().type == "left_bracket"):
            self.Rn()
            self.build_tree("gamma", 2)


    def Rn(self):
        if self.debug:
            print("Rn", self.input_stream.peek().value, self.input_stream.peek().type)

        if self.input_stream.peek().type == "IDENTIFIER":
            self.read(type_check=True, type_="IDENTIFIER")

        elif self.input_stream.peek().type == "INTEGER":
            self.read(type_check=True, type_="INTEGER")

        elif self.input_stream.peek().type == "STRING":
            self.read(type_check=True, type_="STRING")
        
        elif self.input_stream.peek().value == "true":
            self.read("true")
            self.build_tree("true", 1)
        
        elif self.input_stream.peek().value == "false":
            self.read("false")
            self.build_tree("false", 1)

        elif self.input_stream.peek().value == "nil":
            self.read("nil")
            self.build_tree("nil", 1)
            
        elif self.input_stream.peek().value == "(":
            self.read("(")
            self.E()
            self.read(")")
        
        elif self.input_stream.peek().value == "dummy":
            self.read("dummy")
            self.build_tree("dummy", 0)

        else:
            raise Exception(f"Expected an identifier, integer, string, nil, dummy, true, false or an expression but got {self.input_stream.peek()}")


    def D(self):
        if self.debug:
            print("D", self.input_stream.peek().value)

        self.Da()

        if self.input_stream.peek().value == "within":
            self.read("within")
            print("D -> Da within D")
            self.D()
            self.build_tree("within", 2)
        

    def Da(self):
        if self.debug:
            print("Da", self.input_stream.peek().value)

        self.Dr()
        if self.input_stream.peek().value == "and":
            self.read("and")
            self.Dr()
            n = 2
            while self.input_stream.peek().value == "and":
                self.read("and")
                self.Dr()
                n+= 1
            self.build_tree("and", n)
        
    def Dr(self):
        if self.debug:
            print("Dr", self.input_stream.peek().value)

        if self.input_stream.peek().value =="rec":
            self.read("rec")
            self.Db()
            self.build_tree("rec", 1)
        elif self.input_stream.peek().type == "IDENTIFIER" or self.input_stream.peek().type == "left_bracket":
            self.Db()
        else:
            raise Exception(f"Expected rec or IDENTIFIER or left_bracket but got {self.input_stream.peek().value}")

    def Db(self):
        if self.debug:
            print("Db", self.input_stream.peek().value)

        if self.input_stream.peek().type == "IDENTIFIER":
            print(self.input_stream.peek(index=1))
            if self.input_stream.peek(index=1).type == "IDENTIFIER" or self.input_stream.peek(index=1).value == "(":
                self.read(type_check=True, type_="IDENTIFIER")
                self.Vb()
                n = 2
                while self.input_stream.peek().type == "IDENTIFIER" or self.input_stream.peek().value == "(":
                    self.Vb()
                    n += 1
                self.read("=")
                self.E()
                self.build_tree("function_form", n+1)
                # print("Db -> Vb+ = E")
            elif self.input_stream.peek(index=1).value == "=" or self.input_stream.peek(index=1).value == ",":
                # self.read(type_check=True, type_="IDENTIFIER")
                self.Vl()
                self.read("=")
                self.E()
                self.build_tree("=", 2)
        elif self.input_stream.peek().value == "(":
            self.read("(")
            self.D()
            self.read(")")
            print("Db -> (D)")
        
        else:
            raise Exception("Expected IDENTIFIER or ( but got {self.input_stream.peek().value}")
        

    def Vb(self):
        if self.debug:
            print("Vb", self.input_stream.peek().value)

        if self.input_stream.peek().type == "IDENTIFIER":
            self.read(type_check=True, type_="IDENTIFIER")
        elif self.input_stream.peek().value == "(":
            self.read("(")
            if self.input_stream.peek() is not None and self.input_stream.peek().type == "IDENTIFIER":
                self.Vl()
                self.read(")")
            else:
                self.read(")")
                self.build_tree("()", 0)
        else:
            raise Exception(f"Expected IDENTIFIER or ( but got {self.input_stream.peek().value}")
        
    def Vl(self):
        if self.debug:
            print("Vl", self.input_stream.peek().value)
            
        if self.input_stream.peek().type == "IDENTIFIER":
            n = 1
            self.read(type_check=True, type_="IDENTIFIER")
            while self.input_stream.peek().value == ",":
                self.read(",")
                self.read(type_check=True, type_="IDENTIFIER")
                n+= 1
            if n > 1:
                self.build_tree(",", n)
        else:
            raise Exception(f"Expected IDENTIFIER but got {self.input_stream.peek().value}")