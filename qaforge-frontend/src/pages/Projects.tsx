import { useEffect, useState } from 'react'

import {
getProjects,
createProject,
updateProject,
deleteProject,
type Project,
} from '../api/projects'


function Projects() {
const [projects, setProjects] = useState<Project[]>([])
const [loading, setLoading] = useState(true)
const [error, setError] = useState<string | null>(null)

// Create Project Modal
const [showCreateModal, setShowCreateModal] = useState(false)
const [editingProject, setEditingProject] = useState<Project | null>(null)

// Create Project Form
const [name, setName] = useState('')
const [description, setDescription] = useState('')
const [executionTimeout, setExecutionTimeout] = useState(3000)

// Create Project Status
const [creating, setCreating] = useState(false)
const [createError, setCreateError] = useState<string | null>(null)

const [deletingProjectId, setDeletingProjectId] = useState<number | null>(null)


// Create Project
async function handleCreateProject(
    event: React.FormEvent<HTMLFormElement>
) {
    event.preventDefault()

    setCreateError(null)
    setCreating(true)

    try {
    await createProject({
        name,
        description,
        execution_timeout: executionTimeout,
    })

    // Close modal
    setShowCreateModal(false)

    // Reset form
    setName('')
    setDescription('')
    setExecutionTimeout(3000)

    // Reload projects
    const data = await getProjects()
    setProjects(data)

    } catch (error) {
    setCreateError('Failed to create project')
    } finally {
    setCreating(false)
    }
}

// Update Project
async function handleEditProject(
    event: React.FormEvent<HTMLFormElement>
    ) {
    event.preventDefault()

    setCreateError(null)
    setCreating(true)

    try {
        if (!editingProject) {
        return
        }

        await updateProject(editingProject.id, {
        name,
        description,
        execution_timeout: executionTimeout,
        })

        // Close modal
        setShowCreateModal(false)

        // Clear editing state
        setEditingProject(null)

        // Reset form
        setName('')
        setDescription('')
        setExecutionTimeout(3000)

        // Reload projects
        const data = await getProjects()
        setProjects(data)

    } catch (error) {
        setCreateError('Failed to update project')
    } finally {
        setCreating(false)
    }
}

// Delete Project
async function handleDeleteProject(project: Project) {
    const confirmed = window.confirm(
        `Are you sure you want to delete "${project.name}"?`
    )

    if (!confirmed) {
        return
    }

    setDeletingProjectId(project.id)

    try {
        await deleteProject(project.id)

        const data = await getProjects()
        setProjects(data)
    } catch (error) {
        setError('Failed to delete project')
    } finally {
        setDeletingProjectId(null)
    }
}

// Load Projects
useEffect(() => {
    async function loadProjects() {
    try {
        const data = await getProjects()

        setProjects(data)
    } catch (error) {
        setError('Failed to load projects')
    } finally {
        setLoading(false)
    }
    }

    loadProjects()
}, [])


// Loading State
if (loading) {
    return (
    <main className="dashboard">
        <h1>Projects</h1>
        <p>Loading projects...</p>
    </main>
    )
}


// Error State
if (error) {
    return (
    <main className="dashboard">
        <h1>Projects</h1>
        <p>{error}</p>
    </main>
    )
}


return (
    <main className="dashboard">

    {/* Page Header */}

    <div className="page-header">

        <div>
        <h1>Projects</h1>
        <p>Manage your QAForge projects.</p>
        </div>

        <button
            onClick={() => {
                setEditingProject(null)
                setName('')
                setDescription('')
                setExecutionTimeout(3000)
                setCreateError(null)
                setShowCreateModal(true)
            }}
        >
            + Create Project
        </button>

    </div>


    {/* Projects Table */}

    <div className="project-table-container">

        <table className="project-table">

        <thead>
            <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Description</th>
            <th>Execution Timeout</th>
            <th>Actions</th>
            </tr>
        </thead>

        <tbody>

            {projects.map((project) => (

            <tr key={project.id}>

                <td>
                {project.id}
                </td>

                <td>
                <strong>
                    {project.name}
                </strong>
                </td>

                <td>
                {project.description || '-'}
                </td>

                <td>
                {project.execution_timeout} ms
                </td>

                <td>

                <button
                    onClick={() => {
                        setEditingProject(project)

                        setName(project.name)
                        setDescription(project.description || '')
                        setExecutionTimeout(project.execution_timeout)

                        setCreateError(null)
                        setShowCreateModal(true)
                    }}
                >
                    Edit
                </button>

                <button
                    onClick={() => handleDeleteProject(project)}
                    disabled={deletingProjectId === project.id}
                >
                    {deletingProjectId === project.id
                        ? 'Deleting...'
                        : 'Delete'}
                </button>

                </td>

            </tr>

            ))}

        </tbody>

        </table>


        {projects.length === 0 && (
        <p className="empty-state">
            No projects found.
        </p>
        )}

    </div>


    {/* Create Project Modal */}

    {showCreateModal && (

        <div className="modal-overlay">

        <div className="modal">

            <div className="modal-header">

            <h2>
                {editingProject ? 'Edit Project' : 'Create Project'}
            </h2>

            <button
                type="button"
                onClick={() => {
                    setShowCreateModal(false)
                    setEditingProject(null)
                }}
            >
                ×
            </button>

            </div>


            <form
                onSubmit={
                    editingProject
                    ? handleEditProject
                    : handleCreateProject
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


            {/* Execution Timeout */}

            <div className="form-group">

                <label>
                Execution Timeout (ms)
                </label>

                <input
                type="number"
                value={executionTimeout}
                onChange={(event) =>
                    setExecutionTimeout(
                    Number(event.target.value)
                    )
                }
                min={0}
                required
                />

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
                    setEditingProject(null)
                }}
                >
                Cancel
                </button>

                <button
                type="submit"
                disabled={creating}
                >
                {creating
                ? editingProject
                    ? 'Updating...'
                    : 'Creating...'
                : editingProject
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


export default Projects