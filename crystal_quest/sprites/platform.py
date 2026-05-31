"""Статичные платформы уровня."""

import arcade

from crystal_quest.constants import TILE_SCALING
from crystal_quest.level_loader import PlatformData


class Platform(arcade.Sprite):
    """Платформа, создаваемая из цветного прямоугольника."""

    COLORS = (
        arcade.color.DARK_GREEN,
        arcade.color.DARK_BLUE,
        arcade.color.DARK_RED,
    )

    def __init__(self, platform_data: PlatformData, level_index: int) -> None:
        color = self.COLORS[level_index % len(self.COLORS)]
        texture = arcade.make_soft_square_texture(
            64,
            color,
            outer_alpha=255,
        )
        super().__init__(texture, scale=TILE_SCALING)
        self.center_x = platform_data.x + platform_data.width / 2
        self.center_y = platform_data.y + platform_data.height / 2
        self.width = platform_data.width
        self.height = platform_data.height


class ExitPortal(arcade.Sprite):
    """Портал выхода с уровня."""

    def __init__(self, x: float, y: float) -> None:
        super().__init__(
            ":resources:images/items/keyBlue.png",
            scale=0.8,
        )
        self.center_x = x
        self.center_y = y
        self.rotation_speed = 45

    def update_animation(self, delta_time: float) -> None:
        self.angle += self.rotation_speed * delta_time
