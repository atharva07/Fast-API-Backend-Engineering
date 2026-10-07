function Dashboard() {
  return (
    <main className="dashboard">
      <div className="welcome">
        <h1>Welcome to QAForge</h1>
        <p>Test Management & Automation Platform</p>
      </div>

      <div className="stats">
        <div className="stat-card">
          <h3>Projects</h3>
          <p>0</p>
        </div>

        <div className="stat-card">
          <h3>Test Suites</h3>
          <p>0</p>
        </div>

        <div className="stat-card">
          <h3>Test Cases</h3>
          <p>0</p>
        </div>

        <div className="stat-card">
          <h3>Executions</h3>
          <p>0</p>
        </div>
      </div>
    </main>
  )
}

export default Dashboard