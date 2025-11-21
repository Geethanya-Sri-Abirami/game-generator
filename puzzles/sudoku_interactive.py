import numpy as np
import pandas as pd

def create_interactive_grid(board):
    """
    Converts your generated Sudoku board into an editable DataFrame.
    0 → empty cell
    """
    df = pd.DataFrame(board).replace(0, "")
    return df

def validate_sudoku(user_grid, solution_grid):
    """
    Compare user's current grid with the correct solution.
    Return: correct mask, incorrect mask, is_complete
    """
    user_array = user_grid.replace("", 0).astype(int).values
    correct_mask = (user_array == solution_grid)
    incorrect_mask = (user_array != 0) & (user_array != solution_grid)
    is_complete = np.array_equal(user_array, solution_grid)
    return correct_mask, incorrect_mask, is_complete
