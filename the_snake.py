from abc import ABC, abstractmethod
from random import randint, choice
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject(ABC):
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=None):
        if position:
            self.position = position
        else:
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    @abstractmethod
    def draw(self):
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self, position=None):
        """Инициализирует объект яблока с заданной позицией или случайной."""
        super().__init__(position)
        self.body_color = APPLE_COLOR  # Красный цвет яблока
        self.randomize_position()

    def randomize_position(self):
        """Генерирует случайную позицию для яблока в пределах игрового поля."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовывает яблоко на экране
        (в данной версии просто выводит сообщение).
        """
        pygame.draw.rect(screen, self.body_color,
                         (self.position[0],
                          self.position[1], GRID_SIZE, GRID_SIZE))


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(self, position=None):
        """Инициализирует объект змейки с заданной позицией
        или по умолчанию в центре экрана.
        """
        super().__init__(position)
        self.body_color = SNAKE_COLOR  # Зеленый цвет змейки
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT  # Направление: вправо
        self.next_direction = None
        self.last = None

    def update_direction(self, direction):
        """Обновляет направление движения змейки,
        если новое направление не противоположно текущему.
        """
        if (self.next_direction
                is None or (
                        self.next_direction[0] != -direction[0]
                        and self.next_direction[1] != -direction[1])
        ):
            self.next_direction = direction

    def move(self):
        """Двигает змейку в текущем направлении и обновляет её позицию."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        # Получаем текущую головную позицию
        head_x, head_y = self.positions[0]
        new_head = (head_x + self.direction[0]
                    * GRID_SIZE, head_y + self.direction[1] * GRID_SIZE)

        # Обрабатываем столкновение с краем экрана
        new_head = (new_head[0] % SCREEN_WIDTH, new_head[1] % SCREEN_HEIGHT)

        # Проверка на столкновение с собой
        if new_head in self.positions[1:]:
            self.reset()  # Сбрасываем змейку, если она столкнулась с собой

        # Добавляем новую голову в начало списка
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()  # Удаляем последний сегмент

    def draw(self):
        """Отрисовывает змейку на экране
        (в данной версии просто выводит сообщение).
        """
        for position in self.positions:
            pygame.draw.rect(screen, self.body_color,
                             (position[0], position[1], GRID_SIZE, GRID_SIZE))

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное
        состояние после столкновения с собой.
        """
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.update_direction(choice([UP, DOWN, LEFT, RIGHT]))


def handle_keys(snake, key):
    """Функция управления"""
    if key == pygame.K_UP:
        snake.update_direction(UP)
    elif key == pygame.K_DOWN:
        snake.update_direction(DOWN)
    elif key == pygame.K_LEFT:
        snake.update_direction(LEFT)
    elif key == pygame.K_RIGHT:
        snake.update_direction(RIGHT)


def main():
    """Функция main"""
    # Инициализация PyGame:
    pygame.init()

    # Создание объектов змейки и яблока:
    snake = Snake()
    apple = Apple()

    # Основной игровой цикл
    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)  # Очистка экрана

        # Обработка событий:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                handle_keys(snake, event.key)

        # Двигаем змейку
        snake.move()

        # Проверяем съедание яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1  # Увеличиваем длину змейки
            snake.positions.append(snake.positions[-1])
            apple.randomize_position()  # Перемещаем яблоко

        # Отрисовка объектов
        snake.draw()
        apple.draw()

        # Обновление экрана
        pygame.display.update()

        # Установка частоты кадров
        clock.tick(SPEED)


if __name__ == '__main__':
    main()

# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif (event.key == pygame.K_LEFT
#                   and game_object.direction != RIGHT):
#                 game_object.next_direction = LEFT
#             elif (event.key == pygame.K_RIGHT
#                   and game_object.direction != LEFT):
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
