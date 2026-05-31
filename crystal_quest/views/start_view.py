"""Стартовое окно с меню и таблицей рекордов."""

import arcade

from crystal_quest.constants import (
    COLOR_HINT,
    COLOR_SUBTITLE,
    COLOR_TITLE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from crystal_quest.database import HighScoreDatabase


class StartView(arcade.View):
    """Приветственный экран перед началом игры."""

    def __init__(self, player_name: str = "Игрок") -> None:
        super().__init__()
        self.player_name = player_name
        self.database = HighScoreDatabase()
        self.pulse_time = 0.0
        self.prompt_text: arcade.Text | None = None
        self.highscore_lines: list[arcade.Text] = []
        self.static_texts: list[arcade.Text] = []

    def on_show_view(self) -> None:
        arcade.set_background_color(arcade.color.DARK_SLATE_BLUE)
        self._build_texts()

    def _build_texts(self) -> None:
        center_x = SCREEN_WIDTH / 2
        self.static_texts = [
            arcade.Text(
                "CRYSTAL QUEST",
                center_x,
                SCREEN_HEIGHT * 0.72,
                COLOR_TITLE,
                54,
                anchor_x="center",
                bold=True,
            ),
            arcade.Text(
                "Кристальный квест",
                center_x,
                SCREEN_HEIGHT * 0.62,
                COLOR_SUBTITLE,
                24,
                anchor_x="center",
            ),
            arcade.Text(
                "Собери все кристаллы и доберись до портала!",
                center_x,
                SCREEN_HEIGHT * 0.48,
                arcade.color.WHITE,
                18,
                anchor_x="center",
            ),
            arcade.Text(
                "Управление: A/D или ←/→ — движение, W/↑/Space — прыжок",
                center_x,
                SCREEN_HEIGHT * 0.40,
                COLOR_HINT,
                16,
                anchor_x="center",
            ),
            arcade.Text(
                "Таблица рекордов",
                center_x,
                SCREEN_HEIGHT * 0.18,
                arcade.color.GOLD,
                18,
                anchor_x="center",
            ),
        ]
        self.prompt_text = arcade.Text(
            "Нажмите ENTER, чтобы начать",
            center_x,
            SCREEN_HEIGHT * 0.28,
            arcade.color.GOLD,
            22,
            anchor_x="center",
        )
        self._build_highscore_lines()

    def _build_highscore_lines(self) -> None:
        scores = self.database.get_top_scores(limit=5)
        center_x = SCREEN_WIDTH / 2
        self.highscore_lines = []

        if not scores:
            self.highscore_lines.append(
                arcade.Text(
                    "Пока нет сохранённых результатов",
                    center_x,
                    SCREEN_HEIGHT * 0.10,
                    COLOR_HINT,
                    14,
                    anchor_x="center",
                )
            )
            return

        y = SCREEN_HEIGHT * 0.12
        for index, record in enumerate(scores, start=1):
            line = (
                f"{index}. {record['player_name']} — "
                f"{record['score']} очков "
                f"({record['levels_completed']} ур.)"
            )
            self.highscore_lines.append(
                arcade.Text(
                    line,
                    center_x,
                    y,
                    arcade.color.LIGHT_GRAY,
                    14,
                    anchor_x="center",
                )
            )
            y -= 22

    def on_draw(self) -> None:
        self.clear()
        for text in self.static_texts:
            text.draw()
        if self.prompt_text:
            self.prompt_text.draw()
        for text in self.highscore_lines:
            text.draw()

    def on_update(self, delta_time: float) -> None:
        self.pulse_time += delta_time
        if not self.prompt_text:
            return
        pulse = 0.6 + 0.4 * abs((self.pulse_time % 1.0) - 0.5) * 2
        self.prompt_text.color = (int(255 * pulse), int(220 * pulse), 100)

    def _start_game(self) -> None:
        from crystal_quest.views.game_view import GameView

        self.window.show_view(GameView(player_name=self.player_name))

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.ENTER:
            self._start_game()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        self._start_game()
