## RUN USING cd Code -> python final-minesweeper.py
import random
import re

# board object to represent game
# so we can say "create new board object" or "dig here", or "render this game for this object"
class Board:
    def __init__(self, dim_size, num_bombs):
        # keep track of dimensions
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # create the board
        self.board = self.make_new_board()
        # plant the bombs
        self.assign_values_to_board()

        # initialize a set to keep track of which locations user digs
        # save (row,col) tuples into this set
        self.dug = set()

    def make_new_board(self):
        # make new board based on dimensions (size & bombs)
        # generate new board

        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        # place bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:

            # return random integer within range of 0 and largest value in set
            # gives row & column # of location
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == '*':
                # if there is already a bomb, keep going
                continue

            # place bomb
            board[row][col] = '*'
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        # assign 0-8 for neighboring spaces
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    # if there is a bomb, don't do anyhting
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        # iterate through each neighboring positions and add number of bombs
        # top left: (row-1, col-1)
        # top middle: (row-1, col)
        # top right: (row-1, col+1)
        # left: (row, col-1)
        # right: (row, col+1)
        # bottom left: (row+1, col-1)
        # bottom middle: (row+1, col)
        # bottom right: (row+1, col+1)

        # stay in bounds

        # check spaces 1 row & column left, right, above, and below each space
        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):

                # if checking original position, contiune
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def dig(self, row, col):

        # dig at selected location, return true if not a bomb, false if it is a bomb
        # keep track of where user is digging
        self.dug.add((row, col)) # keep track that we dug here

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        # if self.board[row][col] == 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):

                # dont dig where the user has already dug
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)

        # if our initial dig didn't hit a bomb, we *shouldn't* hit a bomb here
        return True

    def __str__(self):

        # function to print out board as a string for player to see
        # create arrayt of field for user
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        # put into string
        string_rep = ''
        # max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep

# play the game
def play(dim_size=10, num_bombs=10):
    # Step 1: create the board and plant the bombs
    board = Board(dim_size, num_bombs)

    # Step 2: show the user the board and ask for where they want to dig
    # Step 3a: if location is a bomb, show game over message
    # Step 3b: if location is not a bomb, dig recursively until each square is at least
    #          next to a bomb
    # Step 4: repeat steps 2 and 3a/b until there are no more places to dig -> VICTORY!
    alive = True

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)

        # detect commas & white spaces and split string at the comma
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))  # '0, 3'
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location. Try again.")
            continue

        # if user inputs a valid location, dig
        alive = board.dig(row, col)
        if not alive:

            # dug a bomb -> dead/game over
            break

    if alive:
        print("CONGRATS!!!! YOU WIN!")
    else:
        print("L + GAME OVER :P")

        # reveal whole board after game over
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

# only run if user types python final-minesweeper.py
if __name__ == '__main__':
    play()