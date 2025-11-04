import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { api } from '../api/client'
import './TeamStats.css'

const TeamStats = () => {
  const [selectedTeam, setSelectedTeam] = useState('')

  const { data: teams } = useQuery({
    queryKey: ['teams'],
    queryFn: api.getTeams,
  })

  const { data: stats, isLoading } = useQuery({
    queryKey: ['team-stats', selectedTeam],
    queryFn: () => api.getTeamStats(selectedTeam),
    enabled: !!selectedTeam,
  })

  return (
    <div className="team-stats">
      <h1>Team Statistics</h1>
      <p className="subtitle">Select a team to view detailed statistics</p>

      <div className="team-selector">
        <label>Select Team</label>
        <select
          value={selectedTeam}
          onChange={(e) => setSelectedTeam(e.target.value)}
        >
          <option value="">Choose a team...</option>
          {teams?.map((team) => (
            <option key={team.id} value={team.name}>
              {team.name}
            </option>
          ))}
        </select>
      </div>

      {isLoading && selectedTeam && (
        <div className="loading">Loading statistics...</div>
      )}

      {stats && !isLoading && (
        <div className="stats-container">
          <div className="stats-header">
            <h2>{stats.team}</h2>
            {stats.position && (
              <div className="position-badge">Position: {stats.position}</div>
            )}
          </div>

          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-label">Matches Played</div>
              <div className="stat-value">{stats.matches_played}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Wins</div>
              <div className="stat-value wins">{stats.wins}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Draws</div>
              <div className="stat-value draws">{stats.draws}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Losses</div>
              <div className="stat-value losses">{stats.losses}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Goals For</div>
              <div className="stat-value">{stats.goals_for}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Goals Against</div>
              <div className="stat-value">{stats.goals_against}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Goal Difference</div>
              <div
                className={`stat-value ${
                  stats.goal_diff > 0 ? 'positive' : stats.goal_diff < 0 ? 'negative' : ''
                }`}
              >
                {stats.goal_diff > 0 ? '+' : ''}
                {stats.goal_diff}
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Points</div>
              <div className="stat-value points">{stats.points}</div>
            </div>
          </div>

          {stats.form && (
            <div className="form-section">
              <h3>Recent Form</h3>
              <div className="form-indicator">
                {stats.form.split('').map((result, index) => (
                  <span
                    key={index}
                    className={`form-result ${result.toLowerCase()}`}
                  >
                    {result}
                  </span>
                ))}
              </div>
            </div>
          )}

          {stats.wins && stats.matches_played > 0 && (
            <div className="additional-stats">
              <div className="additional-stat">
                <span>Win Rate:</span>
                <span className="stat-number">
                  {((stats.wins / stats.matches_played) * 100).toFixed(1)}%
                </span>
              </div>
              <div className="additional-stat">
                <span>Goals per Game:</span>
                <span className="stat-number">
                  {(stats.goals_for / stats.matches_played).toFixed(2)}
                </span>
              </div>
              <div className="additional-stat">
                <span>Points per Game:</span>
                <span className="stat-number">
                  {(stats.points / stats.matches_played).toFixed(2)}
                </span>
              </div>
            </div>
          )}
        </div>
      )}

      {!selectedTeam && (
        <div className="no-selection">
          <p>Please select a team to view statistics</p>
        </div>
      )}
    </div>
  )
}

export default TeamStats

