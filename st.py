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
    def __init__(self, name, left=None, right=None, value=None):
        self.name = name
        self.value = value
        if type(self.name) != str:
            raise Exception(f"Invalid Name Type, {self.name}, {type(self.name)}")
        self.left = left
        self.right = right
        self.mid = None # Will be used for ->
        self.children = None

    def set_mid(self, mid):
        self.mid = mid

    def __repr__(self):
        return self.name
    def __str__(self) -> str:
        return self.name

  
    
    def print_st_node(self, level=0):
        if self.children:
            print("."*level + self.name)
            for child in self.children:
                if type(child) == ST_node:
                    child.print_st_node(level+1)
                else:
                    print("."*(level+1) + str(child))
            return
        else:
            print("."*level + self.name, self.value)
            for child in (self.left, self.mid, self.right):
                if child is not None:
                    child.print_st_node(level+1)
    
    @staticmethod
    def let(x,p,e):

         
            lamb = ST_node("lambda", x, p)
            gam = ST_node("gamma", lamb, e)
            return gam

    @staticmethod
    def where(x,p,e):

        lamb = ST_node("lambda", x, p)
        gam = ST_node("gamma", lamb, e)
        return gam
    
    @staticmethod
    def op(op, E1,E2):
        gam2 = ST_node("gamma", ST_node(op), E1)
        gam1 = ST_node("gamma", gam2, E2)
        return gam1
    
    @staticmethod
    def fcn_form(p,v,E):
        if type(v) == ST_node:
            print("This is for the comma node")
            print('The Comma Node......', v.children)
            lamb = ST_node("lambda", v, E)
            return ST_node("=",p, lamb)
       
        lamb = ST_node("lambda", v[-1], E)

        for n in reversed(v[:-1]):
            lamb = ST_node("lambda", n, lamb)
            
        return ST_node("=",p, lamb) 
    

    @staticmethod
    def within(x1, e1, x2, e2):
        lamb = ST_node("lambda", x1, e2)
        gamma = ST_node("gamma", lamb, e1)
        eq = ST_node("=", x2, gamma)

        return eq

    @staticmethod
    def tau(lst):

        t_node = ST_node("tau")
        t_node.children = lst
        return t_node
    
    @staticmethod
    def parse_multiple_lambda(V,E):
        lamb = E 
        for n in V[::-1]:
            lamb = ST_node("lambda", n, lamb)
        return lamb
    
    @staticmethod
    def ternary(B, T, F): # The "->" node
        ternary_node = ST_node("->", B, F)
        ternary_node.set_mid(T)
        return ternary_node



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
                node.children[n] = ST_node(name=child.type, value=child.value)
                
            
            

            if type(child) == Node:

                if child.name == '=':#if you encounter an eqaul node make it a st node while adding allready converted childs as children
                    node.children[n] = ST_node("=", child.children[0], child.children[1])
                elif child.name == 'gamma':
                    node.children[n] = ST_node("gamma", child.children[0], child.children[1])
                elif child.name == 'and' and all(x.name == '=' for x in child.children):
                    
                    tau = Node("tau")
                    tau.children = [x.right for x in child.children]
                    parsed_tau = self.parse_node(tau)
                    
                    com = Node("com")
                    com.children = [x.left for x in child.children]

                    gam = parsed_tau


                    node.children[n] = ST_node("=", com, parsed_tau)





                else:
                    node.children[n] = self.parse_node(child)

            print(f"{node.name}....",node.children)

    def parse_node(self,child):
        #print(child.name, child.children)
        if child.name == "gamma":
            return ST_node("gamma", child.children[0], child.children[1])
        
        elif child.name == "let":
            #since = is a converted one
            return ST_node.let(child.children[0].left, child.children[1], child.children[0].right)

        elif child.name == "where":
            return ST_node.where(child.children[1].left,child.children[0], child.children[1].right)
        
        elif child.name in ["aug", "or", "&", "+", "-", "/", "*", "**", "gr", "ge", "ls", "le", "<", "<=", ">", ">=", "eq"]:
            # return ST_node.op(child.name, child.children[0], child.children[1])
            return ST_node(child.name, child.children[0], child.children[1])
        
        elif child.name == "function_form":
            
            if child.children[1].name == ",":
                # x = ST_node.fcn_form(child.children[0], child.children[1].children, child.children[2])
                x = ST_node.fcn_form(child.children[0], child.children[1], child.children[2])
            else:
                x = ST_node.fcn_form(child.children[0], child.children[1:-1], child.children[-1])
            return x
        
        elif child.name =="within":
            x = ST_node.within(child.children[0].left, child.children[0].right, child.children[1].left, child.children[1].right)
            return x

        elif child.name == "tau":
            return ST_node.tau(child.children)
        elif child.name == "lambda":
            #print("Parse multiple lambda called")
            return ST_node.parse_multiple_lambda(child.children[:-1], child.children[-1])
        
        elif child.name in ["neg", "not"]:
            # return ST_node("gamma", ST_node(child.name), child.children[0])
            return ST_node(child.name, child.children[0])
        elif child.name == "@":
            gam = ST_node("gamma", child.children[1], child.children[0])
            gam = ST_node("gamma", gam, child.children[2])
            return gam
        elif child.name == "rec":
            lamb = ST_node("lambda", child.children[0].left, child.children[0].right)
            gam = ST_node("gamma", ST_node("ystar"), lamb)
        
            return ST_node("=", child.children[0].left, gam)
        elif child.name == "->":
            return ST_node.ternary(child.children[0], child.children[1], child.children[2])
        
        elif child.name == ",":
            # , node is not standardized
            # The children are extracted within the function_form of the parent of the , node
            # Other uses of , may need to be handle
            # POSSIBLE ERROR: If the , node is not a child of function_form this may lead to unexpected results

            com_node = ST_node(",")
            com_node.children = child.children
            return com_node
    

            
    def parse_tree(self):
        self.create_tree(self.root)
        self.root = self.parse_node(self.root)
        return self
    
    def print_tree(self):
        print("\n\nStandardized Tree..")
        self.root.print_st_node()
        print("Done and Dusted\n\n")