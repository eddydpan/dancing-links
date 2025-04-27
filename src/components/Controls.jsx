// Start/stop/next/prev playback, select problem type
import { useState } from 'react';

function EditMatButton() {
    return (
        <button className="editMat">Edit Matrix</button>
    );
}

function StepButton() {
    return (
        <button className="step">Step</button>
    );
}

function BackButton() {
    return (
        <button className="back">Back</button>
    );
}

function PlayButton({ isRunning, toggleRunning }) {
    return (
        <button onClick={toggleRunning}>
            {isRunning ? "Pause" : "Play"}
        </button>
    );
}

function Controls() {
    const [isRunning, setIsRunning] = useState(false);

    function toggleRunning() {
        setIsRunning(!isRunning);
    }

    return (
        <div>
            <h1>Controls View</h1>
            <div
                className="button"
                style={{ backgroundColor: isRunning ? 'red' : 'green' }}
            >
                <PlayButton isRunning={isRunning} toggleRunning={toggleRunning} />
            </div>
            
            <div className="button">
                <StepButton />
            </div>
            
            <div className="button">
                <BackButton />
            </div>

            <div className="button">
                <EditMatButton />
            </div>
            
        </div>
    );
}

export default Controls;
