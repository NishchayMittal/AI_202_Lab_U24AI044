class PriorityQueue:   #PRIORITY QUEUE FOR WORKING WITH A* BEFS
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)
        self.items.sort(key=f_h)   

    def pop(self):
        if self.is_empty():
            return None
        return self.items.pop(0)

class greedyPriorityQueue:   #PRIORITY QUEUE FOR WORKING WITH GREEDY BEFS
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)
        self.items.sort(key=h)   

    def pop(self):
        if self.is_empty():
            return None
        return self.items.pop(0)

#CITIES STORED 
cities = [
    "Syracuse", "Buffalo", "Detroit", "Cleveland", "Pittsburgh",
    "Philadelphia", "New York", "Columbus", "Indianapolis", "Chicago",
    "Boston", "Providence", "Portland", "Baltimore"
]


#INDEX CORRESPONDING TO CITIES
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

# ADJ MATRIX FOR CITIES AND CONNECTIONS
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


#h(n)
def h(node):
    heuristic=(260, 400, 610, 550, 470, 270, 215, 640, 780, 860, 0, 50, 107, 360)
    return heuristic[city_index[node["STATE"]]]

#f(n) + h(n)
def f_h(node):
    return h(node) + f(node)

#A* befs
def A_BEST_FIRST_SEARCH(problem,initial,goal):
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


ans, explored=A_BEST_FIRST_SEARCH(graph, "Chicago", "Boston")
print("A* BEST FIRST SEARCH")

if ans:
    path=extract_path(ans)
    print("Best-First Path:", path)
    print("Total Cost:", ans["PATH-COST"])
    print("Nodes Explored:", explored)
else:
    print("Failure")

print(" ")
print(" ")
print(" ")

#greedy befs
def GREEDY_BEST_FIRST_SEARCH(problem,initial,goal):
    node ={
        "STATE" : initial,
        "PARENT" : None,
        "ACTION" : None,
        "PATH-COST" : 0
    }

    frontier = greedyPriorityQueue()
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

ans, explored=GREEDY_BEST_FIRST_SEARCH(graph, "Chicago", "Boston")
print("GREEDY BEST FIRST SEARCH")

if ans:
    path=extract_path(ans)
    print("Best-First Path:", path)
    print("Total Cost:", ans["PATH-COST"])
    print("Nodes Explored:", explored)
else:
    print("Failure")
