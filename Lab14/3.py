def negate(literal):
    return literal[1:] if literal.startswith("~") else "~" + literal
def resolve(ci, cj):
    resolvents = []
    for li in ci:
        for lj in cj:
            if li == negate(lj):
                new_clause = (ci - {li}) | (cj - {lj})
                resolvents.append(frozenset(new_clause))
    return resolvents
def resolution(kb, goal):
    clauses = set(kb)
    # Add negation of goal
    clauses.add(frozenset([negate(goal)]))

    print("Initial Clauses:")
    for c in clauses:
        print(set(c))

    new = set()

    while True:
        pairs = [(ci, cj) for ci in clauses for cj in clauses if ci != cj]

        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)

            for r in resolvents:
                print(f"Resolving {set(ci)} and {set(cj)} -> {set(r)}")

                if len(r) == 0:
                    print("\nEmpty clause derived → PROVED")
                    return True

                new.add(r)

        if new.issubset(clauses):
            print("\nNo new clauses → NOT PROVED")
            return False

        clauses |= new
print("CASE (a)")
# Convert to CNF:
# P ∨ Q
# P → R  = ¬P ∨ R
# Q → S  = ¬Q ∨ S
# R → S  = ¬R ∨ S
kb_a = [
    frozenset(["P", "Q"]),
    frozenset(["~P", "R"]),
    frozenset(["~Q", "S"]),
    frozenset(["~R", "S"])
]
goal_a = "S"
resolution(kb_a, goal_a)
print("\n CASE (b)")
# CNF:
# P → Q = ¬P ∨ Q
# Q → R = ¬Q ∨ R
# S → ¬R = ¬S ∨ ¬R
# P
kb_b = [
    frozenset(["~P", "Q"]),
    frozenset(["~Q", "R"]),
    frozenset(["~S", "~R"]),
    frozenset(["P"])
]
goal_b = "S"
resolution(kb_b, goal_b)