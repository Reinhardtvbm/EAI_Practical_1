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
        prev_value = self.move.value
        self.children = [Node(prev_value + 'R'), Node(prev_value + 'P'), Node(prev_value + 'S')]

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

class RPS:
    valid_chars = ['R', 'P', 'S']

    def __init__(self) -> None:
        pass

    def rock(self):
        return 'R'
    
    def paper(self):
        return 'P'
    
    def scissors(self):
        return 'S'
    
    def counter(self, move):
        if move == "R":
            return "P"
        elif move == "P":
            return "S"
        elif move == "S":
            return "R"
        else:
            return "C"

class GameData:
    def __init__(self):
        self.visited = set()
        self.dfs_queue = []
        self.break_sequence = []
        self.prev_enemy_move = ""
        self.curr_enemy_move = ""
        self.counter_move = ""
        self.index = 0

    def reset(self):
        self.visited = set()
        self.dfs_queue = []
        self.prev_enemy_move = ""
        self.curr_enemy_move = ""
    
    def next_in_break_seq(self):
        next_move = self.break_sequence[self.index % len(self.break_sequence)]
        self.index = (self.index + 1) % len(self.break_sequence)

        return next_move

def deep_copy(list):
    copy = []

    for element in list:
        copy.append(element)

    return copy

# while True:
# inp = input()

if input == "":
    sequence_found = False

    # create the start node with "", and expand the children, so we get ['R', 'P', 'S'] inp the queue
    start_node = Node("")
    start_node.expand_children()
    
    game_data = GameData()
    game_data.dfs_queue = start_node.children

    rps = RPS()

    curr_sequence = []
    prev_sequence = []
    curr_seq_copy = []
    repeating = False

if len(curr_sequence) == 0 and sequence_found == False:
    # make the current node the queue's first element 
    curr_node = game_data.dfs_queue.pop(0)
    
    # add the current node to the already visited nodes
    game_data.visited.add(curr_node)
    sequence = curr_node.move.value

    # the current sequence to test is now the list of characters contained 
    # by the Node's move field
    prev_sequence = curr_sequence
    curr_sequence = list(sequence)
    curr_seq_copy = deep_copy(curr_sequence)

    curr_node.expand_children()

    for child_node in curr_node.children:
        if child_node not in game_data.visited:
            game_data.dfs_queue.append(child_node)

game_data.prev_enemy_move = game_data.curr_enemy_move
game_data.curr_enemy_move = input

if sequence_found == False:
    output = curr_sequence.pop(0)

    if game_data.prev_enemy_move == game_data.curr_enemy_move and game_data.curr_enemy_move in ["R", "P", "S"]:
        sequence_found = True
        repeating = True
        game_data.break_sequence = curr_seq_copy
        game_data.counter_move = rps.counter(game_data.curr_enemy_move)
else:
    repeating = game_data.prev_enemy_move == game_data.curr_enemy_move and game_data.curr_enemy_move in ["R", "P", "S"]

    if repeating:
        output = game_data.counter_move
    else:
        output = game_data.next_in_break_seq()
        game_data.counter_move = rps.counter(game_data.curr_enemy_move)

    # print(output)