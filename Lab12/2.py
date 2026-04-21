class Deque:
    def __init__(self):
        self.data = []
        self.front = 0

    def append(self, item):
        self.data.append(item)

    def popleft(self):
        if self.is_empty():
            return None
        item = self.data[self.front]
        self.front += 1
        return item

    def is_empty(self):
        return self.front >= len(self.data)

def parse_grid(grid_str):
    grid = []
    for i in range(9):
        row = []
        for j in range(9):
            row.append(int(grid_str[i * 9 + j]))
        grid.append(row)
    return grid


def init_domains(grid):
    domains = {}
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                domains[(r, c)] = set(range(1, 10))
            else:
                domains[(r, c)] = {grid[r][c]}
    return domains
def get_neighbors(r, c):
    neighbors = set()

    for i in range(9):
        if i != c:
            neighbors.add((r, i))
        if i != r:
            neighbors.add((i, c))

    box_r, box_c = (r // 3) * 3, (c // 3) * 3
    for i in range(box_r, box_r + 3):
        for j in range(box_c, box_c + 3):
            if (i, j) != (r, c):
                neighbors.add((i, j))

    return neighbors

def generate_arcs():
    arcs = []
    for r in range(9):
        for c in range(9):
            for n in get_neighbors(r, c):
                arcs.append(((r, c), n))
    return arcs
def revise(domains, Xi, Xj):
    removed_values = set()

    for x in domains[Xi]:
        if not any(x != y for y in domains[Xj]):
            removed_values.add(x)

    if removed_values:
        print(f"\n ARC PRUNED: {Xi} <- {Xj}")
        print(f"   Before: {domains[Xi]}")
        print(f"   Removing: {removed_values}")

        domains[Xi] -= removed_values

        print(f"   After: {domains[Xi]}")

        return True, len(removed_values)

    return False, 0
def ac3(domains):
    queue = Deque()

    for arc in generate_arcs():
        queue.append(arc)

    total_removed = 0
    step = 1

    while not queue.is_empty():
        Xi, Xj = queue.popleft()

        revised, removed = revise(domains, Xi, Xj)
        total_removed += removed

        if revised:
            print(f"   (Step {step}) Domain reduced\n")
            step += 1

            if len(domains[Xi]) == 0:
                print(" FAILURE: Domain became empty")
                return False, total_removed

            for Xk in get_neighbors(*Xi):
                if Xk != Xj:
                    queue.append((Xk, Xi))

    return True, total_removed
if __name__ == "__main__":

    grid_str = (
        "000000000"
        "059000008"
        "200008000"
        "045000000"
        "003000000"
        "006003050"
        "000070000"
        "000000000"
        "000050002"
    )

    grid = parse_grid(grid_str)
    domains = init_domains(grid)

    print("AC-3 IMPORTANT TRACE")

    success, removed = ac3(domains)
    print(f"Total values removed: {removed}")

    if success:
        print(" No domain empty → Consistent")
    else:
        print(" Failure detected")