import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { login } from '../api/auth'

function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const navigate = useNavigate()

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault()

    setError(null)
    setLoading(true)

    try {
      const response = await login({
        email,
        password,
      })

      sessionStorage.setItem(
        'access_token',
        response.access_token
      )

      navigate('/dashboard')
    } catch (error) {
      setError('Invalid email or password')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="login-page">

      <div className="login-card">

        {/* Brand */}
        <div className="login-brand">
          <h1>QAForge</h1>

          <p>
            Test Management & Automation Platform
          </p>
        </div>


        {/* Login Heading */}
        <div className="login-heading">
          <h2>Welcome back</h2>

          <p>
            Sign in to continue to your account.
          </p>
        </div>


        {/* Login Form */}
        <form
          className="login-form"
          onSubmit={handleSubmit}
        >

          {/* Email */}
          <div className="login-field">

            <label htmlFor="email">
              Email address
            </label>

            <input
              id="email"
              type="email"
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              placeholder="you@example.com"
              autoComplete="email"
              required
              disabled={loading}
            />

          </div>


          {/* Password */}
          <div className="login-field">

            <label htmlFor="password">
              Password
            </label>

            <input
              id="password"
              type="password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              placeholder="Enter your password"
              autoComplete="current-password"
              required
              disabled={loading}
            />

          </div>


          {/* Error */}
          {error && (
            <div
              className="login-error"
              role="alert"
            >
              {error}
            </div>
          )}


          {/* Submit */}
          <button
            type="submit"
            className="login-button"
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="login-spinner" />
                Signing in...
              </>
            ) : (
              'Sign in'
            )}
          </button>

        </form>


        {/* Footer */}
        <div className="login-footer">
          <span>QAForge</span>
          <span>•</span>
          <span>Secure Access</span>
        </div>

      </div>

    </main>
  )
}

export default Login