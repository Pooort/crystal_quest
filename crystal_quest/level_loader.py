"""Загрузка уровней из CSV-файлов."""

import csv
from dataclasses import dataclass, field
from pathlib import Path

from crystal_quest.constants import (
    CRYSTALS_CSV,
    DATA_DIR_NAME,
    ENEMIES_CSV,
    LEVELS_CSV,
    PLATFORMS_CSV,
)


@dataclass
class PlatformData:
    """Прямоугольная платформа."""

    x: float
    y: float
    width: float
    height: float


@dataclass
class CrystalData:
    """Позиция кристалла."""

    x: float
    y: float


@dataclass
class EnemyData:
    """Параметры патрулирующего врага."""

    x: float
    y: float
    patrol_left: float
    patrol_right: float
    speed: float


@dataclass
class LevelData:
    """Полное описание одного уровня."""

    level_id: int
    name: str
    background_color: str
    width: float
    time_limit: int
    player_start_x: float
    player_start_y: float
    platforms: list[PlatformData] = field(default_factory=list)
    crystals: list[CrystalData] = field(default_factory=list)
    enemies: list[EnemyData] = field(default_factory=list)


class LevelLoader:
    """Читает CSV и собирает объекты уровней."""

    def __init__(self, base_dir: Path | None = None) -> None:
        root = base_dir or Path(__file__).resolve().parent.parent
        self.data_dir = root / DATA_DIR_NAME

    def load_all_levels(self) -> list[LevelData]:
        """Загружает все уровни из набора CSV."""
        levels = self._load_level_meta()
        platforms = self._group_by_level(self._read_csv(PLATFORMS_CSV))
        crystals = self._group_by_level(self._read_csv(CRYSTALS_CSV))
        enemies = self._group_by_level(self._read_csv(ENEMIES_CSV))

        for level in levels:
            level_id = str(level.level_id)
            level.platforms = [
                PlatformData(
                    x=float(row["x"]),
                    y=float(row["y"]),
                    width=float(row["width"]),
                    height=float(row["height"]),
                )
                for row in platforms.get(level_id, [])
            ]
            level.crystals = [
                CrystalData(x=float(row["x"]), y=float(row["y"]))
                for row in crystals.get(level_id, [])
            ]
            level.enemies = [
                EnemyData(
                    x=float(row["x"]),
                    y=float(row["y"]),
                    patrol_left=float(row["patrol_left"]),
                    patrol_right=float(row["patrol_right"]),
                    speed=float(row["speed"]),
                )
                for row in enemies.get(level_id, [])
            ]
        return levels

    def _load_level_meta(self) -> list[LevelData]:
        rows = self._read_csv(LEVELS_CSV)
        return [
            LevelData(
                level_id=int(row["level_id"]),
                name=row["name"],
                background_color=row["background_color"],
                width=float(row["width"]),
                time_limit=int(row["time_limit"]),
                player_start_x=float(row["player_start_x"]),
                player_start_y=float(row["player_start_y"]),
            )
            for row in rows
        ]

    def _read_csv(self, filename: str) -> list[dict[str, str]]:
        path = self.data_dir / filename
        with path.open(encoding="utf-8", newline="") as file:
            return list(csv.DictReader(file))

    @staticmethod
    def _group_by_level(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
        grouped: dict[str, list[dict[str, str]]] = {}
        for row in rows:
            grouped.setdefault(row["level_id"], []).append(row)
        return grouped
