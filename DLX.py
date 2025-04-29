"""File containing classes and functions for construction a dancing linked list
"""

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
    def __init__(self, col_ID):
        # This super means the column will also have all the properties of a
        # Node, so referencing the Column is also referencing its header
        super().__init__()
        self.size = 0
        self.col_ID = col_ID

class DLX():
    """Class for using DLX to solve N-Queens"""
    def __init__(self, cover_mat = []):
        # TODO note that cover_mat needs to have a row of zero padding on top
        """Initialize the DLX solver"""
        self.header = Column("Header")
        self.cover_mat = cover_mat
        self.solutions = []
        self.curr_sol = []

    def queens_to_exact_cover(self):
        """Converts a binary occupancy matrix of an square N-Queens problem into
        an exact cover matrix"""
        # TODO test that this is performing as expected
        # TODO base the input on what you would get for the leetcode
        # Psuedo code:
        # 1. Iterate through the binary occupancy matrix
        #   2. If value is 1, already occupied
        # 
        # OH YOU CAN JUST APPEND ANY PRE-DETERMINED ROWS INTO THE SOLUTIONS
        # BEFORE STARTING THE SEARCH
        pass

    def empty_to_exact_cover(self, n):
        # TODO might not be necessary, converts a dimension n into the exact
        # cover matrix representing an empty N-Queens exact cover matrix
        # Psuedo code:
        # 1. Create an empty exact cover matrix. n + n + (2n - 1) + (2n - 1) by n**2
        #    for n rows, n cols, 2n - 1 positive diagonals and 2n - 1 negative diagonals
        pass

    def exact_cover_to_dancing_list(self):
        """Converts an exact cover matrix into a dancing linked list"""
        # TODO write a test for this
        # 1. Create a column node + 1 for each column in the exact cover matrix (gives us the dummy home node too)
        # 2. Add that a reference to that column at the self.cover_mat[0][i]
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
        pass

    def least_constrained_col(self):
        # TODO make sure that this doesn't choose soft constraints
        pass

    def cover(self, col_head):
        """Covers a column in the dancing linked list"""
        # TODO write a test for this of some kind? namely a check if dancing lists
        # are equal
        # Psuedo code:
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
        """Uncovers a column in the dancing linked list"""
        # TODO unittest
        # Psuedo code:
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
        """Searches for solutions to the N-Queens problem using Algorithm X"""
        # TODO check if this functions correctly
        # Psuedo code:
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
        
        # 1st base case, cleared out the hard requirements TODO add soft requirements detection
        if self.header.right == self.header:
            self.solutions.append(self.curr_sol)
            return
        
        # Heuristic to improve speed
        curr_col = self.least_constrained_col()

        # Cover the chosen column
        self.cover(curr_col)

        # Try all possible rows that satisfy this column. Find first row below
        # column header
        row = curr_col.down
        while row != row.col:
            # Try the current row
            self.curr_sol.append(row)

            # Cover all columns that intersect with the row
            cover_node = row.right
            while cover_node != row:
                self.cover(cover_node.col)

            # Recursively run AlgoX on the remainder of the dancing linked list
            self.AlgoX()

            # Choose the option of not trying the current row
            self.curr_sol.pop()
            
            # Uncover all columns that intersect with the row (reverse order)
            uncover_node = row.left
            while uncover_node != row:
                self.uncover(uncover_node.col)

            # Move on to the next row
            row = row.down

        # Uncover the originally chosen column
        self.uncover(curr_col)

        # 2nd base case, reached the end of search
        return
