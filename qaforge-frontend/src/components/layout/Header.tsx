import { useNavigate } from 'react-router-dom'

function Header() {
  const navigate = useNavigate()

  function handleLogout() {
    sessionStorage.removeItem('access_token')

    navigate('/login', { replace: true })
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