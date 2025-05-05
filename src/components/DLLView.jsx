import React, { useState, useEffect, useMemo } from 'react';
import { DancingLinks } from '../refactored.js'

const NODE_OFFSET = 50;
const NODE_SIZE = 50;
const OFFSET = 100;
/**
 * Component for a DLLNode
 * 50px * 50px 
 * @param {*} param0 
 * @returns 
 */
function DLLNode( {id, xPos, yPos} ) {

    return (
    <div 
        className="w-12 h-12 flex border border-gray-500 items-center justify-center text-xl absolute"
        style={{ 
            left: `${xPos}px`, top: `${yPos}px`, 
            backgroundColor: id[0] === 0 ? 'lightblue' : 'white' 
            }}>
        {id[0] === 0 ? `H${id[1]}`: `${id[0]}, ${id[1]}` }
    </div>
    );
}
/**
 * Finds the absolute positions of all the nodes of an exact cover matrix and
 * stores them in an array.
 * 
 * Note: dlx must have already had generateDLLMat() called on it once.
 * @param {DancingLinks} dlx a DancingLinks object that stores the exact cover matrix and
 *                dimensions.
 * @param {Int} frameWidth the width of the div containing the grid.
 * @param {Int} frameHeight the height of the div containing the grid.
 * @return An array of objects containing the x and y position of the nodes.
 */
function findNodePos(dlx, frameWidth, frameHeight) {

    // Initialize dimensions and ranges
    let numRows = dlx.numRows; let numCols = dlx.numCols;
    let rowRange = [...Array(numRows).keys()]; // 0 1 2...
    let colRange = [...Array(numCols).keys()];

    // Find row positions and col positions
    let rowPos = rowRange.map(i => (frameHeight/2) +((NODE_OFFSET + NODE_SIZE) * (i - ((numRows-1)/ 2))));
    let colPos = colRange.map(j => (frameWidth/2) + ((NODE_OFFSET + NODE_SIZE) * (j - ((numCols-1)/ 2))));

    // Init posMat to store the absolute positions of each cell in the grid
    let posMat = Array.from({ length: numRows }, () =>
        Array(numCols).fill([])
    );

    // Populate posMat with the positions of each potential node
    for (let r = 0; r < numRows; r++) {
        for (let c = 0; c < numCols; c++) {
            posMat[r][c] = ([Math.round(rowPos[r]), Math.round(colPos[c])]);
        }
    }
    
    return posMat;
}
/**
 * Takes in two nodes' indices (r1, c1) and (r2, c2), and draws an arrow from
 * n1 to n2.
 * @param {*} param0 
 * @returns 
 */
function SVGArrow({x1, y1, x2, y2}) {
    const strokeWidth = 2;
    const markerHeight = 7;
    const markerWidth = 9;
    
    return (
        <svg className="absolute left-0 top-0" width="100%" height="100%" style={{ pointerEvents: 'none', zIndex: 2 }}>
            <line 
                x1={x1} 
                y1={y1} 
                x2={x2} 
                y2={y2}
                stroke="black" strokeWidth={strokeWidth}
                markerEnd="url(#arrowhead)" 
            />
            <defs>
                <marker id="arrowhead" 
                        markerWidth={markerWidth} 
                        markerHeight={markerHeight}
                        refX="0" refY="2.5" orient="auto">
                    <polygon points="0 0, 10 2.5, 0 5" fill="black" />
                </marker>
            </defs>
        </svg>
    );
}

/**
 * Finds the (x1,y1) and (x2,y2) absolute positions for a <SVGArrow /> 
 * component.
 * 
 * This uses a lot of hard-coded constants to ensure the arrows are placed at
 * the proper absolute positions relative to each of the nodes. Each node's
 * pointers look a bit like this:
 * 
 *                |
 *           -- [    ]
 *              [    ] --
 *                 |
 * @param {Int[][]} posMat the position matrix for each of the nodes' poses.
 * @param {Int} r1 row index of n1 to draw the arrow from.
 * @param {Int} c1 column index of n1 to draw the arrow from.
 * 
 * @param {Int} r2 row index of n2 to draw the arrow to.
 * @param {Int} c2 column index of n2 to draw the arrow to.
 * @param {String} dir a String representing the direction. Either "up",
 *                     "down", "left", or "right".
 * @returns {Int32Array} the positions of the arrows stored as [x1, y1, x2, y2]
 */
function findArrowPos(posMat, r1, c1, r2, c2, dir) {
    // console.log("------- New --------");
    // console.log("r1c1: ", r1, c1, "r2c2: ", r2, c2);

    let [y1, x1] = posMat[r1][c1];
    let [y2, x2] = posMat[r2][c2];
    let [x1Mod, y1Mod, x2Mod, y2Mod] = [0, 0, 0, 0];

    // Helper for wrap-around detection
    const isWrapAround = () => {
        if (dir === "up") return r2 > r1;
        if (dir === "down") return r2 < r1;
        if (dir === "left") return c2 > c1;
        if (dir === "right") return c2 < c1;
        return false;
    };

    const wrapped = isWrapAround();

    /* Right Arrow */
    if (dir === 'right') {
        if (wrapped) {
            // Custom wrap-around offset for right
            x1Mod = 1+47; y1Mod = 25+18;
            x2Mod = -17 + 100*(posMat[0].length-c2); y2Mod = 25+18;
        } else {
            x1Mod = 1 + 47;
            y1Mod = 25 + 18;
            x2Mod = -17;
            y2Mod = 25 + 18;
        }
    }

    /* Left Arrow */
    else if (dir === 'left') {
        if (wrapped) {
            x1Mod = 2; y1Mod = 25+30;
            x2Mod = -20-100*c2; y2Mod = 25+30;
        } else {
            x1Mod = 2;
            y1Mod = 25 + 30;
            x2Mod = 20 + 47;
            y2Mod = 25 + 30;
        }
    }

    /* Down Arrow */
    else if (dir === 'down') {
        if (wrapped) {
            x1Mod = 30; y1Mod = 73;
            x2Mod = 30; y2Mod = (posMat.length - r2)*100;
        } else {
            x1Mod = 2 + 30;
            x2Mod = 2 + 30;
            y1Mod = 25 + 47;
            y2Mod = 7;
        }
    }

    /* Up Arrow */
    else if (dir === 'up') {
        if (wrapped) {
            x1Mod = 2+18; y1Mod = 26;
            x2Mod = 2+18; y2Mod = -r2*100;
        } else {
            x1Mod = 2 + 18;
            x2Mod = 2 + 18;
            y1Mod = 26;
            y2Mod = 90;
        }
    }
    // console.log("Find Arrow Pos: ", [x1 + x1Mod, y1 + y1Mod, x2 + x2Mod, y2 + y2Mod], " dir: ", dir, " wrapped: ", wrapped);
    
    return [x1 + x1Mod, y1 + y1Mod, x2 + x2Mod, y2 + y2Mod];
}


/**
 * Creates a highlight component from index (r1,c1) to (r2,c2).
 * @param {*} posMat 
 * @param {*} r1 
 * @param {*} c1 
 * @param {*} r2 
 * @param {*} c2 
 * @param {String} color
 * @returns 
 */
function Highlight( {posMat, r1, c1, r2, c2, color} ) {
    const [y1, x1] = posMat[r1][c1];
    const [y2, x2] = posMat[r2][c2];

    const top = Math.min(y1, y2);
    const left = Math.min(x1, x2);
    const width = Math.abs(x2 - x1) + NODE_SIZE + 30;
    const height = Math.abs(y2 - y1) + NODE_SIZE + 30;

    return (
        <div
            key={`highlight-${r1}-${c1}-${r2}-${c2}`}
            className={`absolute bg-${color}-300 opacity-50`}
            style={{
                top: `${top}px`,
                left: `${left}px`,
                width: `${width}px`,
                height: `${height}px`,
                zIndex: 2,
            }}
        />
    );
}


function applyLogsToDLX(clonedDLX, posMat, logIndex, logs, setSolution, highlights) {
    highlights = [];
    
    for (let i = 0; i <= logIndex; i++) {
        const currLog = logs[i];
        
        switch (currLog.action) {
            case 'cover':
                console.log(`Applying ${currLog.action} on row ${currLog.targetRow}, col ${currLog.targetCol}`);
                clonedDLX.cover(clonedDLX.matrix[currLog.targetRow][currLog.targetCol]);
                break;
            case 'uncover':
                console.log(`Applying ${currLog.action} on row ${currLog.targetRow}, col ${currLog.targetCol}`);
                clonedDLX.uncover(clonedDLX.matrix[currLog.targetRow][currLog.targetCol]);
                break;

            case 'solution':
                setSolution(currLog.solution)
                console.log("Solution: ", currLog.solution);
                break;
            
            case 'select_col':
                console.log("Highlighting: ", '(', r1, c1, ')', ', (', r2, c2, ')');
                highlights.push(<Highlight
                    posMat={posMat}
                    r1={0}
                    c1={currLog.col}
                    r2={clonedDLX.numRows}
                    c2={currLog.col}
                    color="yellow"
                />)
                break;
            case 'select_row':
                break;
            case 'select_node':
                break;
            default:
                console.warn(`Unknown log type: ${currLog.action}`);
                break;
        }
    }
}



/** 
 * Displays the "dancing links" of the DLX algorithm in DLL view.
 * 
 * @param {Int[][]} matrix the exact cover matrix
 * @param {JSON} currIter a JSON object representing the current iteration
 * @returns 
 */
export default function LinkedListView( {dlx, matrix, logs, logIndex} ) {
    /*
     * Nodes are approximately ~50px in width and length
     */

    if (!logs || logs.length === 0) return <div>No logs yet. Press the Generate Mat button, then the Play button.</div>;
    const frameHeight = 5 * Math.round(window.innerHeight / 6) - OFFSET; // DLLView div height
    const frameWidth = window.innerWidth / 2 - OFFSET; // DLLView div width

    /* Clone dlx to make changes on in this LinkedListView */
    const clonedDLX = useMemo(() => {
        const dlx = new DancingLinks(matrix);
        dlx.generateDLLMat();
        return dlx;
    }, [matrix]);

    const [solution, setSolution] = useState([]);
    let posMat = findNodePos(clonedDLX, frameWidth, frameHeight);

    useEffect(() => {
        applyLogsToDLX(clonedDLX, posMat, logIndex, logs, setSolution);
    }, [posMat, logIndex, logs, clonedDLX]);

    
    
    
    // const arrows = [];
    


    // clonedDLX.matrix.forEach((row, rowIndex) => {
    //     row.forEach((node, colIndex) => {
    //         if (!node) return;

    //         const directions = {
    //             right: node.right,
    //             left: node.left,
    //             up: node.up,
    //             down: node.down,
    //         };

    //         for (const [dir, neighbor] of Object.entries(directions)) {
    //             if (neighbor && neighbor !== node) {
    //                 // Skip the root node
    //                 if (neighbor.column.id === "root") {
    //                     // console.log("Logged at root");
    //                     continue;
    //                 }
    //                 let [x1, y1, x2, y2] = findArrowPos(posMat, rowIndex, colIndex, neighbor.rowId, neighbor.column.id, dir);
    //                 arrows.push(
    //                     <SVGArrow
    //                         key={`arrow-${rowIndex}-${colIndex}-${dir}`}
    //                         x1={x1}
    //                         y1={y1}
    //                         x2={x2}
    //                         y2={y2}
    //                     />
    //                 );
    //             }
    //         }
    //     });
    // });

    let root = clonedDLX.header; // The root header node
    let arrows = [];
    let nodes = [];

    let column = root.right;
    while (column !== root) {
        // Traverse down each column
        let rowNode = column.down;
        while (rowNode !== column) {
            // Save node info for DLLNode rendering
            const row = rowNode.rowId;
            const col = rowNode.column.id;
            const pos = posMat[row][col];

            nodes.push(
                <DLLNode
                    key={`node-${row}-${col}`}
                    id={[row, col]}
                    xPos={pos[1]}
                    yPos={pos[0]}
                />
            );

            // Traverse neighbors to draw arrows
            const directions = {
                right: rowNode.right,
                left: rowNode.left,
                up: rowNode.up,
                down: rowNode.down,
            };

            for (const [dir, neighbor] of Object.entries(directions)) {
                if (neighbor && neighbor !== rowNode && neighbor.column.id !== "root") {
                    const [x1, y1, x2, y2] = findArrowPos(
                        posMat,
                        row,
                        col,
                        neighbor.rowId,
                        neighbor.column.id,
                        dir
                    );
                    arrows.push(
                        <SVGArrow
                            key={`arrow-${row}-${col}-${dir}`}
                            x1={x1}
                            y1={y1}
                            x2={x2}
                            y2={y2}
                        />
                    );
                }
            }

            rowNode = rowNode.down;
        }

        column = column.right;
    }

   
    return (
        <div className='relative mx-auto'>
            <h1>Linked List View {frameWidth} {frameHeight}</h1>
            
            <div 
                className='relative mx-auto' 
                style={
                    { 
                        width: `${frameWidth}px`,
                        height: `${frameHeight}px`,
                        border: '1px solid black' 
                    }
                }
            >   
                {/* {posMat.flatMap((row, rowIndex) =>
                    row.map((cell, colIndex) => (
                        clonedDLX.matrix[rowIndex][colIndex] !== null && (
                            <DLLNode 
                                key={`${rowIndex}-${colIndex}`}
                                id={[rowIndex, colIndex]}
                                xPos={cell[1]} // x position
                                yPos={cell[0]} // y position
                            />
                        )
                    ))
                )} */}
                {nodes}
                <div style={{ position: 'absolute', top: 0, left: '50%', transform: 'translateX(-50%)', zIndex: 3 }}>
                    Solutions: {solution.join(', ')}
                </div>
            </div>

            {/* SVGArrows */}
            {arrows}
        </div>
    );
}

