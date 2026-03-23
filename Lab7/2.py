# import random
# import math

# #  Heuristic Function 
# def heuristic(state):
#     conflicts = 0
#     for i in range(8):
#         for j in range(i+1, 8):
#             if state[i] == state[j] or abs(state[i]-state[j]) == abs(i-j):
#                 conflicts += 1
#     return conflicts


# def random_board():
#     return [random.randint(0,7) for _ in range(8)]


# def random_neighbor(state):
#     col = random.randint(0,7)
#     row = random.randint(0,7)
#     new_state = state.copy()
#     new_state[col] = row
#     return new_state


# # First Choice Hill Climbing 
# def first_choice(initial):
#     current = initial
#     steps = 0

#     while True:
#         current_h = heuristic(current)
#         improved = False

#         for _ in range(100):
#             neighbor = random_neighbor(current)
#             if heuristic(neighbor) < current_h:
#                 current = neighbor
#                 steps += 1
#                 improved = True
#                 break

#         if not improved:
#             return current_h, steps, current_h == 0


# # Steepest Ascent (used in Random Restart) 
# def steepest_ascent(initial):
#     current = initial
#     steps = 0

#     while True:
#         current_h = heuristic(current)
#         best = current
#         best_h = current_h

#         for col in range(8):
#             for row in range(8):
#                 if row != current[col]:
#                     new_state = current.copy()
#                     new_state[col] = row
#                     h = heuristic(new_state)
#                     if h < best_h:
#                         best = new_state
#                         best_h = h

#         if best_h >= current_h:
#             return current_h, steps, current_h == 0

#         current = best
#         steps += 1


# # Random Restart 
# def random_restart(max_restarts=50):
#     total_steps = 0

#     for restart in range(max_restarts):
#         board = random_board()
#         final_h, steps, solved = steepest_ascent(board)
#         total_steps += steps
#         if solved:
#             return final_h, total_steps, True, restart+1

#     return final_h, total_steps, False, max_restarts


# #Simulated Annealing 
# def simulated_annealing(initial, max_steps=10000):
#     current = initial
#     T = 100
#     cooling = 0.99

#     for step in range(max_steps):
#         current_h = heuristic(current)
#         if current_h == 0:
#             return current_h, step, True

#         neighbor = random_neighbor(current)
#         delta = heuristic(neighbor) - current_h

#         if delta < 0:
#             current = neighbor
#         else:
#             probability = math.exp(-delta / T)
#             if random.random() < probability:
#                 current = neighbor

#         T *= cooling
#         if T < 0.001:
#             break

#     return heuristic(current), max_steps, heuristic(current) == 0


# def main():
#     runs = 50

#     # ================= FIRST CHOICE =================
#     print("\nFIRST CHOICE HILL CLIMBING\n")
#     fc_success = 0
#     fc_total_steps = 0

#     for i in range(runs):
#         board = random_board()
#         initial_h = heuristic(board)
#         final_h, steps, solved = first_choice(board)

#         print(f"Run {i+1}: Initial={initial_h}, Final={final_h}, Steps={steps}, Solved={solved}")

#         fc_total_steps += steps
#         if solved:
#             fc_success += 1

#     # ================= RANDOM RESTART =================
#     print("\nRANDOM RESTART HILL CLIMBING \n")
#     rr_success = 0
#     rr_total_steps = 0

#     for i in range(runs):
#         board = random_board()
#         initial_h = heuristic(board)
#         final_h, steps, solved, restarts = random_restart()

#         print(f"Run {i+1}: Initial={initial_h}, Final={final_h}, Steps={steps}, Restarts={restarts}, Solved={solved}")

#         rr_total_steps += steps
#         if solved:
#             rr_success += 1

#     # ================= SIMULATED ANNEALING =================
#     print("\n SIMULATED ANNEALING\n")
#     sa_success = 0
#     sa_total_steps = 0

#     for i in range(runs):
#         board = random_board()
#         initial_h = heuristic(board)
#         final_h, steps, solved = simulated_annealing(board)

#         print(f"Run {i+1}: Initial={initial_h}, Final={final_h}, Steps={steps}, Solved={solved}")

#         sa_total_steps += steps
#         if solved:
#             sa_success += 1

#     # ================= FINAL COMPARISON TABLE =================
#     print("\nFINAL COMPARISON TABLE \n")

#     print("{:<25} {:<15} {:<15} {:<15}".format(
#         "Algorithm", "Success", "Success Rate", "Avg Steps"))

#     print("-" * 70)

#     print("{:<25} {:<15} {:<15} {:<15}".format(
#         "First Choice",
#         f"{fc_success}/{runs}",
#         f"{(fc_success/runs)*100:.2f}%",
#         f"{fc_total_steps/runs:.2f}"
#     ))

#     print("{:<25} {:<15} {:<15} {:<15}".format(
#         "Random Restart",
#         f"{rr_success}/{runs}",
#         f"{(rr_success/runs)*100:.2f}%",
#         f"{rr_total_steps/runs:.2f}"
#     ))

#     print("{:<25} {:<15} {:<15} {:<15}".format(
#         "Simulated Annealing",
#         f"{sa_success}/{runs}",
#         f"{(sa_success/runs)*100:.2f}%",
#         f"{sa_total_steps/runs:.2f}"
#     ))


# if __name__ == "__main__":
#     main()

import random
import math

N = 8


# heuristic (number of conflicts)
def heuristic(board):
    conflicts = 0
    for i in range(N):
        for j in range(i+1, N):
            if board[i] == board[j] or abs(board[i]-board[j]) == abs(i-j):
                conflicts += 1
    return conflicts


# generate random board
def random_board():
    return [random.randint(0, N-1) for _ in range(N)]


# generate neighbors
def get_neighbors(board):
    neighbors = []
    for col in range(N):
        for row in range(N):
            if board[col] != row:
                new_board = board.copy()
                new_board[col] = row
                neighbors.append(new_board)
    return neighbors


# -----------------------------
# FIRST CHOICE HILL CLIMBING
# -----------------------------
def first_choice_hill_climb(board):

    current = board
    steps = 0

    while True:

        current_h = heuristic(current)

        neighbors = get_neighbors(current)
        random.shuffle(neighbors)

        found = False

        for n in neighbors:
            if heuristic(n) < current_h:
                current = n
                steps += 1
                found = True
                break

        if not found:
            return current, steps


# -----------------------------
# RANDOM RESTART HILL CLIMBING
# -----------------------------
def hill_climb(board):

    current = board
    steps = 0

    while True:

        neighbors = get_neighbors(current)
        best = min(neighbors, key=heuristic)

        if heuristic(best) >= heuristic(current):
            return current, steps

        current = best
        steps += 1


def random_restart():

    total_steps = 0

    while True:

        board = random_board()
        result, steps = hill_climb(board)

        total_steps += steps

        if heuristic(result) == 0:
            return result, total_steps


# -----------------------------
# SIMULATED ANNEALING
# -----------------------------
def simulated_annealing(board):

    current = board
    steps = 0
    T = 100

    while T > 0.1:

        if heuristic(current) == 0:
            return current, steps

        neighbors = get_neighbors(current)
        next_state = random.choice(neighbors)

        delta = heuristic(current) - heuristic(next_state)

        if delta > 0:
            current = next_state
        else:
            prob = math.exp(delta / T)
            if random.random() < prob:
                current = next_state

        T *= 0.95
        steps += 1

    return current, steps


# -----------------------------
# RUN 50 EXPERIMENTS
# -----------------------------
def experiment(algorithm, name):

    print("\n", name)

    success = 0

    for i in range(50):

        board = random_board()

        initial_h = heuristic(board)

        if name == "Random Restart":
            final_board, steps = random_restart()
        else:
            final_board, steps = algorithm(board)

        final_h = heuristic(final_board)

        status = "Solved" if final_h == 0 else "Fail"

        if status == "Solved":
            success += 1

        print(i + 1, "   ","initial h :" ,initial_h, "      ","final h :", final_h, "     ","Steps :", steps, "   ", "result :" ,status)

    print("Success rate:", success, "/ 50")


# run experiments
experiment(first_choice_hill_climb, "First Choice")
experiment(random_restart, "Random Restart")
experiment(simulated_annealing, "Simulated Annealing")