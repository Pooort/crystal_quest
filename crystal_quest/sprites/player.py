"""Анимированный персонаж игрока."""

import arcade

from crystal_quest.constants import (
    FACING_LEFT,
    FACING_RIGHT,
    PLAYER_SCALING,
)


class Player(arcade.Sprite):
    """Герой с анимацией ходьбы, прыжка и падения."""

    def __init__(self) -> None:
        super().__init__(scale=PLAYER_SCALING)
        self.facing_direction = FACING_RIGHT
        self.current_texture_index = 0
        self.animation_cooldown = 0
        self.health = 3
        self.invulnerable_timer = 0.0

        base_path = ":resources:images/animated_characters/female_adventurer/femaleAdventurer"
        idle = arcade.load_texture(f"{base_path}_idle.png")
        jump = arcade.load_texture(f"{base_path}_jump.png")
        fall = arcade.load_texture(f"{base_path}_fall.png")

        self.idle_textures = (idle, idle.flip_left_right())
        self.jump_textures = (jump, jump.flip_left_right())
        self.fall_textures = (fall, fall.flip_left_right())
        self.walk_textures = []
        for index in range(8):
            texture = arcade.load_texture(f"{base_path}_walk{index}.png")
            self.walk_textures.append((texture, texture.flip_left_right()))

        self.texture = self.idle_textures[FACING_RIGHT]

    def update_animation(self, delta_time: float) -> None:
        """Переключает текстуры в зависимости от движения."""
        if self.change_x < 0:
            self.facing_direction = FACING_LEFT
        elif self.change_x > 0:
            self.facing_direction = FACING_RIGHT

        if self.change_y > 0.5:
            self.texture = self.jump_textures[self.facing_direction]
            return

        if self.change_y < -0.5:
            self.texture = self.fall_textures[self.facing_direction]
            return

        if abs(self.change_x) < 0.1:
            self.texture = self.idle_textures[self.facing_direction]
            self.current_texture_index = 0
            return

        self.animation_cooldown += delta_time
        if self.animation_cooldown >= 0.08:
            self.animation_cooldown = 0
            self.current_texture_index = (self.current_texture_index + 1) % 8
            self.texture = self.walk_textures[self.current_texture_index][
                self.facing_direction
            ]

    def take_damage(self) -> bool:
        """Наносит урон, если нет неуязвимости. Возвращает True при попадании."""
        if self.invulnerable_timer > 0:
            return False
        self.health -= 1
        self.invulnerable_timer = 1.5
        return True

    def update_timers(self, delta_time: float) -> None:
        """Уменьшает таймер неуязвимости."""
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= delta_time
