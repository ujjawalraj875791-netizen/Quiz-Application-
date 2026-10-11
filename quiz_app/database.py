import sqlite3
from pathlib import Path
from .models import QuizResult

class Database:
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._create_tables()

    def connect(self):
        return sqlite3.connect(self.db_path)

    def _create_tables(self):
        with self.connect() as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS leaderboard (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player TEXT NOT NULL,
                    category TEXT NOT NULL,
                    total_questions INTEGER NOT NULL,
                    correct INTEGER NOT NULL,
                    wrong INTEGER NOT NULL,
                    unanswered INTEGER NOT NULL,
                    score REAL NOT NULL,
                    percentage REAL NOT NULL,
                    time_taken INTEGER NOT NULL,
                    played_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            con.commit()

    def save_result(self, result: QuizResult):
        with self.connect() as con:
            con.execute("""
                INSERT INTO leaderboard
                (player, category, total_questions, correct, wrong,
                 unanswered, score, percentage, time_taken)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                result.player, result.category, result.total_questions,
                result.correct, result.wrong, result.unanswered,
                result.score, result.percentage, result.time_taken
            ))
            con.commit()

    def top_scores(self, category="All", limit=10):
        query = """
            SELECT player, category, score, percentage, correct,
                   wrong, unanswered, time_taken, played_at
            FROM leaderboard
        """
        params = []
        if category != "All":
            query += " WHERE category = ?"
            params.append(category)
        query += """
            ORDER BY score DESC, percentage DESC, time_taken ASC,
                     played_at ASC LIMIT ?
        """
        params.append(limit)
        with self.connect() as con:
            return con.execute(query, params).fetchall()
