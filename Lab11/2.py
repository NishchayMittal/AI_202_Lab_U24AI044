

# ── Variables and domains ─────────────────────────────────────────────────────
VARIABLES = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']

# Full domains: 0-9 for all; leading letters S, M cannot be 0
INITIAL_DOMAINS = {
    'S': set(range(1, 10)),   # S ≠ 0 (leading digit of SEND)
    'E': set(range(0, 10)),
    'N': set(range(0, 10)),
    'D': set(range(0, 10)),
    'M': set(range(1, 10)),   # M ≠ 0 (leading digit of MORE and MONEY)
    'O': set(range(0, 10)),
    'R': set(range(0, 10)),
    'Y': set(range(0, 10)),
}


# ── Core arithmetic constraint ────────────────────────────────────────────────

def check_constraint(assignment):
    vars_needed = ['S', 'E', 'N', 'D', 'M', 'O', 'R', 'Y']

    # If not all assigned yet, do a partial column-wise check
    if not all(v in assignment for v in vars_needed):
        return partial_check(assignment)

    # Full check: all letters assigned
    S, E, N, D = assignment['S'], assignment['E'], assignment['N'], assignment['D']
    M, O, R, Y = assignment['M'], assignment['O'], assignment['R'], assignment['Y']

    SEND  = 1000*S + 100*E + 10*N + D
    MORE  = 1000*M + 100*O + 10*R + E
    MONEY = 10000*M + 1000*O + 100*N + 10*E + Y

    return SEND + MORE == MONEY


def partial_check(assignment):
    a = assignment

    # Each carry can only be 0 or 1 (sum of two single digits + carry ≤ 19)
    for c1 in range(2):
        # Column 0: D + E = Y + 10*c1
        if all(v in a for v in ['D', 'E', 'Y']):
            if (a['D'] + a['E']) % 10 != a['Y']:
                continue
            if (a['D'] + a['E']) // 10 != c1:
                continue

        for c2 in range(2):
            # Column 1: N + R + c1 = E + 10*c2
            if all(v in a for v in ['N', 'R', 'E']):
                if (a['N'] + a['R'] + c1) % 10 != a['E']:
                    continue
                if (a['N'] + a['R'] + c1) // 10 != c2:
                    continue

            for c3 in range(2):
                # Column 2: E + O + c2 = N + 10*c3
                if all(v in a for v in ['E', 'O', 'N']):
                    if (a['E'] + a['O'] + c2) % 10 != a['N']:
                        continue
                    if (a['E'] + a['O'] + c2) // 10 != c3:
                        continue

                for c4 in range(2):
                    # Column 3: S + M + c3 = O + 10*c4
                    if all(v in a for v in ['S', 'M', 'O']):
                        if (a['S'] + a['M'] + c3) % 10 != a['O']:
                            continue
                        if (a['S'] + a['M'] + c3) // 10 != c4:
                            continue

                    # Column 4: c4 = M
                    if 'M' in a:
                        if c4 != a['M']:
                            continue

                    return None  # At least one carry combo is consistent

    return False   # All carry combos failed → contradiction


# ── All-different constraint ──────────────────────────────────────────────────

def all_different(assignment):
    """No two assigned letters may share the same digit."""
    vals = list(assignment.values())
    return len(vals) == len(set(vals))


# ── Forward Checking ──────────────────────────────────────────────────────────

def forward_check(var, value, domains, assignment):
    """
    After assigning var=value, remove `value` from all unassigned
    variables' domains (all-different constraint).
    Returns updated domains, or None if any domain becomes empty.
    """
    new_domains = {v: set(d) for v, d in domains.items()}
    for other in VARIABLES:
        if other not in assignment and other != var:
            new_domains[other].discard(value)
            if not new_domains[other]:
                return None   # Domain wipe-out → prune
    return new_domains


# ── MRV variable selection ────────────────────────────────────────────────────

def select_variable(assignment, domains):
    """
    MRV: pick the unassigned variable with the smallest remaining domain.
    Tie-break by the predefined variable order (S,E,N,D,M,O,R,Y) —
    earlier variables tend to appear in more columns.
    """
    unassigned = [v for v in VARIABLES if v not in assignment]
    return min(unassigned, key=lambda v: len(domains[v]))


# ── Backtracking search ───────────────────────────────────────────────────────

def backtrack(assignment, domains):
    """
    Recursive backtracking with:
      - MRV variable ordering
      - Forward checking (all-different propagation)
      - Arithmetic constraint checking at each step
    """
    # Goal test
    if len(assignment) == len(VARIABLES):
        if check_constraint(assignment) is True:
            return assignment
        return None

    var = select_variable(assignment, domains)

    for value in sorted(domains[var]):
        # Tentative assignment
        assignment[var] = value

        # 1. All-different check
        if not all_different(assignment):
            del assignment[var]
            continue

        # 2. Arithmetic partial check (column-wise with carries)
        constraint_result = check_constraint(assignment)
        if constraint_result is False:
            del assignment[var]
            continue

        # 3. Forward checking: propagate all-different to remaining domains
        new_domains = forward_check(var, value, domains, assignment)
        if new_domains is None:
            del assignment[var]
            continue

        # Recurse
        result = backtrack(assignment, new_domains)
        if result is not None:
            return result

        del assignment[var]   # Backtrack

    return None   # No value worked → signal failure


# ── Display helpers ───────────────────────────────────────────────────────────

def print_solution(solution):
    S, E, N, D = solution['S'], solution['E'], solution['N'], solution['D']
    M, O, R, Y = solution['M'], solution['O'], solution['R'], solution['Y']

    SEND  = 1000*S + 100*E + 10*N + D
    MORE  = 1000*M + 100*O + 10*R + E
    MONEY = 10000*M + 1000*O + 100*N + 10*E + Y

    print("\n" + "="*45)
    print("   CRYPTARITHMETIC SOLUTION: SEND + MORE = MONEY")
    print("="*45)
    print("\n  Letter → Digit mapping:")
    print("  " + "-"*26)
    for letter in VARIABLES:
        print(f"    {letter}  →  {solution[letter]}")
    print("  " + "-"*26)

    print(f"\n    S E N D      =  {S} {E} {N} {D}  =  {SEND}")
    print(f"  + M O R E      =  {M} {O} {R} {E}  =  {MORE}")
    print(f"  " + "-"*16)
    print(f"  M O N E Y      = {M} {O} {N} {E} {Y}  =  {MONEY}")
    print(f"\n  Verification: {SEND} + {MORE} = {MONEY}  →  {'CORRECT ' if SEND+MORE==MONEY else 'WRONG '}")
    print("="*45)


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Cryptarithmetic CSP Solver")
    print("  SEND + MORE = MONEY")
    print("  Constraints: all letters unique, S≠0, M≠0\n")
    print("Running backtracking CSP with forward checking …")

    domains = {v: set(d) for v, d in INITIAL_DOMAINS.items()}
    solution = backtrack({}, domains)

    if solution:
        print_solution(solution)
    else:
        print("No solution found.")