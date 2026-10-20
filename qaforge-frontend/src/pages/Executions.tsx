import { useEffect, useState } from 'react'
import { getTestResults } from '../api/testCases'
import type { TestExecution } from '../api/testCases'

function Executions() {
  const [results, setResults] = useState<TestExecution[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)

  // Values currently entered/selected in the filter form
  const [testCaseId, setTestCaseId] = useState('')
  const [status, setStatus] = useState('')

  // Values actually applied to the API request
  const [appliedTestCaseId, setAppliedTestCaseId] = useState('')
  const [appliedStatus, setAppliedStatus] = useState('')

  const pageSize = 10

  async function loadResults() {
    setLoading(true)
    setError(null)

    try {
      const data = await getTestResults(
        page,
        pageSize,
        appliedTestCaseId
          ? Number(appliedTestCaseId)
          : undefined,
        appliedStatus || undefined
      )

      setResults(data.items)
      setTotalPages(data.total_pages)
    } catch (error) {
      setError('Failed to load test results')
    } finally {
      setLoading(false)
    }
  }

  // Load results whenever the page or applied filters change
  useEffect(() => {
    loadResults()
  }, [page, appliedTestCaseId, appliedStatus])

  function handleTestCaseIdChange(value: string) {
    setTestCaseId(value)
  }

  function handleStatusChange(value: string) {
    setStatus(value)
  }

  function handleSearch() {
    setAppliedTestCaseId(testCaseId)
    setAppliedStatus(status)
    setPage(1)
  }

  function handleClearFilters() {
    setTestCaseId('')
    setStatus('')

    setAppliedTestCaseId('')
    setAppliedStatus('')

    setPage(1)
  }

  return (
    <main className="page executions-page">

      {/* Page Header */}

      <div className="page-header">
        <div>
          <h1>Test Results</h1>

          <p>
            View the history of test case executions.
          </p>
        </div>

        <button
          className="primary-button"
          onClick={loadResults}
          disabled={loading}
        >
          {loading ? 'Refreshing...' : 'Refresh'}
        </button>
      </div>


      {/* Filters */}

      <div className="executions-filters">

        <div className="filter-field">
          <label htmlFor="test-case-filter">
            Test Case ID
          </label>

          <input
            id="test-case-filter"
            type="number"
            min="1"
            placeholder="Enter test case ID"
            value={testCaseId}
            onChange={(event) =>
              handleTestCaseIdChange(
                event.target.value
              )
            }
          />
        </div>


        <div className="filter-field">
          <label htmlFor="status-filter">
            Status
          </label>

          <select
            id="status-filter"
            value={status}
            onChange={(event) =>
              handleStatusChange(
                event.target.value
              )
            }
          >
            <option value="">
              All statuses
            </option>

            <option value="RUNNING">
              Running
            </option>

            <option value="PASSED">
              Passed
            </option>

            <option value="FAILED">
              Failed
            </option>
          </select>
        </div>


        {/* Search */}

        <button
          className="filter-search-button"
          onClick={handleSearch}
          disabled={loading}
        >
          Search
        </button>


        {/* Clear */}

        <button
          className="filter-clear-button"
          onClick={handleClearFilters}
          disabled={
            !testCaseId &&
            !status &&
            !appliedTestCaseId &&
            !appliedStatus
          }
        >
          Clear
        </button>

      </div>


      {/* Error */}

      {error && (
        <p className="form-error">
          {error}
        </p>
      )}


      {/* Results */}

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

              {results.length === 0 ? (

                <tr>
                  <td
                    colSpan={3}
                    className="empty-state"
                  >
                    No test results found.
                  </td>
                </tr>

              ) : (

                results.map((result) => (

                  <tr key={result.id}>

                    <td>
                      {result.id}
                    </td>

                    <td>
                      {result.test_case_id}
                    </td>

                    <td>
                      <span
                        className={`result-status ${result.status.toLowerCase()}`}
                      >
                        {result.status}
                      </span>
                    </td>

                  </tr>

                ))

              )}

            </tbody>

          </table>


          {/* Pagination */}

          {results.length > 0 && (
            <div className="pagination">

              <button
                className="pagination-button"
                onClick={() => setPage(1)}
                disabled={
                  page === 1 ||
                  loading
                }
              >
                First
              </button>


              <button
                className="pagination-button"
                onClick={() =>
                  setPage(
                    (currentPage) =>
                      currentPage - 1
                  )
                }
                disabled={
                  page === 1 ||
                  loading
                }
              >
                Previous
              </button>


              <div className="pagination-pages">

                {Array.from(
                  {
                    length: totalPages,
                  },
                  (_, index) =>
                    index + 1
                ).map(
                  (pageNumber) => (

                    <button
                      key={pageNumber}
                      className={`pagination-page ${
                        page === pageNumber
                          ? 'active'
                          : ''
                      }`}
                      onClick={() =>
                        setPage(pageNumber)
                      }
                      disabled={loading}
                    >
                      {pageNumber}
                    </button>

                  )
                )}

              </div>


              <button
                className="pagination-button"
                onClick={() =>
                  setPage(
                    (currentPage) =>
                      currentPage + 1
                  )
                }
                disabled={
                  page === totalPages ||
                  loading
                }
              >
                Next
              </button>


              <button
                className="pagination-button"
                onClick={() =>
                  setPage(totalPages)
                }
                disabled={
                  page === totalPages ||
                  loading
                }
              >
                Last
              </button>

            </div>
          )}

        </div>
      )}

    </main>
  )
}

export default Executions