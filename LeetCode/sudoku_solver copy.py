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
        '''
        Convert a 9×9 Sudoku board into an exact-cover binary matrix.

        Args:
            sudoku (list[list[int]]): 9×9 grid with 0 for empty and 1–9 for givens.

        Returns:
            list[list[int]]: A (729+1)×324 matrix where each of the 729 candidate
                            (r,c,v) assignments is a row, and the 324 columns
                            correspond to the four Sudoku constraints:
                            1) cell-filled
                            2) row-digit
                            3) column-digit
                            4) box-digit
        '''
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
        '''
        Map a Sudoku candidate (r, c, v) to its exact-cover row and constraint columns.

        Args:
            r (int): Row index in the Sudoku grid (0–8).
            c (int): Column index in the Sudoku grid (0–8).
            v (int): Value index (0–8) corresponding to digit v+1.

        Returns:
            tuple: (row_pos, cell_col, row_col, col_col, box_col)
                where row_pos is the matrix‐row for this candidate, and the
                others are the four column‐indices it covers.
        '''
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

                self.matrix[0][row_left.column.ID].size += 1
                row_left = row_left.left

            row = row.up  


        target_col.left.right = target_col
        target_col.right.left = target_col


    def get_col_with_least_nodes(self):

        head = self.header

        least_nodes = head.right
        head = head.right

        while (head != self.header):

            if (head.size < least_nodes.size):
                least_nodes = head
            
            head = head.right
        
        return least_nodes

    def convert_to_sudoku(self, solution):
        '''
        Build a solved 9×9 Sudoku grid from the selected exact-cover solution rows.

        Args:
            solutions (list): Either Data nodes (with .row_id) or integer row IDs
                            representing the picked (r,c,v) assignments.

        Side-effect:
            Populates self.solution as a 9×9 array of integers 1–9.
        '''
        self.solution = np.zeros((9,9), dtype="int64")

        for row in solution:
            row_id = row.row_id # We have to extract the row, col, value information from the row in the solution
            row_id -= 1 # Take into account the column row
            c = row_id // 81
            r = (row_id % 81) // 9
            n = (row_id % 81) % 9
            self.solution[c][r] = n + 1 # Convert from zero base
        
        print(self.solution)


    def search(self, k):
        
        if (self.header.right == self.header):
            return self.convert_to_sudoku(self.solutions)
        
        column = self.get_col_with_least_nodes()

        self.cover(column) # Cover that column

        row = column.down
        while (row != column):
            self.solutions.append(row)

            row_right = row.right

            while (row_right != row):
                self.cover(row_right)
                row_right = row_right.right
            
            self.search(k+1)


            self.solutions.pop()

            column = row.column
            left_node = row.left
            while (left_node != row):
                self.uncover(left_node)
                left_node = left_node.left
            
            row = row.down
        
        self.uncover(column)
        return

TEST_INPUT = np.array([
                    [0,2,0, 0,0,6, 9,0,0],
                    [0,0,0, 0,5,0, 0,2,0],
                    [6,0,0, 3,0,0, 0,0,0],

                    [9,4,0, 0,0,7, 0,0,0],
                    [0,0,0, 4,0,0, 7,0,0],
                    [0,3,0, 2,0,0, 0,8,0],

                    [0,0,9, 0,4,0, 0,0,0],
                    [3,0,0, 9,0,2, 0,1,7],
                    [0,0,8, 0,0,0, 0,0,2]
    ])

def sudoku_solver(sudoku):
    dlx = DLX(sudoku)
    dlx.create_linked_mat()
    dlx.search(0)
        

st = time.process_time()
sudoku_solver(TEST_INPUT)
et = time.process_time()
print(f"search finished in {et-st} secs")