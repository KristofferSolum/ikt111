import heapq


def heuristic(current_position, apple_position):
    manhattan = abs(current_position[0] - apple_position[0]) + abs(current_position[1] - apple_position[1])
    return manhattan


def calculate_space_score(position, game_state):
    x, y = position
    length, width = len(game_state), len(game_state[0])
    space_count = 0

    for move_x, move_y in[(-1, 0), (1, 0), (0, -1), (0, 1)]:
        for i in range(1, 4):
            new_x, new_y = x + move_x*i, y + move_y*i

            if 0 <= new_x < length and 0 <= new_y < width:
                if game_state[new_x][new_y] == 0:
                    space_count += 1

    return -1 * space_count


def create_path(snake):
    possible_moves = ['up', 'down', 'left', 'right']

    snake_position = snake.get_snake_head_position()
    apple_position = snake.get_apple_position()

    queue = [(0, 0, snake_position, [])]  # (f_cost, g_cost, position, path to position)
    visited_positions = set()

    while queue:
        f_cost, g_cost, current_position, snake_path = heapq.heappop(queue)

        visited_positions.add(tuple(current_position))

        if snake.is_winning(snake_path):

            return snake_path

        for move in possible_moves:
            new_position = snake.simulate_move(current_position, move)
            path_to_new_position = snake_path + [move]

            if tuple(new_position) not in visited_positions and snake.is_legal(path_to_new_position):
                g_new = g_cost + 1
                h_cost = heuristic(new_position, apple_position)
                space_score = calculate_space_score(new_position, snake.game_state)

                f_cost = g_new + h_cost + space_score

                heapq.heappush(queue, (f_cost, g_new, new_position, path_to_new_position))

                visited_positions.add(tuple(new_position))

    return []
