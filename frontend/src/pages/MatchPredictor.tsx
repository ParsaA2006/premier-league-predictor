import { useState, useEffect, useCallback, useRef } from 'react'
import { useQuery } from '@tanstack/react-query'
import { api, MatchPrediction, Team } from '../api/client'
import './MatchPredictor.css'

const MatchPredictor = () => {
  const [homeTeam, setHomeTeam] = useState('')
  const [awayTeam, setAwayTeam] = useState('')
  const [prediction, setPrediction] = useState<MatchPrediction | null>(null)
  const [loading, setLoading] = useState(false)
  const [showScore, setShowScore] = useState(false)
  const isPredictingRef = useRef(false)

  const { data: teams } = useQuery({
    queryKey: ['teams'],
    queryFn: api.getTeams,
  })

  const [homeTeamData, setHomeTeamData] = useState<Team | null>(null)
  const [awayTeamData, setAwayTeamData] = useState<Team | null>(null)
  const [homeStats, setHomeStats] = useState<any>(null)
  const [awayStats, setAwayStats] = useState<any>(null)

  const handlePredict = useCallback(async () => {
    if (!homeTeam || !awayTeam || homeTeam === awayTeam || isPredictingRef.current) {
      return
    }

    isPredictingRef.current = true
    setLoading(true)
    setShowScore(false)
    try {
      // Clear previous prediction immediately
      setPrediction(null)
      
      // Find team data for logos
      const home = teams?.find(t => t.name === homeTeam)
      const away = teams?.find(t => t.name === awayTeam)
      setHomeTeamData(home || null)
      setAwayTeamData(away || null)
      
      // Fetch team stats
      try {
        const [homeStatsData, awayStatsData] = await Promise.all([
          api.getTeamStats(homeTeam),
          api.getTeamStats(awayTeam)
        ])
        setHomeStats(homeStatsData)
        setAwayStats(awayStatsData)
      } catch (e) {
        console.log('Stats not available')
      }
      
      const result = await api.predictMatch(homeTeam, awayTeam)
      setPrediction(result)
      
      // Animate score reveal
      setTimeout(() => setShowScore(true), 300)
    } catch (error) {
      console.error('Prediction error:', error)
      alert('Error making prediction. Please try again.')
    } finally {
      setLoading(false)
      isPredictingRef.current = false
    }
  }, [homeTeam, awayTeam, teams])

  // Auto-predict when both teams are selected and different
  useEffect(() => {
    if (homeTeam && awayTeam && homeTeam !== awayTeam && !loading) {
      const timeoutId = setTimeout(() => {
        handlePredict()
      }, 300) // Small delay to debounce rapid changes
      
      return () => clearTimeout(timeoutId)
    } else {
      // Clear prediction if teams are not both selected
      setPrediction(null)
    }
  }, [homeTeam, awayTeam]) // Removed handlePredict from dependencies

  const getResultLabel = (result: string) => {
    switch (result) {
      case 'HOME_WIN':
        return 'Home Win'
      case 'AWAY_WIN':
        return 'Away Win'
      case 'DRAW':
        return 'Draw'
      default:
        return result
    }
  }

  const getResultColor = (result: string) => {
    switch (result) {
      case 'HOME_WIN':
        return '#4CAF50'
      case 'AWAY_WIN':
        return '#2196F3'
      case 'DRAW':
        return '#FFC107'
      default:
        return '#667eea'
    }
  }

  const renderForm = (form: string | null, stats: any) => {
    if (form && form.length > 0) {
      return (
        <div className="form-indicators">
          {form.split('').slice(0, 5).map((result, i) => (
            <span
              key={i}
              className={`form-indicator ${result === 'W' ? 'win' : result === 'D' ? 'draw' : 'loss'}`}
            >
              {result}
            </span>
          ))}
        </div>
      )
    }
    
    // Fallback: Show win rate if form not available
    if (stats && stats.matches_played > 0) {
      const winRate = ((stats.wins / stats.matches_played) * 100).toFixed(0)
      return (
        <div className="form-fallback">
          <span className="win-rate">{winRate}% Win Rate</span>
        </div>
      )
    }
    
    return <span className="form-na">N/A</span>
  }

  return (
    <div className="match-predictor">
      <h1>Match Predictor</h1>
      <p className="subtitle">Select two teams to get an AI-powered prediction</p>

      <div className="predictor-form">
        <div className="team-selector">
          <label>Home Team</label>
          <select
            value={homeTeam}
            onChange={(e) => setHomeTeam(e.target.value)}
            disabled={loading}
          >
            <option value="">Select home team</option>
            {teams?.map((team) => (
              <option key={team.id} value={team.name}>
                {team.name}
              </option>
            ))}
          </select>
        </div>

        <div className="vs-divider">vs</div>

        <div className="team-selector">
          <label>Away Team</label>
          <select
            value={awayTeam}
            onChange={(e) => setAwayTeam(e.target.value)}
            disabled={loading}
          >
            <option value="">Select away team</option>
            {teams?.map((team) => (
              <option key={team.id} value={team.name}>
                {team.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      <button
        className="predict-button"
        onClick={handlePredict}
        disabled={loading || !homeTeam || !awayTeam}
      >
        {loading ? (
          <span className="loading-button">
            <span className="spinner"></span>
            Predicting...
          </span>
        ) : (
          'Predict Match'
        )}
      </button>

      {prediction && (
        <div className="prediction-result">
          <h2>Prediction Result</h2>
          
          {/* Team Comparison Cards */}
          <div className="teams-comparison">
            <div className="team-card home-team">
              {homeTeamData?.crest && (
                <img src={homeTeamData.crest} alt={prediction.home_team} className="team-crest" />
              )}
              <div className="team-card-content">
                <h3>{prediction.home_team}</h3>
                {homeStats && (
                  <div className="team-stats-mini">
                    <div className="stat-item">
                      <span className="stat-label">Points:</span>
                      <span className="stat-value">{homeStats.points}</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Position:</span>
                      <span className="stat-value">#{homeStats.position}</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Form:</span>
                      {renderForm(homeStats.form, homeStats)}
                    </div>
                  </div>
                )}
              </div>
            </div>

            <div className="vs-large">VS</div>

            <div className="team-card away-team">
              {awayTeamData?.crest && (
                <img src={awayTeamData.crest} alt={prediction.away_team} className="team-crest" />
              )}
              <div className="team-card-content">
                <h3>{prediction.away_team}</h3>
                {awayStats && (
                  <div className="team-stats-mini">
                    <div className="stat-item">
                      <span className="stat-label">Points:</span>
                      <span className="stat-value">{awayStats.points}</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Position:</span>
                      <span className="stat-value">#{awayStats.position}</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Form:</span>
                      {renderForm(awayStats.form, awayStats)}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="predicted-result">
            <div 
              className="result-badge"
              style={{ backgroundColor: getResultColor(prediction.predicted_result) }}
            >
              {getResultLabel(prediction.predicted_result)}
            </div>
            <div className="confidence">
              <span className="confidence-label">Confidence:</span>
              <span className="confidence-value">{(prediction.confidence * 100).toFixed(1)}%</span>
            </div>
          </div>

          {prediction.predicted_home_score !== null && prediction.predicted_away_score !== null && (
            <div className={`predicted-score ${showScore ? 'revealed' : ''}`}>
              <div className="score-container">
                <div className="score home-score">{prediction.predicted_home_score}</div>
                <div className="score-divider">-</div>
                <div className="score away-score">{prediction.predicted_away_score}</div>
              </div>
            </div>
          )}

          <div className="probabilities">
            <h3>Win Probabilities</h3>
            <div className="probability-bars">
              <div className="probability-item">
                <div className="prob-label">Home Win</div>
                <div className="prob-bar">
                  <div
                    className="prob-fill home-win"
                    style={{ width: `${prediction.home_win_probability * 100}%` }}
                  />
                </div>
                <div className="prob-value">
                  {(prediction.home_win_probability * 100).toFixed(1)}%
                </div>
              </div>
              <div className="probability-item">
                <div className="prob-label">Draw</div>
                <div className="prob-bar">
                  <div
                    className="prob-fill draw"
                    style={{ width: `${prediction.draw_probability * 100}%` }}
                  />
                </div>
                <div className="prob-value">
                  {(prediction.draw_probability * 100).toFixed(1)}%
                </div>
              </div>
              <div className="probability-item">
                <div className="prob-label">Away Win</div>
                <div className="prob-bar">
                  <div
                    className="prob-fill away-win"
                    style={{ width: `${prediction.away_win_probability * 100}%` }}
                  />
                </div>
                <div className="prob-value">
                  {(prediction.away_win_probability * 100).toFixed(1)}%
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default MatchPredictor

