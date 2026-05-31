"""Собираемые кристаллы."""

import math

import arcade

from crystal_quest.constants import CRYSTAL_SCALING, TEXTURE_CRYSTAL
from crystal_quest.level_loader import CrystalData


class Crystal(arcade.Sprite):
    """Мерцающий кристалл с простой анимацией."""

    def __init__(self, crystal_data: CrystalData) -> None:
        super().__init__(TEXTURE_CRYSTAL, scale=CRYSTAL_SCALING)
        self.center_x = crystal_data.x
        self.center_y = crystal_data.y
        self.pulse_time = 0.0
        self.base_scale = CRYSTAL_SCALING

    def update_animation(self, delta_time: float) -> None:
        """Плавное изменение масштаба создаёт эффект мерцания."""
        self.pulse_time += delta_time * 4
        pulse = 1.0 + 0.15 * math.sin(self.pulse_time)
        self.scale = self.base_scale * pulse
