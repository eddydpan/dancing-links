<App>
  <div className="flex flex-row h-screen w-screen">
    <MatrixView className="w-1/2" />   // ← Left side: 2D matrix
    <div className="flex flex-col w-1/2">
      <LinkedListView />               // ← Right side: DLX node grid
      <Controls />
      <LogTimeline />
    </div>
  </div>
</App>
