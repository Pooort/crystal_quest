"""Константы игры Crystal Quest."""

# Размеры окна
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Crystal Quest — Кристальный квест"

# Масштаб спрайтов
TILE_SCALING = 0.5
PLAYER_SCALING = 0.6
CRYSTAL_SCALING = 0.4
ENEMY_SCALING = 0.5
PORTAL_SCALING = 0.8

# Физика и управление
GRAVITY = 0.8
PLAYER_MOVE_SPEED = 5
PLAYER_JUMP_SPEED = 14
PLAYER_MAX_HEALTH = 3

# Направления для анимации
FACING_RIGHT = 0
FACING_LEFT = 1

# Очки
SCORE_PER_CRYSTAL = 100
SCORE_PER_LEVEL_BONUS = 500
SCORE_TIME_BONUS_MULTIPLIER = 2

# Пути к данным
DATA_DIR_NAME = "data"
LEVELS_CSV = "levels.csv"
PLATFORMS_CSV = "platforms.csv"
CRYSTALS_CSV = "crystals.csv"
ENEMIES_CSV = "enemies.csv"
HIGHSCORES_DB = "highscores.db"

# Звуки (встроенные ресурсы Arcade)
SOUND_COIN = ":resources:sounds/coin1.wav"
SOUND_JUMP = ":resources:sounds/jump1.wav"
SOUND_HURT = ":resources:sounds/hurt1.wav"
SOUND_GAMEOVER = ":resources:sounds/gameover1.wav"
SOUND_FANFARE = ":resources:sounds/fanfare.wav"

# Текстуры
TEXTURE_CRYSTAL = ":resources:images/items/gemBlue.png"
TEXTURE_PORTAL = ":resources:images/items/keyBlue.png"
TEXTURE_PARTICLE = ":resources:images/pinball/bumper.png"

# Цвета интерфейса
COLOR_TITLE = (100, 200, 255)
COLOR_SUBTITLE = (180, 220, 255)
COLOR_HINT = (150, 150, 170)
COLOR_SCORE = (255, 255, 100)
COLOR_HEALTH = (255, 80, 80)
