class Node {
    constructor() {
        this.left = this;
        this.right = this;
        this.up = this;
        this.down = this;
        this.column = this;
        this.rowId = 0;
    }
}
  
class ColumnHeader extends Node {
    constructor(id) {
        super();
        this.id = id;
        this.size = 0;
    }
}
  
export class DancingLinks {
    constructor(coverMatrix) {
        this.header = new ColumnHeader('root');
        this.coverMatrix = [[...Array(coverMatrix[0].length).fill(0)], ...coverMatrix];
        this.numRows = this.coverMatrix.length;
        this.numCols = this.coverMatrix[0].length;

        this.matrix = Array.from({ length: this.numRows }, () =>
            Array(this.numCols).fill(null)
        );

        this.partialSolution = [];
        this.result = [];

        this.logs = []; // stack to hold action logs
    }
    resetDLLMat() {
        this.matrix = Array.from({ length: this.numRows }, () =>
            Array(this.numCols).fill(null)
        );
    }
    generateDLLMat() {
        // Create column headers
        this.resetDLLMat();

        for (let c = 0; c < this.numCols; c++) {
            const colNode = new ColumnHeader(c);

            colNode.left = this.header.left || this.header;
            colNode.right = this.header;

            if (this.header.left) {
                this.header.left.right = colNode;
            }
            this.header.left = colNode;

            this.matrix[0][c] = colNode;
        }

        // Create and link nodes
        for (let r = 1; r < this.numRows; r++) {
            let refNode = null;

            for (let c = 0; c < this.numCols; c++) {
                if (this.coverMatrix[r][c] === 1) {
                    const newNode = new Node();
                    newNode.column = this.matrix[0][c];

                    // Vertical links
                    newNode.up = newNode.column.up || newNode.column;
                    newNode.down = newNode.column;
                    newNode.column.up && (newNode.column.up.down = newNode);
                    newNode.column.up = newNode;

                    newNode.column.size++;
                    newNode.rowId = r;

                    // Horizontal links
                    if (refNode === null) {
                        refNode = newNode;
                    }
                    newNode.left = refNode.left || refNode;
                    newNode.right = refNode;
                    refNode.left && (refNode.left.right = newNode);
                    refNode.left = newNode;

                    this.matrix[r][c] = newNode;
                }
            }
        }
    }

    getColWithFewestNodes() {
        let head = this.header.right;
        let minCol = head;

        while (head !== this.header) {
        if (head.size < minCol.size) {
            minCol = head;
        }

        head = head.right;
        }

        return minCol;
    }

    cover(targetNode, currDepth) {
        let affectedRows = [];
        const col = targetNode.column;

        col.left.right = col.right;
        col.right.left = col.left;

        let colNode = col.down;
        while (colNode !== col) {
            affectedRows.push(colNode.rowId);
            let rowNode = colNode.right;
            while (rowNode !== colNode) {
                rowNode.up.down = rowNode.down;
                rowNode.down.up = rowNode.up;
                rowNode.column.size--;
                rowNode = rowNode.right;    
            }
            colNode = colNode.down;
        }

        this.logs.push(
        {   
            targetRow: targetNode.rowId,
            targetCol: col.id,
            index: this.logs.length,
            action: 'cover',
            column: targetNode.column.id,
            changes: {
                numChanges: affectedRows.length,
                affectedRows: affectedRows,
            },
            depth: currDepth,
            partialSolution: this.partialSolution,
            //matrixState: this.getMatrixSnapshot()
        });
    }

    uncover(targetNode, currDepth) {
        let affectedRows = [];

        const col = targetNode.column;
        let colNode = col.up;

        while (colNode !== col) {
            affectedRows.push(colNode.rowId);

            let rowNode = colNode.left;
            while (rowNode !== colNode) {
                rowNode.up.down = rowNode;
                rowNode.down.up = rowNode;
                rowNode.column.size++;
                rowNode = rowNode.left;
            }
            colNode = colNode.up;
        }

        col.left.right = col;
        col.right.left = col;

        this.logs.push({
            targetRow: targetNode.rowId,
            targetCol: col.id,
            index: this.logs.length,
            action: 'uncover',
            column: targetNode.column.id,
            changes: {
                numChanges: affectedRows.length,
                affectedRows: affectedRows,
            },
            depth: currDepth,
            partialSolution: this.partialSolution,
            //matrixState: this.getMatrixSnapshot()
        });
    }

    search(k = 0) {
        if (this.header.right === this.header) {
            let solution = [...this.partialSolution]
            this.result.push(solution);
            this.logs.push(
                {
                    action: 'solution',
                    solution: solution,
                }
            )
            return;
        }

        const col = this.getColWithFewestNodes();
        this.cover(col, k);

        let row = col.down;
        while (row !== col) {
            this.partialSolution.push(row.rowId);

            let rightNode = row.right;
            while (rightNode !== row) {
                this.cover(rightNode, k);
                rightNode = rightNode.right;
            }

            this.search(k + 1);
            this.partialSolution.pop();

            let leftNode = row.left;
            while (leftNode !== row) {
                this.uncover(leftNode, k);
                leftNode = leftNode.left;
            }

            row = row.down;
        }

        this.uncover(col, k);
    }

    solve() {
        this.generateDLLMat();
        this.search();
        const final = this.result.reduce((a, b) => (a.length < b.length ? a : b), []);
        console.log(`Final result: ${final}, All solutions:`, this.result);
        return final.length;
    }
}

// // Example usage
// const TEST_COVER_MATRIX = [
// [1, 0, 0, 1],
// [1, 1, 1, 1],
// [0, 1, 1, 0],
// [0, 1, 0, 0],
// [1, 0, 1, 1]
// ];

// const dlx = new DancingLinks(TEST_COVER_MATRIX);
// dlx.solve();
// console.log(dlx.logs)
