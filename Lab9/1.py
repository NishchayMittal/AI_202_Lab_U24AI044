

import math
import time

PLAYER_X = 'X'  # MAX
PLAYER_O = 'O'  # MIN
EMPTY = ' '

nodes_expanded = 0




def TO_MOVE(state):
    x = sum(row.count('X') for row in state)
    o = sum(row.count('O') for row in state)
    return PLAYER_X if x == o else PLAYER_O


def ACTIONS(state):
    acts = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == EMPTY:
                acts.append((i, j))
    return acts


def RESULT(state, action):
    i, j = action
    new_state = [row[:] for row in state]
    new_state[i][j] = TO_MOVE(state)
    return new_state


def IS_TERMINAL(state):
    return CHECK_WINNER(state) is not None or all(cell != EMPTY for row in state for cell in row)




def UTILITY(state, player, depth=0):
    winner = CHECK_WINNER(state)
    if winner == PLAYER_X:
        return 10 - depth   # win sooner = higher score
    elif winner == PLAYER_O:
        return depth - 10   # lose later = higher score
    else:
        return 0


def CHECK_WINNER(state):
    lines = []

    # rows
    lines.extend(state)

    # columns
    lines.extend([[state[i][j] for i in range(3)] for j in range(3)])

    # diagonals
    lines.append([state[i][i] for i in range(3)])
    lines.append([state[i][2 - i] for i in range(3)])

    for line in lines:
        if all(cell == PLAYER_X for cell in line):
            return PLAYER_X
        if all(cell == PLAYER_O for cell in line):
            return PLAYER_O

    return None




def MINIMAX_SEARCH(game, state):
    player = TO_MOVE(state)
    value, move = MAX_VALUE(game, state)
    return move



def MAX_VALUE(game, state, depth=0):
    global nodes_expanded
    nodes_expanded += 1
    if IS_TERMINAL(state):
        return UTILITY(state, PLAYER_X, depth), None
    v = -math.inf
    best_move = None
    for a in ACTIONS(state):
        v2, _ = MIN_VALUE(game, RESULT(state, a), depth + 1)
        if v2 > v:
            v = v2
            best_move = a
    return v, best_move



def MIN_VALUE(game, state, depth=0):
    global nodes_expanded
    nodes_expanded += 1
    if IS_TERMINAL(state):
        return UTILITY(state, PLAYER_X, depth), None
    v = math.inf
    best_move = None
    for a in ACTIONS(state):
        v2, _ = MAX_VALUE(game, RESULT(state, a), depth + 1)
        if v2 < v:
            v = v2
            best_move = a
    return v, best_move

def PRINT_BOARD(state):
    for row in state:
        print(row)
    print()


def PRINT_TREE(state, depth=0, is_max=True):
    indent = "  " * depth
    if IS_TERMINAL(state):
        print(f"{indent}Leaf: Utility = {UTILITY(state, PLAYER_X)}")
        return

    print(f"{indent}{'MAX' if is_max else 'MIN'} Node")

    for a in ACTIONS(state):
        print(f"{indent} Move: {a}")
        PRINT_TREE(RESULT(state, a), depth + 1, not is_max)


if __name__ == "__main__":

    X = "X"
    O = "O"
    initial_state = [
        [X, O, EMPTY],
        [EMPTY, X, O],
        [EMPTY, EMPTY, EMPTY]
    ]

    print("Initial Board:")
    PRINT_BOARD(initial_state)

    start = time.time()
    best_move = MINIMAX_SEARCH(None, initial_state)
    end = time.time()

    print("Best Move:", best_move)
    print("Nodes Expanded:", nodes_expanded)
    print("Time Taken:", end - start)

    print("\nSearch Tree:")
    PRINT_TREE(initial_state)