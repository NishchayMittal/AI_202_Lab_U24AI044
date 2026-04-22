
def bool_combinations(n):
    """Generate all True/False combinations for n variables (like a truth table)."""
    total = 2 ** n
    result = []
    for i in range(total):
        combo = []
        for j in range(n - 1, -1, -1):
            combo.append(bool((i >> j) & 1))
        result.append(combo)
    return result


# ── Logical connective classes ────────────────────────────────────────────────

class Symbol:
    def __init__(self, name):
        self.name = name

    def evaluate(self, assignment):
        return assignment[self.name]

    def symbols(self):
        return [self.name]

    def __repr__(self):
        return self.name


class Not:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, assignment):
        return not self.expr.evaluate(assignment)

    def symbols(self):
        return self.expr.symbols()

    def __repr__(self):
        return f"~{self.expr}"


class And:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, assignment):
        return self.left.evaluate(assignment) and self.right.evaluate(assignment)

    def symbols(self):
        return self.left.symbols() + self.right.symbols()

    def __repr__(self):
        return f"({self.left} ^ {self.right})"


class Or:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, assignment):
        return self.left.evaluate(assignment) or self.right.evaluate(assignment)

    def symbols(self):
        return self.left.symbols() + self.right.symbols()

    def __repr__(self):
        return f"({self.left} v {self.right})"


class Conditional:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, assignment):
        return (not self.left.evaluate(assignment)) or self.right.evaluate(assignment)

    def symbols(self):
        return self.left.symbols() + self.right.symbols()

    def __repr__(self):
        return f"({self.left} -> {self.right})"


class Biconditional:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, assignment):
        return self.left.evaluate(assignment) == self.right.evaluate(assignment)

    def symbols(self):
        return self.left.symbols() + self.right.symbols()

    def __repr__(self):
        return f"({self.left} <-> {self.right})"


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_symbols(expr):
    """Return unique symbols in order of appearance."""
    seen = []
    for s in expr.symbols():
        if s not in seen:
            seen.append(s)
    return seen


def print_truth_table(expr, label=None):
    syms = get_symbols(expr)
    if label is None:
        label = str(expr)

    header = ""
    for s in syms:
        header += f"{s}\t"
    header += label
    print(header)
    print("-" * (len(header) + 10))

    for values in bool_combinations(len(syms)):
        assignment = {}
        for i in range(len(syms)):
            assignment[syms[i]] = values[i]

        row = ""
        for v in values:
            row += ("T" if v else "F") + "\t"

        result = expr.evaluate(assignment)
        row += "T" if result else "F"
        print(row)

    print()


# ── Symbols ───────────────────────────────────────────────────────────────────

P = Symbol('P')
Q = Symbol('Q')
R = Symbol('R')

print("=" * 50)
print("TRUTH TABLES FOR ALL PROPOSITIONS")
print("=" * 50)

# 1. ~P -> Q
print("\n1. ~P -> Q")
prop1 = Conditional(Not(P), Q)
print_truth_table(prop1, "~P->Q")

# 2. ~P ^ ~Q
print("2. ~P ^ ~Q")
prop2 = And(Not(P), Not(Q))
print_truth_table(prop2, "~P^~Q")

# 3. ~P v ~Q
print("3. ~P v ~Q")
prop3 = Or(Not(P), Not(Q))
print_truth_table(prop3, "~Pv~Q")

# 4. ~P -> ~Q
print("4. ~P -> ~Q")
prop4 = Conditional(Not(P), Not(Q))
print_truth_table(prop4, "~P->~Q")

# 5. ~P <-> ~Q
print("5. ~P <-> ~Q")
prop5 = Biconditional(Not(P), Not(Q))
print_truth_table(prop5, "~P<->~Q")

# 6. (P v Q) ^ (~P -> Q)
print("6. (P v Q) ^ (~P -> Q)")
prop6 = And(Or(P, Q), Conditional(Not(P), Q))
print_truth_table(prop6, "(PvQ)^(~P->Q)")

# 7. (P v Q) -> ~R
print("7. (P v Q) -> ~R")
prop7 = Conditional(Or(P, Q), Not(R))
print_truth_table(prop7, "(PvQ)->~R")

# 8. ((P v Q) -> ~R) <-> ((~P ^ ~Q) -> ~R)
print("8. ((P v Q) -> ~R) <-> ((~P ^ ~Q) -> ~R)")
prop8 = Biconditional(
    Conditional(Or(P, Q), Not(R)),
    Conditional(And(Not(P), Not(Q)), Not(R))
)
print_truth_table(prop8, "((PvQ)->~R)<->((~P^~Q)->~R)")

# 9. ((P->Q) ^ (Q->R)) -> (Q->R)
print("9. ((P->Q) ^ (Q->R)) -> (Q->R)")
prop9 = Conditional(
    And(Conditional(P, Q), Conditional(Q, R)),
    Conditional(Q, R)
)
print_truth_table(prop9, "((P->Q)^(Q->R))->(Q->R)")

# 10. (P -> (Q v R)) -> (~P ^ ~Q ^ ~R)
print("10. (P -> (Q v R)) -> (~P ^ ~Q ^ ~R)")
prop10 = Conditional(
    Conditional(P, Or(Q, R)),
    And(And(Not(P), Not(Q)), Not(R))
)
print_truth_table(prop10, "(P->(QvR))->(~P^~Q^~R)")