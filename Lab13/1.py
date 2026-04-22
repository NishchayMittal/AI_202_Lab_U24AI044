class symbol:
    def __init__(self, name):
        self.name = name
        self.value = None   
def NOT(p): return not p
def AND(p, q): return p and q
def OR(p, q): return p or q
def IMP(p, q): return (not p) or q
def IFF(p, q): return p == q


def b(x):
    return 1 if x else 0

def truth_table_2(name, func):
    P = symbol('P')
    Q = symbol('Q')

    vals = [False, True]
    print(name)
    print("P Q Result")

    for p_val in vals:
        for q_val in vals:
            P.value = p_val
            Q.value = q_val

            result = func(P, Q)

            print(b(P.value), b(Q.value), "True" if result else "False")
    print()

def truth_table_3(name, func):
    P = symbol('P')
    Q = symbol('Q')
    R = symbol('R')

    vals = [False, True]
    print(name)
    print("P Q R Result")

    for p_val in vals:
        for q_val in vals:
            for r_val in vals:
                P.value = p_val
                Q.value = q_val
                R.value = r_val

                result = func(P, Q, R)

                print(b(P.value), b(Q.value), b(R.value),
                      "True" if result else "False")
    print()



truth_table_2("~P -> Q", lambda P, Q: IMP(NOT(P.value), Q.value))
truth_table_2("~P ∧ Q", lambda P, Q: AND(NOT(P.value), Q.value))
truth_table_2("~P V Q", lambda P, Q: OR(NOT(P.value), Q.value))
truth_table_2("P -> Q", lambda P, Q: IMP(P.value, Q.value))
truth_table_2("~P <-> Q", lambda P, Q: IFF(NOT(P.value), Q.value))
truth_table_2("(P V Q) ∧ (~P -> Q)",lambda P, Q: AND(OR(P.value, Q.value),IMP(NOT(P.value), Q.value)))
truth_table_3("(P V Q) -> R",lambda P, Q, R: IMP(OR(P.value, Q.value), R.value))
truth_table_3("((P V Q) -> R) <-> ((~P ∧ Q) -> R)",lambda P, Q, R: IFF(IMP(OR(P.value, Q.value), R.value),IMP(AND(NOT(P.value), Q.value), R.value)))
truth_table_3("((P -> Q) ∧ (Q -> R)) -> (P -> R)",lambda P, Q, R: IMP(AND(IMP(P.value, Q.value), IMP(Q.value, R.value)),IMP(P.value, R.value)))
truth_table_3("((P -> (Q V R)) -> (~P ∧ ~Q ∧ ~R))",lambda P, Q, R: IMP(IMP(P.value, OR(Q.value, R.value)),AND(NOT(P.value), AND(NOT(Q.value), NOT(R.value)))))