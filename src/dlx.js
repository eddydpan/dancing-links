/**
 * Contains functionality for the Dancing Links Algorithm (DLX)
 */


/**
 * A class that represents a node in a circular doubly linked list
 */
class Node {
    constructor() {
        this.up = this;
        this.down = this;
        this.right = this;
        this.left = this;
        this.column = this;
        this.row_id = 0;
    }
}

/**
 * Class to represent the Column Header nodes.
 */
class ColumnHeader extends Node {
    constructor(id) {
        super();
        this.size = 0;
        this.id = id;
    }
}

export class DLX {
    /**
     * 
     * @param {Int[][]} coverMatrix 
     */
    constructor(coverMatrix) {
        this.header = new ColumnHeader("root");
        
        coverMatrix.unshift(Array.from( {length: coverMatrix[0].length}, () => 0));
        this.coverMatrix = coverMatrix;
        console.log(this.coverMatrix);
        this.numRows = coverMatrix.length;
        this.numCols = coverMatrix[0].length;
        this.matrix = Array.from({ length: this.numRows}, () =>
            Array.from({ length: this.numCols }, () => null)
        );
     
        
        this.results = new Array();
        this.partialSolutions = new Array();

        this.searchSteps = [];
        this.logs = [];

    }

    generateDLLMat() {
        /* Generate all column headers */
        for (let i = 0; i < this.numCols; i++) {
            let colHeader = new ColumnHeader(i);

            // Link the new ColumnHeader with its neighbors and vice versa
            colHeader.left = this.header.left;
            colHeader.right = this.header;

            this.header.left.right = colHeader;
            this.header.left = colHeader;

            this.matrix[0][i] = colHeader;
        }
        /* Iterate through all indices of this.matrix to make + link nodes*/
        for (let r = 1; r < this.numRows; r++) { // start at row after headers
            let refNode = null;
            
            for (let c = 0; c < this.numCols; c++) {
                if (this.coverMatrix[r][c] == 1) {

                    let newNode = new Node();
                    // Create vertical links
                    newNode.column = this.matrix[0][c];
                    newNode.up = newNode.column.up;
                    newNode.down = newNode.column;

                    newNode.column.up.down = newNode;
                    newNode.column.up = newNode;

                    // Update instance variables to reflect adding a new node
                    newNode.row_id = r;
                    newNode.column.size += 1;

                    // Create horizontal links
                    if (refNode == null) { // case where refNode is null, first iter
                        refNode = newNode;
                    }

                    newNode.left = refNode.left;
                    newNode.right = refNode;
                    refNode.left.right = newNode;
                    refNode.left = newNode;

                    this.matrix[r][c] = newNode;
                }
            }
        }
    }

    /**
     * Helper function to select the column with the fewest 1s.
     * @returns {ColumnHeader} column with the fewest 1s
     */
    selectColumn() {
        let selectedCol = this.matrix[0][0];
        for (let i = 1; i < this.numCols; i++) {
            if (this.matrix[0][i].size < selectedCol.size) {
                selectedCol = this.matrix[0][i];
            }
        }
        // console.log("Size of selected col: ", selectedCol.size); //FIXME:
        return selectedCol;
    }

    /**
     * Covers a column.
     * @param {Node} target the node whose column will be covered :O
     * @returns a dictionary with set values
     */
    cover(target, currDepth) {
        const affectedRows = [];

        // Cover the column - remove its links from the other ColHeaders
        let coveredCol = target.column;
        coveredCol.left.right = coveredCol.right;
        coveredCol.right.left = coveredCol.left;

        let row = coveredCol.down;
        while (row != coveredCol) {
            affectedRows.push(row.row_id);
            let rowRight = row.right;
            // Chop vertical links of rows
            while (rowRight != row) {
                rowRight.up.down = rowRight.down;
                rowRight.down.up = rowRight.up;
                this.matrix[0][rowRight.column.id].size -= 1;
                rowRight = rowRight.right;
            }
            
            row = row.down;
        }


        this.logs.push({
            action: 'cover',
            column: target.id,
            affectedRows,
            depth: currDepth,
            //matrixState: this.getMatrixSnapshot()
        });
    }
    /**
     * Uncovers a column.
     * @param {Node} target the node whose column will be uncovered :D
     */
    uncover(target, currDepth) {
        const affectedRows = [];
        let uncoveredCol = target.column;

        let row = uncoveredCol.up;
        while (row != uncoveredCol) {
            affectedRows.push(row.row_id)
            let rowLeft = row.left;
            while (rowLeft != row) {
                // Add vertical links back in
                rowLeft.up.down = rowLeft;
                rowLeft.down.up = rowLeft;
                this.matrix[0][rowLeft.column.id].size += 1;
                rowLeft = rowLeft.left;
            }

            row = row.up;
        }
        
        // Add links from neighbors to uncoveredCol back in
        uncoveredCol.left.right = uncoveredCol;
        uncoveredCol.right.left = uncoveredCol;

        this.logs.push({
            action: 'uncover',
            column: target.id,
            affectedRows,
            depth: currDepth,
            //matrixState: this.getMatrixSnapshot()
        });
    }
    /**
     * Backtracking algorithm to find a solution given the cover matrix.
     * @param {Int} k represents the depth of the backtracking search
     */
    search(k) {
        // if (k > 5) {
        //     return;
        // }
        if (this.header == this.header.right) {
            this.results.push([...this.partialSolutions]);
            return;
        }   

        // Select and cover the col with fewest 1s
        let selectedCol = this.selectColumn()
        console.log("Selected column:", selectedCol.id, "size:", selectedCol.size, "depth: ", k);
        this.cover(selectedCol, k);

        let col = selectedCol.down;
        while (col != selectedCol) {
            this.partialSolutions.push(col.row_id);

            console.log("I'm in column ", col.column.id);

            // Cover
            let rowR = col.right;
            while (rowR != col) {
                console.log("covering ", rowR.row_id, " ", rowR.column.id);
                this.cover(rowR, k);
                rowR = rowR.right; 
            }
            // Recurse
            this.search(k+1);

            // Backtrack
            this.partialSolutions.pop();
            
            // Uncover in the opposite direction
            let rowL = col.left;
            while (rowL != col) {
                console.log("uncovering ", rowL.row_id, " ", rowL.column.id);
                this.uncover(rowL, k);
                rowL = rowL.left;
            } 

            col = col.down;
        }
        this.uncover(selectedCol, k);
        return;
        
    }

    solve() {
        this.generateDLLMat();
        this.search(0);
        let solution = this.results.reduce((min, current) => 
            current.length < min.length ? current : min, this.results[0]);
        return solution;
    }
}

let TEST_MATRIX = [
    [1, 0, 0, 1],
    [1, 1, 0, 1],
    [0, 0, 1, 0],
    [1, 0, 0, 0],
    [1, 1, 1, 0]
]
// let dlx = new DLX(TEST_MATRIX);
// // dlx.generateDLLMat();

// let sol = dlx.solve();
// console.log(dlx.results);
