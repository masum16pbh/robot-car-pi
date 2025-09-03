N = 8

def print_solution(board):
    for row in board:
        print(" ".join("Q" if col else "." for col in row))
    print()

def is_safe(board, row, col):
    # Check left side of this row
    for i in range(col):
        if board[row][i]:
            return False

    # Check upper diagonal
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j]:
            return False

    # Check lower diagonal
    for i, j in zip(range(row, N), range(col, -1, -1)):
        if board[i][j]:
            return False

    return True

def solve(board, col):
    if col >= N:
        print_solution(board)
        return True

    res = False
    for i in range(N):
        if is_safe(board, i, col):
            board[i][col] = 1
            res = solve(board, col + 1) or res
            board[i][col] = 0  # backtrack

    return res

# main
board = [[0]*N for _ in range(N)]
solve(board, 0)
