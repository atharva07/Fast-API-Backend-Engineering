import { useEffect, useState } from 'react'

import {
  getProjects,
  type Project,
} from '../api/projects'

import {
  getTestSuites,
  type TestSuite,
} from '../api/testSuites'

import {
  getTestCases,
  createTestCase,
  updateTestCase,
  deleteTestCase,
  executeTestCase,
  type TestCase,
  type TestExecution,
} from '../api/testCases'

function TestCases() {
  // Projects
  const [projects, setProjects] = useState<Project[]>([])
  const [selectedProjectId, setSelectedProjectId] =
    useState<number | null>(null)

  // Test Suites
  const [testSuites, setTestSuites] = useState<TestSuite[]>([])
  const [selectedSuiteId, setSelectedSuiteId] =
    useState<number | null>(null)

  // Test Cases
  const [testCases, setTestCases] = useState<TestCase[]>([])

  // Loading
  const [loadingProjects, setLoadingProjects] = useState(true)
  const [loadingSuites, setLoadingSuites] = useState(false)
  const [loadingTestCases, setLoadingTestCases] = useState(false)

  // Error
  const [error, setError] = useState<string | null>(null)

  const [showCreateModal, setShowCreateModal] = useState(false)
  const [editingTestCase, setEditingTestCase] = useState<TestCase | null>(null)

  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [priority, setPriority] = useState('MEDIUM')

  const [creating, setCreating] = useState(false)
  const [createError, setCreateError] = useState<string | null>(null)

  const [executingTestCaseId, setExecutingTestCaseId] =
    useState<number | null>(null)

  const [execution, setExecution] =
    useState<TestExecution | null>(null)

  const [executionError, setExecutionError] =
    useState<string | null>(null)


  async function handleCreateTestCase(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault()

    if (selectedSuiteId === null) {
      setCreateError('Please select a test suite')
      return
    }

    setCreateError(null)
    setCreating(true)

    try {
      await createTestCase(selectedSuiteId, {
        name,
        description,
        priority,
      })

      setShowCreateModal(false)

      setName('')
      setDescription('')
      setPriority('MEDIUM')

      const suiteId = selectedSuiteId

      const data = await getTestCases(suiteId)

      setTestCases(data)

    } catch (error) {
      setCreateError('Failed to create test case')
    } finally {
      setCreating(false)
    }
  }

  async function handleEditTestCase(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault()

    if (!editingTestCase) {
      return
    }

    setCreateError(null)
    setCreating(true)

    try {
      await updateTestCase(editingTestCase.id, {
        name,
        description,
        priority,
      })

      setShowCreateModal(false)
      setEditingTestCase(null)

      setName('')
      setDescription('')
      setPriority('MEDIUM')

      if (selectedSuiteId !== null) {
        const suiteId = selectedSuiteId

        const data = await getTestCases(suiteId)

        setTestCases(data)
      }

    } catch (error) {
      setCreateError('Failed to update test case')
    } finally {
      setCreating(false)
    }
  }

  async function handleDeleteTestCase(testCase: TestCase) {
    const confirmed = window.confirm(
      `Are you sure you want to delete "${testCase.name}"?`
    )

    if (!confirmed) {
      return
    }

    try {
      await deleteTestCase(testCase.id)

      if (selectedSuiteId !== null) {
        const suiteId = selectedSuiteId

        const data = await getTestCases(suiteId)

        setTestCases(data)
      }

    } catch (error) {
      setError('Failed to delete test case')
    }
  }

  async function handleExecuteTestCase(
    testCase: TestCase
  ) {
    setExecutingTestCaseId(testCase.id)
    setExecutionError(null)
    setExecution(null)

    try {
      const result = await executeTestCase(testCase.id)

      setExecution(result)

    } catch (error) {
      setExecutionError(
        'Failed to execute test case'
      )
    } finally {
      setExecutingTestCaseId(null)
    }
  }

  // Load Projects
  useEffect(() => {
    async function loadProjects() {
      try {
        const data = await getProjects()

        setProjects(data)

        if (data.length > 0) {
          setSelectedProjectId(data[0].id)
        }

      } catch (error) {
        setError('Failed to load projects')
      } finally {
        setLoadingProjects(false)
      }
    }

    loadProjects()
  }, [])


  // Load Test Suites when Project changes
  useEffect(() => {
    if (selectedProjectId === null) {
      return
    }

    const projectId = selectedProjectId

    async function loadTestSuites() {
      setLoadingSuites(true)
      setError(null)

      try {
        const data = await getTestSuites(projectId)

        setTestSuites(data)

        if (data.length > 0) {
          setSelectedSuiteId(data[0].id)
        } else {
          setSelectedSuiteId(null)
          setTestCases([])
        }

      } catch (error) {
        setError('Failed to load test suites')
      } finally {
        setLoadingSuites(false)
      }
    }

    loadTestSuites()
  }, [selectedProjectId])


  // Load Test Cases when Suite changes
  useEffect(() => {
    if (selectedSuiteId === null) {
      return
    }

    const suiteId = selectedSuiteId

    async function loadTestCases() {
      setLoadingTestCases(true)
      setError(null)

      try {
        const data = await getTestCases(suiteId)

        setTestCases(data)

      } catch (error) {
        setError('Failed to load test cases')
      } finally {
        setLoadingTestCases(false)
      }
    }

    loadTestCases()
  }, [selectedSuiteId])


  // Loading Projects
  if (loadingProjects) {
    return (
      <main className="dashboard">
        <h1>Test Cases</h1>
        <p>Loading projects...</p>
      </main>
    )
  }


  // Error
  if (error) {
    return (
      <main className="dashboard">
        <h1>Test Cases</h1>
        <p>{error}</p>
      </main>
    )
  }


  return (
    <main className="dashboard">

      {/* Page Header */}

      <div className="page-header">
        <div>
          <h1>Test Cases</h1>
          <p>
            Manage test cases for your test suites.
          </p>
        </div>

        <button
          onClick={() => {
            setName('')
            setDescription('')
            setPriority('MEDIUM')
            setCreateError(null)
            setShowCreateModal(true)
            setEditingTestCase(null)
          }}
          disabled={selectedSuiteId === null}
        >
          + Create Test Case
        </button>

      </div>


      {/* Project Selector */}

      <div className="form-group">

        <label>
          Project
        </label>

        <select
          value={selectedProjectId ?? ''}
          onChange={(event) => {
            const projectId = Number(event.target.value)

            setSelectedProjectId(projectId)

            // Clear dependent selections
            setSelectedSuiteId(null)
            setTestSuites([])
            setTestCases([])
          }}
        >

          <option value="" disabled>
            Select a project
          </option>

          {projects.map((project) => (

            <option
              key={project.id}
              value={project.id}
            >
              {project.name}
            </option>

          ))}

        </select>

      </div>


      {/* Suite Selector */}

      <div className="form-group">

        <label>
          Test Suite
        </label>

        <select
          value={selectedSuiteId ?? ''}
          onChange={(event) => {
            setSelectedSuiteId(
              Number(event.target.value)
            )
          }}
          disabled={
            loadingSuites ||
            testSuites.length === 0
          }
        >

          <option value="" disabled>
            {loadingSuites
              ? 'Loading suites...'
              : 'Select a test suite'}
          </option>

          {testSuites.map((suite) => (

            <option
              key={suite.id}
              value={suite.id}
            >
              {suite.name}
            </option>

          ))}

        </select>

      </div>


      {/* Loading Test Cases */}

      {loadingTestCases && (
        <p>
          Loading test cases...
        </p>
      )}


      {/* Test Cases Table */}

      {!loadingTestCases && (

        <div className="project-table-container">

          <table className="project-table">

            <thead>

              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Description</th>
                <th>Priority</th>
                <th>Status</th>
                <th>Suite ID</th>
                <th>Actions</th>
              </tr>

            </thead>

            <tbody>

              {testCases.map((testCase) => (

                <tr key={testCase.id}>

                  <td>
                    {testCase.id}
                  </td>

                  <td>
                    <strong>
                      {testCase.name}
                    </strong>
                  </td>

                  <td>
                    {testCase.description || '-'}
                  </td>

                  <td>
                    {testCase.priority}
                  </td>

                  <td>
                    {testCase.status}
                  </td>

                  <td>
                    {testCase.suite_id}
                  </td>

                  <td>
                    <button
                      onClick={() => {
                        setEditingTestCase(testCase)

                        setName(testCase.name)
                        setDescription(testCase.description || '')
                        setPriority(testCase.priority)

                        setCreateError(null)
                        setShowCreateModal(true)
                      }}
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDeleteTestCase(testCase)}
                    >
                      Delete
                    </button>
                    <button
                      onClick={() =>
                        handleExecuteTestCase(testCase)
                      }
                      disabled={
                        executingTestCaseId === testCase.id
                      }
                    >
                      {executingTestCaseId === testCase.id
                        ? 'Running...'
                        : 'Execute'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {testCases.length === 0 && (
            <p className="empty-state">
              No test cases found for this suite.
            </p>
          )}

          {execution && (
            <div className="execution-result">
              <h3>
                Latest Execution
              </h3>
              <p>
                Execution ID: {execution.id}
              </p>
              <p>
                Test Case ID: {execution.test_case_id}
              </p>
              <p>
                Status: <strong>{execution.status}</strong>
              </p>
            </div>
          )}

          {executionError && (
            <p className="form-error">
              {executionError}
            </p>
          )}
        </div>
      )}

      {showCreateModal && (

      <div className="modal-overlay">
        <div className="modal">
          <div className="modal-header">

            <h2>
              {editingTestCase
                ? 'Edit Test Case'
                : 'Create Test Case'}
            </h2>

            <button
              type="button"
              onClick={() => {
                setShowCreateModal(false)
                setEditingTestCase(null)
              }}
            >
              ×
            </button>
          </div>

          <form
            onSubmit={
              editingTestCase
                ? handleEditTestCase
                : handleCreateTestCase
            }
          >
            {/* Name */}

            <div className="form-group">
              <label>
                Name
              </label>
              <input
                type="text"
                value={name}
                onChange={(event) =>
                  setName(event.target.value)
                }
                required
              />
            </div>

            {/* Description */}

            <div className="form-group">
              <label>
                Description
              </label>
              <textarea
                value={description}
                onChange={(event) =>
                  setDescription(event.target.value)
                }
                rows={4}
              />
            </div>

            {/* Priority */}

            <div className="form-group">
              <label>
                Priority
              </label>
              <select
                value={priority}
                onChange={(event) =>
                  setPriority(event.target.value)
                }
              >
                <option value="LOW">
                  Low
                </option>
                <option value="MEDIUM">
                  Medium
                </option>
                <option value="HIGH">
                  High
                </option>
              </select>
            </div>

            {/* Error */}

            {createError && (
              <p className="form-error">
                {createError}
              </p>
            )}

            {/* Actions */}

            <div className="modal-actions">

              <button
                type="button"
                onClick={() => {
                  setShowCreateModal(false)
                  setEditingTestCase(null)
                }}
              >
                Cancel
              </button>

              <button
                type="submit"
                disabled={creating}
              >
                {creating
                ? editingTestCase
                  ? 'Updating...'
                  : 'Creating...'
                : editingTestCase
                  ? 'Update'
                  : 'Create'}
              </button>
            </div>
          </form>
        </div>
      </div>
    )}
    </main>
  )
}

export default TestCases