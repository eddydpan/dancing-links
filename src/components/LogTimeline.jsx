function LogTimeline( {logs, logIndex} ) {
    let actions = logs.map((log) => ([log.action, log.column, log.affectedRows]))

    return (
        <div>
            <h1>Log Timeline View</h1>
            <h2>Step Number: {logIndex}</h2>
            {/* <h2>{actions}</h2> */}
        </div>
    );
}

export default LogTimeline;
