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

function MatrixCell({ cell, className, onClick }) {
  return (
    <button className={className} onClick={onClick}>
      {cell}
    </button>
  );
}

export default function MatrixView({ matrix, setMatrix }) {
  // Function to handle cell value toggle
  function toggleCell(row, col) {
    const newMatrix = matrix.map((r, rowIndex) =>
      r.map((c, colIndex) => (rowIndex === row && colIndex === col ? (c === 1 ? 0 : 1) : c))
    );
    setMatrix(newMatrix);
  }

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="w-full flex justify-center">
        <h1 className="text-2xl font-bold">Exact Cover Problem</h1>
        {/*FIXME: delete this*/}
        <h3>{matrix}</h3> 
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
                cell={cell}
                className="w-12 h-12 flex items-center justify-center text-xl"
                onClick={() => toggleCell(rowIndex, colIndex)} // Pass toggle function
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
