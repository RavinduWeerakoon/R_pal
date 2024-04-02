from token_ import Token

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, item) -> None:
        self.queue.append(item)
    def dequeue(self) -> Token:
        return self.queue.pop(0)
    def is_empty(self) -> bool:
        return len(self.queue) == 0
    def peek(self, index=0) -> Token:
        if len(self.queue) > index + 1:
            return self.queue[index]
        else:
            return None