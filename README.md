# Crystal Quest

2D-платформер на Python и [Arcade](https://api.arcade.academy/) для учебного проекта Яндекс.Лицея.

## Идея

Игрок управляет искательницей приключений, собирает кристаллы на трёх уровнях, избегает слаймов и добирается до портала. Счёт сохраняется в SQLite.

## Запуск

```bash
cd crystal_quest
pip install -r requirements.txt
python main.py
python main.py --name "Иван Иванов"
```

## Управление

| Клавиша | Действие |
|---------|----------|
| A / ← | Влево |
| D / → | Вправо |
| W / ↑ / Space | Прыжок |
| Enter | Старт / меню |
| R | Новая игра (на экране результатов) |
| Esc | Выход в меню результатов |

## Структура проекта

```
crystal_quest/
├── main.py                 # Точка входа
├── requirements.txt
├── data/                   # CSV-уровни и SQLite-рекорды
│   ├── levels.csv
│   ├── platforms.csv
│   ├── crystals.csv
│   └── enemies.csv
├── docs/                   # Пояснительная записка и презентация
└── crystal_quest/
    ├── constants.py
    ├── database.py         # SQLite — хранение рекордов
    ├── level_loader.py     # CSV — загрузка уровней
    ├── particles.py        # Система частиц
    ├── sprites/            # Спрайты игрока, врагов, кристаллов
    └── views/              # Стартовый, игровой и финальный экраны
```

## Использованные технологии Arcade

| Технология | Где реализована |
|------------|-----------------|
| Стартовое окно | `views/start_view.py` |
| Финальное окно | `views/end_view.py` |
| Подсчёт результатов | `views/game_view.py`, `views/end_view.py` |
| Спрайты | `sprites/` |
| collide | `views/game_view.py` |
| Анимация | `sprites/player.py`, `sprites/crystal.py` |
| Несколько уровней | `data/*.csv`, `level_loader.py` |
| Камера | `views/game_view.py` — `Camera2D` |
| Система частиц | `particles.py` |
| Звук | `views/*.py`, `game_view.py` |
| Физический движок | `PhysicsEnginePlatformer` |
| Хранение данных | CSV (уровни) + SQLite (рекорды) |

## Авторы

Укажите ФИО участников группы перед сдачей проекта.
