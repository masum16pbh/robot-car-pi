N = 8
def print_board(board):
    for row in board:
        print(" ".join('Q' if x else '.' for x in row))

    print()

def is_safe(board, row,col):
    for i in range(row):
        if board[i][col] == 1:
            return False

    for i,j in zip(range(row-1,-1,-1),range(col-1,-1,-1)):
        if board[i][j] == 1:
            return False

    for i,j in zip(range(row-1,-1,-1), range(col+1,N)):
        if board[i][j] == 1:
            return False
    return True

def solve(board, row):
    if row == N:
        print_board(board)
        return True
    for col in range(N):
        if is_safe(board,row,col):
            board[row][col] = 1
            if solve(board,row+1):
                return True
            board[row][col] = 0 # It can backtrack
    return False

board = [[0]*N for _ in range(N)]
first_quine = int(input("You can cose a position of the first queen in first row. Put the col number "))
if 0<=first_quine <N:
    board[0][first_quine] = 1
solve(board,row = 1)