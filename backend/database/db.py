import sqlite3
import os
from typing import List, Optional, Dict
import json
from datetime import datetime

class Database:
    """SQLite database for storing teams, matches, and statistics"""
    
    def __init__(self, db_path: str = None):
        # Use absolute path in backend directory
        if db_path is None:
            backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.db_path = os.path.join(backend_dir, "premier_league.db")
        else:
            self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Teams table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                short_name TEXT,
                crest TEXT,
                founded INTEGER,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Team stats table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS team_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_name TEXT NOT NULL,
                matches_played INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                draws INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                goals_for INTEGER DEFAULT 0,
                goals_against INTEGER DEFAULT 0,
                goal_diff INTEGER DEFAULT 0,
                points INTEGER DEFAULT 0,
                position INTEGER DEFAULT 0,
                form TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(team_name)
            )
        """)
        
        # Matches table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY,
                home_team TEXT NOT NULL,
                away_team TEXT NOT NULL,
                match_date TIMESTAMP,
                home_score INTEGER,
                away_score INTEGER,
                status TEXT,
                result TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_teams(self, teams: List[Dict]):
        """Save teams to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        for team in teams:
            cursor.execute("""
                INSERT OR REPLACE INTO teams (id, name, short_name, crest, founded, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                team.get('id'),
                team.get('name'),
                team.get('short_name'),
                team.get('crest'),
                team.get('founded'),
                datetime.now()
            ))
        
        conn.commit()
        conn.close()
    
    def get_teams(self) -> List[Dict]:
        """Get all teams from database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, short_name, crest, founded FROM teams")
        rows = cursor.fetchall()
        
        teams = []
        for row in rows:
            teams.append({
                'id': row[0],
                'name': row[1],
                'short_name': row[2],
                'crest': row[3],
                'founded': row[4]
            })
        
        conn.close()
        return teams
    
    def save_team_stats(self, team_name: str, stats: Dict):
        """Save team statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO team_stats 
            (team_name, matches_played, wins, draws, losses, goals_for, 
             goals_against, goal_diff, points, position, form, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            stats.get('team', team_name),
            stats.get('matches_played', 0),
            stats.get('wins', 0),
            stats.get('draws', 0),
            stats.get('losses', 0),
            stats.get('goals_for', 0),
            stats.get('goals_against', 0),
            stats.get('goal_diff', 0),
            stats.get('points', 0),
            stats.get('position', 0),
            stats.get('form', ''),
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
    
    def get_team_stats(self, team_name: str) -> Optional[Dict]:
        """Get team statistics with fuzzy name matching"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Try multiple name variations
        name_variations = [
            team_name,  # Exact match
            team_name + " FC",  # Add FC
            team_name.replace(" FC", ""),  # Remove FC if present
            team_name.replace("United", "Utd"),  # United -> Utd
            team_name.replace("Utd", "United"),  # Utd -> United
        ]
        
        # Also try case-insensitive matches
        for name_var in name_variations:
            cursor.execute("""
                SELECT matches_played, wins, draws, losses, goals_for, 
                       goals_against, goal_diff, points, position, form
                FROM team_stats
                WHERE LOWER(team_name) = LOWER(?)
            """, (name_var,))
            
            row = cursor.fetchone()
            if row:
                conn.close()
                return {
                    'matches_played': row[0],
                    'wins': row[1],
                    'draws': row[2],
                    'losses': row[3],
                    'goals_for': row[4],
                    'goals_against': row[5],
                    'goal_diff': row[6],
                    'points': row[7],
                    'position': row[8],
                    'form': row[9]
                }
        
        # If no exact match, try to find by partial match
        cursor.execute("""
            SELECT matches_played, wins, draws, losses, goals_for, 
                   goals_against, goal_diff, points, position, form
            FROM team_stats
            WHERE LOWER(team_name) LIKE LOWER(?)
               OR LOWER(team_name) LIKE LOWER(?)
        """, (f"%{team_name}%", f"%{team_name.replace(' FC', '')}%"))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'matches_played': row[0],
                'wins': row[1],
                'draws': row[2],
                'losses': row[3],
                'goals_for': row[4],
                'goals_against': row[5],
                'goal_diff': row[6],
                'points': row[7],
                'position': row[8],
                'form': row[9]
            }
        return None
    
    def save_match(self, match: Dict):
        """Save match to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Determine result
        home_score = match.get('home_score')
        away_score = match.get('away_score')
        result = None
        if home_score is not None and away_score is not None:
            if home_score > away_score:
                result = "HOME_WIN"
            elif away_score > home_score:
                result = "AWAY_WIN"
            else:
                result = "DRAW"
        
        cursor.execute("""
            INSERT OR REPLACE INTO matches 
            (id, home_team, away_team, match_date, home_score, away_score, status, result, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            match.get('id'),
            match.get('home_team'),
            match.get('away_team'),
            match.get('date'),
            home_score,
            away_score,
            match.get('status'),
            result,
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
    
    def get_matches(self, limit: int = 100) -> List[Dict]:
        """Get matches from database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, home_team, away_team, match_date, home_score, away_score, status, result
            FROM matches
            ORDER BY match_date DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        matches = []
        for row in rows:
            matches.append({
                'id': row[0],
                'home_team': row[1],
                'away_team': row[2],
                'date': row[3],
                'home_score': row[4],
                'away_score': row[5],
                'status': row[6],
                'result': row[7]
            })
        
        conn.close()
        return matches
    
    def save_team_players(self, team_name: str, players: List[Dict]):
        """Save team players to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create players table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS team_players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_name TEXT NOT NULL,
                player_id INTEGER,
                player_name TEXT NOT NULL,
                position TEXT,
                date_of_birth TEXT,
                nationality TEXT,
                role TEXT,
                shirt_number INTEGER,
                photo TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Delete old players for this team
        cursor.execute("DELETE FROM team_players WHERE team_name = ?", (team_name,))
        
        # Insert new players
        for player in players:
            cursor.execute("""
                INSERT INTO team_players 
                (team_name, player_id, player_name, position, date_of_birth, 
                 nationality, role, shirt_number, photo, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                team_name,
                player.get('id'),
                player.get('name'),
                player.get('position'),
                player.get('dateOfBirth'),
                player.get('nationality'),
                player.get('role'),
                player.get('shirtNumber'),
                player.get('photo'),
                datetime.now()
            ))
        
        conn.commit()
        conn.close()
    
    def get_team_players(self, team_name: str) -> List[Dict]:
        """Get team players from database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Try exact match first
        cursor.execute("""
            SELECT player_id, player_name, position, date_of_birth, 
                   nationality, role, shirt_number, photo
            FROM team_players 
            WHERE team_name = ?
            ORDER BY 
                CASE position
                    WHEN 'Goalkeeper' THEN 1
                    WHEN 'Defence' THEN 2
                    WHEN 'Defender' THEN 2
                    WHEN 'Midfield' THEN 3
                    WHEN 'Midfielder' THEN 3
                    WHEN 'Offence' THEN 4
                    WHEN 'Attacker' THEN 4
                    WHEN 'Forward' THEN 4
                    ELSE 5
                END,
                shirt_number
        """, (team_name,))
        
        rows = cursor.fetchall()
        if rows:
            players = []
            for row in rows:
                players.append({
                    'id': row[0],
                    'name': row[1],
                    'position': row[2],
                    'dateOfBirth': row[3],
                    'nationality': row[4],
                    'role': row[5],
                    'shirtNumber': row[6],
                    'photo': row[7]
                })
            conn.close()
            return players
        
        # Try fuzzy matching
        normalized_input = team_name.lower().replace(" fc", "").strip()
        cursor.execute("SELECT DISTINCT team_name FROM team_players")
        all_teams = cursor.fetchall()
        
        for (db_team_name,) in all_teams:
            normalized_db = db_team_name.lower().replace(" fc", "").strip()
            if normalized_input == normalized_db or normalized_input in normalized_db or normalized_db in normalized_input:
                cursor.execute("""
                    SELECT player_id, player_name, position, date_of_birth, 
                           nationality, role, shirt_number, photo
                    FROM team_players 
                    WHERE team_name = ?
                    ORDER BY 
                        CASE position
                            WHEN 'Goalkeeper' THEN 1
                            WHEN 'Defence' THEN 2
                            WHEN 'Defender' THEN 2
                            WHEN 'Midfield' THEN 3
                            WHEN 'Midfielder' THEN 3
                            WHEN 'Offence' THEN 4
                            WHEN 'Attacker' THEN 4
                            WHEN 'Forward' THEN 4
                            ELSE 5
                        END,
                        shirt_number
                """, (db_team_name,))
                rows = cursor.fetchall()
                if rows:
                    players = []
                    for row in rows:
                        players.append({
                            'id': row[0],
                            'name': row[1],
                            'position': row[2],
                            'dateOfBirth': row[3],
                            'nationality': row[4],
                            'role': row[5],
                            'shirtNumber': row[6],
                            'photo': row[7]
                        })
                    conn.close()
                    return players
        
        conn.close()
        return []

