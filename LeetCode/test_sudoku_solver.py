import unittest
from sudoku_solver import Solution

class TestSudokuSolver(unittest.TestCase):
    def setUp(self):
        self.solver = Solution()

    def assert_valid_sudoku(self, board):
        """Assert that each row, column, and 3x3 box contains exactly '1'-'9'."""
        digits = set(str(d) for d in range(1, 10))
        # rows
        for r, row in enumerate(board):
            self.assertEqual(set(row), digits, f"Row {r} invalid: {row}")
        # columns
        for c in range(9):
            col = {board[r][c] for r in range(9)}
            self.assertEqual(col, digits, f"Column {c} invalid: {[board[c][r] for r in range(9)]}")
        # 3×3 boxes
        for br in (0, 3, 6):
            for bc in (0, 3, 6):
                box = {
                    board[r][c]
                    for r in range(br, br + 3)
                    for c in range(bc, bc + 3)
                }
                self.assertEqual(
                    box, digits,
                    f"Box starting at ({br},{bc}) invalid: "
                    f"{[[board[c][r] for c in range(bc, bc+3)] for r in range(br,br+3)]}"
                )

    def test_empty_board(self):
        """An all-'.' board should be filled into a valid Sudoku."""
        board = [['.' for _ in range(9)] for __ in range(9)]
        self.solver.solveSudoku(board)
        self.assert_valid_sudoku(board)

    def test_already_solved(self):
        """A fully solved board should remain unchanged (and valid)."""
        solved = [
            ["5","3","4","6","7","8","9","1","2"],
            ["6","7","2","1","9","5","3","4","8"],
            ["1","9","8","3","4","2","5","6","7"],
            ["8","5","9","7","6","1","4","2","3"],
            ["4","2","6","8","5","3","7","9","1"],
            ["7","1","3","9","2","4","8","5","6"],
            ["9","6","1","5","3","7","2","8","4"],
            ["2","8","7","4","1","9","6","3","5"],
            ["3","4","5","2","8","6","1","7","9"],
        ]
        board = [row[:] for row in solved]
        self.solver.solveSudoku(board)
        self.assertEqual(board, solved)

    def test_invalid_duplicate_in_row(self):
        """Two same digits in one row should raise an error."""
        board = [['.' for _ in range(9)] for __ in range(9)]
        board[0][0] = '1'
        board[0][1] = '1'
        with self.assertRaises(ValueError):
            self.solver.solveSudoku(board)

    def test_invalid_duplicate_in_column(self):
        """Two same digits in one column should raise an error."""
        board = [['.' for _ in range(9)] for __ in range(9)]
        board[0][0] = '2'
        board[1][0] = '2'
        with self.assertRaises(ValueError):
            self.solver.solveSudoku(board)

    def test_invalid_duplicate_in_box(self):
        """Two same digits in the same 3×3 box should raise an error."""
        board = [['.' for _ in range(9)] for __ in range(9)]
        board[0][0] = '3'
        board[1][1] = '3'
        with self.assertRaises(ValueError):
            self.solver.solveSudoku(board)

    def test_value_out_of_range(self):
        """Entries outside '1'-'9' (or negative) should raise an error."""
        for bad in ['0', '10', '-1', 'a']:
            board = [['.' for _ in range(9)] for __ in range(9)]
            board[0][0] = bad
            with self.assertRaises(ValueError, msg=f"Did not reject {bad!r}"):
                self.solver.solveSudoku(board)

if __name__ == '__main__':
    unittest.main()