import numpy as np
import time

class Data:

    def __init__(self):
        # pointing to self at the beginning to create valid tiny circular
        # doubly linked list pointing to itself which helps with splicing later
        # and safe removal/restoration during covering and uncovering
        self.left = self
        self.right = self
        self.up = self
        self.down = self
        self.column = self
        self.row_id =  0


class Column(Data):

    def __init__(self, ID):
        super().__init__() # makes sure the the column has all links established
        self.size = 0 # number of 1's in the column
        self.ID = ID # numerical ID of the column (0-323)



class DLX:

    def __init__(self, sudoku):
        '''
        Args:
            sudoku = 9x9 matrix with 0s for empty cells and 1-9 for givens
        '''
        self.header = Column("Start")
        self.exact_cover_matrix = self.convert_to_exact_cover(sudoku)
        self.rows = len(self.exact_cover_matrix)
        self.cols = len(self.exact_cover_matrix[0])
        self.matrix = np.zeros((self.rows, self.cols), dtype = "object_") # object‐dtype NumPy array to later hold linked‐list nodes
        self.solutions = []
        self.solution = []

    def convert_to_exact_cover(self, sudoku):

        col_size = 324
        row_size = 729

        exact_cover = [[0 for _ in range(col_size)] for _ in range(row_size + 1)] # +1 for header

        R = range(len(sudoku))
        C = range(len(sudoku[0]))
        V = range(9)

        for r in R:
            for c in C:
                if sudoku[r][c] == 0:
                    for v in V:
                        sudoku[r][c] = v
                        mapping = self.calculate_mappings(r, c, v)
                        exact_cover = self.apply_to_matrix(exact_cover, mapping)
                else:
                    v = sudoku[r][c] - 1
                    sudoku[r][c] = v
                    mapping = self.calculate_mappings(r, c, v)
                    exact_cover = self.apply_to_matrix(exact_cover, mapping)
        return exact_cover

    def calculate_mappings(self, r, c, v):
        # Constraint starting indexes
        start_cell = 0
        start_row = 81
        start_col = 162
        start_box = 243

        row_pos = 9 * (r*9) + (c*9) + v + 1
        cell_constraint = start_cell + (r*9) + c # get the cell index in the exact cover matrix for a given v
        row_constraint = start_row + (r*9) + v # get the row index in the exact cover matrix for a given v
        col_constraint = start_col + (c*9) + v # get the column index in the exact cover matrix for a given v

        box_row = (r - (r % 3))
        box_column = c // 3
        box_index = (box_row + box_column) * 9
        box_constraint = start_box + box_index + v # get the box index in the exact cover matrix for a given v

        return (row_pos, cell_constraint, row_constraint, col_constraint, box_constraint)

    def apply_to_matrix(self, matrix, constraints):
        """
        Set 1 for a given value in its corresponding cell, row, column, box
        constraint column using the row position in the exact cover matrix
        """
        (row_pos, cell_constraint, row_constraint, col_constraint, box_constraint) = constraints

        matrix[row_pos][cell_constraint] = True
        matrix[row_pos][row_constraint] = True
        matrix[row_pos][col_constraint] = True
        matrix[row_pos][box_constraint] = True

        return matrix

    def create_linked_mat(self):
        
        # Linking Columns - First row of matrix is only column objects
        for c in range(self.cols):
            col_node = Column(c)

            # making a doubly linked list
            col_node.left = self.header.left
            col_node.right = self.header
            self.header.left.right = col_node
            self.header.left =  col_node
            self.matrix[0][c] = col_node # name the column the col_num

        # Link rows
        for r in range(1, self.rows): # Start from 1 (columns are already linked)
            reference_node = None # Used as a reference point when linking rows
            for c in range(self.cols):
                if self.exact_cover_matrix[r][c]: # If true

                    column_node = self.matrix[0][c] # Get the column header of this data object

                    data_node = Data()
                    data_node.column = column_node # add reference to column header
                    data_node.up = column_node.up 
                    data_node.down = column_node
                    data_node.row_id = r

                    column_node.up.down = data_node
                    column_node.up = data_node
                    column_node.size += 1

                    if reference_node == None: 
                        reference_node = data_node # The initial reference is the first data object of the row

                    data_node.left = reference_node.left
                    data_node.right = reference_node
                    reference_node.left.right = data_node
                    reference_node.left = data_node

                    self.matrix


    # The cover function as described in Knuth's paper
    def cover(self, target):

        # Get the column of the target node
        target_col = target.column

        # Unlink column header 
        target_col.left.right = target_col.right
        target_col.right.left = target_col.left


        # Unlink rows
        row = target_col.down
        # We unlink all rows of the column
        while (row != target_col):

            row_right = row.right

            # Unlink this row
            while (row_right != row):

                row_right.up.down = row_right.down
                row_right.down.up = row_right.up

                # Decrement the number of nodes this column has
                self.matrix[0][row_right.column.ID].size -= 1
                row_right = row_right.right

            row = row.down  

    # The uncover function as described in Knuth's paper
    def uncover(self, target):
        target_col = target.column


        # Link rows
        row = target_col.up
        
        # We link all rows of this column
        while (row != target_col):

            row_left = row.left

            # Link this row
            while (row_left != row):

                row_left.up.down = row_left
                row_left.down.up = row_left

                # Increment the number of nodes this column has
                self.matrix[0][row_left.column.ID].size += 1
                row_left = row_left.left

            row = row.up  


        target_col.left.right = target_col
        target_col.right.left = target_col


    # Heuristic which choose the column with the least number of nodes (helps reduce the branching factor of our search)
    def get_col_with_least_nodes(self):

        head = self.header

        least_nodes = head.right
        head = head.right

        while (head != self.header):

            if (head.size < least_nodes.size):
                least_nodes = head
            
            head = head.right
        
        return least_nodes

    def convert_to_sudoku(self, solution, board):
        self.solution = np.zeros((9,9), dtype="int64")

        for row in solution:
            row_id = row.row_id # We have to extract the row, col, value information from the row in the solution
            row_id -= 1 # Take into account the column row
            c = row_id // 81
            r = (row_id % 81) // 9
            n = (row_id % 81) % 9
            self.solution[c][r] = n + 1
            board[c][r] = n + 1
        # print(self.solution)


    # The search function as described in Knuth's paper
    def search(self, k, board):
        
        # We managed to cover all columns, and therefore found solution(s)
        if (self.header.right == self.header):
            # return self.convert_to_sudoku(self.solutions, board)
            self.convert_to_sudoku(self.solutions, board)
            return True
        
        column = self.get_col_with_least_nodes()

        self.cover(column)

        row = column.down
        while (row != column):
            self.solutions.append(row)

            row_right = row.right

            while (row_right != row):
                self.cover(row_right)
                row_right = row_right.right
            
            # self.search(k+1, board)
            if self.search(k+1, board):
                return True


            self.solutions.pop()

            column = row.column
            left_node = row.left
            while (left_node != row):
                self.uncover(left_node)
                left_node = left_node.left
            
            row = row.down
        
        # self.uncover(column)
        self.uncover(column)
        return False

class Solution:
    def _validate_input(self, board):
        """
        Ensure board is 9×9, entries are '.' or '1'–'9', and no duplicates in row/col/box.
        Raises ValueError on any violation.
        """
        # Dimension check
        if len(board) != 9 or any(len(row) != 9 for row in board):
            raise ValueError("Board must be 9×9")

        # Track seen digits
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]

        for r in range(9):
            for c in range(9):
                val = board[r][c]
                if val == '.':
                    continue

                # Type & range check
                if not (isinstance(val, str) and len(val) == 1 and '1' <= val <= '9'):
                    raise ValueError(f"Invalid entry {val!r} at ({r},{c})")

                # Row duplicate?
                if val in rows[r]:
                    raise ValueError(f"Duplicate {val!r} in row {r}")
                rows[r].add(val)

                # Column duplicate?
                if val in cols[c]:
                    raise ValueError(f"Duplicate {val!r} in column {c}")
                cols[c].add(val)

                # Box duplicate?
                bi = (r // 3) * 3 + (c // 3)
                if val in boxes[bi]:
                    raise ValueError(f"Duplicate {val!r} in box {bi}")
                boxes[bi].add(val)

    def solveSudoku(self, board):
        """
        Solve the Sudoku board in-place using DLX algorithm.
        Args:
            board: 9x9 list of lists with '.' for empty cells and '1'-'9' for givens
            OR
            board: 9x9 list of lists with 0 for empty cells and 1-9 for givens
        Raises:
            ValueError: If the board is not a valid Sudoku or if it cannot be solved.
        Returns:
            None: The board is modified in-place to be a valid Sudoku solution.
        """
        # Uncomment line 344 to print the str board or line 230 in convert_to_sudoku to print the int board
        
        self._validate_input(board)
    
        if isinstance(board[0][0], str):
            grid = [[int(board[r][c]) if board[r][c] != '.' else 0
                   for c in range(9)] for r in range(9)]
        else:
            grid = board
        dlx = DLX(np.array(grid))
        dlx.create_linked_mat()
        dlx.search(0, grid)
        # write back into sudoku as strings
        if isinstance(board[0][0], str):
            for r in range(9):
                for c in range(9):
                    board[r][c] = str(dlx.solution[r][c])
            # print(f"List of Strings: {board}")

TEST_INPUT = [
                    [0,2,0, 0,0,6, 9,0,0],
                    [0,0,0, 0,5,0, 0,2,0],
                    [6,0,0, 3,0,0, 0,0,0],

                    [9,4,0, 0,0,7, 0,0,0],
                    [0,0,0, 4,0,0, 7,0,0],
                    [0,3,0, 2,0,0, 0,8,0],

                    [0,0,9, 0,4,0, 0,0,0],
                    [3,0,0, 9,0,2, 0,1,7],
                    [0,0,8, 0,0,0, 0,0,2]
    ]

# LeetCode Input type:
board = [["5","3",".",".","7",".",".",".","."],
         ["6",".",".","1","9","5",".",".","."],
         [".","9","8",".",".",".",".","6","."],
         ["8",".",".",".","6",".",".",".","3"],
         ["4",".",".","8",".","3",".",".","1"],
         ["7",".",".",".","2",".",".",".","6"],
         [".","6",".",".",".",".","2","8","."],
         [".",".",".","4","1","9",".",".","5"],
         [".",".",".",".","8",".",".","7","9"]]

sol = Solution()
sol.solveSudoku(board)