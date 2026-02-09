# graph = {
#     "Syracuse": [("Buffalo", 150), ("New York", 254), ("Boston", 312)],
#     "Buffalo": [("Syracuse", 150), ("Detroit", 256), ("Cleveland", 189), ("Pittsburgh", 215)],
#     "Detroit": [("Buffalo", 256), ("Cleveland", 169), ("Chicago", 283)],
#     "Cleveland": [("Detroit", 169), ("Buffalo", 189), ("Chicago", 345),
#                   ("Columbus", 144), ("Pittsburgh", 134)],
#     "Columbus": [("Cleveland", 144), ("Indianapolis", 176), ("Pittsburgh", 185)],
#     "Indianapolis": [("Columbus", 176), ("Chicago", 182)],
#     "Pittsburgh": [("Buffalo", 215), ("Cleveland", 134), ("Columbus", 185),
#                     ("Philadelphia", 305), ("Baltimore", 247)],
#     "Philadelphia": [("Pittsburgh", 305), ("Baltimore", 101), ("New York", 97)],
#     "Baltimore": [("Pittsburgh", 247), ("Philadelphia", 101)],
#     "New York": [("Syracuse", 254), ("Philadelphia", 97), ("Boston", 215)],
#     "Boston": [("Syracuse", 312), ("New York", 215)]
# }

# def f(node):
#     return node["PATH-COST"]

# def EXPAND(problem, node):
#     s=node["STATE"]
#     children=[]

#     for neighbor, weight in problem[s]:
#         s0=neighbor
#         cost=node["PATH-COST"]+weight

#         child={
#             "STATE": s0,
#             "PARENT": node,
#             "ACTION": neighbor,
#             "PATH-COST": cost
#         }
#         children.append(child)

#     return children

# def BEST_FIRST_SEARCH(problem, start, goal):

#     node={
#         "STATE": start,
#         "PARENT": None,
#         "ACTION": None,
#         "PATH-COST": 0
#     }

#     frontier=[node]
#     reached={start: node}

#     explored_count=0

#     while frontier:

#         frontier.sort(key=f)
#         node=frontier.pop(0)
#         explored_count+=1

#         if node["STATE"]==goal:
#             return node, explored_count
        
#         for child in EXPAND(problem, node):
#             s=child["STATE"]

#             if s not in reached or child["PATH-COST"]<reached[s]["PATH-COST"]:
#                 reached[s]=child
#                 frontier.append(child)

#     return None, explored_count

# def extract_path(node):
#     path=[]
#     while node:
#         path.append(node["STATE"])
#         node=node["PARENT"]
#     return path[::-1]

# result_node, explored=BEST_FIRST_SEARCH(graph, "Syracuse", "Chicago")

# if result_node:
#     path=extract_path(result_node)
#     print("Best-First Path:", path)
#     print("Total Cost:", result_node["PATH-COST"])
#     print("Nodes Explored:", explored)
# else:
#     print("Failure")



# def dfs_all_paths(graph, node, goal, path, cost, results):
#     if node==goal:
#         results.append((path, cost))
#         return

#     for neighbor, weight in graph[node]:
#         if neighbor not in path:
#             dfs_all_paths(graph, neighbor, goal, path+[neighbor], cost+weight, results)

# dfs_results=[]
# dfs_all_paths(graph, "Syracuse", "Chicago", ["Syracuse"], 0, dfs_results)

# dfs_paths = len(dfs_results)

# print("\nComparison")
# print("BFS Paths Found:", bfs_paths, "| Nodes Explored:", bfs_explored)
# print("DFS Paths Found:", dfs_paths)
# print("Best-First Nodes Explored:", explored)

class PriorityQueue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)
        self.items.sort(key=f)   

    def pop(self):
        if self.is_empty():
            return None
        return self.items.pop(0)


cities = [
    "Syracuse", "Buffalo", "Detroit", "Cleveland", "Pittsburgh",
    "Philadelphia", "New York", "Columbus", "Indianapolis", "Chicago",
    "Boston", "Providence", "Portland", "Baltimore"
]


city_index = {city: i for i, city in enumerate(cities)}

edges = [
    ("Syracuse","Buffalo",150), ("Syracuse","Philadelphia",253),
    ("Syracuse","New York",254), ("Syracuse","Boston",312),

    ("Buffalo","Detroit",256), ("Buffalo","Cleveland",189),
    ("Buffalo","Pittsburgh",215),

    ("Detroit","Cleveland",169), ("Detroit","Chicago",283),

    ("Cleveland","Chicago",345), ("Cleveland","Columbus",144),
    ("Cleveland","Pittsburgh",134),

    ("Pittsburgh","Columbus",185), ("Pittsburgh","Philadelphia",305),
    ("Pittsburgh","Baltimore",247),

    ("Philadelphia","New York",97), ("Philadelphia","Baltimore",101),

    ("New York","Boston",215), ("New York","Providence",181),

    ("Columbus","Indianapolis",176),

    ("Indianapolis","Chicago",182),

    ("Boston","Providence",50), ("Boston","Portland",107)
]


INF = float('inf')
n = len(cities)

graph = []

for i in range(n):
    row = []
    for j in range(n):
        if i == j:
            row.append(0)     
        else:
            row.append(INF)    
    graph.append(row)


for a, b, w in edges:
    i, j = city_index[a], city_index[b]
    graph[i][j] = w
    graph[j][i] = w  





# Nodes expansion func after reaching them (generates all possible nodes with path cost which is possible )
def EXPAND(problem, node):
    s = node["STATE"]
    children = []
    i = city_index[s]

    for j in range(len(cities)):
        if problem[i][j] != INF and problem[i][j] != 0:
            cost = node["PATH-COST"] + problem[i][j]
            child = {
                "STATE": cities[j],
                "PARENT": node,
                "ACTION": cities[j],
                "PATH-COST": cost
            }
            children.append(child)

    return children


# defining f() func for implementing befs
def f(node):
    return node["PATH-COST"]

def BEST_FIRST_SEARCH(problem,initial,goal):
    node ={
        "STATE" : initial,
        "PARENT" : None,
        "ACTION" : None,
        "PATH-COST" : 0
    }

    frontier = PriorityQueue()
    frontier.push(node)

    reached = {initial : node}
    count = 0

    while not frontier.is_empty():
        node = frontier.pop()
        count += 1
        if node["STATE"]==goal:
            return node,count
        for child in EXPAND(problem,node):
            s=child["STATE"]
            if s not in reached or child["PATH-COST"] < reached[s]["PATH-COST"]:
                reached[s]=child
                frontier.push(child)
    return None,count 


def extract_path(node):
    path=[]
    while node:
        path.append(node["STATE"])
        node=node["PARENT"]
    return path[::-1]


ans, explored=BEST_FIRST_SEARCH(graph, "Syracuse", "Chicago")

if ans:
    path=extract_path(ans)
    print("Best-First Path:", path)
    print("Total Cost:", ans["PATH-COST"])
    print("Nodes Explored:", explored)
else:
    print("Failure")


def bfs_all_paths(problem, start, goal):
    start_idx = city_index[start]
    goal_idx = city_index[goal]

    queue = [(start_idx, [start], 0)]  
    results = []
    explored = 0

    while queue:
        current, path, cost = queue.pop(0)
        explored += 1

        if current == goal_idx:
            results.append((path, cost))
            continue

        for j in range(len(cities)):
            if problem[current][j] != INF and problem[current][j] != 0:
                next_city = cities[j]
                if next_city not in path:
                    queue.append(
                        (j, path + [next_city], cost + problem[current][j])
                    )

    return results, explored

paths, explored = bfs_all_paths(graph, "Syracuse", "Chicago")

print("Total BFS Paths Found:", len(paths))
print("Nodes Explored:", explored)


def DFS_all_paths(problem, start, end, path=None, cost=0):
    if path is None:
        path = [start]

    if start == end:
        return [(path, cost)]

    all_paths = []
    i = city_index[start]

    for j in range(len(cities)):
        if problem[i][j] != INF and problem[i][j] != 0:
            next_city = cities[j]
            if next_city not in path:
                new_paths = DFS_all_paths(
                    problem,
                    next_city,
                    end,
                    path + [next_city],
                    cost + problem[i][j]
                )
                for p in new_paths:
                    all_paths.append(p)

    return all_paths

dfs_paths = DFS_all_paths(graph, "Syracuse", "Chicago")

print("Total DFS Paths Found:", len(dfs_paths))




