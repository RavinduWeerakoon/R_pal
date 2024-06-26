from CSE_helpers import Delta, Delta_node, Stack_node, env_node
from stack import Stack
from st import ST_node


class CSE:
    def __init__(self, st_tree, debug=False):
        self.deltas = [Delta()]
        self.delta_index = 0
        self.env_index = 0
        self.debug = debug

        # Convert ST to CSE
        self.st_to_cse(st_tree.root)

        # Setup Stack
        self.stack = Stack([Stack_node.create_env(0)])

        # Setup control structure
        self.control = Delta([Delta_node.create_env(0)]) #Initialize with e0 env node
        self.control.push_delta(self.deltas[0]) # Push the first delta to the control structure

        # Setup environment
        primitive_env = env_node(index=0)

        # Add a definition for Print to the primitive environment
        # Print will be assigned to a node of type Print
        # When the identifier Print is encountered, the node of type Print will be pushed to the stack
        # When gamma operation is encountered, the Print node will print the preceding node of the stack
        # Likewise for all the other primitive functions
        primitive_env.add_assignment("Print", Stack_node("Print"))

        # Order definition
        # Will return the length (order) of the tuple when gamma is applied to Order on the stack
        primitive_env.add_assignment("Order", Stack_node("Order"))

        # Conc function
        # Will concatenate two strings
        primitive_env.add_assignment("Conc", Stack_node("Conc"))

        # Stern function
        # Will return the string after the first character
        primitive_env.add_assignment("Stern", Stack_node("Stern"))

        # Stem function
        # Will return the first character of the string
        primitive_env.add_assignment("Stem", Stack_node("Stem"))

        #Istuple function
        #Will return true if the given value is a tuple
        primitive_env.add_assignment("Istuple", Stack_node("Istuple"))

        #Isstring function
        #Will return true if the given value is a string
        primitive_env.add_assignment("Isstring", Stack_node("Isstring"))

        #ItoS function
        #Will convert an integer to a string
        primitive_env.add_assignment("ItoS", Stack_node("ItoS"))



        self.envs = [primitive_env]


    def increment_delta_index(self):
        self.delta_index += 1
        return self.delta_index
    
    def increment_env_index(self):
        self.env_index += 1
        return self.env_index
    
    def print_deltas(self):
        if self.debug:
            print("\n")
            print("PRINTING DELTAS: ")
            for delta in self.deltas:
                print(delta)


    def st_to_cse(self, st_node:ST_node, index=0):
        if self.debug:
            print("From st_to_cse",st_node)
        delta = self.deltas[index]
        if st_node.name == "lambda":
            # lambda_delta_node = Delta_node("lambda", index=self.increment_index(), variable=st_node.left.value)
            #Ravindu-when we encounter multiple vars via "," node
            # print(st_node.left)
            if st_node.left.name == ",":
                #adding the values of each varaibles
                lambda_delta_node = Delta_node.create_lambda(self.increment_delta_index(), [s.value for s in st_node.left.children])
                #print("From when , node ",st_node.left.children)
            else:
                lambda_delta_node = Delta_node.create_lambda(self.increment_delta_index(), st_node.left.value)
            delta.push(lambda_delta_node)
            self.deltas.append(Delta())
            self.st_to_cse(st_node.right, self.delta_index)
        elif st_node.name == "gamma":
            delta.push(Delta_node("gamma"))
            self.st_to_cse(st_node.left, index)
            self.st_to_cse(st_node.right, index)
        elif st_node.name == "->":
            # Add the beta node to the delta
            delta.push(Delta_node.create_beta(self.increment_delta_index()))
            # Add the conditional expression to the delta
            self.st_to_cse(st_node.left, index)
            #Truthy Expression
            self.deltas.append(Delta())
            self.st_to_cse(st_node.mid, self.delta_index)
            #Falsey Expression
            self.deltas.append(Delta())
            self.st_to_cse(st_node.right, self.increment_delta_index())

            # Clarification - Beta node will only store one index
            # However there are two deltas that are created for the true and false expressions
            # If the conditional is true, delta[index] will be executed
            # If the conditional is false, delta[index+1] will be executed
            # This is implmented in the CSE operate function

        elif st_node.name == "IDENTIFIER":
            delta.push(Delta_node("identifier", value=st_node.value))
        elif st_node.name == "INTEGER":
            delta.push(Delta_node("INTEGER", value=st_node.value))
        elif st_node.name == "BOOLEAN":
            delta.push(Delta_node("BOOLEAN", value=st_node.value))
        elif st_node.name == "STRING":
            delta.push(Delta_node("STRING", value=st_node.value))
        elif st_node.name == "nil":
            delta.push(Delta_node("nil"))
        # elif st_node.name == "aug":
        #     delta.push(Delta_node("aug"))
        elif st_node.name == "true":
            delta.push(Delta_node("BOOLEAN", value=True))
        elif st_node.name == "false":
            delta.push(Delta_node("BOOLEAN", value=False))
        elif st_node.name in ["aug", "or", "&", "+", "-", "/", "*", "**", "<", "<=", ">", ">=", "gr", "ge", "ls", "le", "eq", "ne"]:
            delta.push(Delta_node("OPERATOR", value=st_node.name))
            self.st_to_cse(st_node.left, index)
            self.st_to_cse(st_node.right, index)
        elif st_node.name == "not" or st_node.name == "neg":
            delta.push(Delta_node("UNARY_OPERATOR", value=st_node.name))
            self.st_to_cse(st_node.left, index)
        elif st_node.name == "ystar":
            delta.push(Delta_node("ystar"))
        elif st_node.name == ",":
            vars = [s for s in st_node.children]
            lambda_delta_node = Delta_node.create_lambda(self.increment_delta_index(), vars)
            # for var in lambda_delta_node.variable:
            #     self.st_to_cse(var, index)

        elif st_node.name == "tau":
            tau_node = Delta_node("tau", value=len(st_node.children))
            delta.push(tau_node)
            for child in st_node.children:
                self.st_to_cse(child, index)
            

        else:
            raise Exception(f"Invalid ST_node {st_node.name}")
        

    def operate(self):
        if self.debug:
            self.print_deltas()
            print("\nSTARTING CSE OPERATE()", self.control, "\n")
        control_element: Delta_node = self.control.pop()

        while control_element is not None:

            if self.debug:
                print(control_element, "   ========   ", self.stack.peek())

            if control_element.type == "env":
                stack_env = self.stack.peek(index=1)
                if stack_env and stack_env.index == control_element.index:
                    temp = self.stack.pop()
                    self.stack.pop()
                    self.stack.push(temp)
                else:
                    raise Exception("Invalid env or delta and stack env do not match")
                
            elif control_element.type == "identifier":
                current_env = self.control.get_env()
                value = self.envs[current_env].get_assignment(control_element.value)
                if type(value) == int:
                    self.stack.push(Stack_node("INTEGER", value))
                elif type(value) == str:
                    self.stack.push(Stack_node("STRING", value))
                elif type(value) == bool:
                    self.stack.push(Stack_node("BOOLEAN", value))
                elif type(value) == tuple:
                    self.stack.push(Stack_node("Tuple", value))
                elif type(value) == Stack_node:
                    self.stack.push(value)
                elif not value:
                    self.stack.push(Stack_node("nil"))
                else:
                    raise Exception(f"Invalid value / type not handled. Value: {value}")
                
            elif control_element.type == "lambda":
                current_env = self.control.get_env()
                lambda_stack_node = Stack_node.create_lambda(index=control_element.index, variable=control_element.variable, env_index=current_env)
                self.stack.push(lambda_stack_node)


            elif control_element.type == "gamma":
                operand1 = self.stack.peek()
                if operand1.type == "lambda":
                    # Pop the lambda node off the stack
                    lambda_node = self.stack.pop()

                    # Create a new env and add the lambda variable to the new env
                    new_env = env_node(index=self.increment_env_index(), parent=self.envs[lambda_node.env_index])


                    if len(lambda_node.variable) > 1:
                        # Multiple variables in lambda
                            # rand:Stack_node = self.stack.pop()
                            # print("\n\nADDING TO ENV: ", var, rand, "\n\n")
                            # new_env.add_assignment(var, rand)

                        rand:Stack_node = self.stack.pop()
                        for i, var in enumerate(lambda_node.variable):
                            new_env.add_assignment(var, rand.value[i])
                    else:
                        # Single variable in lambda
                        rand = self.stack.pop()
                        new_env.add_assignment(lambda_node.variable[0], rand)
                        
                    self.envs.append(new_env)

                    # Push the new env to the control structure and push the delta to the control structure
                    self.control.push(Delta_node.create_env(self.env_index))
                    self.control.push_delta(self.deltas[lambda_node.index])

                    # Push the new env to the stack
                    self.stack.push(Stack_node.create_env(self.env_index))

                elif operand1.type == "ystar":
                    ystar_node = self.stack.pop()
                    lambda_node = self.stack.pop()
                    eeta_node = Stack_node.create_eeta(lambda_node.index, lambda_node.variable, lambda_node.env_index)
                    # print("from ystar---", lambda_node.variable)
                    self.stack.push(eeta_node)

                elif operand1.type == "eeta":
                    eeta_node = self.stack.pop()
                    lambda_node = Stack_node.create_lambda(eeta_node.index, eeta_node.variable, eeta_node.env_index)
                    self.stack.push(eeta_node)
                    self.stack.push(lambda_node)

                    self.control.push(Delta_node("gamma"))
                    self.control.push(Delta_node("gamma"))

                elif operand1.type == "Tuple":
                    # When gamma is applied with a tuple on the stack,
                    # The nth [actually n-1 in python] element 
                    # of the tuple is pushed to the stack
                    # n is an integer on the stack, after the tuple

                    tuple_ = self.stack.pop()
                    n = self.stack.pop()

                    if type(tuple_.value) != tuple:
                        raise Exception("Invalid top of stack for Tuple. Must be Tuple", tuple_.type, type(tuple_.value))
                    
                    if n.type != "INTEGER":
                        raise Exception("Invalid index for tuple. Must be INTEGER")
                    
                    if n.value > len(tuple_.value):
                        raise Exception("Invalid index for tuple. n > len(Tuple)")
                    

                    value = tuple_.value[n.value - 1]
                    if type(value) == int:
                        self.stack.push(Stack_node("INTEGER", value))
                    elif type(value) == bool:
                        self.stack.push(Stack_node("BOOLEAN", value))
                    elif type(value) == str:
                        self.stack.push(Stack_node("STRING", value))
                    elif type(value) == tuple:
                        self.stack.push(Stack_node("Tuple", value))
                    elif not value:
                        self.stack.push(Stack_node("nil"))
                    else:
                        raise Exception(f"Invalid value / type found with index {n.value} of tuple. Value: {value}, Type : {value.type}")
                    # self.stack.push(tuple_.value[n.value - 1])
                        

                elif operand1.type == "Print":
                    self.stack.pop()
                    # THIS IS THE ACTUAL PRINT FUNCTION!!!
                    print(self.stack.peek().value)

                elif operand1.type == "Order":
                    self.stack.pop()
                    stack_node = self.stack.pop()
                    if stack_node.type == "nil":
                        self.stack.push(Stack_node("INTEGER", 0))
                    elif stack_node.type == "Tuple":
                        self.stack.push(Stack_node("INTEGER", len(stack_node.value)))
                    else:
                        raise Exception(f"Invalid top of stack for Order. Must be Tuple or nil got {stack_node.type}")
                    

                elif operand1.type == "Conc":
                    conc = self.stack.pop()
                    operand2 = self.stack.pop()
                    operand1 = self.stack.pop()
                    if operand1.type != "STRING" or operand2.type != "STRING":
                        raise Exception(f"Invalid operands for Conc. Must be STRING got {operand1.type} and {operand2.type}")
                    self.stack.push(Stack_node("STRING", operand2.value + operand1.value))

                    # Pop off a second gamma from the control structure
                    self.control.pop()

                elif operand1.type == "Stern":
                    stern = self.stack.pop()
                    string = self.stack.pop()
                    if string.type != "STRING":
                        raise Exception(f"Invalid operand for Stern. Must be STRING got {string.type}")
                    self.stack.push(Stack_node("STRING", string.value[1:]))

                elif operand1.type == "Stem":
                    stem = self.stack.pop()
                    string = self.stack.pop()
                    if string.type != "STRING":
                        raise Exception(f"Invalid operand for Stern. Must be STRING got {string.type}")
                    
                    if len(string.value) == 0:
                        self.stack.push(Stack_node("STRING", ""))
                    else:
                        self.stack.push(Stack_node("STRING", string.value[0]))

                elif operand1.type == "Istuple":
                    istuple = self.stack.pop()
                    value = self.stack.pop()
                    if value.type == "Tuple":
                        self.stack.push(Stack_node("BOOLEAN", True))
                    else:
                        self.stack.push(Stack_node("BOOLEAN", False))

                elif operand1.type == "Isstring":
                    isstring = self.stack.pop()
                    value = self.stack.pop()
                    if value.type == "STRING":
                        self.stack.push(Stack_node("BOOLEAN", True))
                    else:
                        self.stack.push(Stack_node("BOOLEAN", False))

                elif operand1.type == "ItoS":
                    itos = self.stack.pop()
                    integer = self.stack.pop()
                    if integer.type != "INTEGER":
                        raise Exception(f"Invalid operand for ItoS. Must be INTEGER got {integer.type}")
                    self.stack.push(Stack_node("STRING", str(integer.value)))

                else:
                    # print("Invalid gamma operation. Operand1:", operand1.type)
                    raise Exception("Invalid gamma operation. No lambda / eeta on top of stack")
                
            elif control_element.type == "ystar":
                self.stack.push(Stack_node("ystar"))


            elif control_element.type == "tau":
                new_tuple = Stack_node("Tuple", tuple())
                for i in range(control_element.value):
                    rand = self.stack.pop()
                    new_tuple.value =  new_tuple.value + (rand.value,)
                self.stack.push(new_tuple)


            elif control_element.type == "beta":
                operand1 = self.stack.pop()
                if operand1.type == "BOOLEAN":
                    if operand1.value:
                        self.control.push_delta(self.deltas[control_element.index])
                    else:
                        self.control.push_delta(self.deltas[control_element.index + 1])
                else:
                    raise Exception(f"Invalid top of stack for beta. Must be BOOLEAN got {operand1.type}")
                
            elif control_element.type == "UNARY_OPERATOR":
                operand = self.stack.pop()
                if control_element.value == "not":
                    if operand.type != "BOOLEAN":
                        raise Exception(f"Invalid Operand for NOT, must be BOOLEAN got {operand.type}")
                    self.stack.push(Stack_node("BOOLEAN", not operand.value))
                elif control_element.value == "neg":
                    if operand.type != "INTEGER":
                        raise Exception(f"Invalid Operand for NEG, must be INTEGER got {operand.type}")
                    self.stack.push(Stack_node("INTEGER", -operand.value))
                else:
                    raise Exception(f"Invalid Unary Operator {control_element.value}")
            
            elif control_element.type == "OPERATOR":
                operand1 = self.stack.pop()
                operand2 = self.stack.pop()

                if control_element.value == "+":
                    self.stack.push(Stack_node("INTEGER", operand1.value + operand2.value))
                elif control_element.value == "-":
                    self.stack.push(Stack_node("INTEGER", operand1.value - operand2.value))
                elif control_element.value == "*":
                    self.stack.push(Stack_node("INTEGER", int(operand1.value * operand2.value)))
                elif control_element.value == "/":
                    self.stack.push(Stack_node("INTEGER", int(operand1.value / operand2.value)))
                elif control_element.value == "*":
                    self.stack.push(Stack_node("INTEGER", int(operand1.value * operand2.value)))
                elif control_element.value == "**":
                    self.stack.push(Stack_node("INTEGER", int(operand1.value ** operand2.value)))
                elif control_element.value == "&":
                    self.stack.push(Stack_node("BOOLEAN", operand1.value and operand2.value))
                elif control_element.value == "or":
                    self.stack.push(Stack_node("BOOLEAN", operand1.value or operand2.value))
                elif control_element.value == "gr" or control_element.value == ">":
                    self.stack.push(Stack_node("BOOLEAN", operand1.value > operand2.value))
                elif control_element.value == "ge" or control_element.value == ">=":
                    self.stack.push(Stack_node("BOOLEAN", operand1.value >= operand2.value))
                elif control_element.value == "ls" or control_element.value == "<":
                    self.stack.push(Stack_node("BOOLEAN", operand1.value < operand2.value))
                elif control_element.value == "le" or control_element.value == "<=":
                    self.stack.push(Stack_node("BOOLEAN", operand1.value <= operand2.value))
                elif control_element.value == "eq":
                    self.stack.push(Stack_node("BOOLEAN", operand1.value == operand2.value))
                elif control_element.value == "ne":
                    self.stack.push(Stack_node("BOOLEAN", operand1.value != operand2.value))
                elif control_element.value == "aug":
                    if operand1.type == "Tuple":
                        if operand2.type == "nil":
                            self.stack.push(operand1)
                        else:
                            new_tuple = operand1.value + (operand2.value,)
                            self.stack.push(Stack_node("Tuple", new_tuple))
                    elif operand1.type == "nil":
                        if operand2.type == "nil":
                            self.stack.push(Stack_node("nil"))
                        elif operand2.type == "Tuple":
                            self.stack.push(operand2)
                        else:
                            self.stack.push(Stack_node("Tuple", (operand2.value,)))
                    else:
                        if operand2.type == "nil":
                            self.stack.push(Stack_node("Tuple", (operand1.value,)))
                        elif operand2.type == "Tuple":
                            new_tuple = (operand1.value,) + operand2.value
                            self.stack.push(Stack_node("Tuple", new_tuple))
                        else:
                            new_tuple = (operand1.value, operand2.value)
                            self.stack.push(Stack_node("Tuple", new_tuple))
                else:
                    raise Exception(f"Invalid Operator {control_element.value}")


            elif control_element.type == "nil":
                self.stack.push(Stack_node("nil"))

            elif control_element.type == "INTEGER":
                self.stack.push(Stack_node("INTEGER", int(control_element.value)))

            elif control_element.type == "BOOLEAN":
                self.stack.push(Stack_node("BOOLEAN", control_element.value))
            
            elif control_element.type == "STRING":
                string = control_element.value
                if (string[0] == '"' and string[-1] == '"') or (string[0] == "'" and string[-1] == "'"):
                    self.stack.push(Stack_node("STRING", string[1:-1]))
                else:
                    raise Exception(f"Invalid STRING format {string}")

            # Get the next control element
            control_element = self.control.pop()

        else:
            result = self.stack.pop().value
            if self.debug:
                print("\nFinished Execution")
                print("Result:", result)
            return result