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
        
        # Normalize team name for matching (remove FC, handle variations)
        normalized_input = team_name.lower().replace(" fc", "").strip()
        
        for team in teams:
            normalized_team_name = team["name"].lower().replace(" fc", "").strip()
            # Try exact match first
            if team["name"].lower() == team_name.lower():
                team_id = team["id"]
                break
            # Try normalized match (without FC)
            elif normalized_team_name == normalized_input:
                team_id = team["id"]
                break
            # Try partial match
            elif normalized_input in normalized_team_name or normalized_team_name in normalized_input:
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
    
    async def get_player_photo(self, player_name: str, team_name: str) -> Optional[str]:
        """Get player photo from Wikipedia/Wikimedia Commons"""
        try:
            wiki_search_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"
            
            # Try multiple name variations for better matching
            name_parts = player_name.split()
            name_variations = []
            
            # Full name variations
            if len(name_parts) >= 2:
                # "Erling Haaland" -> "Erling_Haaland"
                name_variations.append("_".join(name_parts))
                # "Erling Haaland" -> "Erling Haaland" (with space)
                name_variations.append(" ".join(name_parts))
            
            # Last name only (often works for famous players)
            if len(name_parts) > 1:
                name_variations.append(name_parts[-1])  # "Haaland"
            
            # First name + Last name (common format)
            if len(name_parts) >= 2:
                name_variations.append(f"{name_parts[0]}_{name_parts[-1]}")  # "Erling_Haaland"
            
            async with aiohttp.ClientSession() as session:
                for wiki_name in name_variations:
                    try:
                        # URL encode properly
                        encoded_name = wiki_name.replace(" ", "_")
                        url = f"{wiki_search_url}{encoded_name}"
                        
                        async with session.get(
                            url, 
                            timeout=aiohttp.ClientTimeout(total=1.5),
                            headers={"User-Agent": "PremierLeaguePredictor/1.0 (https://premierleaguepredictor.com)"}
                        ) as response:
                            if response.status == 200:
                                data = await response.json()
                                # Check if it's actually about a person (not a disambiguation page)
                                if data.get("type") == "standard" and data.get("thumbnail"):
                                    thumbnail = data.get("thumbnail", {})
                                    if thumbnail and thumbnail.get("source"):
                                        photo_url = thumbnail["source"]
                                        # Make sure it's a valid image URL
                                        if photo_url and photo_url.startswith("http"):
                                            return photo_url
                    except asyncio.TimeoutError:
                        continue
                    except Exception as e:
                        continue
        except Exception:
            pass  # Silently skip errors
        return None
    
    async def fetch_team_squad(self, team_name: str) -> List[Dict]:
        """Fetch squad/players for a specific team"""
        # First, get the team ID
        teams = await self.fetch_teams()
        team_id = None
        
        # Normalize team name for matching
        normalized_input = team_name.lower().replace(" fc", "").strip()
        
        for team in teams:
            normalized_team_name = team["name"].lower().replace(" fc", "").strip()
            if team["name"].lower() == team_name.lower():
                team_id = team["id"]
                break
            elif normalized_team_name == normalized_input:
                team_id = team["id"]
                break
            elif normalized_input in normalized_team_name or normalized_team_name in normalized_input:
                team_id = team["id"]
                break
        
        if not team_id:
            return []
        
        # Fetch team squad
        endpoint = f"teams/{team_id}"
        data = await self._make_request(endpoint)
        
        if data and "squad" in data:
            players = []
            squad_players = data.get("squad", [])
            
            # Fetch photos in parallel but with a total timeout
            # Only fetch for first 25 players to avoid too many requests
            players_to_fetch = squad_players[:25]
            photo_tasks = []
            for player in players_to_fetch:
                player_name = player.get("name")
                photo_tasks.append(self.get_player_photo(player_name, team_name))
            
            # Wait for photos with a reasonable timeout (5 seconds max)
            try:
                photos = await asyncio.wait_for(
                    asyncio.gather(*photo_tasks, return_exceptions=True),
                    timeout=5.0
                )
            except asyncio.TimeoutError:
                # If timeout, create None list for photos
                photos = [None] * len(players_to_fetch)
            
            # Process all players
            for i, player in enumerate(squad_players):
                player_name = player.get("name")
                # Get photo if we fetched it, otherwise None
                if i < len(photos):
                    photo = photos[i] if not isinstance(photos[i], Exception) and photos[i] else None
                else:
                    photo = None
                
                # Include all players from squad
                players.append({
                    "id": player.get("id"),
                    "name": player_name,
                    "position": player.get("position"),
                    "dateOfBirth": player.get("dateOfBirth"),
                    "nationality": player.get("nationality"),
                    "role": player.get("role"),
                    "shirtNumber": player.get("shirtNumber"),
                    "photo": photo  # Add photo URL if found
                })
            # Sort by position (Goalkeeper, Defender, Midfielder, Attacker) and shirt number
            def get_position_order(pos):
                if not pos:
                    return 5
                pos_lower = pos.lower()
                if "goalkeeper" in pos_lower or "keeper" in pos_lower:
                    return 1
                elif "defence" in pos_lower or "defender" in pos_lower or "back" in pos_lower:
                    return 2
                elif "midfield" in pos_lower or "midfielder" in pos_lower:
                    return 3
                elif "offence" in pos_lower or "attacker" in pos_lower or "forward" in pos_lower or "striker" in pos_lower or "winger" in pos_lower:
                    return 4
                return 5
            
            players.sort(key=lambda x: (
                get_position_order(x.get("position", "")),
                x.get("shirtNumber") or 99
            ))
            return players  # Return all players
        return []

