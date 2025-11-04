import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { api, MatchPrediction } from '../api/client'
import './MatchPredictor.css'

const MatchPredictor = () => {
  const [homeTeam, setHomeTeam] = useState('')
  const [awayTeam, setAwayTeam] = useState('')
  const [prediction, setPrediction] = useState<MatchPrediction | null>(null)
  const [loading, setLoading] = useState(false)

  const { data: teams } = useQuery({
    queryKey: ['teams'],
    queryFn: api.getTeams,
  })

  const handlePredict = async () => {
    if (!homeTeam || !awayTeam || homeTeam === awayTeam) {
      alert('Please select two different teams')
      return
    }

    setLoading(true)
    try {
      const result = await api.predictMatch(homeTeam, awayTeam)
      setPrediction(result)
    } catch (error) {
      console.error('Prediction error:', error)
      alert('Error making prediction. Please try again.')
    } finally {
      setLoading(false)
    }
  }

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
        {loading ? 'Predicting...' : 'Predict Match'}
      </button>

      {prediction && (
        <div className="prediction-result">
          <h2>Prediction Result</h2>
          <div className="match-info">
            <div className="team-name">{prediction.home_team}</div>
            <div className="vs">vs</div>
            <div className="team-name">{prediction.away_team}</div>
          </div>

          <div className="predicted-result">
            <div className="result-badge">
              {getResultLabel(prediction.predicted_result)}
            </div>
            <div className="confidence">
              Confidence: {(prediction.confidence * 100).toFixed(1)}%
            </div>
          </div>

          {prediction.predicted_home_score !== null && prediction.predicted_away_score !== null && (
            <div className="predicted-score">
              <div className="score">{prediction.predicted_home_score}</div>
              <div className="score-divider">-</div>
              <div className="score">{prediction.predicted_away_score}</div>
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

