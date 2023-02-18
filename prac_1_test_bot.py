import random

class Move:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value;

    def print(self):
        print(self.value)

class Node:
    def __init__(self, value):
        self.move = Move(value)
        self.children = []

    def expand_children(self):
        self.children = [Node(self.move.value + 'R'), Node(self.move.value + 'P'), Node(self.move.value + 'S')]

    def get_children(self):
        return self.children

    def get_sequence(self):
        self.move.get_value()

    def bfs(self):
        queue = [self]
        visited = set()

        while queue:
            current_node = queue.pop(0)
            visited.add(current_node)

            current_node.move.print()
            
            for child_node in current_node.children:
                if child_node not in visited:
                    queue.append(child_node)



def construct_tree(depth):
    # create the root node
    root_node = Node("")

    # retrieve its children (depth 1), and store in a list
    root_node.expand_children()

    current_children = [root_node.get_children()]

    for _ in range(depth - 1):
        new_children = []

        # expand each node in the current children list, and add their new children to a new list 
        for child_nodes in current_children:
            for node in child_nodes:
                node.expand_children()
                new_children.append(node.get_children())

        # clear the current children list, as these children are now old
        current_children.clear()

        # set the current children to the new children
        current_children = new_children

    # return the root node for traversing
    return root_node

# n = construct_tree(4)
# n.bfs()

SEQUENCE_MIN_LEN = 2
SEQUENCE_MAX_LEN = 5

inp = ""

while inp != 'E':
    inp = input()

    if inp == 'start':
        print('starting...')
        # create the start node with "", and expand the children, so we get ['R', 'P', 'S'] in the queue
        start_node = Node("")
        start_node.expand_children()
        
        queue = start_node.children
        
        # the set of already visited nodes
        visited = set()
        break_sequence = curr_sequence
        curr_sequence = []

        prev_input = ""
        curr_input = ""

        in_break = False


    if len(curr_sequence) == 0:
        # make the current node the queue's first element 
        curr_node = queue.pop(0)
        
        # add the current node to the already visited nodes
        visited.add(curr_node)
        sequence = curr_node.move.value

        # the current sequence to test is now the list of characters contained 
        # by the Node's move field
        curr_sequence = list(sequence + sequence)
        test_seq_len = len(curr_sequence)

        curr_node.expand_children()

        for child_node in curr_node.children:
            if child_node not in visited:
                queue.append(child_node)

    prev_input = curr_input
    curr_input = inp

    

    if in_break == False:
        output = curr_sequence.pop(0)

        if curr_input == prev_input:
            print("found sequence!")
            in_break = True

            visited = set()
            curr_sequence = []
            break_sequence = []
            
            if curr_input == 'R':
                exploit = 'P'
            elif curr_input == 'P':
                exploit = 'S'
            else:
                exploit = 'R'
    else:
        output = exploit
        
        if prev_input != curr_input:
            print("stopped repeating...")
            in_break = False


    print(inp + ' : ' + output) 