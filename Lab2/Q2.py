class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

    def is_empty(self):
        return len(self.items) == 0


# MUST be tuple (ordered)
goal = (0, 1, 2,
        3, 4, 5,
        6, 7, 8)

start = (7, 2, 4,
         5, 0, 6,
         8, 3, 1)


def notmove(state):
    moveup = movel = mover = moved = True

    for i in range(3):
        if state[i] == 0:
            moveup = False

    for i in (0, 3, 6):
        if state[i] == 0:
            movel = False

    for i in (2, 5, 8):
        if state[i] == 0:
            mover = False

    for i in (6, 7, 8):
        if state[i] == 0:
            moved = False

    return moveup, movel, moved, mover
def DFS(start, goal):
    stack = [(start, 0)]   # (state, depth)
    visited = set()
    visited.add(start)

    count = 0

    while stack:
        curr, depth = stack.pop()
        count += 1

        if curr == goal:
            return count, depth   # depth = cost

        moveu, movel, moved, mover = notmove(curr)
        zero = curr.index(0)

        if moveu:
            new = list(curr)
            new[zero], new[zero - 3] = new[zero - 3], new[zero]
            new = tuple(new)
            if new not in visited:
                visited.add(new)
                stack.append((new, depth + 1))

        if moved:
            new = list(curr)
            new[zero], new[zero + 3] = new[zero + 3], new[zero]
            new = tuple(new)
            if new not in visited:
                visited.add(new)
                stack.append((new, depth + 1))

        if movel:
            new = list(curr)
            new[zero], new[zero - 1] = new[zero - 1], new[zero]
            new = tuple(new)
            if new not in visited:
                visited.add(new)
                stack.append((new, depth + 1))

        if mover:
            new = list(curr)
            new[zero], new[zero + 1] = new[zero + 1], new[zero]
            new = tuple(new)
            if new not in visited:
                visited.add(new)
                stack.append((new, depth + 1))

    return count, None

states, cost = DFS(start, goal)

print("Number of states explored using DFS:", states)
print("Cost of solution (depth):", cost)
