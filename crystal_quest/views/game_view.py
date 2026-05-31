"""Основной игровой экран с уровнями, физикой и камерой."""

import arcade
from arcade.types import Color

from crystal_quest.constants import (
    COLOR_HEALTH,
    COLOR_SCORE,
    GRAVITY,
    PLAYER_JUMP_SPEED,
    PLAYER_MAX_HEALTH,
    PLAYER_MOVE_SPEED,
    SCORE_PER_CRYSTAL,
    SCORE_PER_LEVEL_BONUS,
    SCORE_TIME_BONUS_MULTIPLIER,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SOUND_COIN,
    SOUND_GAMEOVER,
    SOUND_HURT,
    SOUND_JUMP,
)
from crystal_quest.level_loader import LevelData, LevelLoader
from crystal_quest.particles import ParticleManager
from crystal_quest.sprites.crystal import Crystal
from crystal_quest.sprites.enemy import SlimeEnemy
from crystal_quest.sprites.platform import ExitPortal, Platform
from crystal_quest.sprites.player import Player
from crystal_quest.views.end_view import EndView


class GameView(arcade.View):
    """Управляет одним или несколькими уровнями игры."""

    def __init__(self, player_name: str = "Игрок") -> None:
        super().__init__()
        self.player_name = player_name
        self.level_loader = LevelLoader()
        self.levels = self.level_loader.load_all_levels()
        self.current_level_index = 0

        self.player: Player | None = None
        self.player_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList(use_spatial_hash=True)
        self.crystal_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.portal_list = arcade.SpriteList()
        self.portal: ExitPortal | None = None

        self.physics_engine: arcade.PhysicsEnginePlatformer | None = None
        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()
        self.particles = ParticleManager()

        self.score = 0
        self.crystals_collected = 0
        self.crystals_total = 0
        self.level_time = 0.0
        self.level_completed = False
        self.game_finished = False

        self.left_pressed = False
        self.right_pressed = False
        self.jump_pressed = False

        self.sound_coin = arcade.load_sound(SOUND_COIN)
        self.sound_jump = arcade.load_sound(SOUND_JUMP)
        self.sound_hurt = arcade.load_sound(SOUND_HURT)
        self.sound_gameover = arcade.load_sound(SOUND_GAMEOVER)

        self.score_text: arcade.Text | None = None
        self.level_text: arcade.Text | None = None
        self.timer_text: arcade.Text | None = None
        self.health_text: arcade.Text | None = None
        self.hint_text: arcade.Text | None = None
        self.level_complete_text: arcade.Text | None = None

    @property
    def current_level(self) -> LevelData:
        return self.levels[self.current_level_index]

    def on_show_view(self) -> None:
        self.setup_level(self.current_level_index)

    def setup_level(self, level_index: int) -> None:
        """Инициализирует спрайты и физику для выбранного уровня."""
        self.current_level_index = level_index
        level = self.current_level

        self.platform_list = arcade.SpriteList(use_spatial_hash=True)
        self.crystal_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.portal_list = arcade.SpriteList()
        self.particles.clear()

        for platform_data in level.platforms:
            self.platform_list.append(Platform(platform_data, level_index))

        for crystal_data in level.crystals:
            self.crystal_list.append(Crystal(crystal_data))

        for enemy_data in level.enemies:
            enemy = SlimeEnemy(enemy_data)
            platform = SlimeEnemy.find_platform_for_x(
                enemy_data.x,
                self.platform_list,
            )
            if platform is not None:
                enemy.attach_to_platform(platform)
            self.enemy_list.append(enemy)

        self.player = Player()
        self.player.center_x = level.player_start_x
        self.player.center_y = level.player_start_y
        self.player.health = PLAYER_MAX_HEALTH
        self.player_list.append(self.player)

        last_platform = level.platforms[-1]
        portal_x = last_platform.x + last_platform.width - 40
        portal_y = last_platform.y + last_platform.height + 40
        self.portal = ExitPortal(portal_x, portal_y)
        self.portal_list.append(self.portal)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            walls=self.platform_list,
            gravity_constant=GRAVITY,
        )

        self.crystals_collected = 0
        self.crystals_total = len(self.crystal_list)
        self.level_time = float(level.time_limit)
        self.level_completed = False
        self.game_finished = False
        self.portal_sparkle_timer = 0.0
        self.respawn_x = level.player_start_x
        self.respawn_y = level.player_start_y
        self.fall_death_y = min(
            platform.bottom for platform in self.platform_list
        ) - 32

        self._create_hud_texts(level)
        self.level_complete_text = None
        arcade.set_background_color(Color.from_hex_string(level.background_color))

    def _create_hud_texts(self, level: LevelData) -> None:
        self.score_text = arcade.Text(
            f"Счёт: {self.score}",
            12,
            SCREEN_HEIGHT - 28,
            COLOR_SCORE,
            18,
        )
        self.level_text = arcade.Text(
            f"Уровень {level.level_id}: {level.name}",
            12,
            SCREEN_HEIGHT - 54,
            arcade.color.WHITE,
            16,
        )
        self.timer_text = arcade.Text(
            f"Время: {int(self.level_time)}",
            12,
            SCREEN_HEIGHT - 80,
            arcade.color.LIGHT_BLUE,
            16,
        )
        self.health_text = arcade.Text(
            f"Жизни: {self.player.health}",
            12,
            SCREEN_HEIGHT - 106,
            COLOR_HEALTH,
            16,
        )
        self.hint_text = arcade.Text(
            f"Кристаллы: 0/{self.crystals_total}",
            12,
            SCREEN_HEIGHT - 132,
            arcade.color.LIGHT_GREEN,
            16,
        )

    def on_draw(self) -> None:
        self.clear()

        self.camera.use()
        self.platform_list.draw()
        self.crystal_list.draw()
        self.enemy_list.draw()
        self.portal_list.draw()
        self.player_list.draw()
        self.particles.draw()

        self.gui_camera.use()
        for text in (
            self.score_text,
            self.level_text,
            self.timer_text,
            self.health_text,
            self.hint_text,
        ):
            if text:
                text.draw()

        if self.level_complete_text:
            self.level_complete_text.draw()

    def on_update(self, delta_time: float) -> None:
        if self.game_finished or not self.player or not self.physics_engine:
            return

        self.physics_engine.update()
        self.player.update_animation(delta_time)
        self.player.update_timers(delta_time)
        if self.player.invulnerable_timer > 0:
            self.player.visible = int(self.player.invulnerable_timer * 10) % 2 == 0
        else:
            self.player.visible = True
        self.enemy_list.update(delta_time)

        for crystal in self.crystal_list:
            crystal.update_animation(delta_time)
        if self.portal:
            self.portal.update_animation(delta_time)
            if self.level_completed:
                self.portal_sparkle_timer += delta_time
                if self.portal_sparkle_timer >= 0.4:
                    self.portal_sparkle_timer = 0.0
                    self.particles.spawn_portal_sparkle(
                        self.portal.center_x,
                        self.portal.center_y,
                    )

        self.particles.update(delta_time)
        self._update_movement()
        self._handle_crystal_collisions()
        self._handle_enemy_collisions()
        self._handle_fall_death()
        self._handle_portal_collision()
        self._update_timer(delta_time)
        self._update_camera()
        self._update_hud()

    def _update_movement(self) -> None:
        if self.left_pressed and not self.right_pressed:
            self.player.change_x = -PLAYER_MOVE_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x = PLAYER_MOVE_SPEED
        else:
            self.player.change_x = 0

        if self.jump_pressed and self.physics_engine.can_jump():
            self.player.change_y = PLAYER_JUMP_SPEED
            arcade.play_sound(self.sound_jump)

    def _handle_crystal_collisions(self) -> None:
        hit_list = arcade.check_for_collision_with_list(
            self.player,
            self.crystal_list,
        )
        for crystal in hit_list:
            crystal.remove_from_sprite_lists()
            self.crystals_collected += 1
            self.score += SCORE_PER_CRYSTAL
            arcade.play_sound(self.sound_coin)
            self.particles.spawn_collect_burst(crystal.center_x, crystal.center_y)

        if (
            not self.level_completed
            and self.crystals_collected >= self.crystals_total
        ):
            self.level_completed = True
            self.score += SCORE_PER_LEVEL_BONUS
            self.level_complete_text = arcade.Text(
                "Уровень пройден! Идите к порталу →",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT * 0.5,
                arcade.color.GOLD,
                22,
                anchor_x="center",
            )

    def _handle_enemy_collisions(self) -> None:
        hit_list = arcade.check_for_collision_with_list(
            self.player,
            self.enemy_list,
        )
        for enemy in hit_list:
            if self.player.take_damage():
                arcade.play_sound(self.sound_hurt)
                self.particles.spawn_hurt_burst(
                    self.player.center_x,
                    self.player.center_y,
                )
                self.player.center_x -= 40 * (1 if self.player.change_x >= 0 else -1)

        if self.player.health <= 0:
            self._finish_game(victory=False)

    def _handle_fall_death(self) -> None:
        """Обрабатывает падение игрока за пределы уровня."""
        if self.player.bottom >= self.fall_death_y:
            return

        if self.player.health <= 1:
            self._finish_game(victory=False)
            return

        self.player.health -= 1
        self.player.center_x = self.respawn_x
        self.player.center_y = self.respawn_y
        self.player.change_x = 0
        self.player.change_y = 0
        self.player.invulnerable_timer = 2.0
        arcade.play_sound(self.sound_hurt)
        self.particles.spawn_hurt_burst(
            self.player.center_x,
            self.player.center_y,
        )

    def _handle_portal_collision(self) -> None:
        if not self.level_completed or not self.portal:
            return
        if arcade.check_for_collision(self.player, self.portal):
            time_bonus = int(self.level_time) * SCORE_TIME_BONUS_MULTIPLIER
            self.score += time_bonus
            self._go_to_next_level()

    def _update_timer(self, delta_time: float) -> None:
        self.level_time -= delta_time
        if self.level_time <= 0:
            self.level_time = 0
            self._finish_game(victory=False)

    def _update_camera(self) -> None:
        level = self.current_level
        target_x = self.player.center_x
        target_y = self.player.center_y

        left_bound = SCREEN_WIDTH / 2
        right_bound = level.width - SCREEN_WIDTH / 2
        if right_bound < left_bound:
            target_x = level.width / 2
        else:
            target_x = max(left_bound, min(target_x, right_bound))

        target_y = max(SCREEN_HEIGHT / 2, min(target_y, SCREEN_HEIGHT / 2 + 80))
        self.camera.position = (target_x, target_y)

    def _update_hud(self) -> None:
        if self.score_text:
            self.score_text.text = f"Счёт: {self.score}"
        if self.timer_text:
            self.timer_text.text = f"Время: {max(0, int(self.level_time))}"
        if self.health_text and self.player:
            self.health_text.text = f"Жизни: {self.player.health}"
        if self.hint_text:
            self.hint_text.text = (
                f"Кристаллы: {self.crystals_collected}/{self.crystals_total}"
            )

    def _go_to_next_level(self) -> None:
        next_index = self.current_level_index + 1
        if next_index >= len(self.levels):
            self._finish_game(victory=True)
            return
        self.setup_level(next_index)

    def _finish_game(self, victory: bool) -> None:
        if self.game_finished:
            return
        self.game_finished = True
        if not victory:
            arcade.play_sound(self.sound_gameover)

        levels_done = (
            len(self.levels)
            if victory
            else self.current_level_index
        )
        end_view = EndView(
            player_name=self.player_name,
            score=self.score,
            levels_completed=levels_done,
            total_levels=len(self.levels),
            victory=victory,
        )
        self.window.show_view(end_view)

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key in (arcade.key.A, arcade.key.LEFT):
            self.left_pressed = True
        elif key in (arcade.key.D, arcade.key.RIGHT):
            self.right_pressed = True
        elif key in (arcade.key.W, arcade.key.UP, arcade.key.SPACE):
            self.jump_pressed = True
        elif key == arcade.key.ESCAPE:
            self.window.show_view(
                EndView(
                    player_name=self.player_name,
                    score=self.score,
                    levels_completed=self.current_level_index,
                    total_levels=len(self.levels),
                    victory=False,
                )
            )

    def on_key_release(self, key: int, modifiers: int) -> None:
        if key in (arcade.key.A, arcade.key.LEFT):
            self.left_pressed = False
        elif key in (arcade.key.D, arcade.key.RIGHT):
            self.right_pressed = False
        elif key in (arcade.key.W, arcade.key.UP, arcade.key.SPACE):
            self.jump_pressed = False
