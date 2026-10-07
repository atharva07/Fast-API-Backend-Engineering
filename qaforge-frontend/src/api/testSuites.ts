import apiClient from './client'

export interface TestSuite {
  id: number
  name: string
  description: string | null
  project_id: number
}

export interface CreateTestSuiteRequest {
  name: string
  description: string
}

export interface UpdateTestSuiteRequest {
  name?: string
  description?: string
}

export async function getTestSuites(
  projectId: number
): Promise<TestSuite[]> {
  const response = await apiClient.get<TestSuite[]>(
    `/api/projects/${projectId}/suites`
  )

  return response.data
}

export async function getTestSuite(
  suiteId: number
): Promise<TestSuite> {
  const response = await apiClient.get<TestSuite>(
    `/api/suites/${suiteId}`
  )

  return response.data
}

export async function createTestSuite(
  projectId: number,
  data: CreateTestSuiteRequest
): Promise<TestSuite> {
  const response = await apiClient.post<TestSuite>(
    `/api/projects/${projectId}/suites`,
    data
  )

  return response.data
}

export async function updateTestSuite(
  suiteId: number,
  data: UpdateTestSuiteRequest
): Promise<TestSuite> {
  const response = await apiClient.patch<TestSuite>(
    `/api/suites/${suiteId}`,
    data
  )

  return response.data
}

export async function deleteTestSuite(
  suiteId: number
): Promise<void> {
  await apiClient.delete(
    `/api/suites/${suiteId}`
  )
}