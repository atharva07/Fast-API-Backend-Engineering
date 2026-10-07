import { useEffect, useState } from 'react'

import {
  getTestSuites,
  createTestSuite,
  updateTestSuite,
  deleteTestSuite,
  type TestSuite,
} from '../api/testSuites'

import {
  getProjects,
  type Project,
} from '../api/projects'

function TestSuites() {
  const [projects, setProjects] = useState<Project[]>([])
  const [selectedProjectId, setSelectedProjectId] = useState<number | null>(null)

  const [testSuites, setTestSuites] = useState<TestSuite[]>([])

  const [loadingProjects, setLoadingProjects] = useState(true)
  const [loadingSuites, setLoadingSuites] = useState(false)

  const [error, setError] = useState<string | null>(null)

  const [showCreateModal, setShowCreateModal] = useState(false)
  const [editingSuite, setEditingSuite] = useState<TestSuite | null>(null)

  const [name, setName] = useState('')
  const [description, setDescription] = useState('')

  const [creating, setCreating] = useState(false)
  const [createError, setCreateError] = useState<string | null>(null)

  const [deletingSuiteId, setDeletingSuiteId] = useState<number | null>(null)

  async function handleCreateTestSuite(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault()

    if (selectedProjectId === null) {
      setCreateError('Please select a project')
      return
    }

    setCreateError(null)
    setCreating(true)

    try {
      await createTestSuite(selectedProjectId, {
        name,
        description,
      })

      setShowCreateModal(false)

      setName('')
      setDescription('')

      const projectId = selectedProjectId

      const data = await getTestSuites(projectId)

      setTestSuites(data)

    } catch (error) {
      setCreateError('Failed to create test suite')
    } finally {
      setCreating(false)
    }
  }

  async function handleEditTestSuite(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault()

    if (!editingSuite) {
      return
    }

    setCreateError(null)
    setCreating(true)

    try {
      await updateTestSuite(editingSuite.id, {
        name,
        description,
      })

      setShowCreateModal(false)
      setEditingSuite(null)

      setName('')
      setDescription('')

      if (selectedProjectId !== null) {
        const projectId = selectedProjectId

        const data = await getTestSuites(projectId)

        setTestSuites(data)
      }

    } catch (error) {
      setCreateError('Failed to update test suite')
    } finally {
      setCreating(false)
    }
  }

  async function handleDeleteTestSuite(suite: TestSuite) {
    const confirmed = window.confirm(
      `Are you sure you want to delete "${suite.name}"?`
    )

    if (!confirmed) {
      return
    }

    setDeletingSuiteId(suite.id)

    try {
      await deleteTestSuite(suite.id)

      if (selectedProjectId !== null) {
        const projectId = selectedProjectId

        const data = await getTestSuites(projectId)

        setTestSuites(data)
      }

    } catch (error) {
      setError('Failed to delete test suite')
    } finally {
      setDeletingSuiteId(null)
    }
  }

  // Load Projects
  useEffect(() => {
    async function loadProjects() {
      try {
        const data = await getProjects()

        setProjects(data)

        // Select first project automatically
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


  // Load Test Suites
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

      } catch (error) {
        setError('Failed to load test suites')
      } finally {
        setLoadingSuites(false)
      }
    }

    loadTestSuites()
  }, [selectedProjectId])


  if (loadingProjects) {
    return (
      <main className="dashboard">
        <h1>Test Suites</h1>
        <p>Loading projects...</p>
      </main>
    )
  }


  if (error) {
    return (
      <main className="dashboard">
        <h1>Test Suites</h1>
        <p>{error}</p>
      </main>
    )
  }


  return (
    <main className="dashboard">

      {/* Page Header */}

      <div className="page-header">

        <div>
          <h1>Test Suites</h1>
          <p>
            Manage test suites for your projects.
          </p>
        </div>

        <button
          onClick={() => {
            setEditingSuite(null)
            setName('')
            setDescription('')
            setCreateError(null)
            setShowCreateModal(true)
          }}
          disabled={selectedProjectId === null}
        >
          + Create Suite
        </button>

      </div>


      {/* Project Selector */}

      <div className="form-group">

        <label>
          Project
        </label>

        <select
          value={selectedProjectId ?? ''}
          onChange={(event) =>
            setSelectedProjectId(
              Number(event.target.value)
            )
          }
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


      {/* Loading Suites */}

      {loadingSuites && (
        <p>
          Loading test suites...
        </p>
      )}


      {/* Test Suites Table */}

      {!loadingSuites && (

        <div className="project-table-container">

          <table className="project-table">

            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Description</th>
                <th>Project ID</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>

              {testSuites.map((suite) => (

                <tr key={suite.id}>

                  <td>
                    {suite.id}
                  </td>

                  <td>
                    <strong>
                      {suite.name}
                    </strong>
                  </td>

                  <td>
                    {suite.description || '-'}
                  </td>

                  <td>
                    {suite.project_id}
                  </td>

                  <td>
                    <button
                      onClick={() => {
                        setEditingSuite(suite)

                        setName(suite.name)
                        setDescription(suite.description || '')

                        setCreateError(null)
                        setShowCreateModal(true)
                      }}
                    >
                      Edit
                    </button>

                    <button
                      onClick={() => handleDeleteTestSuite(suite)}
                      disabled={deletingSuiteId === suite.id}
                    >
                      {deletingSuiteId === suite.id
                        ? 'Deleting...'
                        : 'Delete'}
                    </button>
                  </td>
                </tr>

              ))}

            </tbody>

          </table>


          {testSuites.length === 0 && (
            <p className="empty-state">
              No test suites found for this project.
            </p>
          )}

        </div>

      )}

    {showCreateModal && (

      <div className="modal-overlay">

        <div className="modal">

          <div className="modal-header">

            <h2>
              {editingSuite
                ? 'Edit Test Suite'
                : 'Create Test Suite'}
            </h2>

            <button
              type="button"
              onClick={() => {
                setShowCreateModal(false)
                setEditingSuite(null)
              }}
            >
              ×
            </button>

          </div>

          <form
            onSubmit={
              editingSuite
                ? handleEditTestSuite
                : handleCreateTestSuite
            }
          >

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


            {createError && (
              <p className="form-error">
                {createError}
              </p>
            )}


            <div className="modal-actions">

              <button
                type="button"
                onClick={() => {
                  setShowCreateModal(false)
                  setEditingSuite(null)
                }}
              >
                Cancel
              </button>

              <button
                type="submit"
                disabled={creating}
              >
                {creating
                ? editingSuite
                  ? 'Updating...'
                  : 'Creating...'
                : editingSuite
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


export default TestSuites