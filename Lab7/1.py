
import random

N = 8


# VALUE function (higher value = better)
def VALUE(board):
    conflicts = 0
    for i in range(N):
        for j in range(i + 1, N):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return -conflicts


def random_board():
    return [random.randint(0, N - 1) for _ in range(N)]


def get_successors(board):
    successors = []

    for col in range(N):
        for row in range(N):
            if board[col] != row:
                new_board = board.copy()
                new_board[col] = row
                successors.append(new_board)

    return successors


# function HILL-CLIMBING(problem)
def HILL_CLIMBING(initial):

    current = initial
    steps = 0

    while True:

        successors = get_successors(current)

        neighbor = max(successors, key=VALUE)

        if VALUE(neighbor) <= VALUE(current):
            return current, steps

        current = neighbor
        steps += 1



for i in range(50):

    board = random_board()

    initial_h = -VALUE(board)

    final_board, steps = HILL_CLIMBING(board)

    final_h = -VALUE(final_board)

    status = "Solved" if final_h == 0 else "Fail"

    print(i + 1, "   ","initial h :" ,initial_h, "      ","final h :", final_h, "     ","Steps :", steps, "   ", "result :" ,status)