// src/components/MatrixView.jsx
import React from 'react';

function LeftParenthesis() {
  return (
    <svg viewBox="0 0 50 200" className="h-full w-4" xmlns="http://www.w3.org/2000/svg">
      <path d="M40,10 Q10,100 40,190" stroke="black" fill="none" strokeWidth="4" />
    </svg>
  );
}
function RightParenthesis() {
  return (
    <svg viewBox="0 0 50 200" className="h-full w-4" xmlns="http://www.w3.org/2000/svg">
      <path d="M10,10 Q40,100 10,190" stroke="black" fill="none" strokeWidth="4" />
    </svg>
  );
}

function MatrixCell( {cell, className} ) {
  return <div className={className}>
    {cell}
  </div>
}

export default function MatrixView( {matrix, setMatrix} ) {

  /* TODO: 
  * implement editCell to JUST EDIT A CELL rather than update the entire matrix
  * Maybe this means making each cell of the matrix a state that can be
  * independently updated.
  */ 
  function editCell(row, col) {
    tempMat = matrix;
    tempMat[row][col] += 1 % 2;
    setMatrix(tempMat) 
  }
  return (
    <div className="flex flex-col items-center justify-center">
      <div className="w-full flex justify-center">
        <h1 className="text-2xl font-bold">Exact Cover Problem</h1>
      </div>
      <div className="flex items-stretch mt-4">
        {/* Left parenthesis */}
        <div className="flex items-center">
          <LeftParenthesis />
        </div>

        {/* Matrix grid */}
        <div
          className="grid gap-1 mx-2"
          style={{
            gridTemplateColumns: `repeat(${matrix[0].length}, minmax(0, 1fr))`,
          }}
        >
          {matrix.map((row, rowIndex) =>
            row.map((cell, colIndex) => (
              <MatrixCell
                key={`${rowIndex}-${colIndex}`}
                cell={cell} // TODO: update this to be dynamic: onClick()
                className="w-12 h-12 flex items-center justify-center text-xl"
              />
            ))
          )}
        </div>

        {/* Right parenthesis */}
        <div className="flex items-center">
          <RightParenthesis />
        </div>
      </div>
    </div>
  );
}



// Displays the DLX matrix, animations for cover/uncover

/* Render the array as a table/grid with tailwind */

/* put in a 1 or 0 in each cell */

/* Allow for highlighting cells + rows + columns */


