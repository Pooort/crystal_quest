"""Враги, патрулирующие платформы."""

import arcade

from crystal_quest.constants import ENEMY_SCALING
from crystal_quest.level_loader import EnemyData


class SlimeEnemy(arcade.Sprite):
    """Слайм с горизонтальным патрулированием по одной платформе."""

    PATROL_MARGIN = 12

    def __init__(self, enemy_data: EnemyData) -> None:
        texture = arcade.load_texture(
            ":resources:images/enemies/slimeBlue.png"
        )
        super().__init__(texture, scale=ENEMY_SCALING)
        self.center_x = enemy_data.x
        self.center_y = enemy_data.y
        self.boundary_left = enemy_data.patrol_left
        self.boundary_right = enemy_data.patrol_right
        self.change_x = enemy_data.speed
        self.host_platform: arcade.Sprite | None = None

    def attach_to_platform(self, platform: arcade.Sprite) -> None:
        """Ставит слайма на верх платформы и ограничивает патруль её краями."""
        self.host_platform = platform
        margin = max(self.PATROL_MARGIN, self.width * 0.25)

        self.boundary_left = platform.left + margin
        self.boundary_right = platform.right - margin
        if self.boundary_right <= self.boundary_left:
            center = platform.center_x
            self.boundary_left = center - margin
            self.boundary_right = center + margin

        self.center_x = max(
            self.boundary_left,
            min(self.center_x, self.boundary_right),
        )
        self.center_y = platform.top + self.height / 2

    @staticmethod
    def find_platform_for_x(
        x: float,
        platforms: arcade.SpriteList,
    ) -> arcade.Sprite | None:
        """Находит платформу, на которой должен стоять враг."""
        on_platform = [
            platform
            for platform in platforms
            if platform.left <= x <= platform.right
        ]
        if on_platform:
            return max(on_platform, key=lambda platform: platform.top)

        return min(
            platforms,
            key=lambda platform: abs(platform.center_x - x),
        )

    def update(self, delta_time: float = 1 / 60) -> None:
        super().update(delta_time)

        if self.host_platform is not None:
            self.center_y = self.host_platform.top + self.height / 2

        if self.right >= self.boundary_right and self.change_x > 0:
            self.change_x *= -1
            self.center_x = self.boundary_right
        elif self.left <= self.boundary_left and self.change_x < 0:
            self.change_x *= -1
            self.center_x = self.boundary_left
