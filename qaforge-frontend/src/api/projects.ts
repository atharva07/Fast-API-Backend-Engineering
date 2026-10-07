import apiClient from './client'

export interface Project {
  id: number
  name: string
  description: string | null
  execution_timeout: number
}

export interface CreateProjectRequest {
  name: string
  description: string
  execution_timeout: number
}

export interface UpdateProjectRequest {
  name?: string
  description?: string
  execution_timeout?: number
}

export async function getProjects(): Promise<Project[]> {
  const response = await apiClient.get<Project[]>(
    '/api/projects/'
  )

  return response.data
}

export async function createProject(
  data: CreateProjectRequest
): Promise<Project> {
  const response = await apiClient.post<Project>(
    '/api/projects/',
    data
  )

  return response.data
}

export async function updateProject(
  projectId: number,
  data: UpdateProjectRequest
): Promise<Project> {
  const response = await apiClient.patch<Project>(
    `/api/projects/${projectId}`,
    data
  )

  return response.data
}

export async function deleteProject(
  projectId: number
): Promise<void> {
  await apiClient.delete(
    `/api/projects/${projectId}`
  )
}