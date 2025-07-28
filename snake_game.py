import random

class SnakeGame:
    GRID_SIZE = 20
    INIT_LENGTH = 3
    DIRECTIONS = {
        'UP': (0, -1),
        'DOWN': (0, 1),
        'LEFT': (-1, 0),
        'RIGHT': (1, 0)
    }

    def __init__(self):
        self.reset()

    def reset(self):
        mid = self.GRID_SIZE // 2
        self.snake = [(mid - i, mid) for i in range(self.INIT_LENGTH)]
        self.direction = 'RIGHT'
        self.food = self._place_food()
        self.score = 0
        self.game_over = False
        self.victory = False

    def _place_food(self):
        positions = set(self.snake)
        all_positions = set(
            (x, y) for x in range(self.GRID_SIZE) for y in range(self.GRID_SIZE)
        )
        available_positions = list(all_positions - positions)
        if not available_positions:
            # No available position for food, snake fills the grid
            self.victory = True
            return None
        return random.choice(available_positions)

    def get_state(self):
        return {
            'snake': self.snake,
            'food': self.food,
            'score': self.score,
            'game_over': self.game_over,
            'victory': self.victory,
            'grid_size': self.GRID_SIZE
        }

    def change_direction(self, direction):
        if direction not in self.DIRECTIONS:
            return
        dx, dy = self.DIRECTIONS[direction]
        cdx, cdy = self.DIRECTIONS[self.direction]
        if (dx, dy) == (-cdx, -cdy):
            return
        self.direction = direction

    def update(self):
        if self.game_over or self.victory:
            return
        dx, dy = self.DIRECTIONS[self.direction]
        head_x, head_y = self.snake[0]
        new_head = (head_x + dx, head_y + dy)

        # Check wall collision
        if not (0 <= new_head[0] < self.GRID_SIZE and 0 <= new_head[1] < self.GRID_SIZE):
            self.game_over = True
            return

        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        # Check food
        if self.food is not None and new_head == self.food:
            self.score += 1
            self.food = self._place_food()
            if self.victory:
                # Snake has filled the grid after eating the last food
                return
        else:
            self.snake.pop()
