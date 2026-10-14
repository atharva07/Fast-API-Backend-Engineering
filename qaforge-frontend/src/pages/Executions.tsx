import { useEffect, useState } from 'react'
import { getTestResults } from '../api/testCases'
import type { TestExecution } from '../api/testCases'

function Executions() {
  const [results, setResults] = useState<TestExecution[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  async function loadResults() {
    setLoading(true)
    setError(null)

    try {
      const data = await getTestResults()
      setResults(data)
    } catch (error) {
      setError('Failed to load test results')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadResults()
  }, [])

  return (
    <main className="page">
      <div className="page-header">
        <div>
          <h1>Test Results</h1>
          <p>View the history of test case executions.</p>
        </div>

        <button
          className="primary-button"
          onClick={loadResults}
          disabled={loading}
        >
          {loading ? 'Refreshing...' : 'Refresh'}
        </button>
      </div>

      {error && (
        <p className="form-error">
          {error}
        </p>
      )}

      {!loading && !error && (
        <div className="project-table-container">
          <table className="project-table">
            <thead>
              <tr>
                <th>Result ID</th>
                <th>Test Case ID</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              {results.map((result) => (
                <tr key={result.id}>
                  <td>{result.id}</td>
                  <td>{result.test_case_id}</td>
                  <td>
                    <span
                      className={`result-status ${result.status.toLowerCase()}`}
                    >
                      {result.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </main>
  )
}

export default Executions