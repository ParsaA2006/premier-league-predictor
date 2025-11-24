import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { api, Team } from '../api/client'
import './PlayerStats.css'

interface Player {
  id: number
  name: string
  position?: string
  dateOfBirth?: string
  nationality?: string
  role?: string
  shirtNumber?: number
}

const PlayerStats = () => {
  const [selectedTeam, setSelectedTeam] = useState<string>('')

  const { data: teams } = useQuery({
    queryKey: ['teams'],
    queryFn: api.getTeams,
  })

  const { data: players, isLoading } = useQuery({
    queryKey: ['players', selectedTeam],
    queryFn: () => api.getTeamPlayers(selectedTeam),
    enabled: !!selectedTeam,
  })

  const getPlayerPhoto = (player: Player) => {
    // Use real photo if available, otherwise fallback to avatar
    if (player.photo) {
      return player.photo
    }
    // Fallback to generated avatar
    const name = encodeURIComponent(player.name)
    return `https://ui-avatars.com/api/?name=${name}&size=200&background=667eea&color=fff&bold=true`
  }

  const getPositionColor = (position?: string) => {
    if (!position) return '#667eea'
    const pos = position.toLowerCase()
    if (pos.includes('goalkeeper') || pos.includes('keeper')) return '#f44336'
    if (pos.includes('defence') || pos.includes('defender') || pos.includes('back')) return '#2196F3'
    if (pos.includes('midfield') || pos.includes('midfielder')) return '#4CAF50'
    if (pos.includes('offence') || pos.includes('attacker') || pos.includes('forward') || 
        pos.includes('striker') || pos.includes('winger') || pos.includes('centre-forward')) return '#FF9800'
    return '#667eea'
  }

  const groupPlayersByPosition = (players: Player[]) => {
    const groups: { [key: string]: Player[] } = {
      'Goalkeeper': [],
      'Defence': [],
      'Midfield': [],
      'Offence': [],
      'Other': []
    }

    players.forEach(player => {
      const pos = (player.position || 'Other').toLowerCase()
      if (pos.includes('goalkeeper') || pos.includes('keeper')) {
        groups['Goalkeeper'].push(player)
      } else if (pos.includes('defence') || pos.includes('defender') || pos.includes('back')) {
        groups['Defence'].push(player)
      } else if (pos.includes('midfield') || pos.includes('midfielder')) {
        groups['Midfield'].push(player)
      } else if (pos.includes('offence') || pos.includes('attacker') || pos.includes('forward') || 
                 pos.includes('striker') || pos.includes('winger') || pos.includes('centre-forward')) {
        groups['Offence'].push(player)
      } else {
        groups['Other'].push(player)
      }
    })

    return groups
  }

  return (
    <div className="player-stats">
      <h1>Player Statistics</h1>
      <p className="subtitle">View squad and player information for each team</p>

      <div className="team-selector-section">
        <label htmlFor="team-select">Select Team:</label>
        <select
          id="team-select"
          value={selectedTeam}
          onChange={(e) => setSelectedTeam(e.target.value)}
          className="team-select"
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
        <div className="loading">Loading players...</div>
      )}

      {players && players.length > 0 && (
        <div className="players-container">
          <h2>{selectedTeam} Squad</h2>
          <div className="players-grid">
            {Object.entries(groupPlayersByPosition(players)).map(([position, positionPlayers]) => {
              if (positionPlayers.length === 0) return null
              return (
                <div key={position} className="position-group">
                  <h3 className="position-header" style={{ borderLeftColor: getPositionColor(position) }}>
                    {position} ({positionPlayers.length})
                  </h3>
                  <div className="players-list">
                    {positionPlayers.map((player) => (
                      <div key={player.id} className="player-card">
                        <div className="player-photo-container">
                          <img
                            src={getPlayerPhoto(player)}
                            alt={player.name}
                            className="player-photo"
                            loading="lazy"
                            onError={(e) => {
                              // Fallback to avatar if image fails
                              const target = e.target as HTMLImageElement
                              const name = encodeURIComponent(player.name)
                              target.src = `https://ui-avatars.com/api/?name=${name}&size=200&background=667eea&color=fff&bold=true`
                            }}
                          />
                          {player.shirtNumber && (
                            <div className="shirt-number">{player.shirtNumber}</div>
                          )}
                        </div>
                        <div className="player-info">
                          <h4 className="player-name">{player.name}</h4>
                          {player.position && (
                            <div className="player-position" style={{ color: getPositionColor(player.position) }}>
                              {player.position}
                            </div>
                          )}
                          {player.nationality && (
                            <div className="player-nationality">🇺🇳 {player.nationality}</div>
                          )}
                          {player.dateOfBirth && (
                            <div className="player-age">
                              Age: {new Date().getFullYear() - new Date(player.dateOfBirth).getFullYear()}
                            </div>
                          )}
                          {player.role === 'CAPTAIN' && (
                            <div className="captain-badge">© Captain</div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {players && players.length === 0 && selectedTeam && !isLoading && (
        <div className="no-players">
          <p>No player data available for {selectedTeam}</p>
          <p style={{ fontSize: '0.9em', color: '#666', marginTop: '10px' }}>
            This may be due to API rate limits. Please try again in a few minutes, or try a different team.
          </p>
        </div>
      )}

      {!selectedTeam && (
        <div className="select-team-prompt">
          <p>👆 Select a team above to view their squad and player information</p>
        </div>
      )}
    </div>
  )
}

export default PlayerStats

