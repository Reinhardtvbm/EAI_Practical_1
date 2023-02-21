# a single node in the tree
class RPSNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    # produce the child nodes: ["'prev'"R", "'prev'"P", "'prev'"S"] (prev is parent node value)
    # for dynamically explanding the tree during a search
    def expand_children(self):
        parent_val = self.value
        self.children = [RPSNode(parent_val + "R"), RPSNode(parent_val + "P"), RPSNode(parent_val + "S")]

    # return the node's value as a list of chars in ['R', 'P', 'S']
    def sequence(self):
        return list(self.value)

# first-in-first-out queue for iterative implementation of a breadth first search
class FIFOQueue:
    def __init__(self):
        self.queue = []

    def push(self, element):
        self.queue.append(element)
    
    def pop(self):
        return self.queue.pop(0)

# for completing the breadth first search of the tree
class BFS:
    def __init__(self):
        self.queue = FIFOQueue()
        parent_nodes = [RPSNode("R"), RPSNode("P"), RPSNode("S")]
        
        # we start with the level two nodes in the queue, since the min length of the 
        # break sequence is 2 (only means we have to check 3 fewer sequences, but is 
        # more correct for the pedantic among us)
        for node in parent_nodes:
            node.expand_children()

            for child in node.children:
                self.queue.push(child)

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

# stack for iterative implementation of a depth first search
class Stack:
    def __init__(self):
        self.list = []
    
    def push(self, element):
        self.list.append(element)

    def pop(self):
        return self.list.pop()

    def empty(self):
        return len(self.list) == 0

# for completing the depth first search of the tree
class DFS:
    def __init__(self, depth):
        self.depth = depth
        self.stack = Stack()
        self.stack.push(RPSNode("S"))
        self.stack.push(RPSNode("P"))
        self.stack.push(RPSNode("R"))

    def get_next_node_sequence(self):
        if not self.stack.empty(): 
            next_node = self.stack.pop()

            next_node.expand_children()

            if len(next_node.children[0].sequence()) <= self.depth:
                for child in reversed(next_node.children):
                    self.stack.push(child)

            return next_node.sequence()
        else:
            return RPSNode("R").sequence()

# a class for playing an already found break sequence when repetition stops during a match 
class BreakSequence:
    def __init__(self, sequence):
        self.sequence = sequence
        self.index = 0

    def get_next_move(self):
        next_move = self.sequence[self.index]

        self.index += 1
        self.index %= len(self.sequence)

        return next_move
    
    def reached_end(self):
        return self.index == 0

# had issues with lists being shallow copies?
def deep_copy(list):
    copy = []

    for element in list:
        copy.append(element)

    return copy

# prduce the move which beats the input move
def counter_move(move):
    if move == "R":
        return "P"
    elif move == "P":
        return "S"
    elif move == "S":
        return "R"
    else:
        return None

# rpsrunner code:

# while True: (used for testing with own input using input())
bot_move = input
use_bfs = True

# initialisation for first move
if bot_move == "":
    # class to be used for breadth first search
    breadth_first_search = BFS()
    depth_first_search = DFS(5) # longest break sequnece = 5 moves

    # the sequence of moves currently being tested
    if use_bfs:
        curr_sequence = breadth_first_search.get_next_node_sequence()
    else:
        curr_sequence = depth_first_search.get_next_node_sequence()
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
    # update the previously played move and the current move
    prev_enemy_bot_move = enemy_bot_move
    enemy_bot_move = bot_move

if len(curr_sequence) == 0:
    # if all the moves in the current sequence have been played, then update the sequence to be tested
    #   NOTE: the break sequence will be the sequence tested previously when moves are repeated, 
    #         and not the sequence currently being tested
    prev_sequence = copy_sequence
    
    if use_bfs:
        curr_sequence = breadth_first_search.get_next_node_sequence()
    else:
        curr_sequence = depth_first_search.get_next_node_sequence()

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
        counter = counter_move(enemy_bot_move) # update the move to counter repeatition

        # if we have played the entire break sequence, and the bot is still
        # not repeating moves, then tree search must continue
        if break_sequence.reached_end():
            cracked = False

# ============= END OF FILE ==================