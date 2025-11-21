import numpy as np
import random

class SudokuGenerator:
    def __init__(self, difficulty="Easy"):
        self.board = np.zeros((9, 9), dtype=int)
        self.difficulty = difficulty

    # -----------------------------
    # UTILITY FUNCTIONS
    # -----------------------------
    def used_in_row(self, row, num):
        return num in self.board[row]

    def used_in_col(self, col, num):
        return num in self.board[:, col]

    def used_in_box(self, row, col, num):
        box_r = row - row % 3
        box_c = col - col % 3
        return num in self.board[box_r:box_r+3, box_c:box_c+3]

    def check_safe(self, row, col, num):
        return not self.used_in_row(row, num) and \
               not self.used_in_col(col, num) and \
               not self.used_in_box(row, col, num)

    # -----------------------------
    # FILL DIAGONAL BOXES
    # -----------------------------
    def fill_diagonal(self):
        for i in range(0, 9, 3):
            self.fill_box(i, i)

    def fill_box(self, row, col):
        nums = list(range(1, 10))
        random.shuffle(nums)
        idx = 0
        for i in range(3):
            for j in range(3):
                self.board[row + i][col + j] = nums[idx]
                idx += 1

    # -----------------------------
    # BACKTRACKING FILL
    # -----------------------------
    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    return r, c
        return None

    def solve_board(self):
        empty = self.find_empty()
        if not empty:
            return True

        row, col = empty

        nums = list(range(1, 10))
        random.shuffle(nums)

        for num in nums:
            if self.check_safe(row, col, num):
                self.board[row][col] = num

                if self.solve_board():
                    return True

                self.board[row][col] = 0  # backtrack

        return False

    # -----------------------------
    # REMOVE CELLS FOR DIFFICULTY
    # -----------------------------
    def remove_cells(self):
        if self.difficulty == "Easy":
            remove = 30
        elif self.difficulty == "Medium":
            remove = 40
        else:
            remove = 50

        count = 0
        while count < remove:
            r = random.randint(0, 8)
            c = random.randint(0, 8)

            if self.board[r][c] != 0:
                self.board[r][c] = 0
                count += 1

    # -----------------------------
    # PUBLIC FUNCTION
    # -----------------------------
    def generate_sudoku(self):
        self.fill_diagonal()
        self.solve_board()
        self.remove_cells()
        return self.board


def generate_sudoku(difficulty="Easy"):
    return SudokuGenerator(difficulty).generate_sudoku()
