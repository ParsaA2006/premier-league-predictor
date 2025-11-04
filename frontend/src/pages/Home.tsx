import { useQuery } from '@tanstack/react-query'
import { api } from '../api/client'
import './Home.css'

const Home = () => {
  const { data: matches, isLoading } = useQuery({
    queryKey: ['matches'],
    queryFn: api.getMatches,
  })

  return (
    <div className="home">
      <div className="hero">
        <h1>Premier League AI Predictor</h1>
        <p>Powered by machine learning to predict match outcomes, season standings, and team performance</p>
      </div>

      <div className="features">
        <div className="feature-card">
          <h2>🎯 Match Predictions</h2>
          <p>Get AI-powered predictions for individual matches with win probabilities and score forecasts</p>
        </div>
        <div className="feature-card">
          <h2>📊 Season Forecast</h2>
          <p>Predict the entire season standings and see who will be champions or relegated</p>
        </div>
        <div className="feature-card">
          <h2>📈 Team Analytics</h2>
          <p>Analyze team statistics, form, and performance metrics</p>
        </div>
      </div>

      {isLoading ? (
        <div className="loading">Loading upcoming matches...</div>
      ) : matches && matches.length > 0 ? (
        <div className="upcoming-matches">
          <h2>Upcoming Matches</h2>
          <div className="matches-grid">
            {matches.slice(0, 6).map((match) => (
              <div key={match.id} className="match-card">
                <div className="match-teams">
                  <span className="team">{match.home_team}</span>
                  <span className="vs">vs</span>
                  <span className="team">{match.away_team}</span>
                </div>
                <div className="match-date">
                  {new Date(match.date).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : null}
    </div>
  )
}

export default Home

