class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, item):
        self.queue.append(item)
    def dequeue(self):
        return self.queue.pop(0)
    def is_empty(self):
        return len(self.queue) == 0
    def peek(self, index=0):
        if len(self.queue) > index + 1:
            return self.queue[index]
        else:
            return None