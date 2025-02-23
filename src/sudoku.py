import numpy as np
from constraint import Problem, AllDifferentConstraint


class Sudoku:
    def __init__(self, filledIndex, filledValue):
        self.grid = np.full(81, 0, dtype=int)
        self.grid[filledIndex] = list(map(int, filledValue))
        self.rows = self.grid.reshape(9, 9)
        self.cols = self.rows.T
        self.subgrid = np.array(
            [
                self.rows[r:r+3, c:c+3].flatten()
                for r in range(0, 9, 3)
                for c in range(0, 9, 3)
            ]
        )

    def visualize(self):
        for i, row in enumerate(self.rows):
            if i % 3 == 0 and i != 0:
                print("-" * 25)

            row_str = " | ".join(
                " ".join(str(cell) for cell in row[j:j+3])
                for j in range(0, 9, 3)
            )
            print(row_str)

    def solve(self):
        problem = Problem()

        variables = [(r, c) for r in range(9) for c in range(9)]
        for var in variables:
            if self.rows[var[0], var[1]] == 0:
                problem.addVariable(var, range(1, 10))
            else:
                problem.addVariable(var, [self.rows[var[0], var[1]]])

        # Row constraints
        for row in range(9):
            problem.addConstraint(AllDifferentConstraint(), [(row, col) for col in range(9)])
       
        # Col constraints
        for col in range(9):
            problem.addConstraint(AllDifferentConstraint(), [(row, col) for row in range(9)])

        # Subgrid constraint
        for box_row in range(3):
            for box_col in range(3):
                problem.addConstraint(
                    AllDifferentConstraint(),
                    [
                        (box_row * 3 + i, box_col * 3 + j)
                        for i in range(3)
                        for j in range(3)
                    ]
                )

        solutions = problem.getSolutions()

        if solutions:
            solved_grid = [[solutions[0][(r, c)] for c in range(9)] for r in range(9)]
            solved_array = np.array(solved_grid)
            only_new_value = np.where(self.rows.flatten() == solved_array.flatten(), 0, solved_array.flatten())
            self.rows = np.array(solved_grid)

            return only_new_value
        else:
            print("No solution found.")
