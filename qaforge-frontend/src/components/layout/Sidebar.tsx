import { NavLink } from 'react-router-dom'

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        QAForge
      </div>

      <nav>
        <ul className="sidebar-menu">

          <li>
            <NavLink to="/dashboard">
              Dashboard
            </NavLink>
          </li>

          <li>
            <NavLink to="/projects">
              Projects
            </NavLink>
          </li>

          <li>
            <NavLink to="/test-suites">
              Test Suites
            </NavLink>
          </li>

          <li>
            <NavLink to="/test-cases">
              Test Cases
            </NavLink>
          </li>

          <li>
            <NavLink to="/executions">
              Executions
            </NavLink>
          </li>

        </ul>
      </nav>
    </aside>
  )
}

export default Sidebar