from token_ import Token

class Parser():

    def __init__(self, input_stream):
        self.input_stream = input_stream

    def parse(self):
        E(self.input_stream)

    def read(self, token: Token):
        print(token.value)



def read(token: Token):
    print(token.value)


def D():
    pass

def E(input_stream):
    next = input_stream.pop()
    if next.value == "let":
        read("let")
        D(input_stream)
        read("in")
        E(input_stream)

    elif next.value == "fn":
        read("fn")
    
    else:
        input_stream.push(next)
        Ew(input_stream)


def Ew():
    pass