
from snake import SnakeGame
from snake_AI import create_path

snake = SnakeGame()


@snake.register_ai
def super_ai():
    return create_path(snake)


snake.start(use_ai=True)