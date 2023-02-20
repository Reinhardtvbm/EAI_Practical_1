class RPSNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    # produce the child nodes: ["'prev'"R", "'prev'"P", "'prev'"S"] (prev is parent node value)
    def expand_children(self):
        parent_val = self.value
        self.children = [RPSNode(parent_val + "R"), RPSNode(parent_val + "P"), RPSNode(parent_val + "S")]

    # return the node's value as a list of chars in ['R', 'P', 'S']
    def sequence(self):
        return list(self.value)

class FIFOQueue:
    def __init__(self):
        self.queue = []

    def push(self, element):
        self.queue.append(element)
    
    def pop(self):
        return self.queue.pop(0)

class BFS:
    def __init__(self):
        self.queue = FIFOQueue()
        self.queue.push(RPSNode("R"))
        self.queue.push(RPSNode("P"))
        self.queue.push(RPSNode("S"))

    def get_next_node_sequence(self):
        # get the next node in the queue
        next_node = self.queue.pop()

        # expand the children
        next_node.expand_children()
        child_nodes = next_node.children

        # put the children in the queue
        for child_node in child_nodes:
            self.queue.push(child_node)

        # return the node's value
        return next_node.sequence()

class BreakSequence:
    def __init__(self, sequence):
        self.sequence = sequence
        self.index = 0

    def get_next_move(self):
        next_move = self.sequence[self.index]

        self.index += 1
        self.index %= len(self.sequence)

        return next_move


def deep_copy(list):
    copy = []

    for element in list:
        copy.append(element)

    return copy

def counter_move(move):
    if move == "R":
        return "P"
    elif move == "P":
        return "S"
    elif move == "S":
        return "R"
    else:
        return None

# rpsrunner:

# while True:
bot_move = input

if bot_move == "":
    # class to be used for breadth first search
    breadth_first_search = BFS()

    # the sequence of moves currently being tested
    curr_sequence = breadth_first_search.get_next_node_sequence()
    # the previous sequence that was tested
    prev_sequence = []
    # copy of the current sequence
    copy_sequence = deep_copy(curr_sequence)

    # the break sequence for breakable.py
    break_sequence = None
    # whether the break sequence has been found
    cracked = False

    enemy_bot_move = ""
    prev_enemy_bot_move = ""
else:
    prev_enemy_bot_move = enemy_bot_move
    enemy_bot_move = bot_move

if len(curr_sequence) == 0:
    # if all the moves in the current sequence have been played, then update the sequences
    prev_sequence = copy_sequence
    curr_sequence = breadth_first_search.get_next_node_sequence()
    copy_sequence = deep_copy(curr_sequence)

if cracked == False:
    # if we have not found the break sequence, then the next move to play 
    # is the next move in the current sequence that is being tested
    output = curr_sequence.pop(0)
    
    # if the bot repeats its previous move, then we have found the break sequence
    if prev_enemy_bot_move == enemy_bot_move and enemy_bot_move != "":
        cracked = True
        break_sequence = BreakSequence(prev_sequence)
        counter = counter_move(enemy_bot_move)
else:
    # if we have found the break sequence, then the counter to the move being repeated
    # must be played
    output = counter

    # if the bot is no longer repeating moves, then the break sequence must be played
    # again
    if prev_enemy_bot_move != enemy_bot_move:
        output = break_sequence.get_next_move()
        counter = counter_move(enemy_bot_move)