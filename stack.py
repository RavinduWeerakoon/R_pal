class Stack():
    def __init__(self, stack_list=None):
        self.stack = stack_list if stack_list else []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            return None
        
    def is_empty(self):
        return len(self.stack) == 0
    
    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        else:
            return None
        
    def size(self):
        return len(self.stack)
    
