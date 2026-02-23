
class NODE:
    def __init__(self, state, parent=None):
        self.STATE = state
        self.PARENT = parent
        self.DEPTH = 0 if parent is None else parent.DEPTH + 1



class Problem:
    def __init__(self):
        self.INITIAL = (3, 3, 0)   # (girls_left, boys_left, boat_position)
        self.GOAL = (0, 0, 1)

    def IS_GOAL(self, state):
        return state == self.GOAL



def IS_VALID(g_left, b_left):
    g_right = 3 - g_left
    b_right = 3 - b_left

    if not (0 <= g_left <= 3 and 0 <= b_left <= 3):
        return False

    if g_left > 0 and b_left > g_left:
        return False

    if g_right > 0 and b_right > g_right:
        return False

    return True



def EXPAND(problem, node):
    g_left, b_left, boat = node.STATE
    moves = [(1,0),(2,0),(0,1),(0,2),(1,1)]
    children = []

    for g, b in moves:
        if boat == 0:
            new_state = (g_left - g, b_left - b, 1)
        else:
            new_state = (g_left + g, b_left + b, 0)

        if IS_VALID(new_state[0], new_state[1]):
            children.append(NODE(new_state, node))

    return children

def IS_CYCLE(node):
    current = node.PARENT
    while current:
        if current.STATE == node.STATE:
            return True
        current = current.PARENT
    return False

def DEPTH(node):
    return node.DEPTH


def DLS(problem,l):
    frontier = []
    frontier.append(NODE(problem.INITIAL))
    global dls_count
    dls_count = 0

    result = "FAILURE"

    while frontier :
        node = frontier.pop()


        if problem.IS_GOAL(node.STATE):
            return node
        
        if DEPTH(node) > l:
            result = "CUTOFF"

        elif not IS_CYCLE(node):
            dls_count += 1
            
            for child in EXPAND(problem,node):
                frontier.append(child)
    return result


problem = Problem()

print("Depth Limited Search (limit = 3):")
dls_result = DLS(problem, 3)
print(dls_result)
print("Number of nodes explored:")
print(dls_count)

def IDPS(problem):
    global depth
    depth = 0
    global idps_count
    idps_count = 0
    while True:
        result = DLS(problem, depth)
        idps_count += dls_count
        
        if result != "CUTOFF":
            return result
        
        depth += 1




print("\nIterative Deepening Search:")
ids_result = IDPS(problem)

if isinstance(ids_result, NODE):
    print("Solution found at depth:", ids_result.DEPTH)

    path = []
    while ids_result:
        path.append(ids_result.STATE)
        ids_result = ids_result.PARENT
    path.reverse()
    print(path)
else:
    print(ids_result)

print("Number of nodes explored:")
print(idps_count)