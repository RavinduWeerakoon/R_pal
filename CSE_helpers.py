from stack import Stack

class Delta_node():
        """
        Nodes of a Control Structure
        Possible types are "env", "lambda", "gamma", "identifier", "INTEGER", "BOOLEAN", "nil", "aug", "true", "false", "dummy", "operator"
        lambda uses index and variable
        env uses index
        """
        def __init__(self, type, value=None):
            self.type = type
            self.value = value
            self.index = None
            self.variable = None

        def set_index(self, index):
            self.index = index

        def set_variable(self, variable):
            self.variable = variable
    
        def __str__(self):
            return f"Control_Node: {self.type} | Value : {self.value} | Index : {self.index}"
        

        @staticmethod
        def create_lambda(index, variable):
            lambda_node = Delta_node("lambda")
            lambda_node.set_index(index)
            lambda_node.set_variable(variable)
            return lambda_node

        @staticmethod
        def create_env(index):
            env_node = Delta_node("env")
            env_node.set_index(index)
            return env_node

        @staticmethod
        def create_beta(index):
            beta_node = Delta_node("beta")
            beta_node.set_index(index)
            return beta_node
        


class Delta():
    """
    Control Structure
    Consists of a stack
    """
    def __init__(self, list=None):
        self.stack = Stack(list) if list else Stack()
        
    def push(self, delta_node):
        self.stack.push(delta_node)

    def pop(self):
        return self.stack.pop()
    
    def is_empty(self):
        return self.stack.is_empty()
    
    # Replace the top of the stack with another control structure (Delta)
    def push_delta(self, delta):
        for delta_node in delta.stack.stack:
            self.push(delta_node)

    # Get the current env of the control structure
    def get_env(self):
        index = 0
        delta_node: Delta_node = self.stack.peek(index)
        while delta_node.type != "env" and delta_node != None:
            index += 1
            delta_node = self.stack.peek(index)
        if delta_node.type == "env":
            return delta_node.index
        else:
            raise Exception("No env in Delta")

    def __str__(self):
        return f"{[delta_node.type for delta_node in self.stack.stack]}"
    

class Stack_node():

    """
    Nodes of a Stack on the CSE
    Possible types are "env", "lambda", "eta", "INTEGER", "BOOLEAN", "nil", "aug", "true", "false", "dummy"
    lambda uses index, variable and env_index
    env uses index (NOT env_index!!)
    """

    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        self.index = None
        self.variable = None
        self.env_index = None

    def set_index(self, index):
        self.index = index

    def set_variable(self, variable):
        self.variable = variable

    def set_env(self, env):
        self.env_index = env


    @staticmethod
    def create_env(index):
        env_node = Stack_node("env")
        env_node.set_index(index)
        return env_node
    
    @staticmethod
    def create_lambda(index, variable, env_index):
        lambda_node = Stack_node("lambda")
        lambda_node.set_index(index)
        lambda_node.set_variable(variable)
        lambda_node.set_env(env_index)
        return lambda_node
    
    @staticmethod
    def create_eeta(index, variable, env_index):
        eeta_node = Stack_node("eeta")
        eeta_node.set_index(index)
        eeta_node.set_variable(variable)
        eeta_node.set_env(env_index)
        return eeta_node
    
    def __repr__(self):
        return f"Stack_Node: {self.type} | Value : {self.value} | Index : {self.index} | Variable : {self.variable} | Env : {self.env_index}"


class env_node():
    """
    Environment Node
    """
    def __init__(self, index, parent=None):
        self.index = index
        self.parent = parent
        self.assignments = {}

    # Add a variable assignment to the environment
    def add_assignment(self, variable, value):
        self.assignments[variable] = value

    # Get the value of a variable in the environment
    def get_assignment(self, variable):
        if variable in self.assignments:
            # If the assignment is a node (lambda, eeta) return the node
            if type(self.assignments[variable]) == Stack_node:
                return self.assignments[variable]
            # If the assignment is a primitive return the value
            return self.assignments[variable].value
        elif self.parent:
            return self.parent.get_assignment(variable)
        else:
            raise Exception(f"Variable {variable} not found in env {self.index}")
        
    def __repr__(self):
        return f"Env: {self.index} | Parent : {self.parent.index if self.parent else None} | Assignments : {self.assignments}"
        
    