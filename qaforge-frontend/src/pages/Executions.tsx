import { useEffect, useState } from 'react'
import { getTestResults } from '../api/testCases'
import type { TestExecution } from '../api/testCases'

function Executions() {
  const [results, setResults] = useState<TestExecution[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)

  const pageSize = 10

  async function loadResults() {
    setLoading(true)
    setError(null)

    try {
      const data = await getTestResults(page, pageSize)

      setResults(data.items)
      setTotalPages(data.total_pages)
    } catch (error) {
      setError('Failed to load test results')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadResults()
  }, [page])

  return (
    <main className="page executions-page">
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

          <div className="pagination">
            <button
              className="pagination-button"
              onClick={() => setPage(1)}
              disabled={page === 1 || loading}
            >
              First
            </button>

            <button
              className="pagination-button"
              onClick={() => setPage((currentPage) => currentPage - 1)}
              disabled={page === 1 || loading}
            >
              Previous
            </button>

            <div className="pagination-pages">
              {Array.from({ length: totalPages }, (_, index) => index + 1).map(
                (pageNumber) => (
                  <button
                    key={pageNumber}
                    className={`pagination-page ${
                      page === pageNumber ? 'active' : ''
                    }`}
                    onClick={() => setPage(pageNumber)}
                    disabled={loading}
                  >
                    {pageNumber}
                  </button>
                )
              )}
            </div>

            <button
              className="pagination-button"
              onClick={() => setPage((currentPage) => currentPage + 1)}
              disabled={page === totalPages || loading}
            >
              Next
            </button>

            <button
              className="pagination-button"
              onClick={() => setPage(totalPages)}
              disabled={page === totalPages || loading}
            >
              Last
            </button>
          </div>
        </div>
      )}
    </main>
  )
}

export default Executions