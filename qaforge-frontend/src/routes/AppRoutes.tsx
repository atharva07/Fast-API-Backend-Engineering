import { Routes, Route, Navigate } from 'react-router-dom'

import Login from '../pages/Login'
import Dashboard from '../pages/Dashboard'
import Projects from '../pages/Projects'
import TestSuites from '../pages/TestSuites'
import TestCases from '../pages/TestCases'
import Executions from '../pages/Executions'

import ProtectedRoute from '../components/auth/ProtectedRoute'
import AppLayout from '../components/layout/AppLayout'

function AppRoutes() {
  return (
    <Routes>

      {/* Public routes */}

      <Route path="/login" element={<Login />} />


      {/* Protected routes */}

      <Route element={<ProtectedRoute />}>
        <Route element={<AppLayout />}>

          <Route
            path="/dashboard"
            element={<Dashboard />}
          />

          <Route
            path="/projects"
            element={<Projects />}
          />

          <Route
            path="/test-suites"
            element={<TestSuites />}
          />

          <Route
            path="/test-cases"
            element={<TestCases />}
          />

          <Route
            path="/executions"
            element={<Executions />}
          />

        </Route>
      </Route>


      {/* Default */}

      <Route
        path="/"
        element={<Navigate to="/dashboard" replace />}
      />

    </Routes>
  )
}

export default AppRoutes