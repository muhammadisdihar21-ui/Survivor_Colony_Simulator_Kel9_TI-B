# SINGLE LINKED LIST NODE
# Digunakan untuk activity log
class SingleNode:
    def __init__(self, data):
        self.data = data
        self.next = None


# DOUBLE LINKED LIST NODE
# Digunakan untuk navigasi log
class DoubleNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


# CIRCULAR LINKED LIST NODE
# Digunakan untuk giliran survivor
class CircularNode:
    def __init__(self, survivor):
        self.survivor = survivor
        self.next = None