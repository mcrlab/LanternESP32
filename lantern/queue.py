class LinkedList:
    def __init__(self):
        self.head = None

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def append(self, node):
        if self.head == None:
            self.head = node
            return
        for current_node in self:
            pass
        current_node.set_next(node)

    def clear(self):
        self.head = None

    def remove(self):
        if self.head == None:
            return None
        temp = self.head
        self.head = self.head.next
        return temp


class Node:
    def __init__(self):
        self.next = None

    def set_next(self, node):
        self.next = node


class Step(Node):
    def __init__(self, color, start_time, length):
        super().__init__()
        self.color = color
        self.length = length
        self.start_time = start_time

    def __repr__(self):
        return self.color
