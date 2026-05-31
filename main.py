"""
Crystal Quest — точка входа в игру.

Запуск:
    python main.py
    python main.py --name "Ваше Имя"
"""

import argparse

import arcade

from crystal_quest.constants import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH
from crystal_quest.views.start_view import StartView


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Crystal Quest — платформер на Arcade")
    parser.add_argument(
        "--name",
        default="Игрок",
        help="Имя игрока для таблицы рекордов",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_view(StartView(player_name=args.name))
    arcade.run()


if __name__ == "__main__":
    main()
