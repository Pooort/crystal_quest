"""Хранение рекордов в SQLite."""

import sqlite3
from datetime import datetime
from pathlib import Path

from crystal_quest.constants import DATA_DIR_NAME, HIGHSCORES_DB


class HighScoreDatabase:
    """Работа с таблицей рекордов в SQLite."""

    def __init__(self, base_dir: Path | None = None) -> None:
        root = base_dir or Path(__file__).resolve().parent.parent
        self.db_path = root / DATA_DIR_NAME / HIGHSCORES_DB
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        """Создаёт таблицу, если её ещё нет."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS high_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    levels_completed INTEGER NOT NULL,
                    played_at TEXT NOT NULL
                )
                """
            )

    def save_score(
        self,
        player_name: str,
        score: int,
        levels_completed: int,
    ) -> None:
        """Сохраняет результат игрока."""
        played_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                INSERT INTO high_scores (player_name, score, levels_completed, played_at)
                VALUES (?, ?, ?, ?)
                """,
                (player_name, score, levels_completed, played_at),
            )

    def get_top_scores(self, limit: int = 5) -> list[dict]:
        """Возвращает лучшие результаты."""
        query = """
            SELECT player_name, score, levels_completed, played_at
            FROM high_scores
            ORDER BY score DESC, played_at ASC
            LIMIT ?
        """
        with sqlite3.connect(self.db_path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(query, (limit,)).fetchall()
        return [dict(row) for row in rows]

    def get_best_score(self) -> int:
        """Возвращает максимальный рекорд или 0."""
        with sqlite3.connect(self.db_path) as connection:
            row = connection.execute(
                "SELECT MAX(score) AS best FROM high_scores"
            ).fetchone()
        return int(row[0]) if row and row[0] is not None else 0
