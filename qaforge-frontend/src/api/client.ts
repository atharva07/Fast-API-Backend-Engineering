import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL||'',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
})

// Add JWT to every request
// apiClient.interceptors.request.use(
//   (config) => {
//     const token = sessionStorage.getItem('access_token')
//     if (token) {
//       config.headers.Authorization = `Bearer ${token}`
//     }
//     return config
//   },
//   (error) => {
//     return Promise.reject(error)
//   }
// )

// Handle authentication failures, this will redirect to login screen if the token in expired and returns 401.
// apiClient.interceptors.response.use(
//   (response) => {
//     return response
//   },
//   (error) => {
//     if (error.response?.status === 401) {
//       sessionStorage.removeItem('access_token')
//       window.location.href = '/login'
//     }
//     return Promise.reject(error)
//   }
// )

// export default apiClient

// Handle authentication failures
// Session authentication uses an HttpOnly cookie rather than a JWT in sessionStorage

apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (
      error.response?.status === 401 &&
      window.location.pathname !== '/login'
    ) {
      window.location.href = '/login'
    }

    return Promise.reject(error)
  }
)

export default apiClient