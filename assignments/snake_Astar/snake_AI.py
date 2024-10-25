import heapq


def heuristic(current_position, apple_position):
    manhattan = abs(current_position[0] - apple_position[0]) + abs(current_position[1] - apple_position[1])
    return manhattan


def create_path(snake):
    possible_moves = ['up', 'down', 'left', 'right']

    snake_position = snake.get_snake_head_position()
    apple_position = snake.get_apple_position()

    queue = [(0, 0, snake_position, [])]  # (f_cost, g_cost, position, path to position)
    visited_position = set()

    while queue:
        f_cost, g_cost, current_position, snake_path = heapq.heappop(queue)

        visited_position.add(tuple(current_position))

        if snake.is_winning(snake_path):
            return snake_path

        for move in possible_moves:
            new_position = snake.simulate_move(current_position, move)
            path_to_new_position = snake_path + [move]
            g_new = g_cost + 1
            f_cost = g_new + heuristic(new_position, apple_position)

            if tuple(new_position) not in visited_position and snake.is_legal(path_to_new_position):
                heapq.heappush(queue, (f_cost, g_new, new_position, path_to_new_position))
                visited_position.add(tuple(new_position))

    return []

