from token_ import Token

class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
    
    def __repr__(self):
        return self.name

    def add_child(self, child) -> None:
        self.children.insert(0,child)


    def print_node(self, level=0):
        print("."*level + self.name)
        for child in self.children:
            if type(child) == Node:
                child.print_node(level+1)
            elif type(child) == Token:
                print("."*(level+1) + str(child))
            else:
                raise Exception(f"Invalid Child Type, {child}")

    def __str__(self):
        return f"{self.name} | Children : {len(self.children)}"