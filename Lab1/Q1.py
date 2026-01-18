class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

    def is_empty(self):
        return len(self.items) == 0

graph = {
    'Syracuse': {'Buffalo': 150, 'Philadelphia': 253, 'New York': 254, 'Boston': 312},
    'Buffalo': {'Syracuse': 150, 'Detroit': 256, 'Cleveland': 189, 'Pittsburgh': 215},
    'Detroit': {'Buffalo': 256, 'Cleveland': 169, 'Chicago': 283},
    'Cleveland': {'Buffalo': 189, 'Detroit': 169, 'Chicago': 345, 'Columbus': 144, 'Pittsburgh': 134},
    'Pittsburgh': {'Buffalo': 215, 'Cleveland': 134, 'Columbus': 185, 'Philadelphia': 305, 'Baltimore': 247},
    'Philadelphia': {'Syracuse': 253, 'Pittsburgh': 305, 'New York': 97, 'Baltimore': 101},
    'New York': {'Syracuse': 254, 'Philadelphia': 97, 'Providence': 181, 'Boston': 215},
    'Columbus': {'Cleveland': 144, 'Pittsburgh': 185, 'Indianapolis': 176},
    'Indianapolis': {'Columbus': 176, 'Chicago': 182},
    'Chicago': {'Detroit': 283, 'Cleveland': 345, 'Indianapolis': 182},
    'Boston': {'Syracuse': 312, 'New York': 215, 'Portland': 107, 'Providence': 50},
    'Providence': {'Boston': 50, 'New York': 181},
    'Portland': {'Boston': 107},
    'Baltimore': {'Pittsburgh': 247, 'Philadelphia': 101}
}

def DFS(graph,start,end,path=None,cost=0):
    if path is None:
        path = [start]

    if start == end:
        return[(path,cost)]
    
    allp = []
    for adj,val in graph.get(start,{}).items():
        if adj not in path:
            newp = DFS(graph,adj,end,path+[adj],cost+val)
            for p in newp:
                allp.append(p)
    return allp

def BFS(graph, start, end):
    queue = Queue()
    queue.enqueue((start, [start], 0))
    allp = []

    while not queue.is_empty():
        curr, path, cost = queue.dequeue()

        for adj, val in graph.get(curr, {}).items():
            if adj not in path:
                if adj == end:
                    allp.append((path + [adj], cost + val))
                else:
                    queue.enqueue((adj, path + [adj], cost + val))

    return allp
start = "Syracuse"
end = "Chicago"

print(f"--- Finding all paths from {start} to {end} ---\n")

dfs= DFS(graph, start, end)
print(f"DFS found {len(dfs)} unique paths.")

bfs = BFS(graph, start, end)
print(f"BFS found {len(bfs)} unique paths.\n")

print("Possible Paths:")
for i, (path, cost) in enumerate(bfs[:]):
    print(f"Path {i+1}: {' -> '.join(path)} | Total Cost: {cost} miles")


print("----------")


for i, (path, cost) in enumerate(dfs[:]):
    print(f"Path {i+1}: {' -> '.join(path)} | Total Cost: {cost} miles")