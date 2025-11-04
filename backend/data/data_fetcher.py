import os
import aiohttp
import asyncio
from typing import List, Optional, Dict
from datetime import datetime
import json

class DataFetcher:
    """Fetches Premier League data from Football-Data.org API"""
    
    def __init__(self):
        self.api_key = os.getenv("FOOTBALL_DATA_API_KEY", "")
        self.base_url = "https://api.football-data.org/v4"
        self.headers = {
            "X-Auth-Token": self.api_key,
            "Content-Type": "application/json"
        }
        self.competition_id = "PL"  # Premier League
    
    async def _make_request(self, endpoint: str) -> Optional[Dict]:
        """Make API request"""
        url = f"{self.base_url}/{endpoint}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 429:
                        print("Rate limit exceeded. Waiting...")
                        await asyncio.sleep(60)
                        return await self._make_request(endpoint)
                    else:
                        print(f"API request failed: {response.status}")
                        return None
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
    
    async def fetch_teams(self) -> List[Dict]:
        """Fetch all Premier League teams"""
        endpoint = f"competitions/{self.competition_id}/teams"
        data = await self._make_request(endpoint)
        
        if data and "teams" in data:
            teams = []
            for team in data["teams"]:
                teams.append({
                    "id": team.get("id"),
                    "name": team.get("name"),
                    "short_name": team.get("shortName"),
                    "crest": team.get("crest"),
                    "founded": team.get("founded")
                })
            return teams
        return []
    
    async def fetch_upcoming_matches(self) -> List[Dict]:
        """Fetch upcoming Premier League matches"""
        endpoint = f"competitions/{self.competition_id}/matches?status=SCHEDULED"
        data = await self._make_request(endpoint)
        
        if data and "matches" in data:
            matches = []
            for match in data["matches"]:
                matches.append({
                    "id": match.get("id"),
                    "home_team": match.get("homeTeam", {}).get("name"),
                    "away_team": match.get("awayTeam", {}).get("name"),
                    "date": match.get("utcDate"),
                    "status": match.get("status"),
                    "home_score": match.get("score", {}).get("fullTime", {}).get("home"),
                    "away_score": match.get("score", {}).get("fullTime", {}).get("away")
                })
            return matches
        return []
    
    async def fetch_team_stats(self, team_name: str) -> Optional[Dict]:
        """Fetch statistics for a specific team"""
        # First, get the team ID
        teams = await self.fetch_teams()
        team_id = None
        for team in teams:
            if team["name"].lower() == team_name.lower():
                team_id = team["id"]
                break
        
        if not team_id:
            return None
        
        # Fetch team statistics from standings
        endpoint = f"competitions/{self.competition_id}/standings"
        data = await self._make_request(endpoint)
        
        if data and "standings" in data:
            for standing_group in data["standings"]:
                if standing_group.get("type") == "TOTAL":
                    for table_entry in standing_group.get("table", []):
                        if table_entry.get("team", {}).get("id") == team_id:
                            team_data = table_entry.get("team", {})
                            return {
                                "team": team_data.get("name"),
                                "matches_played": table_entry.get("playedGames", 0),
                                "wins": table_entry.get("won", 0),
                                "draws": table_entry.get("draw", 0),
                                "losses": table_entry.get("lost", 0),
                                "goals_for": table_entry.get("goalsFor", 0),
                                "goals_against": table_entry.get("goalsAgainst", 0),
                                "goal_diff": table_entry.get("goalDifference", 0),
                                "points": table_entry.get("points", 0),
                                "position": table_entry.get("position", 0),
                                "form": table_entry.get("form", "")
                            }
        return None
    
    async def fetch_recent_matches(self, limit: int = 100) -> List[Dict]:
        """Fetch recent completed matches for training"""
        endpoint = f"competitions/{self.competition_id}/matches?status=FINISHED&limit={limit}"
        data = await self._make_request(endpoint)
        
        if data and "matches" in data:
            matches = []
            for match in data["matches"]:
                matches.append({
                    "id": match.get("id"),
                    "home_team": match.get("homeTeam", {}).get("name"),
                    "away_team": match.get("awayTeam", {}).get("name"),
                    "date": match.get("utcDate"),
                    "home_score": match.get("score", {}).get("fullTime", {}).get("home"),
                    "away_score": match.get("score", {}).get("fullTime", {}).get("away"),
                    "status": "FINISHED"
                })
            return matches
        return []

