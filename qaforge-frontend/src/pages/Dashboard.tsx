import { useEffect, useState } from 'react'
import { getDashboardStats } from '../api/dashboard'
import type { DashboardStats } from '../api/dashboard'

function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  async function loadDashboardStats() {
    setLoading(true)
    setError(null)

    try {
      const data = await getDashboardStats()
      setStats(data)
    } catch (error) {
      setError('Failed to load dashboard statistics')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadDashboardStats()
  }, [])

  return (
    <main className="dashboard">
      <div className="welcome">
        <h1>Welcome to QAForge</h1>
        <p>Test Management & Automation Platform</p>
      </div>

      {error && (
        <p className="form-error">
          {error}
        </p>
      )}

      <div className="stats">
        <div className="stat-card">
          <h3>Projects</h3>
          <p>{loading ? '—' : stats?.projects ?? 0}</p>
        </div>

        <div className="stat-card">
          <h3>Test Suites</h3>
          <p>{loading ? '—' : stats?.test_suites ?? 0}</p>
        </div>

        <div className="stat-card">
          <h3>Test Cases</h3>
          <p>{loading ? '—' : stats?.test_cases ?? 0}</p>
        </div>

        <div className="stat-card">
          <h3>Executions</h3>
          <p>{loading ? '—' : stats?.executions ?? 0}</p>
        </div>
      </div>
    </main>
  )
}

export default Dashboard