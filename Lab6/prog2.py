class PriorityQueue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, node):
        self.items.append(node)
        self.items.sort(key=lambda n: f(n))   

    def pop(self):
        return self.items.pop(0)


grid = [
    [2,0,0,0,1],
    [0,1,0,0,3],
    [0,3,0,1,1],
    [0,1,0,0,1],
    [3,0,0,0,3]
]

rows = len(grid)
cols = len(grid[0])

goals = set()
for i in range(rows):
    for j in range(cols):
        if grid[i][j] == 2:
            start = (i, j)
        if grid[i][j] == 3:
            goals.add((i, j))
def g(node):
    return node["PATH-COST"]
def f(node):
    return g(node) + h(node)
def h(node):
    minh = 0
    x1, y1 = node["STATE"]
    if not node["GOALS"]:
        return 0
    minh = float('inf')

    for (x2, y2) in node["GOALS"]:
        dist = abs(x1 - x2) + abs(y1 - y2)
        minh = min(minh, dist)

        

    return minh


def EXPAND(problem, node):
    children = []
    r, c = node["STATE"]
#UP DOWN LEFT RIGHT
    moves = [(-1,0),(1,0),(0,-1),(0,1)]

    for dx, dy in moves:
        nr, nc = r + dx, c + dy

        if 0 <= nr < rows and 0 <= nc < cols:
            if problem[nr][nc] != 1:

                LEFT = set(node["GOALS"])
                if (nr,nc) in LEFT:
                    LEFT.remove((nr,nc))

                child = {
                    "STATE": (nr, nc),
                    "PARENT": node,
                    "ACTION": (nr, nc),
                    "PATH-COST": node["PATH-COST"] + 1,
                    "GOALS" : frozenset(LEFT)
                }
                children.append(child)

    return children

def BEST_FIRST_SEARCH(problem, start):

    node = {
        "STATE": start,
        "PARENT": None,
        "ACTION": None,
        "PATH-COST": 0,
        "GOALS": frozenset(goals)
    }

    frontier = PriorityQueue()
    frontier.push(node)

    reached = {}
    reached[(start, frozenset(goals))] = 0
    explored = 0

    while not frontier.is_empty():

        node = frontier.pop()
        explored += 1

        if not node["GOALS"]:
            return node, explored

        for child in EXPAND(problem, node):
            s = (child["STATE"],child["GOALS"])

            if s not in reached or child["PATH-COST"] < reached[s]:
                reached[s] = child["PATH-COST"]
                frontier.push(child)

    return None, explored

def extract_path(node):
    path = []
    while node:
        path.append(node["STATE"])
        node = node["PARENT"]
    return path[::-1]

result, explored = BEST_FIRST_SEARCH(grid, start)

path = extract_path(result)

print("PATH:")
for p in path:
    print(p)

print("\nTotal steps taken:", result["PATH-COST"])
print("Nodes explored:", explored)
