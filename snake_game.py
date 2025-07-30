import time
import random

class SnakeGame:
    def __init__(self, grid_size=10):
        self.grid_size = grid_size
        self.snake = [(grid_size // 2, grid_size // 2)]
        self.direction = (0, 1)
        self.generate_food()
        self.score = 0
        self.game_over = False

    def generate_food(self):
        while True:
            food = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
            if food not in self.snake:
                self.food = food
                break

    def update_game_state(self):
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        if (new_head[0] < 0 or new_head[0] >= self.grid_size or 
            new_head[1] < 0 or new_head[1] >= self.grid_size):
            self.game_over = True
            return

        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.generate_food()
        else:
            self.snake.pop()

    def render_game(self):
        board = [[' ' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for (i, j) in self.snake:
            board[i][j] = 'S'
        board[self.food[0]][self.food[1]] = 'F'
        
        rendered = '+' + '-' * self.grid_size + '+\n'
        for row in board:
            rendered += '|' + ''.join(row) + '|\n'
        rendered += '+' + '-' * self.grid_size + '+\n'
        print(rendered)

    def run(self):
        iteration = 0
        max_iterations = 20
        while not self.game_over and iteration < max_iterations:
            self.update_game_state()
            self.render_game()
            time.sleep(0.5)
            iteration += 1
        return self.score

if __name__ == "__main__":
    game = SnakeGame()
    final_score = game.run()
    print("Final Score:", final_score)
