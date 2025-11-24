import { Link, useLocation } from 'react-router-dom'
import './Navbar.css'

const Navbar = () => {
  const location = useLocation()

  const isActive = (path: string) => location.pathname === path

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          ⚽ Premier League Predictor
        </Link>
        <ul className="navbar-menu">
          <li>
            <Link 
              to="/" 
              className={isActive('/') ? 'active' : ''}
            >
              Home
            </Link>
          </li>
          <li>
            <Link 
              to="/predict-match" 
              className={isActive('/predict-match') ? 'active' : ''}
            >
              Match Predictor
            </Link>
          </li>
          <li>
            <Link 
              to="/predict-season" 
              className={isActive('/predict-season') ? 'active' : ''}
            >
              Season Predictor
            </Link>
          </li>
          <li>
            <Link 
              to="/team-stats" 
              className={isActive('/team-stats') ? 'active' : ''}
            >
              Team Stats
            </Link>
          </li>
          <li>
            <Link 
              to="/player-stats" 
              className={isActive('/player-stats') ? 'active' : ''}
            >
              Players
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  )
}

export default Navbar

