def negate(literal):
    if literal.startswith('~'):
        return literal[1:]
    else:
        return '~' + literal

def resolve(clause1, clause2):
    c1 = list(clause1)
    c2 = list(clause2)
    for lit in c1:
        if negate(lit) in c2:
            new_clause = set(clause1) | set(clause2)
            new_clause.discard(lit)
            new_clause.discard(negate(lit))
            return new_clause
    return None


def resolution_refutation(clauses, goal):
    # negate the goal and add to KB - proof by contradiction
    negated_goal = negate(goal)
    print(f"Negating goal '{goal}' => adding '{negated_goal}' to KB")

    all_clauses = [set(c) for c in clauses]
    all_clauses.append({negated_goal})

    print("\nInitial clauses:")
    for i, c in enumerate(all_clauses):
        print(f"  C{i+1}: {sorted(c)}")
    print()

    step = len(all_clauses) + 1

    while True:
        found_new = False

        for i in range(len(all_clauses)):
            for j in range(i + 1, len(all_clauses)):
                resolvent = resolve(all_clauses[i], all_clauses[j])

                if resolvent is None:
                    continue

                if resolvent in all_clauses:
                    continue

                c1_label = sorted(all_clauses[i])
                c2_label = sorted(all_clauses[j])
                print(f"  Resolve C{i+1}{c1_label} and C{j+1}{c2_label} => {sorted(resolvent) if resolvent else 'Empty {}'}")

                if len(resolvent) == 0:
                    print("\n  Empty clause derived! CONTRADICTION found.")
                    print(f"  Goal '{goal}' is PROVED by refutation.")
                    return True

                all_clauses.append(resolvent)
                print(f"  Added as C{step}: {sorted(resolvent)}")
                step += 1
                found_new = True

        if not found_new:
            print("\nNo new clauses can be derived.")
            print(f"Goal '{goal}' could NOT be proved.")
            return False


# =============================================
# Problem a
# =============================================
print("=" * 45)
print("Problem a")
print("=" * 45)
print("KB:")
print("  P v Q")
print("  P -> R   =>  ~P v R")
print("  Q -> S   =>  ~Q v S")
print("  R -> S   =>  ~R v S")
print("Goal: S")
print()

# CNF clauses
clauses_a = [
    ['P', 'Q'],       # P v Q
    ['~P', 'R'],      # P -> R
    ['~Q', 'S'],      # Q -> S
    ['~R', 'S'],      # R -> S
]

resolution_refutation(clauses_a, 'S')


# =============================================
# Problem b
# =============================================
print()
print("=" * 45)
print("Problem b")
print("=" * 45)
print("KB:")
print("  P -> Q   =>  ~P v Q")
print("  Q -> R   =>  ~Q v R")
print("  S -> ~R  =>  ~S v ~R")
print("  P")
print()
print("Note: From P we derive Q, then R.")
print("      S -> ~R but R is true, so S must be FALSE.")
print("      Therefore the correct conclusion is ~S (NOT S).")
print("Goal: ~S")
print()

clauses_b = [
    ['~P', 'Q'],      # P -> Q
    ['~Q', 'R'],      # Q -> R
    ['~S', '~R'],     # S -> ~R
    ['P'],            # P (fact)
]

# goal is ~S (we prove NOT S, not S)
resolution_refutation(clauses_b, '~S')