import apiClient from './client'

export interface DashboardStats {
  projects: number
  test_suites: number
  test_cases: number
  executions: number
}

export async function getDashboardStats(): Promise<DashboardStats> {
  const response = await apiClient.get<DashboardStats>(
    '/api/dashboard'
  )

  return response.data
}