N = 8  # বোর্ডের সাইজ

def is_safe(board, row, col):
    # একই কলামে কোনো কুইন আছে কিনা
    for i in range(row):
        if board[i][col] == 1:
            return False

    # বাম-ডায়াগনাল চেক
    for i, j in zip(range(row -1, -1, -1), range(col -1, -1, -1)):
        if board[i][j] == 1:
            return False

    # ডান-ডায়াগনাল চেক
    for i, j in zip(range(row -1, -1, -1), range(col +1, N)):
        if board[i][j] == 1:
            return False

    return True

def print_board(board):
    for row in board:
        print(" ".join("Q" if x else "." for x in row))
    print()

def solve(board, row):
    if row == N:
        print("✅ প্রথম সল্যুশন পাওয়া গেছে:")
        print_board(board)
        return True  # Stop after first solution

    for col in range(N):
        if is_safe(board, row, col):
            board[row][col] = 1
            if solve(board, row + 1):
                return True
            board[row][col] = 0  # Backtrack
    return False

# শুরু করো খালি বোর্ড দিয়ে
board = [[0 for _ in range(N)] for _ in range(N)]
board[0][3] = 1
solve(board, 1)
