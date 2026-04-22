# # ── 1. Adjacency list (symmetric) ────────────────────────────────────────────
# ADJACENCY = {
#     "Kuchchh":          ["Jamnagar", "Rajkot", "Surendranagar", "Patan", "Banaskantha"],
#     "Banaskantha":      ["Kuchchh", "Patan", "Mehsana", "Sabarkantha"],
#     "Patan":            ["Kuchchh", "Banaskantha", "Mehsana", "Surendranagar"],
#     "Mehsana":          ["Banaskantha", "Patan", "Sabarkantha", "Gandhinagar", "Ahmedabad", "Surendranagar"],
#     "Sabarkantha":      ["Banaskantha", "Mehsana", "Gandhinagar", "Kheda", "Panchmahal", "Dahod"],
#     "Gandhinagar":      ["Mehsana", "Sabarkantha", "Ahmedabad"],
#     "Ahmedabad":        ["Mehsana", "Gandhinagar", "Surendranagar", "Kheda", "Anand", "Botad"],
#     "Surendranagar":    ["Kuchchh", "Patan", "Mehsana", "Ahmedabad", "Botad", "Rajkot"],
#     "Rajkot":           ["Kuchchh", "Surendranagar", "Botad", "Amreli", "Jamnagar"],
#     "Jamnagar":         ["Kuchchh", "Rajkot", "Porbandar", "Devbhumi Dwarka"],
#     "Devbhumi Dwarka":  ["Jamnagar", "Porbandar"],
#     "Porbandar":        ["Jamnagar", "Devbhumi Dwarka", "Junaghad"],
#     "Junaghad":         ["Porbandar", "Amreli", "Gir Somnath", "Botad"],
#     "Gir Somnath":      ["Junaghad", "Amreli"],
#     "Amreli":           ["Rajkot", "Junaghad", "Gir Somnath", "Bhavnagar", "Botad"],
#     "Botad":            ["Surendranagar", "Ahmedabad", "Anand", "Bhavnagar", "Amreli", "Rajkot"],
#     "Bhavnagar":        ["Amreli", "Botad", "Anand", "Bharuch"],
#     "Anand":            ["Ahmedabad", "Kheda", "Vadodara", "Bharuch", "Bhavnagar", "Botad"],
#     "Kheda":            ["Ahmedabad", "Sabarkantha", "Gandhinagar", "Anand", "Vadodara", "Panchmahal"],
#     "Panchmahal":       ["Sabarkantha", "Kheda", "Vadodara", "Dahod"],
#     "Dahod":            ["Sabarkantha", "Panchmahal"],
#     "Vadodara":         ["Kheda", "Anand", "Panchmahal", "Bharuch", "Narmada", "Chhota Udaipur"],
#     "Chhota Udaipur":   ["Vadodara", "Narmada", "Panchmahal", "Dahod"],
#     "Bharuch":          ["Bhavnagar", "Anand", "Vadodara", "Narmada", "Surat"],
#     "Narmada":          ["Bharuch", "Vadodara", "Chhota Udaipur", "Surat"],
#     "Surat":            ["Bharuch", "Narmada", "Tapi", "Navsari"],
#     "Tapi":             ["Surat", "Narmada", "Dangs", "Navsari"],
#     "Dangs":            ["Tapi", "Navsari"],
#     "Navsari":          ["Surat", "Tapi", "Dangs", "Valsad"],
#     "Valsad":           ["Navsari"],
# }

# # Build symmetric graph using a plain dict of sets
# graph = {}
# for u, neighbors in ADJACENCY.items():
#     if u not in graph:
#         graph[u] = set()
#     for v in neighbors:
#         graph[u].add(v)
#         if v not in graph:
#             graph[v] = set()
#         graph[v].add(u)

# DISTRICTS = sorted(graph.keys())
# N = len(DISTRICTS)


# # ── 2. CSP Backtracking solver ────────────────────────────────────────────────

# def select_unassigned(assignment, domains, graph):
#     """MRV heuristic + Degree heuristic as tie-breaker."""
#     unassigned = [d for d in DISTRICTS if d not in assignment]
#     min_remaining = min(len(domains[d]) for d in unassigned)
#     candidates = [d for d in unassigned if len(domains[d]) == min_remaining]
#     return max(candidates, key=lambda d: len([n for n in graph[d] if n not in assignment]))


# def forward_check(var, color, domains, graph):
#     """Remove `color` from neighbours' domains.
#     Returns new domains dict, or None if any domain becomes empty."""
#     new_domains = {d: set(vals) for d, vals in domains.items()}
#     for neighbor in graph[var]:
#         if color in new_domains[neighbor]:
#             new_domains[neighbor].discard(color)
#             if not new_domains[neighbor]:
#                 return None
#     return new_domains


# def backtrack(assignment, domains, graph, k):
#     """Recursive backtracking search. Returns coloring dict or None."""
#     if len(assignment) == len(DISTRICTS):
#         return assignment
#     var = select_unassigned(assignment, domains, graph)
#     for color in sorted(domains[var]):
#         assignment[var] = color
#         new_domains = forward_check(var, color, domains, graph)
#         if new_domains is not None:
#             new_domains[var] = {color}
#             result = backtrack(assignment, new_domains, graph, k)
#             if result is not None:
#                 return result
#         del assignment[var]
#     return None


# def solve_min_colors(graph, max_k=6):
#     """Iterate k = 2, 3, ... until a valid coloring is found."""
#     for k in range(2, max_k + 1):
#         print(f"  Trying k = {k} colors ...", end=" ")
#         domains = {d: set(range(k)) for d in DISTRICTS}
#         result = backtrack({}, domains, graph, k)
#         if result is not None:
#             print("Solution found!")
#             return k, result
#         print("No solution.")
#     raise RuntimeError("No solution found within max_k.")


# # ── 3. Verify solution ────────────────────────────────────────────────────────

# def verify(coloring, graph):
#     for u in graph:
#         for v in graph[u]:
#             if coloring[u] == coloring[v]:
#                 print(f"  CONFLICT: {u} and {v} both have color {coloring[u]}")
#                 return False
#     return True


# # ── 4. Pretty-print ───────────────────────────────────────────────────────────

# COLOR_NAMES = {0: "Red", 1: "Blue", 2: "Green", 3: "Yellow", 4: "Purple", 5: "Orange"}

# def pretty_print(k, coloring):
#     print(f"\n{'='*60}")
#     print(f"  Gujarat District Map Coloring  -- {k} colors used")
#     print(f"{'='*60}")
#     groups = {}
#     for d, c in sorted(coloring.items()):
#         if c not in groups:
#             groups[c] = []
#         groups[c].append(d)
#     for c in sorted(groups):
#         name  = COLOR_NAMES.get(c, f"Color-{c}")
#         dists = ", ".join(groups[c])
#         print(f"  {name:8s} ({len(groups[c]):2d} districts): {dists}")
#     print(f"\n  Total districts coloured: {len(coloring)}")
#     print(f"  Chromatic number (min colors): {k}")


# # ── 5. Main ───────────────────────────────────────────────────────────────────

# if __name__ == "__main__":
#     print(f"Gujarat Map Coloring CSP")
#     print(f"Districts: {N}  |  Adjacency edges: {sum(len(v) for v in graph.values())//2}\n")
#     print("Searching for minimum chromatic number via backtracking CSP ...")
#     k, coloring = solve_min_colors(graph)

#     ok = verify(coloring, graph)
#     print(f"\n  Constraint verification: {'PASSED' if ok else 'FAILED'}")

#     pretty_print(k, coloring)

#     print(f"\n{'─'*60}")
#     print("  Raw coloring (district -> color index):")
#     for d in sorted(coloring):
#         c = coloring[d]
#         print(f"    {d:<22s} -> {COLOR_NAMES.get(c, c)} ({c})")

graph = {
    "Kachchh": ["Banaskantha", "Patan", "Surendranagar"],
    "Banaskantha": ["Kachchh", "Patan", "Sabarkantha"],
    "Patan": ["Kachchh", "Banaskantha", "Mehsana", "Surendranagar"],
    "Mehsana": ["Patan", "Sabarkantha", "Gandhinagar", "Ahmedabad"],
    "Sabarkantha": ["Banaskantha", "Mehsana", "Gandhinagar", "Panchmahal"],
    "Gandhinagar": ["Mehsana", "Sabarkantha", "Ahmedabad", "Kheda"],
    "Ahmedabad": ["Mehsana", "Gandhinagar", "Kheda", "Anand", "Surendranagar", "Bhavnagar"],
    "Kheda": ["Gandhinagar", "Ahmedabad", "Anand", "Panchmahal"],
    "Panchmahal": ["Sabarkantha", "Kheda", "Dahod", "Vadodara"],
    "Dahod": ["Panchmahal"],
    "Vadodara": ["Panchmahal", "Anand", "Bharuch", "Narmada"],
    "Anand": ["Ahmedabad", "Kheda", "Vadodara", "Bharuch"],
    "Bharuch": ["Vadodara", "Anand", "Narmada", "Surat"],
    "Narmada": ["Vadodara", "Bharuch", "Surat"],
    "Surat": ["Bharuch", "Narmada", "Navsari", "Dang"],
    "Navsari": ["Surat", "Valsad", "Dang"],
    "Valsad": ["Navsari"],
    "Dang": ["Surat", "Navsari"],
    "Surendranagar": ["Kachchh", "Patan", "Ahmedabad", "Rajkot"],
    "Rajkot": ["Surendranagar", "Jamnagar", "Amreli", "Bhavnagar", "Porbandar", "Junaghad"],
    "Jamnagar": ["Rajkot"],
    "Amreli": ["Rajkot", "Bhavnagar", "Junaghad"],
    "Bhavnagar": ["Rajkot", "Amreli", "Ahmedabad"],
    "Junaghad": ["Rajkot", "Amreli", "Porbandar"],
    "Porbandar": ["Rajkot", "Junaghad"]
}
def is_valid(node,color,assignment):
    for neighbors in graph[node]:
        if neighbors in assignment and assignment[neighbors]==color:
            return False
    return True
colors=["Red","Green","Blue"]
def backtracking(assignment):
    if(len(assignment)==len(graph)):
        return assignment
    for node in graph:
        if node not in assignment:
            break
    for color in colors:
        if(is_valid(node,color,assignment)):
            assignment[node]=color
            result=backtracking(assignment)
            if result:
                return result
            del assignment[node]
    return None
solution=backtracking({})
print(solution)