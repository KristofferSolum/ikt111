
def create_path(snake):
    possible_moves = ['up', 'down', 'left', 'right']

    snake_position = snake.get_snake_head_position()

    queue = [[snake_position, []]]  # [position, path to position]
    visited_position = []
    while queue:
        current_position, snake_path = queue.pop(0)

        if snake.is_winning(snake_path):
            return snake_path

        for move in possible_moves:
            new_position = snake.simulate_move(current_position, move)
            path_to_new_position = snake_path + [move]

            if new_position not in visited_position and snake.is_legal(path_to_new_position):
                queue.append([new_position, path_to_new_position])
                visited_position.append(new_position)
    return []
