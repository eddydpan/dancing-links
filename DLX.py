"""File containing classes and functions for construction a dancing linked list
"""
import numpy as np
import copy

class Node():
    """Create a node for a circular, multi-linked list"""

    def __init__(self):
        self.col = self
        self.up = self
        self.down = self
        self.right = self
        self.left = self
        # Is the row_id strictly necessary? I'm thinking it might not be
        self.row_id = 0

class Column(Node):
    """Class representing a column's header node in a dancing linked list"""
    def __init__(self, col_id):
        # This super means the column will also have all the properties of a
        # Node, so referencing the Column is also referencing its header
        super().__init__()
        self.size = 0
        self.col_id = col_id

class DLX_solver():
    """Class for using DLX to solve N-Queens"""
    def __init__(self, type, n, cover_mat, sudoku):
        """Initialize the DLX solver"""
        self.header = Column("Header")
        self.type = type
        self.solutions = []
        self.curr_sol = []
        if type == "N-Queens":
            self.cover_mat = cover_mat
            self.n = n
            self.queens_boards = []
            
        elif type == "Sudoku":
            self.cover_mat = self.convert_to_exact_cover(sudoku)
            self.rows = len(self.cover_mat)
            self.cols = len(self.cover_mat[0])
            self.matrix = np.zeros((self.rows, self.cols), dtype = "object_") # object‐dtype NumPy array to later hold linked‐list nodes

    def empty_to_exact_cover(self):
        '''
        Generate the exact-cover matrix for an empty N-Queens problem of size n.

        Constructs a matrix with (n**2 + 1) rows and (6*n - 2) columns encoding:
        - n “row” constraints
        - n “column” constraints
        - (2n - 1) positive-diagonal constraints
        - (2n - 1) negative-diagonal constraints

        Each candidate queen placement at (r,c) becomes one row in this matrix,
        with four 1's marking which 4 constraints it satisfies.
        '''
        # cover matrix representing an empty N-Queens exact cover matrix
        # Pseudocode:
        # 1. Create an empty exact cover matrix. n + n + (2n - 1) + (2n - 1) by (n**2 + 1)
        #    for n rows, n cols, 2n - 1 positive diagonals and 2n - 1 negative diagonals
        n = self.n
        
        # Create a matrix of 0s to start with
        self.cover_mat = [[0 for _ in range(6*n - 2)] for _ in range (n**2 + 1)]

        # Iterate through all possible rows and column positions
        for r in range(n):
            for c in range(n):
                # Calculate the conditions that it will cover
                row_map = r # will be 0->n-1
                col_map = (n) + c # will be n->2n-1
                pos_diag_map = (2*n) + r + c # will be 2n->4n-2
                neg_diag_map = (4*n - 2) + n - c + r # will be 4n-2->6n-3

                # Populate the cover_mat. 1 row for each possible position
                self.cover_mat[r*n+c+1][row_map] = 1 
                self.cover_mat[r*n+c+1][col_map] = 1 
                self.cover_mat[r*n+c+1][pos_diag_map] = 1 
                self.cover_mat[r*n+c+1][neg_diag_map] = 1 

    def convert_to_exact_cover(self, sudoku):
        '''
        Convert a 9x9 Sudoku board into an exact-cover binary matrix.

        Args:
            sudoku (list[list[int]]): 9x9 grid with 0 for empty and 1-9 for givens.

        Returns:
            list[list[int]]: A (729+1)x324 matrix where each of the 729 candidate
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
            r (int): Row index in the Sudoku grid (0-8).
            c (int): Column index in the Sudoku grid (0-8).
            v (int): Value index (0-8) corresponding to digit v+1.

        Returns:
            tuple: (row_pos, cell_col, row_col, col_col, box_col)
                where row_pos is the matrix-row for this candidate, and the
                others are the four column-indices it covers.
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
        Set the four 1's in the exact-cover matrix for a single Sudoku candidate.

        Args:
            matrix (list[list[int]]): The current exact-cover matrix (rowxcol).
            constraints (tuple): (row_pos, cell_c, row_c, col_c, box_c) indices.

        Returns:
            list[list[int]]: The updated matrix with four True entries set.
        """
        (row_pos, cell_constraint, row_constraint, col_constraint, box_constraint) = constraints

        matrix[row_pos][cell_constraint] = True
        matrix[row_pos][row_constraint] = True
        matrix[row_pos][col_constraint] = True
        matrix[row_pos][box_constraint] = True
        return matrix

    def convert_to_sudoku(self, solutions):
        '''
        Build a solved 9x9 Sudoku grid from the selected exact-cover solution rows.

        Args:
            solutions (list): Either Data nodes (with .row_id) or integer row IDs
                            representing the picked (r,c,v) assignments.

        Side-effect:
            Populates self.solution as a 9x9 array of integers 1-9.
        '''
        self.solutions = np.zeros((9,9), dtype="int64")

        for row_id in solutions:
            row_id -= 1 # Take into account the column row
            c = row_id // 81
            r = (row_id % 81) // 9
            n = (row_id % 81) % 9
            self.solutions[c][r] = n + 1 # Convert from zero base
        
        print(self.solutions)

    def convert_to_queens(self):
        # create a blank n x n board to reference when building solutions
        blank_board = [["." for _ in range(self.n)] for _ in range(self.n)]

        # for each solution in self.solutions
        for solution in self.solutions:
            curr_board = copy.deepcopy(blank_board)
            # for each row selected for the solution
            for cover_row in solution:
                # find the column and row indeces corresponding to the row
                c = (cover_row-1) % self.n
                r = (cover_row-1-c) // self.n

                # Set the corresponding spot on curr_board to "Q"
                curr_board[r][c] = "Q"
            self.queens_boards.append(curr_board.copy())

    def exact_cover_to_dancing_list(self):
        """
        Build the toroidal dancing-links structure from the exact-cover matrix.

        Reads self.cover_mat (with header padding at row 0) and:
        1. Creates Column header nodes for each constraint.
        2. Links them left↔right off self.header.
        3. For each 1 in self.cover_mat, creates a Node, splices it vertically
            into its column and horizontally into its row.

        Side-effects:
            - Populates self.cover_mat[0][*] with Column objects.
            - Splices every Node into the 4-way linked structure.
        """
        # Pseudocode:
        # 1. Create a column node + 1 for each column in the exact cover matrix (gives us the dummy home node too)
        # 2. Add that reference to that column at the self.cover_mat[0][i]
        # 3. Link each of these columns together left to right
        # 4. Iterate through each row of the cover matrix after padding
        #   5. Create a row_node ref for linking (=None)
        #   6. Iterate through each column index in the row
        #       7. If it's unoccupied
        #           8. Create node object
        #               Give it row ID i
        #           9. Link it to the column at this point (self.matrix[0][j])
        #               Increase the size of the column by 1
        #           10. If row_ref == None
        #               11. Make the current node the reference for the row
        #           12. Append the current node to the row reference
        
        # circularly double link a column for each column in the input matrix
        for i in range(len(self.cover_mat[0])):
            new_col = Column(i)
            new_col.right = self.header
            new_col.left = self.header.left
            self.header.left.right = new_col
            self.header.left = new_col

            # Make a reference to this column in cover_mat
            self.cover_mat[0][i] = new_col

        # Iterate through cover_mat (excluding padding for headers) and populate
        for r in range(1, len(self.cover_mat)):
            # Initialize a reference to the first element of the row to making 
            # adding nodes easier
            row_ref = None
            for c in range(len(self.cover_mat[0])):
                if self.cover_mat[r][c] == 0: # No node here
                    continue
                # Create a node for this element
                new_node = Node()
                new_node.row_id = r


                # Link to its column
                curr_col = self.cover_mat[0][c]
                new_node.col = curr_col # Previously stored column
                new_node.up = curr_col.up
                new_node.down = curr_col
    
                curr_col.up.down = new_node
                curr_col.up = new_node
                curr_col.size += 1

                # Link to its row
                if row_ref == None:
                    row_ref = new_node
                
                new_node.right = row_ref
                new_node.left = row_ref.left

                row_ref.left.right = new_node
                row_ref.left = new_node

                self.cover_mat[r][c] = new_node


    def least_constrained_col(self):
        '''
        Choose the column header with the fewest remaining nodes (smallest size).

        Implements Knuth's “minimum remaining values” heuristic to reduce branching.

        Returns:
            Column: The most constrained column header (fewest 1's) to branch on next.
        '''
        head = self.header
        least_nodes = head.right
        head = head.right

        if self.type == "N-Queens":
            while (head != self.header and head.col_id < 2*self.n):

                if (head.size < least_nodes.size):
                    least_nodes = head
                
                head = head.right
        elif self.type == "Sudoku":
            while (head != self.header):

                if (head.size < least_nodes.size):
                    least_nodes = head
            
                head = head.right

        return least_nodes

    def cover(self, col_head):
        """
        Remove a column (and its rows) from the dancing-links structure.

        Implements Knuth’s cover operation:
        1. Unlink col_head from its left↔right neighbors.
        2. For each row in that column, unlink every node in that row from its
            up↔down neighbors, decrementing column sizes.

        Args:
            col_head (Column): The column header to cover.
        """
        # Pseudocode:
        # 1. Extract the column from the node
        # 2. Disconnect the head of the column from the other heads
        # 3. Iterate through all rows
        #   4. Iterate through all nodes in row (other than in col)
        #       5. disconnect each of those nodes from their columns (up+down)
        
        # Disconnect the column head from the other heads
        col_head.left.right = col_head.right
        col_head.right.left = col_head.left

        # Iterate through all of the rows in the column until you reach the head
        # again. Go top to bottom
        row = col_head.down
        while row != col_head:
            # Iterate through all of the nodes in each row, except for the one
            # in the starting column. Go left to right
            row_node = row.right
            while row_node != row:
                # Disconnect the row node from it's column
                row_node.up.down = row_node.down
                row_node.down.up = row_node.up

                # Move on to the next row_node
                row_node = row_node.right

            # Move on to the next row
            row = row.down

    def uncover(self, col_head):
        """
        Restore a previously covered column and its rows back into the structure.

        The inverse of cover:
        1. For each row in reverse order, relink its nodes vertically.
        2. Reinsert col_head into its left↔right neighbors.

        Args:
            col_head (Column): The column header to uncover.
        """
        # Pseudocode:
        # Basically just the reverse of what we did in cover

        # Iterate through all of the rows in the column until you reach the head
        # again. Go bottoum to top
        row = col_head.up
        while row != col_head:
            # Iterate through all of the nodes in each row, except for the one
            # in the starting column. Go right to left
            row_node = row.left
            while row_node != row:
                # Reconnect the row node from its link
                row_node.up.down = row_node
                row_node.down.up = row_node
                
                # Move on to the next row_node
                row_node = row_node.left

            # Move on to the next row
            row = row.up

        # Reconnect the column head to the other heads
        col_head.left.right = col_head
        col_head.right.left = col_head

    def AlgoX(self):
        """
        Execute Knuth's Algorithm X search to find all solutions.

        Depending on self.type (“N-Queens” or “Sudoku”):
        1. Check base case: if no columns remain, record current solution.
        2. Choose a column via least_constrained_col().
        3. cover(column), then for each row in that column:
            a. Append its row_id (or node) to self.curr_sol.
            b. cover() all other columns touched by that row.
            c. Recursively call AlgoX().
            d. Pop self.curr_sol and uncover() those columns.
        4. uncover(column), return to caller.

        Side-effects:
            - Populates self.solutions (list of row_ids or nodes) on success.
            - For Sudoku, calls convert_to_sudoku at base-case to build final grid.
        """
        # Pseudocode:
        # 1. Base case, header.right = header, append current solution to solutions, return
        # 2. Choose a starting column, probably off of least constraints heuristic
        # 3. Cover the chosen column
        # 4. Iterate through all of the rows of the column
        #   5. self.solution.append(row), try
        #   6. Iterate through all columns that intersect with the row
        #       7. Cover each of the columns
        #   8. Recursively call AlgoX
        #   9. self.solution.pop(), don't try
        #   10. Iterate through the columns that intersect with the row in reverse
        #       11. Uncover each of the columns
        #   12. row = row.down
        # 13. Uncover the column
        # 14. empty return statement, other base case (unsuccessful recursion))
        
        if self.type == "N-Queens":
            n = self.n

            test = self.header.right
            while test != self.header:
                test = test.right
            
            if self.header.right == self.header or self.header.right.col_id >= 2*n - 1:
                self.solutions.append(self.curr_sol.copy())
                return
            
        elif self.type == "Sudoku":
            if (self.header.right == self.header):
                return self.convert_to_sudoku(self.curr_sol)
        
        # Heuristic to improve speed
        curr_col = self.least_constrained_col()

        # Cover the chosen column
        self.cover(curr_col)

        # Try all possible rows that satisfy this column. Find first row below
        # column header
        row = curr_col.down
        while row != row.col:
            # Try the current row
            self.curr_sol.append(row.row_id)

            # Cover all columns that intersect with the row
            cover_node = row.right
            while cover_node != row:
                self.cover(cover_node.col)

                cover_node = cover_node.right

            # Recursively run AlgoX on the remainder of the dancing linked list
            self.AlgoX()

            # Choose the option of not trying the current row
            self.curr_sol.pop()
            
            # Uncover all columns that intersect with the row (reverse order)
            uncover_node = row.left
            while uncover_node != row:
                self.uncover(uncover_node.col)

                uncover_node = uncover_node.left

            # Move on to the next row
            row = row.down

        # Uncover the originally chosen column
        self.uncover(curr_col)
        # 2nd base case, reached the end of search