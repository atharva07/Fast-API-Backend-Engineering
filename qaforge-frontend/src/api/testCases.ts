import apiClient from './client'

export interface TestCase {
  id: number
  name: string
  description: string | null
  priority: string
  status: string
  suite_id: number
}

export interface CreateTestCaseRequest {
  name: string
  description: string
  priority: string
}

export interface UpdateTestCaseRequest {
  name?: string
  description?: string
  priority?: string
}

export interface TestExecution {
  id: number
  test_case_id: number
  status: string
}

export async function getTestCases(
  suiteId: number
): Promise<TestCase[]> {
  const response = await apiClient.get<TestCase[]>(
    `/api/suites/${suiteId}/test_cases`
  )

  return response.data
}

export async function getTestCase(
  testCaseId: number
): Promise<TestCase> {
  const response = await apiClient.get<TestCase>(
    `/api/test_cases/${testCaseId}`
  )

  return response.data
}

export async function createTestCase(
  suiteId: number,
  data: CreateTestCaseRequest
): Promise<TestCase> {
  const response = await apiClient.post<TestCase>(
    `/api/suites/${suiteId}/test_cases`,
    data
  )

  return response.data
}

export async function updateTestCase(
  testCaseId: number,
  data: UpdateTestCaseRequest
): Promise<TestCase> {
  const response = await apiClient.patch<TestCase>(
    `/api/test_cases/${testCaseId}`,
    data
  )

  return response.data
}

export async function deleteTestCase(
  testCaseId: number
): Promise<void> {
  await apiClient.delete(
    `/api/test_cases/${testCaseId}`
  )
}

export async function executeTestCase(
  testCaseId: number
): Promise<TestExecution> {
  const response = await apiClient.post<TestExecution>(
    `/api/test_cases/${testCaseId}/execute`
  )

  return response.data
}

export async function getTestResult(
  resultId: number
): Promise<TestExecution> {
  const response = await apiClient.get<TestExecution>(
    `/api/results/${resultId}`
  )

  return response.data
}

// export async function getTestResults(): Promise<TestExecution[]> {
//   const response = await apiClient.get<TestExecution[]>(
//     '/api/results/'
//   )

//   return response.data
// }

export interface PaginatedTestResults {
  items: TestExecution[]
  page: number
  page_size: number
  total: number
  total_pages: number
}

export async function getTestResults(
  page: number,
  pageSize: number
): Promise<PaginatedTestResults> {
  const response = await apiClient.get<PaginatedTestResults>(
    '/api/results',
    {
      params: {
        page,
        page_size: pageSize,
      },
    }
  )

  return response.data
}