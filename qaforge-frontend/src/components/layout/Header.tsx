
import { useNavigate } from 'react-router-dom'
import apiClient from '../../api/client'

function Header() {
  const navigate = useNavigate()

  async function handleLogout() {
    try {
      await apiClient.post('/api/auth/logout')
    } catch (error) {
      console.error('Logout request failed:', error)
    } finally {
      navigate('/login', { replace: true })
    }
  }

  return (
    <header className="header">
      <h2>QAForge</h2>

      <div className="user">
        <span>Admin</span>

        <button onClick={handleLogout}>
          Logout
        </button>

        <span className="avatar">A</span>
      </div>
    </header>
  )
}

export default Header
