class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

    def is_empty(self):
        return len(self.items) == 0

    def __repr__(self):
        return str(self.items)


def PL_FC_ENTAILS(KB, query):
   

    # count[c] = number of premises in clause c (initially)
    count = {}
    for i, (premises, conclusion) in enumerate(KB):
        count[i] = len(premises)

    # inferred[s] = False for all symbols initially
    inferred = {}

    # queue = all symbols known to be true (facts = clauses with empty premises)
    queue = Queue()
    for i, (premises, conclusion) in enumerate(KB):
        if len(premises) == 0:
            queue.enqueue(conclusion)

    print(f"Initial queue (known facts): {queue}")
    print()

    # while queue is not empty
    while not queue.is_empty():
        p = queue.dequeue()                        # p <- POP(queue)
        print(f"Processing: {p}")

        if p == query:                             # if p = q then return true
            print(f"\nQuery '{query}' is PROVED")
            return True

        if not inferred.get(p, False):             # if inferred[p] = false
            inferred[p] = True                     # inferred[p] <- true

            # for each clause c in KB where p is in c.PREMISE
            for i, (premises, conclusion) in enumerate(KB):
                if p in premises:
                    count[i] -= 1                  # decrement count[c]
                    print(f"  Rule {premises} => {conclusion} | remaining premises: {count[i]}")

                    if count[i] == 0:              # if count[c] = 0
                        print(f"    => Adding '{conclusion}' to queue")
                        queue.enqueue(conclusion)  # add c.CONCLUSION to queue

    print(f"\nQuery '{query}' could NOT be proved")
    return False                                   # return false


# ─────────────────────────────────────────
print("=" * 45)
print("Problem a")
print("=" * 45)

KB_a = [
    (['P'],    'Q'),
    (['L','M'],'P'),
    (['A','B'],'L'),
    ([],       'A'),   # known fact A
    ([],       'B'),   # known fact B
    ([],       'M'),   # known fact M
]

PL_FC_ENTAILS(KB_a, 'Q')


print()
print("=" * 45)
print("Problem b")
print("=" * 45)

KB_b = [
    (['A'],    'B'),
    (['B'],    'C'),
    (['C'],    'D'),
    (['D','E'],'F'),
    ([],       'A'),   # known fact A
    ([],       'E'),   # known fact E
]

PL_FC_ENTAILS(KB_b, 'F')