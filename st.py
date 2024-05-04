from node import Node
from token_ import Token

    # def print_node(self, level=0):
    #     print("."*level + self.name)
    #     for child in self.children:
    #         if type(child) == Node:
    #             child.print_node(level+1)
    #         elif type(child) == Token:
    #             print("."*(level+1) + str(child))
    #         else:
    #             raise Exception(f"Invalid Child Type, {child}")

class ST_node:
    def __init__(self, name, left=None, right=None):
        self.name = name
        if type(self.name) != str:
            raise Exception(f"Invalid Name Type, {self.name}, {type(self.name)}")
        self.left = left
        self.right = right

    def __repr__(self):
        return self.name
    def __str__(self) -> str:
        return self.name 
    
    @staticmethod
    def let(x,p,e):
        lamb = ST_node("lambda", x, p)
        gam = ST_node("gamma", lamb, e)
        return gam

    @staticmethod
    def where(x,p,e):
        lamb = ST_node("lambda", x, p)
        gam = ST_node("gamma", e, lamb)
        return gam
    
    @staticmethod
    def op(op, E1,E2):
        gam2 = ST_node("gamma", ST_node(op), E1)
        gam1 = ST_node("gamma", gam2, E2)
        return gam1
    @staticmethod
    def fcn_form(p,v,E):
        lamb = ST_node("lambda", v[-1], E)

        for n in v[:-1:-1]:
            lamb = ST_node("lambda", n, lamb)
            
        return ST_node("=",p, lamb) 
    
    @staticmethod
    def tau(lst):
        gam = ST_node("nil")

        for x in lst:
            gam1 = ST_node("gamma",ST_node("aug"), gam)
            gam = ST_node("gamma", gam1, x)
        return gam
    



class Standard_tree:
    def __init__(self,node):
        self.root = node


    def create_tree(self, node):
        
        for n in range(len(node.children)):
            
            child = node.children[n]
            
            if type(child) == Node:
                self.create_tree(child)
            
            if type(child) == Token:
                #print("--------------------", child, type(child.value))
                node.children[n] = ST_node(child.value)
                
            
            

            if type(child) == Node:

                if child.name == '=':#if you encounter an eqaul node make it a st node while adding allready converted childs as children
                    node.children[n] = ST_node("=", child.children[0], child.children[1])
                elif child.name == 'gamma':
                    node.children[n] = ST_node("gamma", child.children[0], child.children[1])
                else:
                    node.children[n] = self.parse_node(child)

            print(f"{node.name}....",node.children)

    def parse_node(self,child):
        #print(child.name, child.children)
        if child.name == "let":
            #since = is a converted one
            return ST_node.let(child.children[0].left, child.children[1], child.children[0].right)

        elif child.name == "where":
            return ST_node.where(child.children[1].left, child.children[1].right, child.children[0])
        
        elif child.name in ["aug", "or", "&", "+", "-", "/", "**", "gr", "ge", "ls", "le"]:
            return ST_node.op(child.name, child.children[0], child.children[1])
        
        elif child.name == "function_form":
            x = ST_node.fcn_form(child.children[0], child.children[1:-1], child.children[-1])
            #print("from the fcn ............",x)
            return x
        elif child.name == "tau":
            return ST_node.tau(child.children)

            
    def parse_tree(self):
        self.create_tree(self.root)
        self.root = self.parse_node(self.root)
        return self.root

            
            

           
            





        



    