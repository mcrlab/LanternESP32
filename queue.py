class LinkedList:
    def __init__(self):
        self.head = None

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def __repr__(self):
        nodes = []
        for node in self:
            nodes.append(node.color)
        return " -> ".join(nodes)

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
    def __init__(self, color, length):
        super().__init__()
        self.color = color
        self.length = length

    def __repr__(self):
        return self.color

list = LinkedList()
list.append(Step("FF0000", length=2))
list.append(Step("00FF00", length=3))
list.append(Step("0000FF", length=4))
list.append(Step("FF00FF", length=5))
wait = list.head.length
a = None
for i in range(0, 30):
    if list.head is not None:
        print("{0} {1}".format(i, list.head.color))
        if i >= wait:
            a = list.remove()
            if list.head is not None:
                wait = list.head.length + i
            print(wait)
     