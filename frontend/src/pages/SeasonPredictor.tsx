import { useQuery } from '@tanstack/react-query'
import { api } from '../api/client'
import './SeasonPredictor.css'

const SeasonPredictor = () => {
  const { data: prediction, isLoading, error } = useQuery({
    queryKey: ['season-prediction'],
    queryFn: api.predictSeason,
    refetchOnWindowFocus: false,
  })

  if (isLoading) {
    return (
      <div className="season-predictor">
        <div className="loading">Loading season prediction...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="season-predictor">
        <div className="error">Error loading prediction. Please try again.</div>
      </div>
    )
  }

  if (!prediction || !prediction.predicted_standings.length) {
    return (
      <div className="season-predictor">
        <div className="no-data">No prediction data available</div>
      </div>
    )
  }

  return (
    <div className="season-predictor">
      <h1>Season Prediction</h1>
      <p className="subtitle">
        AI-powered forecast for the {prediction.season} Premier League season
      </p>

      <div className="championship-section">
        <div className="champion-card">
          <h2>🏆 Predicted Champion</h2>
          <div className="champion-name">{prediction.predicted_champion}</div>
        </div>
      </div>

      {prediction.predicted_relegated.length > 0 && (
        <div className="relegation-section">
          <h2>⚠️ Predicted Relegation</h2>
          <div className="relegated-teams">
            {prediction.predicted_relegated.map((team) => (
              <div key={team} className="relegated-team">
                {team}
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="standings-table">
        <h2>Predicted Final Standings</h2>
        <table>
          <thead>
            <tr>
              <th>Pos</th>
              <th>Team</th>
              <th>Current Points</th>
              <th>Predicted Points</th>
              <th>Change</th>
            </tr>
          </thead>
          <tbody>
            {prediction.predicted_standings.map((team, index) => {
              const positionChange = team.current_position - team.predicted_position
              return (
                <tr
                  key={team.team}
                  className={
                    index < 4
                      ? 'champions-league'
                      : index < 6
                      ? 'europa-league'
                      : index >= prediction.predicted_standings.length - 3
                      ? 'relegation'
                      : ''
                  }
                >
                  <td>{team.predicted_position}</td>
                  <td className="team-name">{team.team}</td>
                  <td>{team.current_points}</td>
                  <td className="predicted-points">
                    {team.predicted_points.toFixed(1)}
                  </td>
                  <td>
                    {positionChange !== 0 ? (
                      <span
                        className={
                          positionChange > 0 ? 'position-up' : 'position-down'
                        }
                      >
                        {positionChange > 0 ? '↑' : '↓'} {Math.abs(positionChange)}
                      </span>
                    ) : (
                      <span className="position-same">-</span>
                    )}
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default SeasonPredictor

