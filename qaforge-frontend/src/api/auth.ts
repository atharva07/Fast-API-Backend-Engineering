import apiClient from './client'

export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  message: string
}

export async function login(
  credentials: LoginRequest
): Promise<LoginResponse> {
  const response = await apiClient.post<LoginResponse>(
    '/api/auth/login',
    credentials
  )

  return response.data
}