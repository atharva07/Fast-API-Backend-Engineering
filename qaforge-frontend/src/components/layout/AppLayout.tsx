import { Outlet } from 'react-router-dom'

import Sidebar from './Sidebar'
import Header from './Header'

function AppLayout() {
  return (
    <div className="app">
      <Sidebar />

      <div className="main">
        <Header />

        <Outlet />
      </div>
    </div>
  )
}

export default AppLayout