"""Финальный экран с итогами и сохранением результата."""

import arcade

from crystal_quest.constants import (
    COLOR_SCORE,
    COLOR_SUBTITLE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from crystal_quest.database import HighScoreDatabase


class EndView(arcade.View):
    """Экран победы или поражения."""

    def __init__(
        self,
        player_name: str,
        score: int,
        levels_completed: int,
        total_levels: int,
        victory: bool,
    ) -> None:
        super().__init__()
        self.player_name = player_name
        self.score = score
        self.levels_completed = levels_completed
        self.total_levels = total_levels
        self.victory = victory
        self.database = HighScoreDatabase()
        self.database.save_score(player_name, score, levels_completed)
        self.texts: list[arcade.Text] = []

        if victory:
            self.fanfare = arcade.load_sound(":resources:sounds/fanfare.wav")
            arcade.play_sound(self.fanfare)
        else:
            self.gameover = arcade.load_sound(":resources:sounds/gameover1.wav")
            arcade.play_sound(self.gameover)

    def on_show_view(self) -> None:
        if self.victory:
            arcade.set_background_color(arcade.color.DARK_GREEN)
        else:
            arcade.set_background_color(arcade.color.DARK_RED)
        self._build_texts()

    def _build_texts(self) -> None:
        center_x = SCREEN_WIDTH / 2
        title = "ПОБЕДА!" if self.victory else "ИГРА ОКОНЧЕНА"
        title_color = arcade.color.GOLD if self.victory else arcade.color.ORANGE_RED
        message = (
            "Вы собрали все кристаллы и прошли все уровни!"
            if self.victory
            else "Попробуйте ещё раз — кристаллы ждут!"
        )
        best = self.database.get_best_score()

        self.texts = [
            arcade.Text(
                title,
                center_x,
                SCREEN_HEIGHT * 0.72,
                title_color,
                48,
                anchor_x="center",
                bold=True,
            ),
            arcade.Text(
                f"Игрок: {self.player_name}",
                center_x,
                SCREEN_HEIGHT * 0.58,
                COLOR_SUBTITLE,
                22,
                anchor_x="center",
            ),
            arcade.Text(
                f"Итоговый счёт: {self.score}",
                center_x,
                SCREEN_HEIGHT * 0.48,
                COLOR_SCORE,
                32,
                anchor_x="center",
                bold=True,
            ),
            arcade.Text(
                f"Пройдено уровней: {self.levels_completed} из {self.total_levels}",
                center_x,
                SCREEN_HEIGHT * 0.38,
                arcade.color.WHITE,
                20,
                anchor_x="center",
            ),
            arcade.Text(
                f"Лучший рекорд: {best}",
                center_x,
                SCREEN_HEIGHT * 0.28,
                arcade.color.LIGHT_GRAY,
                18,
                anchor_x="center",
            ),
            arcade.Text(
                message,
                center_x,
                SCREEN_HEIGHT * 0.20,
                arcade.color.WHITE,
                16,
                anchor_x="center",
            ),
            arcade.Text(
                "ENTER — в меню    R — играть снова",
                center_x,
                SCREEN_HEIGHT * 0.08,
                arcade.color.LIGHT_BLUE,
                18,
                anchor_x="center",
            ),
        ]

    def on_draw(self) -> None:
        self.clear()
        for text in self.texts:
            text.draw()

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.ENTER:
            from crystal_quest.views.start_view import StartView

            self.window.show_view(StartView(player_name=self.player_name))
        elif key == arcade.key.R:
            from crystal_quest.views.game_view import GameView

            self.window.show_view(GameView(player_name=self.player_name))
