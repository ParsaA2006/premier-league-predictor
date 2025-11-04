import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface Team {
  id: number
  name: string
  short_name?: string
  crest?: string
  founded?: number
}

export interface Match {
  id: number
  home_team: string
  away_team: string
  date: string
  status: string
  home_score?: number
  away_score?: number
}

export interface MatchPrediction {
  home_team: string
  away_team: string
  predicted_result: string
  home_win_probability: number
  draw_probability: number
  away_win_probability: number
  predicted_home_score?: number
  predicted_away_score?: number
  confidence: number
}

export interface SeasonPrediction {
  season: string
  predicted_standings: Array<{
    team: string
    predicted_points: number
    current_points: number
    current_position: number
    predicted_position: number
  }>
  predicted_champion: string
  predicted_relegated: string[]
  updated_at: string
}

export const api = {
  getTeams: async (): Promise<Team[]> => {
    const response = await apiClient.get('/api/teams')
    return response.data
  },

  getMatches: async (): Promise<Match[]> => {
    const response = await apiClient.get('/api/matches')
    return response.data
  },

  predictMatch: async (homeTeam: string, awayTeam: string): Promise<MatchPrediction> => {
    const response = await apiClient.get(
      `/api/predict/match/${encodeURIComponent(homeTeam)}/${encodeURIComponent(awayTeam)}`
    )
    return response.data
  },

  predictSeason: async (): Promise<SeasonPrediction> => {
    const response = await apiClient.get('/api/predict/season')
    return response.data
  },

  getTeamStats: async (team: string): Promise<any> => {
    const response = await apiClient.get(`/api/stats/${encodeURIComponent(team)}`)
    return response.data
  },
}

