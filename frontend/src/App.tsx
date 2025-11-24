import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import MatchPredictor from './pages/MatchPredictor'
import SeasonPredictor from './pages/SeasonPredictor'
import TeamStats from './pages/TeamStats'
import PlayerStats from './pages/PlayerStats'
import './App.css'

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/predict-match" element={<MatchPredictor />} />
            <Route path="/predict-season" element={<SeasonPredictor />} />
            <Route path="/team-stats" element={<TeamStats />} />
            <Route path="/player-stats" element={<PlayerStats />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App

