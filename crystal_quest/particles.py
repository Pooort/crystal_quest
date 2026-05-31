"""Система частиц для визуальных эффектов."""

import arcade
from arcade.particles import make_burst_emitter

from crystal_quest.constants import TEXTURE_PARTICLE


class ParticleManager:
    """Управляет эмиттерами частиц в игре."""

    def __init__(self) -> None:
        self.emitters: list[arcade.Emitter] = []

    def spawn_collect_burst(self, x: float, y: float) -> None:
        """Вспышка при сборе кристалла."""
        emitter = make_burst_emitter(
            center_xy=(x, y),
            filenames_and_textures=[TEXTURE_PARTICLE],
            particle_count=24,
            particle_speed=4.0,
            particle_lifetime_min=0.2,
            particle_lifetime_max=0.6,
            particle_scale=0.15,
            fade_particles=True,
        )
        self.emitters.append(emitter)

    def spawn_hurt_burst(self, x: float, y: float) -> None:
        """Красноватый эффект при получении урона."""
        texture = arcade.make_circle_texture(16, arcade.color.RED)
        emitter = make_burst_emitter(
            center_xy=(x, y),
            filenames_and_textures=[texture],
            particle_count=16,
            particle_speed=3.0,
            particle_lifetime_min=0.15,
            particle_lifetime_max=0.4,
            particle_scale=0.4,
            fade_particles=True,
        )
        self.emitters.append(emitter)

    def spawn_portal_sparkle(self, x: float, y: float) -> None:
        """Мягкое свечение у портала."""
        texture = arcade.make_circle_texture(12, arcade.color.LIGHT_BLUE)
        emitter = make_burst_emitter(
            center_xy=(x, y),
            filenames_and_textures=[texture],
            particle_count=8,
            particle_speed=1.5,
            particle_lifetime_min=0.4,
            particle_lifetime_max=0.8,
            particle_scale=0.3,
            fade_particles=True,
        )
        self.emitters.append(emitter)

    def update(self, delta_time: float) -> None:
        """Обновляет и удаляет завершившие работу эмиттеры."""
        alive_emitters = []
        for emitter in self.emitters:
            emitter.update(delta_time)
            if not emitter.can_reap():
                alive_emitters.append(emitter)
        self.emitters = alive_emitters

    def draw(self) -> None:
        """Отрисовывает активные частицы."""
        for emitter in self.emitters:
            emitter.draw()

    def clear(self) -> None:
        """Удаляет все эмиттеры."""
        self.emitters.clear()
