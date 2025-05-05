// Start/stop/next/prev playback, select problem type
import { useState } from 'react';
import { DancingLinks } from '../refactored.js';

const preset1 = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
  ];

const preset2 = [
    [0, 0, 0, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0],
];
const preset3 = [
    [0, 0, 1, 0, 1, 1, 0],
    [1, 0, 0, 1, 0, 0, 1],
    [0, 1, 1, 0, 0, 1, 0],
    [1, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 1, 0, 1],
];

function LoadPreset( {name, presetMat, setPreset } ) {
    return (
        <button 
            className="editMat" 
            onClick={() => setPreset(presetMat)}
        >
            {name}
        </button>
    );
}

/**
 * 
 * @param {*} logs 
 * @param {*} iter 
 * @returns 
 */
function StepButton( {logs, logIndex, setLogIndex} ) {
    return (
        <button className="step" onClick={
            () => setLogIndex(Math.min(logIndex + 1, logs.length - 1))}
        >
            Step
        </button>
    );
}

function BackButton( {logIndex, setLogIndex} ) {
    return (
        <button className="back"onClick={
            () => setLogIndex(Math.max(logIndex-1, -1))}
        >
            Back
        </button>
    );
}

function GenerateDLLButton( {matrix, dlx, setDLX, setLogIndex} ) {

    function generateLinks() {
        setDLX(new DancingLinks(matrix));
        setLogIndex(-1);
        dlx.generateDLLMat();
        console.log("Generating DLL Links");
    }
    return (
        <button 
            className="generateMat"
            onClick={() => generateLinks()}
        >
            Generate Nodes
        </button>
    )
}

/**
 * Updates the logs state with the DLX logs
 * @param {*} param0 
 * @returns 
 */
function PlayButton(props) {
    // TODO: implement running search() from DLX
    // props.setLogs([]);
    return (
        <button onClick={props.togglePlay}>
            {props.isRunning ? "Pause" : "Play"}
        </button>
    );
}

function Controls( {logs, setLogs, matrix, setMatrix, dlx, setDLX, logIndex, setLogIndex} ) {
    const [isRunning, setIsRunning] = useState(false);
    let solution;

    function togglePlay() {
        setIsRunning(!isRunning);
        
        dlx.generateDLLMat();
        solution = dlx.search();
        setLogs(dlx.logs);
        console.log(solution);

    }

    return (
        <div>
            <h1>Controls View</h1>
            <div className="button">
                <GenerateDLLButton  matrix={matrix} 
                                    dlx={dlx} 
                                    setDLX={setDLX} 
                                    setLogIndex={setLogIndex}
                />
            </div>
            <div
                className="button"
                style={{ backgroundColor: isRunning ? 'red' : 'green' }}
            >
                <PlayButton isRunning={isRunning} 
                            togglePlay={togglePlay}
                            setLogs={setLogs}
                />
            </div>
            
            <div className="button">
                <StepButton logs={logs}
                            logIndex={logIndex}
                            setLogIndex={setLogIndex}
                />
            </div>
            
            <div className="button">
                <BackButton logIndex={logIndex}
                            setLogIndex={setLogIndex}
                />
            </div>

            <div className="flex flex-row items-center justify-center">
                <div className="button">
                    <LoadPreset name="Preset 1: Demo" presetMat={preset1} setPreset={setMatrix} />
                </div>
                <div className="button">
                    <LoadPreset name="Preset 2: Sudoku" presetMat={preset2} setPreset={setMatrix} />
                </div>
                <div className="button">
                    <LoadPreset name="Preset 3: Exact Cover Problem" presetMat={preset3} setPreset={setMatrix} />
                </div>
            </div>
        </div>
    );
}

export default Controls;
