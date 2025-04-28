import MatrixView from './components/MatrixView.jsx';
import LinkedListView from './components/DLLView.jsx';
import Controls from './components/Controls.jsx';
import LogTimeline from './components/LogTimeline.jsx';
import { useState } from 'react';

function App() {
  const testMat = [
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0],
  ];


  const [matrix, setMatrix] = useState(testMat);
  
  return (
    <div className="flex flex-col h-screen w-screen">
      <div className="flex flex-row h-1/6 bg-gray-200">
        <div className="flex-1 bg-blue-100 flex items-center justify-center">
          <Controls />
        </div>
        <div className="flex-1 bg-green-100 flex items-center justify-center">
          <LogTimeline />
        </div>
      </div>
      <div className="flex flex-row flex-1">
        <div className="w-1/2 bg-yellow-100 flex items-center justify-center">
          <MatrixView matrix={matrix} setMatrix={setMatrix}/>
        </div>
        <div className="w-1/2 bg-red-100 flex items-center justify-center">
          <LinkedListView />
        </div>
      </div>
    </div>
  );
}

export default App;
