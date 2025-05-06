import unittest
from n_queens import Solution

class TestNQueensSolver(unittest.TestCase):
    def setUp(self):
        self.solver = Solution()

    def test_negative_n(self):
        """A negative value of n should raise and exception as that's impossible
        """
        with self.assertRaises(ValueError):
            self.solver.solveNQueens(-1)

    def test_zero_n(self):
        """n = 0 should return one solution, an empty one: [[]]
        """
        self.assertEqual(self.solver.solveNQueens(0), [[]])

    def test_one_n(self):
        """n = 1 should return one solution, [["Q"]]
        """
        self.assertEqual(self.solver.solveNQueens(1), [['Q']])

    def test_two_n(self):
        """n = 2 should return no solution, an empty solutions list
        """
        self.assertEqual(self.solver.solveNQueens(2), [])

    def test_three_n(self):
        """n = 3 should return no solution, an empty solutions list
        """
        self.assertEqual(self.solver.solveNQueens(3), [])

    def test_four_n(self):
        """n = 4 should return 2 solutions:
        [['.Q..', '...Q', 'Q...', '..Q.'], 
        ['..Q.', 'Q...', '...Q', '.Q..']]
        """
        correct_solution = [
            ['.Q..', '...Q', 'Q...', '..Q.'], 
            ['..Q.', 'Q...', '...Q', '.Q..']]

        self.assertEqual(self.solver.solveNQueens(4), correct_solution)

if __name__ == '__main__':
    unittest.main()