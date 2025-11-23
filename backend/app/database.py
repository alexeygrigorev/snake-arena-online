from typing import List, Optional, Dict
from app.models import User, LeaderboardEntry, ActiveGame, GameMode, Point
from datetime import datetime, timezone
import uuid

# Mock storage
users_db: Dict[str, dict] = {} # email -> user_dict (including password_hash)
leaderboard_db: List[LeaderboardEntry] = []
active_games_db: Dict[str, ActiveGame] = {}

def get_user_by_email(email: str) -> Optional[dict]:
    return users_db.get(email)

def get_user_by_id(user_id: str) -> Optional[dict]:
    for user in users_db.values():
        if user["id"] == user_id:
            return user
    return None

def create_user(user_data: dict) -> dict:
    user_id = str(uuid.uuid4())
    user_data["id"] = user_id
    users_db[user_data["email"]] = user_data
    return user_data

def add_leaderboard_entry(entry: LeaderboardEntry):
    leaderboard_db.append(entry)

def get_leaderboard(mode: Optional[GameMode] = None, limit: int = 10) -> List[LeaderboardEntry]:
    filtered = leaderboard_db
    if mode:
        filtered = [entry for entry in leaderboard_db if entry.mode == mode]
    
    # Sort by score descending
    sorted_entries = sorted(filtered, key=lambda x: x.score, reverse=True)
    return sorted_entries[:limit]

def get_active_games() -> List[ActiveGame]:
    return list(active_games_db.values())

# Initialize with fake data for testing
def _init_fake_data():
    """Initialize the database with fake data for testing"""
    from app.auth import get_password_hash
    
    # Sample users
    sample_users = [
        {"email": "alice@example.com", "username": "alice", "password": "password123"},
        {"email": "bob@example.com", "username": "bob", "password": "password123"},
        {"email": "charlie@example.com", "username": "charlie", "password": "password123"},
    ]
    
    for user in sample_users:
        user_data = {
            "email": user["email"],
            "username": user["username"],
            "password_hash": get_password_hash(user["password"])
        }
        create_user(user_data)
    
    # Sample leaderboard entries
    sample_scores = [
        {"username": "alice", "score": 150, "mode": GameMode.walls},
        {"username": "bob", "score": 120, "mode": GameMode.walls},
        {"username": "charlie", "score": 95, "mode": GameMode.walls},
        {"username": "alice", "score": 200, "mode": GameMode.pass_through},
        {"username": "bob", "score": 175, "mode": GameMode.pass_through},
        {"username": "charlie", "score": 140, "mode": GameMode.pass_through},
    ]
    
    for score in sample_scores:
        entry = LeaderboardEntry(
            id=str(uuid.uuid4()),
            username=score["username"],
            score=score["score"],
            mode=score["mode"],
            timestamp=datetime.now(timezone.utc)
        )
        add_leaderboard_entry(entry)
    
    # Sample active games
    sample_games = [
        {
            "username": "alice",
            "score": 75,
            "mode": GameMode.walls,
            "snake": [Point(x=10, y=10), Point(x=9, y=10), Point(x=8, y=10)],
            "food": Point(x=15, y=15)
        },
        {
            "username": "bob",
            "score": 50,
            "mode": GameMode.pass_through,
            "snake": [Point(x=5, y=5), Point(x=4, y=5)],
            "food": Point(x=12, y=8)
        },
    ]
    
    for game in sample_games:
        active_game = ActiveGame(
            id=str(uuid.uuid4()),
            username=game["username"],
            score=game["score"],
            mode=game["mode"],
            snake=game["snake"],
            food=game["food"]
        )
        active_games_db[active_game.id] = active_game

# Initialize fake data on module load
_init_fake_data()
