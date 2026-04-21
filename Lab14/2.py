class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def is_empty(self):
        return len(self.items) == 0

    def __repr__(self):
        return str(self.items)


def backward_chaining(rules, facts, goal, visited=None):
    

    if visited is None:                        # first call — initialise visited set
        visited = set()

    if goal in facts:                          # if goal is already a known fact
        print(f"  '{goal}' is a known fact")
        return True

    if goal in visited:                        # already trying to prove this — loop detected
        return False
    visited.add(goal)                          # mark goal as being attempted

    print(f"  Trying to prove: '{goal}'")

    # use a stack to try each matching rule
    rule_stack = Stack()

    for premises, conclusion in rules:         # find all rules whose conclusion = goal
        if conclusion == goal:
            rule_stack.push((premises, conclusion))

    while not rule_stack.is_empty():
        premises, conclusion = rule_stack.pop()           # take one rule from stack
        print(f"    Found rule: {premises} => {conclusion}")

        all_proved = True
        for p in premises:                                # try to prove every premise
            if not backward_chaining(rules, facts, p, visited):
                all_proved = False
                break

        if all_proved:
            print(f"  '{goal}' is PROVED via {premises}")
            return True

    print(f"  '{goal}' could NOT be proved")             # no rule could prove goal
    return False


# ─────────────────────────────────────────
print("=" * 45)
print("Problem a")
print("=" * 45)

rules_a = [
    (['P'], 'Q'),
    (['R'], 'Q'),
    (['A'], 'P'),
    (['B'], 'R'),
]

facts_a = ['A', 'B']

print("Initial facts:", facts_a)
print("Goal: Q")
print()
result = backward_chaining(rules_a, facts_a, 'Q')
print()
print("Conclusion 'Q' is PROVED" if result else "Conclusion 'Q' could NOT be proved")


print()
print("=" * 45)
print("Problem b")
print("=" * 45)

rules_b = [
    (['A'],      'B'),
    (['B', 'C'], 'D'),
    (['E'],      'C'),
]

facts_b = ['A', 'E']

print("Initial facts:", facts_b)
print("Goal: D")
print()
result = backward_chaining(rules_b, facts_b, 'D')
print()
print("Conclusion 'D' is PROVED" if result else "Conclusion 'D' could NOT be proved")