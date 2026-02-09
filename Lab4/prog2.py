class PriorityQueue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, node, goal):
        self.items.append(node)
        self.items.sort(key=lambda n: f(n, goal))   # ordered by f

    def pop(self):
        return self.items.pop(0)


grid = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,3,1],
    [1,1,1,0,1,1,1,1,0,1],
    [1,0,1,0,1,1,1,1,0,1],
    [1,0,1,0,1,1,0,1,0,1],
    [1,0,1,0,1,1,0,0,0,1],
    [1,0,1,0,1,1,1,1,0,1],
    [1,0,1,2,1,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]
]

rows = len(grid)
cols = len(grid[0])

for i in range(rows):
    for j in range(cols):
        if grid[i][j] == 2:
            start = (i, j)
        if grid[i][j] == 3:
            goal = (i, j)

def f(node, goal):
    x1, y1 = node["STATE"]
    x2, y2 = goal
    return  abs(x1 - x2) + abs(y1 - y2)

def EXPAND(problem, node):
    children = []
    r, c = node["STATE"]
#UP DOWN LEFT RIGHT
    moves = [(-1,0),(1,0),(0,-1),(0,1)]

    for dx, dy in moves:
        nr, nc = r + dx, c + dy

        if 0 <= nr < rows and 0 <= nc < cols:
            if problem[nr][nc] != 1:

                child = {
                    "STATE": (nr, nc),
                    "PARENT": node,
                    "ACTION": (nr, nc),
                    "PATH-COST": node["PATH-COST"] + 1
                }
                children.append(child)

    return children

def BEST_FIRST_SEARCH(problem, start, goal):

    node = {
        "STATE": start,
        "PARENT": None,
        "ACTION": None,
        "PATH-COST": 0
    }

    frontier = PriorityQueue()
    frontier.push(node, goal)

    reached = {start: node}
    explored = 0

    while not frontier.is_empty():

        node = frontier.pop()
        explored += 1

        if node["STATE"] == goal:
            return node, explored

        for child in EXPAND(problem, node):
            s = child["STATE"]

            if s not in reached or child["PATH-COST"] < reached[s]["PATH-COST"]:
                reached[s] = child
                frontier.push(child, goal)

    return None, explored

def extract_path(node):
    path = []
    while node:
        path.append(node["STATE"])
        node = node["PARENT"]
    return path[::-1]

result, explored = BEST_FIRST_SEARCH(grid, start, goal)

path = extract_path(result)

print("PATH:")
for p in path:
    print(p)

print("\nTotal steps taken:", result["PATH-COST"])
print("Nodes explored:", explored)
