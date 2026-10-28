import { Navigate, Outlet } from 'react-router-dom'
import { useEffect, useState } from 'react'
import apiClient from '../../api/client'

function ProtectedRoute() {
  const [authenticated, setAuthenticated] = useState<Boolean | null>(null)

  useEffect(() => {
    let active = true

    apiClient
      .get('/api/auth/me')
      .then(() => {
        if (active) {
          setAuthenticated(true)
        }
      })
      .catch(() => {
        if (active) {
          setAuthenticated(false)
        }
      })

    return () => {
      active = false
    }
  }, [])

  if (authenticated === null) {
    return <div>Checking authentication...</div>
  }

  if (!authenticated) {
    return <Navigate to="/login" replace />
  }

  return <Outlet />
}

export default ProtectedRoute