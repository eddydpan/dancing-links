import numpy as np

class Node:
    """
    A class to represent the circular doubly linked list nodes. 
    """
    def __init__(self):
        self.left = self
        self.right = self
        self.up = self
        self.down = self
        self.column = self
        self.row_id = 0

class ColumnHeader(Node):
    """
    A class to represent the header column nodes to keep track of size and id,
    not to be treated as storing relevant data.

    Extends class Node.
    """
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.size = 0

class DancingLinks:

    def __init__(self, cover_matrix):
        self.header = ColumnHeader("root")
        cover_matrix.insert(0, [0 for _ in range(len(cover_matrix[0]))])
        self.cover_matrix = cover_matrix;
        self.num_rows = len(self.cover_matrix)
        self.num_cols = len(self.cover_matrix[0])
        
        # dtype="object_" --> self.matrix will be populated by DLL nodes
        self.matrix = np.zeros((self.num_rows, self.num_cols), dtype="object_")

        self.partial_solution = [] # stacc
        self.result = []

    def generate_dll_mat(self):
        """
        Populates object attribute self.matrix with nodes

        Creates ColumnHeader nodes then populates the matrix with its vertical
        and horizontal links of all data nodes.
        """

        # Generate ColumnHeader nodes on first row
        for c in range(self.num_cols):
            col_node = ColumnHeader(c) 
            # Insert col_node to the left of the header node, update links
            col_node.left = self.header.left        # 0 <-> "root"
            col_node.right = self.header            # 0 <-> 1 <-> "root"
            # Update the link of the previous node to the left of the header
            self.header.left.right = col_node
            self.header.left = col_node

            # Insert the linked col_node into the matrix
            self.matrix[0][c] = col_node
        
        # Generate and link Nodes, populate the matrix.
        for r in range(1, self.num_rows):
            ref_node = None     # initialize ref_node for linking rows
            for c in range(self.num_cols):
                # Check the exact cover problem matrix 
                if self.cover_matrix[r][c] == 1:
                    # Create a new node, create its links
                    new_node = Node()
                    # Create vertical links
                    new_node.column = self.matrix[0][c] # c repr the col id
                    new_node.up = new_node.column.up                #    H1
                    new_node.down = new_node.column                 #    n1
                    new_node.column.up.down = new_node              # -> n2
                    new_node.column.up = new_node                   #    H1
                    
                    # Assign other properties to node
                    new_node.column.size += 1
                    new_node.row_id = r

                    # Create horizontal links
                    if ref_node == None: # in case of first node
                        ref_node = new_node
                    
                    new_node.left = ref_node.left #  n0 > new_node > ref
                    new_node.right = ref_node
                    ref_node.left.right = new_node
                    ref_node.left = new_node

                    self.matrix[r][c] = new_node


    def get_col_with_fewest_nodes(self):
        """
        Helper function to get the column header with the fewest nodes. Reduces
        the number of branches in the search.

        Returns:
        A ColumnHeader node with the fewest nodes.
        """

        col_with_fewest_nodes = head = self.header.right # move the head once
        
        # cycle check
        while head != self.header:
            if head.size < col_with_fewest_nodes.size:
                col_with_fewest_nodes = head

            head = head.right 
    
        return col_with_fewest_nodes

    def cover(self, target_node):
        """
        Covers a column. Traverses columns downwards and rows rightwards.

        Covering a column means finding all the 1s in the column and traversing
        their respective rows in order to remove the vertical links of all the
        1s in the row.

        Args:
            target_node: a Node object to cover the column of.
        """
        target_col = target_node.column

        # Un-link target_col
        target_col.left.right = target_col.right
        target_col.right.left = target_col.left

        # Iterate through the removed target_col's column (downwards)
        col_node = target_col.down

        while col_node != target_col: # cycle detection

            # Iterate through the row (rightwards)
            row_node = col_node.right
            while row_node != col_node: # cycle detection
                
                # Remove the links
                row_node.up.down = row_node.down
                row_node.down.up = row_node.up

                # Update the number of nodes the column header has
                self.matrix[0][row_node.column.id].size -= 1

                row_node = row_node.right # keep iterating row (rightwards)
            
            col_node = col_node.down # keep iterating col (downwards)

    def uncover(self, node):
        """
        Uncovers a column. Traverses columns upwards and rows leftwards.
        """
        
        target_col = node.column
        col_node = target_col.up

        # Iterate through column nodes (upwards)
        while col_node != target_col:

            # Iterate through row nodes (leftwards)
            row_node = col_node.left
            while row_node != col_node: 

                # Add the vertical links back for the row nodes
                row_node.up.down = row_node
                row_node.down.up = row_node

                # Update the number of nodes in the ColumnHeader node
                self.matrix[0][row_node.column.id].size += 1

                row_node = row_node.left
            
            col_node = col_node.up

        # Add back in the links to the now-uncovered column header
        target_col.left.right = target_col
        target_col.right.left = target_col

    def search(self, k=0):
        """
        Backtracking searcher to find solutions to the exact cover problem.

        Args:
            k: an int representing the depth of search. Start it at 0 lol
        
        Returns:
        The solution!!!!!!!!!!!!!!!!!!!!!!!!11
        """
        # Base case -- all columns have been covered
        if self.header.right == self.header:
            self.result.append(self.partial_solution[:])
            return
        

        col_header = self.get_col_with_fewest_nodes()

        self.cover(col_header)

        # Iterate through the covered column
        dummy_col = col_header.down
        while dummy_col != col_header:
            self.partial_solution.append(dummy_col.row_id)
    
            dummy_row_right = dummy_col.right

            
            # Iterate through the rows of the covered column's 1s & cover them
            while dummy_row_right != dummy_col:
                self.cover(dummy_row_right)
                dummy_row_right = dummy_row_right.right
            # Recurse -- committing to this partial solution
            self.search(k+1)

            # Backtrack
            self.partial_solution.pop() # pop from the stack

            col_header = dummy_col.column # <- I believe this line is redundant
            dummy_row_left = dummy_col.left
            while dummy_row_left != dummy_col:
                self.uncover(dummy_row_left)
                dummy_row_left = dummy_row_left.left
            
            dummy_col = dummy_col.down # move the dummy col node down
        
        self.uncover(col_header)
        return # no solutions

    def solve(self):
        self.generate_dll_mat()
        self.search()
        final = min(self.result, key=len)
        print(f"Our final result: {final}, all the solutions are: {self.result}")
        return len(final)
    
    
TEST_COVER_MATRIX = [
    [1, 0, 0, 1],
    [0, 1, 0, 1],
    [0, 0, 1, 0],
    [1, 0, 0, 0],
    [1, 0, 1, 0]
]

dlx = DancingLinks(TEST_COVER_MATRIX)
dlx.solve()




